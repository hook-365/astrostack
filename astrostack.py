import os
import json
import numpy as np
from astropy.io import fits
from astropy.nddata import CCDData
from astropy.stats import sigma_clip
from astroalign import register
from ccdproc import combine, subtract_dark


# Define the directories
data_directory = "/Users/anthony/Pictures/DWARFII/Astronomy/DWARF_RAW_M51_EXP_10_GAIN_60_2024-05-05-23-02-57-312"  # Update this path
json_file = os.path.join(data_directory, "shotsinfo.json")
dark_frames_directory = "/Users/anthony/Pictures/DWARFII/Astronomy/DWARF_DARK"  # Update this path

# Load the JSON metadata file
with open(json_file, "r") as f:
    metadata = json.load(f)

# Extract relevant metadata for selecting dark frames
exp = metadata["exp"]
gain = metadata["gain"]
binning = metadata["binning"].replace('*', '_')  # replace * with _ for directory naming

# Function to load all FITS files in a directory with a specific prefix
def load_fits_files(directory, prefix):
    fits_files = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith(".fits")]
    images = []
    for file in fits_files:
        filepath = os.path.join(directory, file)
        images.append(fits.getdata(filepath))
    return images

# Function to find the closest matching dark frames subdirectory
def find_closest_dark_frames_dir(base_dir, target_exp, target_gain, target_binning):
    best_match = None
    min_diff = float('inf')
    for subdir in os.listdir(base_dir):
        parts = subdir.split('_')
        if len(parts) != 6 or parts[1] != str(target_exp):
            continue
        exp = int(parts[1])
        gain = int(parts[3])
        binning = parts[5]
        diff = abs(gain - target_gain)
        if diff < min_diff and binning == target_binning:
            min_diff = diff
            best_match = subdir
    return best_match

# Find the closest matching dark frames directory
closest_dark_frames_subdir = find_closest_dark_frames_dir(dark_frames_directory, exp, gain, binning)
dark_frames_path = None
if closest_dark_frames_subdir:
    dark_frames_path = os.path.join(dark_frames_directory, closest_dark_frames_subdir)

# Debug print to check the constructed path
if dark_frames_path:
    print(f"Using dark frames from: {dark_frames_path}")
else:
    print("No suitable dark frames directory found. Proceeding without dark frames.")

# Load relevant FITS files
fits_images = load_fits_files(data_directory, "raw_")

# Optionally load dark frames if available
if dark_frames_path:
    dark_frames = load_fits_files(dark_frames_path, "")
else:
    dark_frames = []

# Process images
if dark_frames:
    # Create a master dark frame by combining the dark frames using the median method
    dark_ccd_images = [CCDData(data=image, unit="adu") for image in dark_frames]
    master_dark = combine(dark_ccd_images, method='median')
    # Subtract the master dark frame from each raw image
    fits_images_corrected = [subtract_dark(CCDData(data=image, unit="adu"), master_dark) for image in fits_images]
else:
    # Use raw images directly if no dark frames are available
    fits_images_corrected = [CCDData(data=image, unit="adu") for image in fits_images]

# Align images
reference_image = fits_images_corrected[0]
aligned_images = [register(image.data, reference_image.data)[0] for image in fits_images_corrected]

# Convert aligned images to CCDData objects
aligned_ccd_images = [CCDData(data=image, unit="adu") for image in aligned_images]

# Stack (combine) images using the average method
# stacked_image = combine(aligned_ccd_images, method='average')
stacked_image = combine(aligned_ccd_images, method='median', sigma_clip=True, sigma_clip_low_thresh=3, sigma_clip_high_thresh=3)


# Save the stacked image
output_file = os.path.join(data_directory, "stacked_image.fits")
fits.writeto(output_file, stacked_image.data, overwrite=True)

print(f"Stacked image saved as {output_file}")

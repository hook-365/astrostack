# AstroStack

AstroStack is a Python-based tool designed for astrophotography image processing with my Dwarf II Smart Telescope. This tool automates the process of loading, aligning, and stacking FITS images to enhance the quality of the final image. Additionally, it incorporates the use of dark frames to reduce noise, if available.

## Features

- **Load FITS Images**: Automatically load all FITS images from a specified directory.
- **Dark Frame Subtraction**: Optionally subtract dark frames to reduce sensor noise.
- **Image Alignment**: Align images using `astroalign` to correct for slight shifts between frames.
- **Image Stacking**: Combine aligned images using various methods to improve signal-to-noise ratio.
- **Flexible Dark Frame Selection**: Selects the closest matching dark frames based on exposure time, gain, and binning.

## Prerequisites

Ensure you have the following Python packages installed:

- `numpy`
- `astropy`
- `astroalign`
- `ccdproc`

You can install these packages using `pip`:

```bash
pip install numpy astropy astroalign ccdproc
```

## Directory Structure

The directory should contain:

- Raw FITS images with filenames starting with raw_.
- A JSON file (shotsinfo.json) containing metadata for the images.
- Optional: A directory (DWARF_DARK) containing dark frames organized by subdirectories based on exposure, - gain, and binning settings.

```Pictures/DWARFII/Astronomy
|-- raw_M51_10s_60_0048.fits
|-- raw_M51_10s_60_0049.fits
|-- shotsinfo.json
|-- DWARF_DARK
    |-- exp_15_gain_100_bin_1
    |   |-- 0000.fits
    |   |-- 0001.fits
    |-- exp_15_gain_110_bin_1
    |   |-- 0000.fits
    |   |-- 0001.fits
    ...
```

## shotsinfo.json

The `shotsinfo.json` file should contain metadata for the images, for example:

```{
    "DEC": 49.13032222,
    "RA": 13.42784111,
    "binning": "1*1",
    "exp": "10",
    "format": "FITS",
    "gain": 60,
    "ir": "PASS",
    "shotsStacked": 50,
    "shotsTaken": 50,
    "shotsToTake": 50,
    "target": "M51"
}
```

## Usage

Update the `data_directory` and `dark_frames_directory` variables in the script with the actual paths to your directories.

```
data_directory = "Pictures/DWARFII/Astronomy"  # Update this path
dark_frames_directory = "Pictures/DWARFII/Astronomy/DWARF_DARK"  # Update this path
```

### The script will:

- Load the raw FITS images.
- Find the closest matching dark frames based on exposure, gain, and binning.
- Subtract the master dark frame from each raw image (if dark frames are available).
- Align the images.
- Stack the images using the specified method.
- Save the final stacked image as stacked_image.fits in the data directory.
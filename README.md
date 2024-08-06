# UltimateTracker_python

Directly read orientation and position data from the VIVE Ultimate Tracker. Only available in WINDOWS

## VIVE Tracker DirectRead

## Overview

**VIVE Tracker DirectRead** is a Python-based tool that allows you to directly read orientation and position data from the VIVE Ultimate Tracker without the need for a headset. This tool logs data to a CSV file and provides real-time plotting of the tracker's position in both 2D and 3D.

## Features

- **Direct Tracker Data Access**: Retrieve orientation and position data from the VIVE Ultimate Tracker.
- **CSV Logging**: Log tracker data to a CSV file for further analysis.
- **Live Plotting**: Real-time plotting of tracker position in both 2D and 3D.
- **High Precision Timing**: Use high precision timing for accurate data sampling.

## Requirements

- Python 3.6+
- `openvr`
- `numpy`
- `matplotlib`
- `collections`
- `mpl_toolkits.mplot3d`
- `win_precise_time`

You can install the required Python libraries using pip:

```sh
pip install openvr numpy matplotlib collections mpl_toolkits.mplot3d win_precise_time

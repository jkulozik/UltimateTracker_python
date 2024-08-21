# UltimateTracker_python

Directly read orientation and position data from the VIVE Ultimate Tracker. Only available on Windows.

## Pre-requirements
- Install Steam VR.
- Use a null driver for Steam VR: https://github.com/username223/SteamVRNoHeadset.
- Install the VIVE Streaming Hub and activate the PC streaming beta:
  - Download from: https://www.vive.com/us/vive-hub/download/
  - Activate with code: "VIVEUTRCPreview" (valid as of 08/2024).
- Follow instructions in the VIVE Streaming Hub. (update: 21.08.2024, Launch of SteamVR no longer necessary but installation and enabling null HMD is still needed)
- When the trackers indicate ready, launch the code as explained below.

## VIVE Tracker DirectRead

### Overview
**VIVE Tracker DirectRead** is a Python tool to read orientation and position data from the VIVE Ultimate Tracker without a VR headset. It logs data to a CSV file and provides real-time 2D and 3D plotting.

### Features
- **Direct Tracker Data Access**: Retrieve orientation and position data of the Ultimate Tracker.
- **CSV Logging**: Log data for analysis.
- **Live Plotting**: Real-time 2D and 3D plotting.

### Requirements
- Python 3.6+
- Libraries: `openvr`, `numpy`, `matplotlib`, `collections`, `mpl_toolkits.mplot3d`, `win_precise_time`


### Contact

For any questions or issues, please contact [kulozik@isir.upmc.fr].

### License

This code is licensed under the MIT License.

### Attribution

When using this code, please cite the following:

[Julian Kulozik]. (2024). VIVE Tracker DirectRead. GitHub repository. URL: [https://github.com/jkulozik/UltimateTracker_python]

Install the required Python libraries:

```sh
pip install openvr numpy matplotlib collections mpl_toolkits.mplot3d win_precise_time

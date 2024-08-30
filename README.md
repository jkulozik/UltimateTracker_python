# UltimateTracker_python

Directly read orientation and position data from the VIVE Ultimate Tracker. Only available on Windows.

## Pre-requirements
- Install Steam VR.
- Enable the null driver for a virtual headset using this: [SteamVRNoHeadset](https://github.com/username223/SteamVRNoHeadset).
- Install the VIVE Streaming Hub and activate the PC streaming beta:
  - Download from: [VIVEStreamingHub](https://www.vive.com/us/vive-hub/download/)
  - Activate teh PC Beta with code: "VIVEUTRCPreview" (valid as of 08/2024).
- Follow instructions in the VIVE Streaming Hub. (update: 21.08.2024, Launch of SteamVR no longer necessary but installation and enabling null HMD is still needed)
- Follow the instructions to create a map. Ignore the last step demanding a SteamVR headset connection.
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

## Application
- run the python code and modify in line 244 to 246 if you want your tracking data to be:
- a. live plotted in a 3D plot (might impact system performance)
- b. live plotted in a time/XYZ plot
- c. saved in a .csv file (file name and path to be defined in line 251)  

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

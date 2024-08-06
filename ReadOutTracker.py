import time
import openvr
import csv
import math
import numpy as np
from win_precise_time import sleep
import matplotlib.pyplot as plt
from collections import deque
from mpl_toolkits.mplot3d import Axes3D

# Define the sampling rate (in Hz)
SAMPLING_RATE = 100 

def precise_wait(duration):
    """
    Wait for a specified duration with high precision.
    Uses sleep for durations >= 1 ms, otherwise uses busy-wait.
    """
    now = time.time()
    end = now + duration
    if duration >= 0.001:
        sleep(duration)
    while now < end:
        now = time.time()

class VRSystemManager:
    def __init__(self):
        """
        Initialize the VR system manager.
        """
        self.vr_system = None

    def initialize_vr_system(self):
        """
        Initialize the VR system.
        """
        try:
            openvr.init(openvr.VRApplication_Other)
            self.vr_system = openvr.VRSystem()
        except Exception as e:
            print(f"Failed to initialize VR system: {e}")
            return False
        return True

    def get_tracker_data(self):
        """
        Retrieve tracker data from the VR system.
        """
        poses = self.vr_system.getDeviceToAbsoluteTrackingPose(
            openvr.TrackingUniverseStanding, 0, openvr.k_unMaxTrackedDeviceCount)
        return poses

    def print_discovered_objects(self):
        """
        Print information about discovered VR devices.
        """
        for device_index in range(openvr.k_unMaxTrackedDeviceCount):
            device_class = self.vr_system.getTrackedDeviceClass(device_index)
            if device_class != openvr.TrackedDeviceClass_Invalid:
                serial_number = self.vr_system.getStringTrackedDeviceProperty(
                    device_index, openvr.Prop_SerialNumber_String)
                model_number = self.vr_system.getStringTrackedDeviceProperty(
                    device_index, openvr.Prop_ModelNumber_String)
                print(f"Device {device_index}: {serial_number} ({model_number})")

    def shutdown_vr_system(self):
        """
        Shutdown the VR system.
        """
        if self.vr_system:
            openvr.shutdown()

class CSVLogger:
    def __init__(self):
        """
        Initialize the CSV logger.
        """
        self.file = None
        self.csv_writer = None

    def init_csv(self, filename):
        """
        Initialize the CSV file for logging tracker data.
        """
        try:
            self.file = open(filename, 'w', newline='')
            self.csv_writer = csv.writer(self.file)
            self.csv_writer.writerow(['TrackerIndex', 'Time', 'PositionX', 'PositionY', 'PositionZ', 'RotationW', 'RotationX', 'RotationY', 'RotationZ'])
        except Exception as e:
            print(f"Failed to initialize CSV file: {e}")
            return False
        return True

    def log_data_csv(self, index, current_time, position):
        """
        Log tracker data to CSV file.
        """
        try:
            self.csv_writer.writerow([index, current_time, *position])
        except Exception as e:
            print(f"Failed to write data to CSV file: {e}")

    def close_csv(self):
        """
        Close the CSV file if it's open.
        """
        if self.file:
            self.file.close()

class DataConverter:
    @staticmethod
    def convert_to_quaternion(pose_mat):
        """
        Convert pose matrix to quaternion and position.
        """
        r_w = math.sqrt(abs(1 + pose_mat[0][0] + pose_mat[1][1] + pose_mat[2][2])) / 2
        if r_w == 0: r_w = 0.0001
        r_x = (pose_mat[2][1] - pose_mat[1][2]) / (4 * r_w)
        r_y = (pose_mat[0][2] - pose_mat[2][0]) / (4 * r_w)
        r_z = (pose_mat[1][0] - pose_mat[0][1]) / (4 * r_w)

        x = pose_mat[0][3]
        y = pose_mat[1][3]
        z = pose_mat[2][3]

        return [x, y, z, r_w, r_x, r_y, r_z]

class LivePlotter:
    def __init__(self):
        """
        Initialize the live plotter.
        """
        self.fig = None
        self.ax1 = None
        self.ax2 = None
        self.ax3 = None
        self.x_data = deque()
        self.y_data = deque()
        self.z_data = deque()
        self.time_data = deque()
        self.first = True
        self.firstx = 0
        self.firsty = 0
        self.firstz = 0
        self.start_time = time.time()
        self.vive_PosVIVE = np.zeros([3])

    def init_live_plot(self):
        """
        Initialize the live plot for VIVE tracker data.
        """
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1)
        self.ax1.set_title('X Position')
        self.ax2.set_title('Y Position')
        self.ax3.set_title('Z Position')
        self.x_line, = self.ax1.plot([], [], 'r-')
        self.y_line, = self.ax2.plot([], [], 'g-')
        self.z_line, = self.ax3.plot([], [], 'b-')
        plt.ion()
        plt.show()

    def update_live_plot(self, vive_PosVIVE):
        """
        Update the live plot with new VIVE tracker data.
        """
        current_time = time.time()
        self.x_data.append(vive_PosVIVE[0])
        self.y_data.append(vive_PosVIVE[1])
        self.z_data.append(vive_PosVIVE[2])
        self.time_data.append(current_time - self.start_time)

        self.x_line.set_data(self.time_data, self.x_data)
        self.y_line.set_data(self.time_data, self.y_data)
        self.z_line.set_data(self.time_data, self.z_data)

        if self.first:
            self.firstx = self.x_data[0]
            self.firsty = self.y_data[0]
            self.firstz = self.z_data[0]
            self.first = False

        self.ax1.set_xlim(self.time_data[0], self.time_data[-1])
        self.ax1.set_ylim([self.firstx - 1.5, self.firstx + 1.5])

        self.ax2.set_xlim(self.time_data[0], self.time_data[-1])
        self.ax2.set_ylim([self.firsty - 1.5, self.firsty + 1.5])

        self.ax3.set_xlim(self.time_data[0], self.time_data[-1])
        self.ax3.set_ylim([self.firstz - 1.5, self.firstz + 1.5])

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def init_3d_plot(self):
        """
        Initialize the 3D live plot for VIVE tracker data.
        """
        self.fig_3d = plt.figure()
        self.ax_3d = self.fig_3d.add_subplot(111, projection='3d')
        self.ax_3d.view_init(elev=1, azim=180, roll=None, vertical_axis='y')

        self.maxlen_3d = 50
        self.x_data_3d = deque(maxlen=self.maxlen_3d)
        self.y_data_3d = deque(maxlen=self.maxlen_3d)
        self.z_data_3d = deque(maxlen=self.maxlen_3d)

        self.line_3d, = self.ax_3d.plot([], [], [], 'r-')

        self.ax_3d.set_xlabel('X')
        self.ax_3d.set_ylabel('Y')
        self.ax_3d.set_zlabel('Z')
        self.ax_3d.set_title('3D Tracker Position')

        plt.ion()
        plt.show()

    def update_3d_plot(self, vive_PosVIVE):
        """
        Update the 3D live plot with new VIVE tracker data.
        """
        x, y, z = vive_PosVIVE

        self.x_data_3d.append(x)
        self.y_data_3d.append(y)
        self.z_data_3d.append(z)

        self.line_3d.set_data(self.x_data_3d, self.y_data_3d)
        self.line_3d.set_3d_properties(self.z_data_3d)

        if len(self.x_data_3d) > 1:
            self.ax_3d.set_xlim(min(self.x_data_3d), max(self.x_data_3d))
            self.ax_3d.set_ylim(min(self.y_data_3d), max(self.y_data_3d))
            self.ax_3d.set_zlim(min(self.z_data_3d), max(self.z_data_3d))

        self.fig_3d.canvas.draw()
        self.fig_3d.canvas.flush_events()

def main():
    vr_manager = VRSystemManager()
    csv_logger = CSVLogger()
    plotter = LivePlotter()

    if not vr_manager.initialize_vr_system():
        return

    if not csv_logger.init_csv("tracker_data.csv"):
        return

    plotter.init_live_plot()
    plotter.init_3d_plot()

    try:
        while True:
            poses = vr_manager.get_tracker_data()
            for i in range(openvr.k_unMaxTrackedDeviceCount):
                if poses[i].bPoseIsValid:
                    device_class = vr_manager.vr_system.getTrackedDeviceClass(i)
                    if device_class == openvr.TrackedDeviceClass_GenericTracker:
                        current_time = time.time()
                        position = DataConverter.convert_to_quaternion(poses[i].mDeviceToAbsoluteTracking)
                        plotter.update_live_plot(position[:3])
                        plotter.update_3d_plot(position[:3])
                        csv_logger.log_data_csv(i - 1, current_time, position)
            precise_wait(1 / SAMPLING_RATE)
    except KeyboardInterrupt:
        print("Stopping data collection...")
    finally:
        vr_manager.shutdown_vr_system()
        csv_logger.close_csv()

if __name__ == "__main__":
    main()

######################################################################################################################
# Study of a visual odometry chain for the localization and autonomous piloting of a maintenance UAV for the Space Rider
# PIE
# ISAE SUPAERO
# Toulouse, 14.03.2021
#
# Authors: BECKE Philipp
#          SECHERESSE Vincent
#
##################
# Camera class
##################
# Creates a virtual camera, which can move and rotate in 3D space. It has different functions to set it's position
# and orientation, as well as it's velocity and angular velocity.
# The functions change only the position and orientation quaternion, to apply it to the camera the 'update_cam'
# function needs to be called.
# The camera is used to calculate the coordinate transformation from 3D to 2D space.
# The class contains also a logging functions which can be called by print_log to return a log.
######################################################################################################################

import numpy as np
import Transformations as tf


class Camera:
    def __init__(self):
        self.camPos = np.array([0, 0, 0])                                                  # camera position
        self.camAng = np.array([0, 0, 0])                                                  # camera angle
        self.camQuat = np.array([0, 0, 0, 1])                                              # camera quaternion
        self.fov = 40 * 3.14 / 180                                                         # camera field of view (40°)
        self.foc = 2 / (2*np.tan(self.fov / 2))                                            # camera focal distance
        self.camSight = self.camPos + np.array([[0, 0, 0], [0, 0, self.foc]])              # line if sight
        self.camSightRel = np.zeros((2, 3))
        self.camLogoRel = np.zeros((12, 3))
        self.camSightRel = tf.apply_quat_to_vec(self.camSight, self.camQuat) + self.camPos # in global coordinates
        self.camLogo = self.create_cam_model()                                             # camera animation triangle
        self.camLogoRel = tf.apply_quat_to_vec(self.camLogo, self.camQuat) + self.camPos   # camera in global coordinates
        self.camSpeed = np.array([0, 0, 0])                                                # camera speed
        self.camOmega = np.array([0, 0, 0])                                                # camera angular velocity
        self.camLog = []                                                                   # logfile of the camera

    # creates the visualization of the camera
    def create_cam_model(self):
        model = self.camPos + np.array([[0, 0, 0],
                                [- self.foc * np.sin(self.fov / 2), - self.foc * np.sin(self.fov / 2), self.foc],
                                [- self.foc * np.sin(self.fov / 2), + self.foc * np.sin(self.fov / 2), self.foc],
                                [+ self.foc * np.sin(self.fov / 2), + self.foc * np.sin(self.fov / 2), self.foc],
                                [+ self.foc * np.sin(self.fov / 2), - self.foc * np.sin(self.fov / 2), self.foc],
                                [- self.foc * np.sin(self.fov / 2), - self.foc * np.sin(self.fov / 2), self.foc],
                                [0, 0, 0],
                                [- self.foc * np.sin(self.fov / 2), + self.foc * np.sin(self.fov / 2), self.foc],
                                [0, 0, 0],
                                [+ self.foc * np.sin(self.fov / 2), + self.foc * np.sin(self.fov / 2), self.foc],
                                [0, 0, 0],
                                [+ self.foc * np.sin(self.fov / 2), - self.foc * np.sin(self.fov / 2), self.foc]])
        return model

    # Set the camera position. The camera is only updated, when update_cam is called.
    # By using 'new' or 'add' the input vector can be set as new position or added to the old position.
    def set_cam_position(self, vector, token):
        if token == 'add':
            self.camPos = self.camPos + np.array(vector)
        elif token == 'new':
            self.camPos = np.array(vector)
        else:
            print('Wrong token in camera positioning')

    # Set the camera orientation. The camera is only updated, when update_cam is called.
    # By using 'new' or 'add' the input vector can be set as new orientation or added to the old orientation.
    def set_cam_orientation(self, quaternion, token):
        if token == 'add':
            self.camQuat = tf.quat_multiply(self.camQuat, np.array(quaternion))
        elif token == 'new':
            self.camQuat = np.array(quaternion)
        else:
            print('Wrong token in camera rotation')

    # Set the camera rotational velocity. The camera is only updated, when update_cam is called.
    # By using 'new' or 'add' the input vector can be set as new velocity or added to the old velocity.
    def set_cam_rot_velocity(self, omega, token):
        if token == 'add':
            self.camOmega = self.camOmega + np.array(omega)
        elif token == 'new':
            self.camOmega = np.array(omega)
        else:
            print('Wrong token in camera rotational velocity')

    # Set the camera translational velocity. The camera is only updated, when update_cam is called.
    # By using 'new' or 'add' the input vector can be set as new velocity or added to the old velocity.
    def set_cam_trans_velocity(self, vector, token):
        if token == 'add':
            self.camSpeed = self.camSpeed + np.array(vector)
        elif token == 'new':
            self.camSpeed = np.array(vector)
        else:
            print('Wrong token in camera translational velocity')

    # This function updates the position and orientation of the satellite according to the values set to 'camQuat' and
    # 'camPos'. If 'camSpeed' or 'camOmega' are set, then they are also used to calculate the orientation and position.
    def update_cam(self, dt):
        self.set_cam_position(self.camSpeed*dt, 'add')
        self.set_cam_orientation(tf.quat_from_euler(self.camOmega*dt, 'xyz', False), 'add')

        self.camSightRel = tf.apply_quat_to_vec(self.camSight, self.camQuat) + self.camPos
        self.camLogoRel = tf.apply_quat_to_vec(self.camLogo, self.camQuat) + self.camPos
        self.camAng = tf.euler_from_quat(self.camQuat, 'xyz', False)
        self.log_camera()

    # create logfile
    def log_camera(self):
        self.camLog.append([self.camPos, self.camAng, self.camSpeed, self.camOmega])

    # returns the log for a predefined variable
    def print_log(self, name):
        pos_mark = 0
        if name == "camPos":
            pos_mark = 0
        elif name == "camAng":
            pos_mark = 1
        elif name == "camSpeed":
            pos_mark = 2
        elif name == "camOmega":
            pos_mark = 3
        else:
            print("Logging error")
        log_back = []
        for i in range(len(self.camLog)):  # combining all relevant values as array
            log_back.append([self.camLog[i][pos_mark]])
        log_back = np.concatenate(log_back)
        return log_back

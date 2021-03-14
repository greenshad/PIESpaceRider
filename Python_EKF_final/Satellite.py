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
# Satellite class
##################
# Creates a virtual satellite, which can move and rotate in 3D space. It has different functions to set it's position
# and orientation, as well as it's velocity and angular velocity.
# The functions change only the position and orientation quaternion, to apply it to the whole satellite the update_sat
# function needs to be called.
# Depending on the mode randomly generated or preset landmarks are used.
# The class contains also a logging functions which can be called by print_log to return a log.
######################################################################################################################

import numpy as np
import random
import itertools
import Transformations as tf


class Satellite:

    # initiate satellite class
    def __init__(self, landmark, mode, scale):
        self.lmkN = landmark                            # number of landmarks on each side
        self.satPos = np.array([0, 0, 10])              # x, y, z position of the center
        self.satAng = np.array([0, 0, 0])               # the rotation of the satellite
        self.satQuat = np.array([0, 0, 0, 1])           # the rotation of the satellite
        self.satRotVec = np.array([0, 0, 0])            # rotational vector of the satellite
        self.satSpeed = np.array([0, 0, 0])             # speed of the satellite
        self.satOmega = np.array([0, 0, 0])             # rotational speed of the satellite
        self.normalVecRel = np.zeros((6, 3))    # direction of each side as normal vector in satellite coordinate system
        self.normalVec = np.zeros((6, 3))       # direction of each side as normal vector in global coordinate system
        if mode == 'simulation':
            self.satSize = np.array([[0.5, 0.5, 1.5], [-0.5, -0.5, -1.5]])          # size of the satellite
        else:
            self.satSize = np.array([[1.55, 1.55, 7.86], [-1.55, -1.55, -2.64]])    # size of the satellite
        # create the dimension and corner positions of the satellite
        self.satDim = np.array([])
        self.crnRelPos = self.sat_dim_sim(mode) / scale
        self.satDim = self.satDim / scale
        # rotates the corners to absolute angle
        self.crnPos = tf.apply_quat_to_vec(self.crnRelPos, self.satQuat) + self.satPos
        self.lmkRelPos = []
        self.lmkPos = []
        self.measure_lmk = []
        self.satLog = []  # logfile
        # initialise landmarks positions
        if mode == 'simulation':
            self.random_lmk(scale)                          # create randomly distributed landmarks
        else:
            self.lmkRelPos = self.set_up_lmk() / scale      # create landmarks based on satellite model

    # this function creates landmarks based on reference model
    def set_up_lmk(self):
        lmkRelPos = np.zeros((13, 3)) # relative landmark positions
        self.lmkPos = np.array([])
        self.measure_lmk = np.zeros((13, 3))        # measured landmark positions (through "measurement" function)
        ###########################################################
        # Change this part for new landmarks of the satellite model
        # Landmarks coordinates are in the satellite frame
        ############################################################
        lmkRelPos[0] = np.array([2.67532, -0.029045, -2.70489])    # Orange_cross
        lmkRelPos[1] = np.array([-0.028639, 2.75912, -2.69887])    # Green_star
        lmkRelPos[2] = np.array([-2.80553, 0.073444, -2.70667])    # Red_circle
        lmkRelPos[3] = np.array([-0.065039, -2.75021, -2.71099])   # Blue_diamond
        lmkRelPos[4] = np.array([0, 0, 7.84647])                   # back
        lmkRelPos[5] = np.array([-1.62686, 0.008147, 3.27367])     # Dassault
        lmkRelPos[6] = np.array([0, 0, 0])                         # Satellite
        lmkRelPos[7] = np.array([0.072215, -1.81692, 0.34593])     # isae
        lmkRelPos[8] = np.array([-0.009222, 1.57393, -0.492374])   # esa
        lmkRelPos[9] = np.array([0, -7, -2.61576])                 # AT_1
        lmkRelPos[10] = np.array([7, 0, -2.63016])                 # AT_2
        lmkRelPos[11] = np.array([0, 7, -2.62335])                 # AT_3
        lmkRelPos[12] = np.array([-7, 0, -2.63461])                # AT_4
        self.lmkN = 13                                             # total number of landmarks
        return lmkRelPos

    # create random landmark for the simulation
    def random_lmk(self, scale):
        self.lmkRelPos = np.zeros((6 * self.lmkN, 3))   # relative landmark positions
        self.lmkPos = np.zeros((6 * self.lmkN, 3))      # absolute landmark positions (global coordinate system)
        self.measure_lmk = np.zeros((self.lmkN*6, 2))   # measured landmark positions (through "measurement" function)
        # create randomly distributed landmarks
        pos = 0
        for j in range(6):  # loop through all sides of the satellite
            side_pnt = [self.satDim[0]/2-0.1, -self.satDim[0]/2+0.1, self.satDim[1]/2-0.1, -self.satDim[1]/2+0.1,
                        self.satDim[2]/2-0.1, -self.satDim[2]/2+0.1]
            turn_pnt = [0, 0, 1, 1, 2, 2]
            for i in range(self.lmkN):  # loop through all 3 coordinates
                for k in range(0, 3):
                    # assures that the point is on the outside of the cube (one coordiante always =1 / =-1)
                    if k == turn_pnt[j]:
                        self.lmkRelPos[pos, k] = np.array(side_pnt[j])
                    else:
                        self.lmkRelPos[pos, k] = np.array((2 * random.random() - 1) * self.satSize[0, k])
                pos += 1
        # scale landmarks
        self.lmkRelPos = self.lmkRelPos / scale
        # rotate landmarks in global coordinate system
        self.lmkPos = tf.apply_quat_to_vec(self.lmkRelPos, self.satQuat) + self.satPos
        # create normal vector for each side (used to calculate if landmarks are visible)
        n_vec = np.zeros((6, 3))
        n_vec[0, 0] = 1
        n_vec[1, 0] = -1
        n_vec[2, 1] = 1
        n_vec[3, 1] = -1
        n_vec[4, 2] = 1
        n_vec[5, 2] = -1
        self.normalVecRel = n_vec
        return self

    # calculates corner positions based on satellite size
    def sat_dim_sim(self, mode):
        val = 0.1
        self.satDim = np.array([self.satSize[0, 0] - self.satSize[1, 0],  # creates dimensions, used to calculate corners
                       self.satSize[0, 1] - self.satSize[1, 1],
                       self.satSize[0, 2] - self.satSize[1, 2]])
        # simple cubesat for the simulation
        if mode == 'simulation':
            crnRelPos = np.array(
                list(itertools.product(*zip(self.satSize[0, :], self.satSize[1, :]))))  # relative corner pos.

        # creates model of the real satellite and adds the dimensions of the solar panels
        else:
            crnRelPos = np.array(
                list(itertools.product(*zip(self.satSize[0, :], self.satSize[1, :]))))  # relative corner pos.
            crnRelPos = np.append(crnRelPos, np.array([[-1.55, 11.975, -2.64], [1.55, 11.975, -2.64],
                                                       [-1.55, -11.975, -2.64], [1.55, -11.975, -2.64],
                                                       [11.975, -1.55, -2.64], [11.975, 1.55, -2.64],
                                                       [-11.975, -1.55, -2.64], [-11.975, 1.55, -2.64]]), axis=0)
        return crnRelPos

    # Set the satellite position. The complete satellite is only updated, when update_sat is called.
    # By using 'new' or 'add' the input vector can be set as new position or added to the old position.
    def set_sat_position(self, vector, token):
        if token == 'add':
            self.satPos = self.satPos + np.array(vector)
        elif token == 'new':
            self.satPos = np.array(vector)
        else:
            print('Wrong token in satellite positioning')

    # Set the satellite orientation. The complete satellite is only updated, when update_sat is called.
    # By using 'new' or 'add' the input vector can be set as new orientation or added to the old orientation.
    def set_sat_orientation(self, quaternion, token):
        if token == 'add':
            self.satQuat = tf.quat_multiply(self.satQuat, np.array(quaternion))
        elif token == 'new':
            self.satQuat = np.array(quaternion)
        else:
            print('Wrong token in satellite rotation')

    # Set the satellite rotational velocity. The complete satellite is only updated, when update_sat is called.
    # By using 'new' or 'add' the input vector can be set as new velocity or added to the old velocity.
    def set_sat_rot_velocity(self, omega, token):
        if token == 'add':
            self.satOmega = self.satOmega + np.array(omega)
        elif token == 'new':
            self.satOmega = np.array(omega)
        else:
            print('Wrong token in satellite rotational velocity')

    # Set the satellite translational velocity. The complete satellite is only updated, when update_sat is called.
    # By using 'new' or 'add' the input vector can be set as new velocity or added to the old velocity.
    def set_sat_trans_velocity(self, vector, token):
        if token == 'add':
            self.satSpeed = self.satSpeed + np.array(vector)
        elif token == 'new':
            self.satSpeed = np.array(vector)
        else:
            print('Wrong token in satellite translational velocity')

    # create logfile
    def log_satellite(self):
        self.satLog.append([self.satPos, self.satAng, self.satSpeed, self.satOmega,
                            self.crnPos, self.crnRelPos, self.lmkRelPos, self.lmkPos, self.measure_lmk, self.satQuat, self.satRotVec])
        return self

    # returns logfile for specific variable
    def print_log(self, name):
        pos_mark = 0
        if name == "satPos":
            pos_mark = 0
        elif name == "satAng":
            pos_mark = 1
        elif name == "satSpeed":
            pos_mark = 2
        elif name == "satOmega":
            pos_mark = 3
        elif name == "crnPos":
            pos_mark = 4
        elif name == "crnRelPos":
            pos_mark = 5
        elif name == "lmkRelPos":
            pos_mark = 6
        elif name == "lmkPos":
            pos_mark = 7
        elif name == "lmkMeas":
            pos_mark = 8
        elif name == "satQuat":
            pos_mark = 9
        elif name == "satRotVec":
            pos_mark = 10
        else:
            print("Logging error")
        log_back = []
        for i in range(len(self.satLog)):  # combining all relevant values as array
            log_back.append([self.satLog[i][pos_mark]])
        log_back = np.concatenate(log_back)
        return log_back

    # this function updates the position and orientation of the satellite according to the values set to 'satQuat' and
    # 'satPos'. If 'satSpeed' or 'satOmega' are set, then they are also used to calculate the orientation and position.
    def update_sat(self, dt):
        self.set_sat_position(self.satSpeed*dt, 'add')
        self.set_sat_orientation(tf.quat_from_euler(self.satOmega*dt, 'xyz', False), 'add')

        self.crnPos = tf.apply_quat_to_vec(self.crnRelPos, self.satQuat) + self.satPos
        self.lmkPos = tf.apply_quat_to_vec(self.lmkRelPos, self.satQuat) + self.satPos
        self.satAng = tf.euler_from_quat(self.satQuat, 'xyz', False)
        self.normalVec = tf.apply_quat_to_vec(self.normalVecRel, self.satQuat)
        self.satRotVec = tf.quat_to_rotvec(self.satQuat)

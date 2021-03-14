#######################################################################################################################
# Study of a visual odometry chain for the localization and autonomous piloting of a maintenance UAV for the Space Rider
# PIE
# ISAE SUPAERO
# Toulouse, 14.03.2021
#
# Authors: BECKE Philipp
#          SECHERESSE Vincent
#
#############
# Description
#############
# This program uses the output of a neural network (here: YOLOv4) to estimate the pose of a satellite.
# It uses an Extended Kalman Filter (EKF) to calculate the orientation and position of the satellite and a
# Perspective-n-Point (PNP) algorithm for finding initial values.
# The input are the markers that the neural network has detected on the satellite.
# The output are the position and orientation of the satellite.
# It can be used in a live mode, using directly a camera feed, in video mode with an already recorded video or in
# simulation mode, where the movement of the satellite can be simulated with a virtual satellite and virtual landmarks.
#
############
# Functions:
############
# EKF.py                - Function that calculates the EKF
# measurement.py        - Functions to read the data from YOLOv4 or simulate a measurement with added noise
# Satellite.py          - Class to create satellite objects
# Camera.py             - Class to create a Camera object
# Transformations.py    - Functions for geometric transformations
# draw.py               - Class to create plots
#######################################################################################################################

import numpy as np
import draw
import Satellite
import Camera
import measurement as mes
import copy
import EKF
import Transformations as tf
import cv2
import time

# General parameters

path = 'C:/Users/Phili/Studium/Studium/SUPAERO/PIE/YOLO/tensorflow-yolov4-tflite-master/yolov4_result.npy'
dt = 0.1                            # Time step
nit = 200                           # Number of maximum iterations
mode = 'video'                      # input modes are: 'live', 'video' or 'simulation'
draw_steps = 2                      # Show the plot every X step. This slows down the calculation a lot if small numbers
                                    # are selected.

# Create objects
graph = draw.Draw()                         # create graph object
# simulated/measured satellite object
sat_mes = Satellite.Satellite(landmark=2, mode=mode, scale=2)
sat_ekf = copy.deepcopy(sat_mes)            # create copy of satellite object to store EKF
sat_pnp = copy.deepcopy(sat_mes)            # create copy of satellite object to store PNP
cam = Camera.Camera()                       # create camera object

# EKF settings
P = 20 * np.eye(12)             # state covariance matrix
Q = 10 * np.eye(12)             # process noise covariance
r = 0.1                         # measurement noise covariance from the YOLOv4 uncertainty
# set initial values for the EKF state vector
X = np.concatenate([sat_ekf.satPos, sat_ekf.satAng, sat_ekf.satSpeed,
                    sat_ekf.satOmega]).astype(float)
pnp_threshold = 10              # specifies when PNP is used additionally

# YOLO settings
max_sec = 10                    # max. number of seconds the program will wait for a new YOLO result
# mes.reset_yolo_protocol()     # use this function to reset yolo-output

# Simulation settings, only applied if mode "simulation" is selected
if mode == 'simulation':
    sat_mes.set_sat_position([0, 1, 7], 'new')                                                  # change position
    sat_mes.set_sat_orientation(tf.quat_from_euler([0, 45, 0], 'xyz', degrees=True), 'new')     # change orientation
    sat_mes.set_sat_rot_velocity([1, 1, 1], 'new')                                              # change rot. velocity
    sat_mes.set_sat_trans_velocity([0.05, 0.05, 0.05], 'new')                                   # change trans. velocity

print('Starting main loop...')

#######################################################################################################################

# Main loop

force_stop = False
for i in range(nit):

    ###################
    # Reading YOLO data
    ###################
    # Reading data from yolo if this mode is selected. If no new data is available, the program will loop until new data
    # is available. The maximum waiting time can be changed by the parameter max_sec.
    if mode == 'video' or mode == 'live':

        z, r = mes.read_yolo(mode, i, path)              # reads data from yolo output

        # This loop is activated if no new data is available
        cnt = 0
        while not z.size or force_stop:
            time.sleep(0.01)
            z, r = mes.read_yolo(mode, i, path)
            cnt += 1
            if cnt % 100 == 0:
                print('End of file. Waiting for new information.', cnt/100, 's of 10s')
            if 0.01 * cnt > max_sec:
                print('Waiting period over. Exit algorithm.')
                force_stop = True
                break

        if z.size:
            sat_mes.lmkPos = z[:, 1:3]           # add measurement to sat_mes object if new data was added
        if force_stop:                           # exit main loop
            break
    elif mode == 'simulation':
        z = mes.get_EKF_measurements(sat_mes, cam, 0.01)
    else:
        print('No mode selected. Exit algorithm.')                      # exit main loop
        break

    #################
    # PNP calculation
    #################
    # Set-up of input data
    new_z = z.copy()                                        # copy measurements
    new_z[:, 1] = -z[:, 1]                                  # change y-direction of the coordinate system
    ind = np.array(z[:, 0], dtype='int')                    # extract all numbers from measurements
    length = np.size(ind, 0)                                # calculate total length
    # read landmark position in satellite reference frame and from measurement
    real_points = np.ascontiguousarray(sat_mes.lmkRelPos[ind, :]).reshape(length, 1, 3)
    image_points = np.ascontiguousarray(new_z[:, 1:3]).reshape(length, 1, 2)
    # calculate camera matrix
    camera_matrix = np.ascontiguousarray(np.array([[cam.foc * 1, 0., 0.],
                                                   [0., cam.foc * 1, 0.],
                                                   [0., 0., 1]])).reshape(3, 1, 3)
    distCoeffs = []                                          # setting for lens distortion
    # try to calculate the PNP-solver. If it fails, it does not have enough reference points
    try:
        (_, rotation_vector, translation_vector) = cv2.solvePnP(real_points, image_points, camera_matrix,
                                                                np.float32(distCoeffs), flags=cv2.SOLVEPNP_EPNP)
        # set the sat_pnp object
        sat_pnp.set_sat_position(np.transpose(translation_vector), 'new')               # position
        sat_pnp.set_sat_orientation(tf.quat_from_rotvec(rotation_vector), 'new')        # orientation

        # Use the PNP output to reset the EKF position. This is not a necessary step, but it has been shown to increase
        # the EKF stability a lot.
        if i < pnp_threshold:
            X[0:3] = np.transpose(translation_vector)
            print('Using PNP')
    # Exception if PNP calculation fails

    except:
        print('Not enough points for PNP')


    #################
    # EKF calculation
    #################
    # EKF set-up
    foc = cam.foc                                        # camera focal length
    carte = sat_ekf.lmkRelPos                            # create map of landmark positions in satellite reference frame
    # EKF calculation
    [X, P] = EKF.stepEKF(X, P, Q, z, dt, carte, foc, r, mode)
    # store the calculated data in the satellite object
    sat_ekf.set_sat_position(X[0:3], 'new')                                         # store position
    sat_ekf.set_sat_orientation(tf.quat_from_euler(X[3:6], 'xyz', False), 'new')    # store rotation

    #############
    # Update Data
    #############
    # Update objects
    cam.update_cam(dt)
    if mode == 'simulation':
        sat_mes.update_sat(dt)
    sat_ekf.update_sat(dt)
    sat_pnp.update_sat(dt)

    # Draw graph every X steps, set by 'draw_steps'
    if i % draw_steps == 0:
        graph.update_draw(sat_mes, cam, z[:, 1:3], sat_ekf, sat_pnp, mode)
        print('Number of iterations: ', i)

    sat_mes.log_satellite()     # log the measured data
    sat_ekf.log_satellite()     # log the EKF data

    if force_stop:
        break

# Show the error plot at the end of the loop
graph.show_plot(sat_mes, sat_ekf, nit, mode)
print('Finished.')

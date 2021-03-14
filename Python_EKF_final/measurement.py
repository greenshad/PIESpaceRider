######################################################################################################################
# Study of a visual odometry chain for the localization and autonomous piloting of a maintenance UAV for the Space Rider
# PIE
# ISAE SUPAERO
# Toulouse, 14.03.2021
#
# Authors: BECKE Philipp
#          SECHERESSE Vincent
#
######################
# Measurement function
######################
# Returns all measured landmarks from the simulation with errors defined by the input or reads the output of the
# YOLOv4 algorithm.
# It is formatted as a vector of [Id, x, y, uncertainty]
######################################################################################################################

import numpy as np
import random
import Transformations as tf
import time

# Returns all measured landmarks from the simulation with errors defined by the input
def get_EKF_measurements(sat, cam, error_size):

    # initialization
    sat_landmark_frame_pos = np.zeros((sat.lmkN*6, 3))
    sat_landmark_frame_pos[:, 0] = [i for i in range(sat.lmkN*6)]

    if sat.lmkN == 0:                                   # if there are no landmarks defined return nan
        sat_landmark_frame_pos = np.nan
    rot_faces = sat.normalVec                           # normal vectors of all sides of the satellite
    n = 0

    # iteration on all landmarks multiplied by all sides
    for i in range(sat.lmkN * 6):
        n_vector = sum(rot_faces[n, :] * cam.camSight[1, :])
        # if landmark is visible
        if (n_vector < -0.1) and not (np.isnan(tf.get_point_pos_in_frame(cam, sat.lmkPos[i, :]))).any():
            [sat_landmark_frame_pos[i, 1], sat_landmark_frame_pos[i, 2]] = tf.get_point_pos_in_frame(cam, sat.lmkPos[i, :]) + (2 * random.random() - 1) * error_size
        else:
            sat_landmark_frame_pos[i, :] = np.nan       # landmark is not visible
        if i%sat.lmkN == (sat.lmkN - 1):
            n += 1
    # only return all values that are not nan
    sat_landmark_frame_pos = sat_landmark_frame_pos[~np.isnan(sat_landmark_frame_pos).any(axis=1), :]
    return sat_landmark_frame_pos

# read the output data from YOLOv4
def read_yolo(input_type, number, path):
    # Try reading the output specified at path. It should be formatted as a vector of: [Id, x, y, uncertainty]
    try:
        mes_real = np.load(path)                                # loading
        mes_real_conf = mes_real[:, 3]                          # extract uncertainty values
        mes_real_conf = mes_real_conf[mes_real_conf != 0]       # delete zeros
        mes_real_coeff = 0.01 * pow(mes_real_conf + 0.001, -30) # linear function, maps 1 to 0.01 and 0.7 to 444

    # if the file could not be read, try again
    except:
        time.sleep(0.01)
        print('Reading of data failed. Trying again.')
        mes_last, mes_real_coeff = read_yolo(input_type, number, path)
        return mes_last

    # Transformations to match the coordinate system used in this algorithm
    pos = np.where(mes_real == -1)
    pos = pos[0]
    # Scaling
    mes_real[:, 1] = np.subtract(mes_real[:, 1] * 2, 1)
    mes_real[:, 2] = np.subtract(mes_real[:, 2] * 2, 1)
    mes_real1 = mes_real.copy()
    # Rotation
    mes_real1[:, 1] = mes_real[:, 1]
    mes_real1[:, 2] = -mes_real[:, 2]
    mes_real = mes_real1

    # Read al lines or only the last line, specified by video (all lines) or live mode (only last line)
    if input_type == 'live':
        mes_last = mes_real[pos[-1]+1:np.size(mes_real, 0)+1, :]
    elif input_type == 'video':
        if number < np.size(mes_real, 0)+1:
            mes_last = mes_real[pos[number]+1:pos[number+1], :]
        else:
            mes_last = mes_real[pos[-1] + 1:np.size(mes_real, 0) + 1, :]
            print('End of file')
    else:
        print('No YOLO input type specified')
        mes_last = np.array([])
        return mes_last
    # sort the vector
    mes_last = mes_last[mes_last[:, 0].argsort()]
    mes_last = mes_last[mes_last[:, 0] != 6., :]  # deletes the satellite landmark, as it introduces mostly noise
    return mes_last, mes_real_coeff

# This function resets the file created as output from YOLOv4. Needs to be run to reset old data.
def reset_yolo_protocol():
    mes_real = np.array([[0, 0, 0, 0]])
    np.save('C:/Users/Phili/Studium/Studium/SUPAERO/PIE/YOLO/tensorflow-yolov4-tflite-master/yolov4_result.npy', mes_real)

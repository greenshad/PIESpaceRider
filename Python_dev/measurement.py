# Measurement function, returns all measured landmarks with error
import numpy as np
import random
import rotate

def get_measurements(sat, cam, error_size):

    sat_landmark_frame_pos = np.zeros((sat.lmkN*6, 2))

    if sat.lmkN == 0:
        sat_landmark_frame_pos = np.nan
    rot_faces = sat.normalVec
    n = 0
    for i in range(sat.lmkN * 6):
        n_vector = sum(rot_faces[n, :] * cam.camSight[1, :])
        if (n_vector < -0.1) and not (np.isnan(cam.get_point_pos_in_frame(sat.lmkPos[i, :]))).any():
            [sat_landmark_frame_pos[i, 0], sat_landmark_frame_pos[i, 1]] = cam.get_point_pos_in_frame(sat.lmkPos[i, :]) + (2 * random.random() - 1) * error_size
        else:
            sat_landmark_frame_pos[i, :] = np.nan
        if i%sat.lmkN == (sat.lmkN - 1):
            n += 1
    sat.measure_lmk = sat_landmark_frame_pos
    return sat_landmark_frame_pos

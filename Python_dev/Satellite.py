# Satellite class, a square of dimension 1 that can move
# and rotate  in 3d. It has a certain number of
# landmarks, randomly generated.

import numpy as np
import random
import itertools
import rotate


class Satellite:
    def __init__(self, landmark):
        self.lmkN = landmark    # number of landmarks on each side
        self.satPos = np.array([0, 10, 0])  # x, y, z position of the center
        self.satAng = [0, 0, 0]  # the = rotation around z axis
        self.satSpeed = [0, 0, 0]
        self.satOmega = 0
        self.normalVec = np.zeros((6, 3))
        self.satSize = np.array([[0.5, 0.5, 1.5], [-0.5, -0.5, -1.5]])
        self.satDim = [self.satSize[0, 0] - self.satSize[1, 0],
                       self.satSize[0, 1] - self.satSize[1, 1],
                       self.satSize[0, 2] - self.satSize[1, 2]]
        self.crnRelPos = np.array(list(itertools.product(*zip(self.satSize[0, :], self.satSize[1, :]))))
        self.crnPos = self.satPos + self.crnRelPos
        self.crnPos = rotate.rotate(self.crnPos, self.satAng, self.satPos)

        # initialise landmarks positions
        self.lmkRelPos = np.zeros((6 * self.lmkN, 3))
        self.lmkPos = np.zeros((6 * self.lmkN, 3))
        self.measure_lmk = np.zeros((self.lmkN*6, 2))
        Satellite.create_lmk(self)

    def create_lmk(self):
        pos = 0
        for j in range(6):
            side_pnt = [self.satDim[0]/2-0.1, -self.satDim[0]/2+0.1, self.satDim[1]/2-0.1, -self.satDim[1]/2+0.1, self.satDim[2]/2-0.1, -self.satDim[2]/2+0.1]
            turn_pnt = [0, 0, 1, 1, 2, 2]
            for i in range(self.lmkN):
                for k in range(0, 3):
                    if k == turn_pnt[j]:
                        self.lmkRelPos[pos, k] = np.array(side_pnt[j])
                    else:
                        self.lmkRelPos[pos, k] = np.array((2 * random.random() - 1) * self.satSize[0, k])
                pos += 1
        self.lmkPos = np.tile(self.satPos, (6 * self.lmkN, 1)) + self.lmkRelPos
        self.lmkPos = rotate.rotate(self.lmkPos, self.satAng, self.satPos)
        n_vec = np.zeros((6, 3))
        n_vec[0, 0] = 1
        n_vec[1, 0] = -1
        n_vec[2, 1] = 1
        n_vec[3, 1] = -1
        n_vec[4, 2] = 1
        n_vec[5, 2] = -1
        self.normalVec = n_vec
        return self

    # functions to interact with the satellite
    def translate_sat(self, vector):
        self.satPos = np.array(self.satPos) + np.array(vector)
        self.crnPos = np.array(self.crnPos) + np.array(vector)
        self.lmkPos = np.array(self.lmkPos) + np.array(vector)
        return self

    def set_sat_pos(self, vector):
        self.crnPos = self.crnPos - self.satPos + vector
        self.lmkPos = self.lmkPos - self.satPos + vector
        self.satPos = np.array(vector)
        return self

    def rotate_sat(self, sat_ang):
        self.crnPos = rotate.rotate(self.crnPos, sat_ang, self.satPos)
        self.lmkPos = rotate.rotate(self.lmkPos, sat_ang, self.satPos)
        self.satAng = np.array(self.satAng) + np.array(sat_ang)
        self.normalVec = rotate.rotate(self.normalVec, sat_ang, [0, 0, 0])
        return self

    def set_sat_angle(self, sat_ang):
        self.crnPos = rotate.rotate(self.crnPos, sat_ang - self.satAng, self.satPos)
        self.lmkPos = rotate.rotate(self.lmkPos, sat_ang - self.satAng, self.satPos)
        self.satAng = np.array(sat_ang)
        return self

    def change_sat_speed(self, vector):
        self.satSpeed = np.array(self.satSpeed) + np.array(vector)
        return self

    def set_sat_speed(self, vector):
        self.satSpeed = np.array(vector)
        return self

    def change_sat_omega(self, omega):
        self.satOmega = self.satOmega + omega
        return self

    def set_sat_omega(self, omega):
        self.satOmega = omega
        return self

    def update_sat_pos(self, dt):
        self.rotate_sat(np.array(self.satOmega)*dt/2)
        self.translate_sat(np.array(self.satSpeed)*dt)
        self.rotate_sat(np.array(self.satOmega)*dt/2)
        return self


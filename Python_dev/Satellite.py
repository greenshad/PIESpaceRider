# Satellite class, a square of dimension 1 that can move
# and rotate  in 3d. It has a certain number of
# landmarks, randomly generated.

import numpy as np
import random


class Satellite:
    def __init__(self, lmkn):
        self.lmkN = lmkn
        self.satPos = np.array([0, 10, 0])  # x, y, z position of the center
        self.satAng = [0, 0, 0]  # the = rotation around z axis
        self.satSpeed = [0, 0, 0]
        self.satOmega = 0

        self.crnRelPos = np.array([-1, 0, -1],
                                  [- 1, 0, 1],
                                  [1, 0, 1],
                                  [1, 0, -1])
        self.crnPos = self.satPos + self.crnRelPos
        self.crnPos = rotate(self.crnPos, self.satAng, self.satPos)

        # initialise landmarks positions
        self.lmkRelPos = np.zeros(self.lmkN, 3)
        for i in self.lmkN:
            self.lmkRelPos[i, 1] = 2 * random.random() - 1
            self.lmkRelPos[i, 3] = 2 * random.random() - 1
        self.lmkPos = self.satPos[1:3] + self.lmkRelPos
        self.lmkPos = rotate(self.lmkPos, self.satAng, self.satPos)

    # functions to interact with the satellite
    def translate_sat(self, vector):
        self.satPos = self.satPos + vector
        self.crnPos = self.crnPos + vector
        self.lmkPos = self.lmkPos + vector
        return self

    def set_sat_pos(self, vector):
        self.crnPos = self.crnPos - self.satPos + vector
        self.lmkPos = self.lmkPos - self.satPos + vector
        self.satPos = vector
        return self

    def rotate_sat(self, sat_ang):
        self.crnPos = rotate(self.crnPos, sat_ang, self.satPos)
        self.lmkPos = rotate(self.lmkPos, sat_ang, self.satPos)
        self.satAng = self.satAng + sat_ang
        return self

    def set_sat_angle(self, theta):
        self.crnPos = rotate(self.crnPos, sat_ang - self.satAng, self.satPos)
        self.lmkPos = rotate(self.lmkPos, sat_ang - self.satAng, self.satPos)
        self.satAng = sat_ang
        return self

    def change_sat_speed(self, vector):
        self.satSpeed = self.satSpeed + vector
        return self

    def set_sat_speed(self, vector):
        self.satSpeed = vector
        return self

    def change_sat_omega(self, omega):
        self.satOmega = self.satOmega + omega
        return self

    def set_sat_omega(self, omega):
        self.satOmega = omega
        return self

    def update_sat_pos(self, dt):
        self.rotateSat(self.satOmega*dt/2)
        self.translateSat(self.satSpeed*dt)
        self.rotateSat(self.satOmega*dt/2)
        return self

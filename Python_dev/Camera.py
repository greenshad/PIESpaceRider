# create the camera object. It can move in 3d and rotate in 3d. Its field of view can be modified

import numpy as np


class Camera:
    def __init__(self):
        self.camPos = np.array([0, 0, 0])  # camera position
        self.camAng = np.array([0, 0, 0])  # camera angle
        self.fov = 40 * 3.14 / 180  # camera field of view
        self.foc = 0.5 / tan(self.fov / 2)  # camera focal distance
        self.camSight = self.camPos + np.array([[0, 0, 0], [0, self.foc, 0]])
        self.camSight = rotate(self.camSight, self.camAng, self.camPos)
        self.camLogo = self.camPos + np.array([[0, 0, 0],
                                        ...[- self.foc * sin(self.fov / 2), self.foc, - self.foc * sin(self.fov / 2)],
                                        ...[+ self.foc * sin(self.fov / 2), self.foc, + self.foc * sin(self.fov / 2)],
                                        ...[0, 0, 0]])
        self.camSpeed = np.array([0, 0, 0])
        self.camOmega = np.array([0, 0, 0])

    def translate_cam(self, vector):
        self.camPos = self.camPos + vector
        self.camSight = self.camSight + vector
        self.camLogo = self.camLogo + vector
        return self

    def set_cam_pos(self, vector):
        self.camSight = self.camSight - self.camPos + vector
        self.camLogo = self.camLogo - self.camPos + vector
        self.camPos = vector
        return self

    def rotate_cam(self, cam_ang):
        self.camSight = rotate(self.camSight, cam_ang, self.camPos)
        self.camLogo = rotate(self.camLogo, cam_ang, self.camPos)
        self.camAng = self.camAng + cam_ang
        return self

    def set_cam_angle(self, cam_ang):
        self.camSight = rotate(self.camSight, cam_ang - self.camAng, self.camPos)
        self.camLogo = rotate(self.camLogo, cam_ang - self.camAng, self.camPos)
        self.camAng = cam_ang,
        return self

    def change_cam_speed(self, vector):
        self.camSpeed = self.camSpeed + vector
        return self

    def set_cam_speed(self, vector):
        self.camSpeed = vector
        return self

    def change_cam_omega(self, omega):
        self.camOmega = self.camOmega + omega
        return self

    def set_cam_omega(self, omega):
        self.camOmega = omega
        return self

    def update_cam_pos(self, dt):
        self.rotateCam(self.camOmega * dt / 2)
        self.translateCam(self.camSpeed * dt)
        self.rotateCam(self.camOmega * dt / 2)
        return self

    def get_point_pos_in_frame(self, abs_pos):
        rel_pos = rotate(abs_pos, -self.camAng, self.camPos) - self.camPos
        relative_angle = np.array([[atan(relPos(1) / relPos(2))],
                                   ...[atan(relPos(3) / relPos(2))]])
        frame_pos = relative_angle * 2 / obj.fov
        if max(abs(frame_pos)) > 1 or rel_pos(2) < 0:
            frame_pos = [np.nan, np.nan]
        return frame_pos

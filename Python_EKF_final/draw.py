######################################################################################################################
# Study of a visual odometry chain for the localization and autonomous piloting of a maintenance UAV for the Space Rider
# PIE
# ISAE SUPAERO
# Toulouse, 14.03.2021
#
# Authors: BECKE Philipp
#          SECHERESSE Vincent
#
############
# Draw class
############
# This class creates axes objects which are used to draw the results of the simulation or measurements.
######################################################################################################################

from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
import Transformations as tf


class Draw:

    # initialisation, creates figure fig1 with two subplots ax and ax2 and sets their limits
    def __init__(self):
        # create figure
        fig1 = plt.figure(figsize=plt.figaspect(0.41)*1.3)
        # axes in 3D and 2D
        self.ax = plt.subplot(1, 2, 1, projection='3d')
        self.ax2 = plt.subplot(1, 2, 2, adjustable='box', aspect=1)
        self.ax.cla()
        self.ax2.cla()
        fig1.tight_layout()
        self.ax.set_xlabel('x-axis')
        self.ax.set_ylabel('y-axis')
        self.ax.set_zlabel('z-axis')
        self.ax_lim = [-10, 10, -10, 10, 0, 20]
        self.ax.set_title("Estimated pose of the satellite in a global frame")
        plt.xlabel('u-axis')
        plt.ylabel('v-axis')
        self.ax2_lim = [-1, -1, 1, 1]
        self.ax.set_xlim([self.ax_lim[0], self.ax_lim[1]])
        self.ax.set_ylim([self.ax_lim[2], self.ax_lim[3]])
        self.ax.set_zlim([self.ax_lim[4], self.ax_lim[5]])
        self.ax2.set_xlim([self.ax2_lim[0], self.ax2_lim[2]])
        self.ax2.set_ylim([self.ax2_lim[1], self.ax2_lim[3]])
        self.ax2.set_axisbelow(True)
        self.ax2.set_title("Estimated pose of the satellite in the camera projection")
        plt.grid(True, color="#93a1a1", alpha=0.3)
        self.pause = 0.001

    # This function draws and updates the plots by first deleting the old axis-object and then redrawing it
    def update_draw(self, sat, camera, mes, sat_EKF, sat_pnp, mode):

        # delete old plot
        for artist in plt.gca().lines + plt.gca().collections:
            artist.remove()
        for artist in self.ax.lines + self.ax.collections:
            artist.remove()

        # draw camera
        self.ax.scatter(camera.camPos[0], camera.camPos[1], camera.camPos[2], color="y")
        for i in range(4):
            self.ax.plot3D(camera.camLogo[:, 0], camera.camLogo[:, 1], camera.camLogo[:, 2], color="y")

        # draw first plot
        # draw satellites
        if mode == 'simulation':
            self.draw_sat_3d(sat, sat_color='b', ax=self.ax)
        self.draw_sat_3d(sat_EKF, sat_color='r', ax=self.ax)
        # draw landmarks
        if mode == 'simulation':
            self.draw_lmk_3d(sat, s=10, color='b', marker='x', ax=self.ax)
        self.draw_lmk_3d(sat_EKF, s=10, color='r', marker='x', ax=self.ax)

        # draw second plot
        # draw satellites
        # self.draw_sat(sat, camera, sat_color="b", ax=self.ax2)
        self.draw_sat(sat_EKF, camera, sat_color="r", ax=self.ax2, label='EKF')
        self.draw_sat(sat_pnp, camera, sat_color="g", ax=self.ax2, label='PNP')
        # draw landmarks
        if mode == 'simulation':
            self.draw_lmk(sat.lmkPos, camera, s=10, color="b", marker="x", facecolors="b", label='False')
        self.draw_lmk(mes, camera, s=24, color="b", marker='s', facecolors='none', label='Measurement')
        self.draw_lmk(sat_EKF.lmkPos, camera, s=10, color="r", marker="x", facecolors="r", label='False')

        # activate legend in second plot
        self.ax2.legend(loc="best")
        plt.pause(self.pause)   # pause drawing to display result, remove for no display during calculation

    # Function to draw the satellite in the 2D plot by connecting the corner points in 'sat.crnPos'
    # It only draws the lines which match the 'satDim' values
    def draw_sat(self, sat, cam, sat_color, ax, label):
        cnt = 0
        val = 0.05
        for s, e in combinations(sat.crnPos, 2):
            if (sat.satDim[0]+val >= np.sqrt(np.sum((s - e) ** 2)) >= sat.satDim[0]-val) \
                    or (sat.satDim[1]+val >= np.sqrt(np.sum((s - e) ** 2)) >= sat.satDim[1]-val)\
                    or (sat.satDim[2]+val >= np.sqrt(np.sum((s - e) ** 2)) >= sat.satDim[2]-val):
                a1 = tf.get_point_pos_in_frame(cam, s)
                a2 = tf.get_point_pos_in_frame(cam, e)
                if not (np.isnan(a1).any() or np.isnan(a2).any()):
                    if cnt == 0 and not label == 'False':
                        ax.plot([a1[0], a2[0]], [a1[1], a2[1]], color=sat_color, label=label)
                        cnt = cnt + 1
                    else:
                        ax.plot([a1[0], a2[0]], [a1[1], a2[1]], color=sat_color)

    # Function to draw the landmarks in the 2D plot
    def draw_lmk(self, lmk_pnt, cam, s, color, marker, facecolors, label):
        cnt = 0
        for i in range(np.size(lmk_pnt,0)):
            if not (np.isnan(lmk_pnt[i])).any():
                if np.size(lmk_pnt,1) == 3:
                    x = tf.get_point_pos_in_frame(cam, lmk_pnt[i, :])
                else:
                    x = lmk_pnt[i, :]
                if not np.isnan(x).any():
                    if cnt == 0 and not label == 'False':
                        self.ax2.scatter(x[0], x[1], s=s, color=color, marker=marker, facecolors=facecolors, label=label)
                        cnt = cnt + 1
                    else:
                        self.ax2.scatter(x[0], x[1], s=s, color=color, marker=marker, facecolors=facecolors)

    # Function to draw the satellite in the 3D plot by connecting the corner points in 'sat.crnPos'
    # It only draws the lines which match the 'satDim' values
    def draw_sat_3d(self, sat, sat_color, ax):
        val = 0.05
        for s, e in combinations(sat.crnPos, 2):
            if (sat.satDim[0]+val >= np.sqrt(np.sum((s - e) ** 2)) >= sat.satDim[0]-val) \
                    or (sat.satDim[1]+val >= np.sqrt(np.sum((s - e) ** 2)) >= sat.satDim[1]-val)\
                    or (sat.satDim[2]+val >= np.sqrt(np.sum((s - e) ** 2)) >= sat.satDim[2]-val):
                ax.plot3D(*zip(s, e), color=sat_color)

    # Function to draw the landmarks in the 3D plot
    def draw_lmk_3d(self, sat, s, color, marker, ax):
        ax.scatter(sat.lmkPos[:, 0], sat.lmkPos[:, 1], sat.lmkPos[:, 2], s=s, color=color, marker=marker)

    # Function that shows the plot and creates the plots from the log. It should only be called at the end.
    def show_plot(self, sat, sat_EKF, nit, mode):
        fig2 = plt.figure(figsize=plt.figaspect(0.4) * 1.2)
        plt.subplot(212)
        if mode == 'simulation':
            plt.plot(sat.print_log('satRotVec')[0:nit,0]-sat_EKF.print_log('satRotVec')[0:nit,0], label='psi')
            plt.plot(sat.print_log('satRotVec')[0:nit,1]-sat_EKF.print_log('satRotVec')[0:nit,1], label='theta')
            plt.plot(sat.print_log('satRotVec')[0:nit,2]-sat_EKF.print_log('satRotVec')[0:nit,2], label='phi')
            plt.title('EKF angular detection error')
        else:
            plt.plot(sat_EKF.print_log('satAng')[0:nit, 0], label='psi')
            plt.plot(sat_EKF.print_log('satAng')[0:nit, 1], label='theta')
            plt.plot(sat_EKF.print_log('satAng')[0:nit, 2], label='phi')
            plt.title('Estimated satellite angle')

        plt.grid(b=True, which='major', color='#666666', linestyle='-')

        plt.legend()

        plt.subplot(211)
        if mode == 'simulation':
            plt.plot(sat.print_log('satPos')[0:nit,0]-sat_EKF.print_log('satPos')[0:nit,0], label='x')
            plt.plot(sat.print_log('satPos')[0:nit,1] - sat_EKF.print_log('satPos')[0:nit,1], label='y')
            plt.plot(sat.print_log('satPos')[0:nit,2] - sat_EKF.print_log('satPos')[0:nit,2], label='z')
            plt.title('EKF translational detection error')
        else:
            plt.plot(sat_EKF.print_log('satPos')[0:nit, 0], label='x')
            plt.plot(sat_EKF.print_log('satPos')[0:nit, 1], label='y')
            plt.plot(sat_EKF.print_log('satPos')[0:nit, 2], label='z')
            plt.title('Estimated satellite position')

        plt.grid(b=True, which='major', color='#666666', linestyle='-')
        plt.tight_layout()
        plt.legend()

        # this function shows the plot, it should only once be called at the end of all other calculations
        plt.show()

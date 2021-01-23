from itertools import combinations
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
import numpy as np
import itertools
import rotate
import measurement
from matplotlib.markers import MarkerStyle


class Draw:

    def __init__(self):
        fig1 = plt.figure(figsize=plt.figaspect(0.4)*1.2)
        self.ax = plt.subplot(1, 2, 1, projection='3d')
        self.ax2 = plt.subplot(1, 2, 2, adjustable='box', aspect=1)
        fig1.tight_layout()
        #self.ax2 = fig2.gca()
        #self.ax = fig1.gca(projection='3d')
        self.ax.cla()
        self.ax2.cla()
        self.ax_lim = [-10, 0, -10, 10, 20, 10]
        self.ax2_lim = [-1, -1, 1, 1]
        self.ax.set_xlim([self.ax_lim[0], self.ax_lim[3]])
        self.ax.set_ylim([self.ax_lim[1], self.ax_lim[4]])
        self.ax.set_zlim([self.ax_lim[2], self.ax_lim[5]])
        self.ax2.set_xlim([self.ax2_lim[0], self.ax2_lim[2]])
        self.ax2.set_ylim([self.ax2_lim[1], self.ax2_lim[3]])
        self.pause = 0.01

    def update_draw(self, sat, camera, mes):
        # draw first plot
        self.ax.cla()
        self.ax2.cla()
        self.ax.set_xlim([self.ax_lim[0], self.ax_lim[3]])
        self.ax.set_ylim([self.ax_lim[1], self.ax_lim[4]])
        self.ax.set_zlim([self.ax_lim[2], self.ax_lim[5]])
        self.ax2.set_xlim([self.ax2_lim[0], self.ax2_lim[2]])
        self.ax2.set_ylim([self.ax2_lim[1], self.ax2_lim[3]])
        self.ax.set_xlabel("x-axis", labelpad=15, fontsize=12, color="#333533");
        self.ax.set_ylabel("y-axis", labelpad=15, fontsize=12, color="#333533");
        self.ax.set_zlabel("z-axis", labelpad=15, fontsize=12, color="#333533");
        self.ax2.set_xlabel("x-axis in frame", labelpad=15, fontsize=12, color="#333533");
        self.ax2.set_ylabel("y-axis in frame", labelpad=15, fontsize=12, color="#333533");
        r = 2
        # draw satellite
        for s, e in combinations(sat.crnPos, 2):
            if (sat.satDim[0]+0.1 >= np.sqrt(np.sum((s - e) ** 2)) >= sat.satDim[0]-0.1) \
                    or (sat.satDim[1]+0.1 >= np.sqrt(np.sum((s - e) ** 2)) >= sat.satDim[1]-0.1)\
                    or (sat.satDim[2]+0.1 >= np.sqrt(np.sum((s - e) ** 2)) >= sat.satDim[2]-0.1):
                self.ax.plot3D(*zip(s, e), color="b")
        # draw landmarks
        self.ax.scatter(sat.lmkPos[:, 0], sat.lmkPos[:, 1], sat.lmkPos[:, 2], s=10, color="g", marker="x")
        # draw camera
        self.ax.scatter(camera.camPos[0], camera.camPos[1], camera.camPos[2], color="y")
        for i in range(4):
            self.ax.plot3D(camera.camLogo[:, 0], camera.camLogo[:, 1], camera.camLogo[:, 2], color="y")
        # draw second plot
        # draw satellite
        for s, e in combinations(sat.crnPos, 2):
            if (sat.satDim[0]+0.1 >= np.sqrt(np.sum((s - e) ** 2)) >= sat.satDim[0]-0.1) \
                    or (sat.satDim[1]+0.1 >= np.sqrt(np.sum((s - e) ** 2)) >= sat.satDim[1]-0.1)\
                    or (sat.satDim[2]+0.1 >= np.sqrt(np.sum((s - e) ** 2)) >= sat.satDim[2]-0.1):
                a1 = camera.get_point_pos_in_frame(s)
                a2 = camera.get_point_pos_in_frame(e)
                if not (np.isnan(a1).any() or np.isnan(a2).any()):  # all(a1 != np.nan) and all(a2 != np.nan):
                    self.ax2.plot([a1[0], a2[0]], [a1[1], a2[1]], color="b")
        # draw landmarks
        for i in range(sat.lmkN*6):
            a = camera.get_point_pos_in_frame(sat.lmkPos[i, :])
            if not (np.isnan(a[:])).any():
                self.ax2.scatter(a[0], a[1], s=10, color="g", marker="x")

        # draw measurement
        # draw landmarks
        for i in range(sat.lmkN*6):
            if not (np.isnan(mes[i, :])).any():
                self.ax2.scatter(mes[i, 0], mes[i, 1], s=24, color="tab:red", marker='s', facecolors='none')
        self.ax2.set_axisbelow(True)
        plt.grid(True, color="#93a1a1", alpha=0.3)
        plt.pause(self.pause)   # pause drawing

    def show_plot(self):
        plt.show()

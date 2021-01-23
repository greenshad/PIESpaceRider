from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
import numpy as np
import itertools
import time

fig = plt.figure()
ax = fig.gca(projection='3d')

def draw(satellite, landmarks):
    plt.cla()
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])
    ax.set_zlim([-5, 5])
    r = 2
    for s, e in combinations(satellite, 2):
        if np.sqrt(np.sum((s-e)**2)) <= 2.1:
            ax.plot3D(*zip(s, e), color="b")
    ah = combinations(satellite, 2)

    plt.pause(0.01)

def rotate(s, rotAng, origin):

    rotvec = R.from_euler('zyx', rotAng, degrees=False)
    if np.size(s) > 3:
        origin = np.tile(origin, (np.size(s, 0), 1))
    s = rotvec.apply(np.array(s)-origin) + origin
    return s


for i in range(1000):
    vec = rotate(np.array(list(itertools.product(*zip([1,1,1],[-1,-1,-1])))), [0,i/10,i/10], np.array([0,0,2]))
    draw(vec, 0)

plt.show()
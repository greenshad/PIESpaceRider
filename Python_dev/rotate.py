# rotate the points s around the axis by angles in radian (around x,y,z)
# rotAng needs to be a vector [rot_x, rot_y, rot_z]

from scipy.spatial.transform import Rotation as R
import numpy as np


def rotate(s, rotAng, origin):
    try:
        rotvec = R.from_euler('zyx', rotAng, degrees=False)
        if np.size(s) > 3:
            origin = np.tile(origin, (np.size(s, 0), 1))
        s = rotvec.apply(np.array(s)-origin) + origin
    except:
        print("Wrong rotation definition")
    return s

vec = rotate(np.array([1,1,1]), np.array([0,0,0]), np.array([0,0,0]))


######################################################################################################################
# Localization of a space cobot by visual odometry
# PIE
# ISAE SUPAERO
# Toulouse, 14.03.2021
#
# Authors: BECKE Philipp
#          SECHERESSE Vincent
#
##########################
# Transformation functions
##########################
# This file contains all relevant functions used for geometric transformations. It uses the scipy spatial transform
# module, see also:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html#scipy.spatial.transform.Rotation
######################################################################################################################

from scipy.spatial.transform import Rotation as Rot
import numpy as np

################
#multiplications
################

# multiplication of two quaternions
def quat_multiply(quaternion_1, quaternion_2):
    rot1 = Rot.from_quat(quaternion_1)
    rot2 = Rot.from_quat(quaternion_2)
    rot3 = rot2 * rot1
    return rot3.as_quat()

# multiplication of a quaternion by euler angles
def quat_euler_multiply(quaternion, euler, order, degrees):
    rot1 = Rot.from_quat(quaternion)
    rot2 = Rot.from_euler(order, euler, degrees=degrees)
    rot3 = rot2 * rot1
    return rot3.as_quat()

###############################
# applying rotations to vectors
###############################

# apply euler angles to vector
def apply_euler_to_vec(vector, euler, order, degrees):
    rot = Rot.from_euler(order, euler, degrees=degrees)
    return rot.apply(vector)

# apply quaternion to vector
def apply_quat_to_vec(vector, quaternion):
    rot = Rot.from_quat(quaternion)
    return rot.apply(vector)

# calculate quaternion from euler angle
def quat_from_euler(euler, order, degrees):
    rot = Rot.from_euler(order, euler, degrees=degrees)
    return rot.as_quat()

######################################
# transformations in different formats
######################################

# calculate euler angle from quaternion
def euler_from_quat(quaternion, order, degrees):
    rot = Rot.from_quat(quaternion)
    return rot.as_euler(order, degrees=degrees)

# calculate quaternion from rotational vector
def quat_from_rotvec(rotation_vector):
    rot = Rot.from_rotvec(np.concatenate(rotation_vector))
    return rot.as_quat()

# calculate rotational vector from quaternion
def quat_to_rotvec(quat):
    rot = Rot.from_quat(quat)
    return rot.as_rotvec()

# calculate quaternion from inverse rotational vector
def quat_from_rotvec_inv(rotation_vector):
    rot = Rot.from_rotvec(np.concatenate(rotation_vector))
    return rot.inv().as_quat()

#######################
# camera transformation
#######################

# gets point in camera frame from absolute frame
def get_point_pos_in_frame(cam, vector):
    rot1 = Rot.from_quat(cam.camQuat)
    rel_pos = rot1.inv().apply(vector) - cam.camPos
    frame_pos = np.array([-cam.foc * rel_pos[0] / rel_pos[2], cam.foc * rel_pos[1] / rel_pos[2]])
    return frame_pos

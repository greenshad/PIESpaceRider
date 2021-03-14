######################################################################################################################
# Study of a visual odometry chain for the localization and autonomous piloting of a maintenance UAV for the Space Rider
# PIE
# ISAE SUPAERO
# Toulouse, 14.03.2021
#
# Authors: BECKE Philipp
#          SECHERESSE Vincent
#
###############
# EKF algorithm
###############
# This functions are used to calculate an Extended Kalman Filter
# See https://en.wikipedia.org/wiki/Extended_Kalman_filter for more information.
# The state vector contains the following variables:
# X = [x, y, z, psi, theta, phi,                                - position and orientation
#      x_p, y_p, z_p, psi_p, theta_p, phi_p]                    - velocity and angular velocity
# carte = [mi], mi = [xi, yi]                                   - reference map of landmarks in sat. coordinates
# z = [zi], zi = [lmkID, [xFrame, yFrame]]                      - landmark measurements
######################################################################################################################

import numpy as np
import Transformations as tf


# Calculate a step of the EKF
def stepEKF(X, P, Q, z, dt, carte, foc, r, mode):

    # Calculation of the prediction
    X1 = f(X, dt)                                   # calculate the prediction with the function f(x)
    F = computeF(X1, dt)                            # calculate the jacobian matrix of the function f(x)
    P = F.dot(P).dot(np.transpose(F)) + Q           # calculate the state covariance matrix
    
    # Correction of the position
    if np.size(z, 0) > 0:
        for i in range(np.size(z, 0)):                              # looping through all landmarks
            # calculate EKF correction for one landmark
            zi = z[i]
            lmkId = zi[0]
            mi = carte[lmkId.astype(int)]
            H = computeH(X1, mi, foc)
            if mode == 'simulation':
                R = r * np.eye(2)
            else:
                R = r[i] * np.eye(2)
            #R = r[i] * np.eye(2)
            y = zi[1:3] - hf(X1, mi, foc)
            S = H.dot(P).dot(np.transpose(H)) + R
            K = P@(np.transpose(H)@np.linalg.inv(S))
            X1 = X1 + K.dot(y)
            P = (np.identity(np.size(P, 0))-K.dot(H)).dot(P)
            X1 = correct_pi_jumps(X1)               # correct for the jump between -pi and pi
    return [X1, P]

# calculate the function f(x)
def f(X, dt):
    #  first order approximation : small rotation speed
    X1 = X.copy()

    # position predictions
    X1[0] += X[6]*dt
    X1[1] += X[7]*dt
    X1[2] += X[8]*dt

    # angular predictions
    X1[3] += X[9]*dt
    X1[4] += X[10]*dt
    X1[5] += X[11]*dt
    return X1

# numerical approximation of the jacobian matrix of the function f(x)
def computeF(X, dt):
    F = np.array([[0. for col in range(np.size(X))] for row in range(np.size(X))])
    dx = 0.05
    for i in range(np.size(F, 0)):
        for j in range(np.size(F, 1)):
            h = np.array([0. for k in range(np.size(X))])
            h[j] = dx
            F[i, j] = (f(X+h, dt)[i]-f(X, dt)[i])/dx
    return F

# function to map state points into measurement reference frame
def hf(X,mi,foc):
    zest = [0, 0]
    miRelPos = tf.apply_euler_to_vec(mi, X[3:6], 'xyz', False) + X[0:3]
    # get position on frame
    zest[0] = -foc * (miRelPos[0]/miRelPos[2])
    zest[1] = foc * (miRelPos[1]/miRelPos[2])
    return zest

# numerical approximation of the jacobian matrix of the function hf(x)
def computeH(X, mi, foc):
    # approximation of the jacobian of h
    H = np.array([[0. for col in range(np.size(X))] for row in range(2)])
    dx = 0.0001
    for i in range(np.size(H, 0)):
        for j in range(np.size(H, 1)):
            h = np.array([0. for k in range(np.size(X))])
            h[j] = dx
            H[i, j] = (hf(X+h, mi, foc)[i]-hf(X, mi, foc)[i])/dx
    return H

# function to correct for values smaller/bigger than -pi/pi
def correct_pi_jumps(X):
    if X[3] > np.pi:
        X[3] += -2*np.pi
    if X[4] > np.pi:
        X[4] += -2*np.pi
    if X[5] > np.pi:
        X[5] += -2*np.pi
    if X[3] < -np.pi:
        X[3] += 2*np.pi
    if X[4] < -np.pi:
        X[4] += 2*np.pi
    if X[5] < -np.pi:
        X[5] += 2*np.pi
    return X

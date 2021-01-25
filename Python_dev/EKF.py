# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:08:42 2021

@author: Vincent
"""
import numpy as np
from scipy.spatial.transform import Rotation as R


def stepEKF(u,X,P,Q,R,z,dt,carte,fov):
    # X = [x, y, z, psi, theta, phi,
    #      x_p, y_p, z_p, psi_p, theta_p, phi_p]
    # u = [ax, ay, az, gx, gy, gz] -> accelerations in cam referential
    # map = [mi], mi = [xi, yi, zi]
    # z = [zi], zi = [lmkID, [xFramei, yFramei]]
    
    
    # PREDICTION
    X = f(X,u,dt)
    # X(4) = mod(X(4)+pi,2*pi)-pi;
    
    F = computeF(X,u,dt)
    P = F*P*F.transpose + Q
    
    # CORRECTION
    for i in range(np.size(z[0])):
        zi = z[i]
        lmkId = zi[1]
        mi = carte[lmkId]
        H = computeH(X,mi,fov)
        
        y = zi - h(X,mi,fov)
        S = H*P*np.transpose.H + R
        K = P*np.transpose.H*np.linalg.inv(S);
        X = X + K*y;
        # X(4) = mod(X(4)+pi,2*pi)-pi;
        P = (np.identity(np.size(P,0))-K*H)*P;
    
    return [X, P]

def f(X,u,dt):
    #  first order approximation : small rotation speed
    X1 = X.copy()
    
    X1[10] += 
    X1[11] += 
    X1[12] += 
    
    X1[7] += u[1]
    X1[8] += u[2]
    X1[9] += u[3]
    
    X1[4] += X[10]*dt
    X1[5] += X[11]*dt
    X1[6] += X[12]*dt
    
    X1[1] += X[7]*dt
    X1[2] += X[8]*dt
    X1[3] += X[9]*dt
    return X1

def computeF(X,u,dt):
    F = np.identity(np.size(X))
    
    F[4,10] = X[10]*dt
    F[5,11] = X[11]*dt
    F[6,12] = X[12]*dt
    
    F[1,7] = X[7]*dt
    F[2,8] = X[8]*dt
    F[3,9] = X[9]*dt
    return F

def h(X,mi,fov):
    
    return 

def computeH(X,mi,fov):
    
    return H
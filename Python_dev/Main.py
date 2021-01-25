# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:08:42 2021

@author: Vincent
"""

import numpy as np

# parameters definition :
# X = [rho, theta, phi, alpha, beta, gamma,
#      rho_p, theta_p, phi_p, alpha_p, beta_p, gamma_p]
# u = [ax, ay, az, gx, gy, gz] -> accelerations in cam referential
# map = [mi], mi = [xi, yi, zi]
# z = [zi], zi = [lmkID, [xFramei, yFramei]]



dt = 0.1
covP = 0.1
covQ = 0.1
covR = 0.1

nit = 2000


cam = camera()
carte = initMap()
sat = satellite()


draw(cam.getX(),sat.getX(),X,z,carte)


P = initP(covP)
Q = initQ(covQ)
R = initR(covR)


for i in range(nit):
    
    u = cam.commandCam(X)
    v = sat.commandSat()
    
    cam.updateCamPosition(u,dt)
    sat.updateSatPosition(v,dt)
    
    z = createZOutput(cam.getX(), sat.getX(),carte,R)
    # YOLOOutput,R = createYOLOOutput(XCam, Xsat,carte,R)
    # z = convertYolo2EKF(YOLOOutput,camParameter)
    [X, P] = stepEKF(u,X,P,Q,R,z,dt,carte,fov)
    
    draw(cam.getX(),sat.getX(),X,z,carte)




# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:08:42 2021

@author: Vincent, Philipp
"""

import numpy as np
import draw
import satellite
import camera
import measurement

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

graph = draw.Draw()
sat = satellite.Satellite(5)
cam = camera.Camera()




for i in range(nit):
    # vec = rotate.rotate(np.array(list(itertools.product(*zip([1, 1, 1],[-1, -1, -1])))), [0, i/10, i/10], np.array([0, 0, 2]))
    # graph.update_draw(vec, 0)
    #sat.rotate_sat([i/1000, np.sin(i/1000), -i/1000])
    
    # u = cam.commandCam(X)
    # v = sat.commandSat()
    
    # cam.updateCamPosition(u,dt)
    # sat.updateSatPosition(v,dt)
    
    # z = createZOutput(cam.getX(), sat.getX(),carte,R)
    # YOLOOutput,R = createYOLOOutput(XCam, Xsat,carte,R)
    # z = convertYolo2EKF(YOLOOutput,camParameter)
    # [X, P] = stepEKF(u,X,P,Q,R,z,dt,carte,fov)
    
    draw(cam.getX(),sat.getX(),X,z,carte)

    cam.set_cam_omega([-np.sin(dt*0.5), np.sin(dt*0.1), np.sin(dt*0.2)])
    sat.set_sat_omega([1, 1, 1])
    sat.set_sat_speed([1, 1, 1])

    sat.update_sat_pos(dt)
    cam.update_cam_pos(dt)
    mes = measurement.get_measurements(sat, cam, 0.01)
    graph.update_draw(sat, cam, mes)

graph.show_plot()

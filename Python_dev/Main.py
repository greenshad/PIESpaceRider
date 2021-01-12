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
    
    cam.updateCamPosition(u)
    cam.updateSatPosition(v)
    
    z = createZOutput(cam.getX(), sat.getX(),carte,R)
    # YOLOOutput,R = createYOLOOutput(XCam, Xsat,carte,R)
    # z = convertYolo2EKF(YOLOOutput,camParameter)
    [X, P] = stepEKF(u,X,P,Q,R,z,dt,carte)
    
    draw(cam.getX(),sat.getX(),X,z,carte)




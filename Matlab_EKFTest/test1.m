close all
clear

lmkN = 8;

cam = camera();
sat = satellite(lmkN);
mes = measurement();
ekf = EKF(sat);

fig = initGraphics(sat,cam,mes,ekf);

mes.setVariance(0.01,0.01,0.01);
% mes.setVariance(0.0,0.0,0.0);
sat.setSatPos([0,10,0]);
sat.setSatAngle(0);
draw(sat,cam,fig,mes)


dt = 0.001;
sat.setSatPos([0,10,0]);
sat.setSatAngle(0);
cam.setCamPos([0, 0, 0]);
cam.setCamAngle(0);

X0 = [0,0,0]';
P0 = 25*eye(size(X0,1));
Q = 0.001*eye(4);
R = 0.1*eye(2);
ekf.setEkfParam(X0,P0,Q,R);

Xreal = zeros(4,400);
Xest = zeros(4,100);
    
for i=1:1000
    sat.changeSatSpeed([0.2*cos(i/60), 0.2*cos(i/70), 0.05*cos(i/80)]);
    sat.changeSatOmega(3.14/30*cos(i/50));
    cam.changeCamSpeed([0.5*cos(i/20), 1*cos(i/30), 0]);
    cam.changeCamOmega(3.14/25*cos(i/10));
    sat.updateSatPos(dt);
    cam.updateCamPos(dt);
    mes.getMeasurements(sat,cam);
    ekf.stepEKF(sat,cam,mes,dt);
    draw(sat,cam,fig,mes,ekf);
    Xreal(:,i) = [sat.satPos, sat.satTheta];
    try
        Xest(:,i) = ekf.ekfX + [cam.camPos, cam.camTheta]';
    end
end 

plotError(Xreal, Xest);
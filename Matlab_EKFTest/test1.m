close all
clear

lmkN = 2;

cam = camera();
sat = satellite(lmkN);
mes = measurement();
ekf = EKF(sat);

fig = initGraphics(sat,cam,mes,ekf);

mes.setVariance(0.02,0.02,0.02);
% mes.setVariance(0.0,0.0,0.0);
sat.setSatPos([0,10,0]);
sat.setSatAngle(0);
draw(sat,cam,fig,mes)


dt = 0.001;
sat.setSatPos([0,10,0]);
sat.setSatAngle(0);
cam.setCamPos([0, 0, 0]);
cam.setCamAngle(0);

initPosSig = 0.001;
X0 = [sat.satPos - cam.camPos, sat.satTheta - cam.camTheta]'+normrnd(0,initPosSig,4,1);
P0 = initPosSig*eye(size(X0,1));
Q = 0.01*eye(4);
R = 0.04*eye(2);
ekf.setEkfParam(X0,P0,Q,R);

niterations = 4000;

Xreal = zeros(4,niterations);
Xest = zeros(4,niterations);
P = zeros(4,niterations);

for i=1:niterations
    sat.changeSatSpeed([0.2*cos(i/60), 0.2*cos(i/70), 0.05*cos(i/80)]);
    sat.changeSatOmega(3.14/100*cos(i/50));
    cam.changeCamSpeed([0.5*cos(i/20), 1*cos(i/30), 0]);
%     cam.changeCamOmega(-3.14/100*cos(i/50));        % x drifting for some reason when uncommented
    sat.updateSatPos(dt);
    cam.updateCamPos(dt);
    mes.getMeasurements(sat,cam);
    ekf.stepEKF(sat,cam,mes,dt);
    if rem(i,20) == 0
        draw(sat,cam,fig,mes,ekf);
    end
    Xreal(:,i) = [sat.satPos, sat.satTheta];
    try
        Xest(:,i) = ekf.ekfX + [cam.camPos, cam.camTheta]';
        for j=1:4
            P(j,i) = ekf.ekfP(j,j);
        end
    end
end

plotError(Xreal, Xest,P,0);
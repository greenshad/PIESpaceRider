close all
clear

lmkN = 5;

cam = camera();
sat = satellite(lmkN);
mes = measurement();
ekf = EKF(sat);

fig = initGraphics(sat,cam,mes,ekf);

mes.setVariance(0.01,0.01,0.01);
sat.setSatPos([0,10,0]);
sat.setSatAngle(0);
draw(sat,cam,fig,mes)



% for i=1:400
%     sat.setSatPos([0,10,0] + [2*sin(i/60), 3*sin(i/70), 1*sin(i/80)]);
%     sat.setSatAngle(3.14/3*sin(i/50));
%     cam.setCamPos([0.5*sin(i/20), 1*sin(i/30), 0]);
%     cam.setCamAngle(3.14/25*sin(i/10));
%     mes.getMeasurements(sat,cam);
%     draw(sat,cam,fig,mes)
%     %pause(0.1)
% end 

dt = 0.001;
sat.setSatPos([0,10,0]);
sat.setSatAngle(0);
cam.setCamPos([0, 0, 0]);
cam.setCamAngle(0);

ekf = EKF(sat);

X0 = [sat.satPos - cam.camPos, sat.satTheta - cam.camTheta]';
P0 = zeros(size(X0,1));
Q = 0*eye(4);
R = 1/100*eye(2);
ekf.setEkfParam(X0,P0,Q,R);
    
for i=1:400
    sat.changeSatSpeed([0.2*cos(i/60), 0.3*cos(i/70), 0.1*cos(i/80)]);
    sat.changeSatOmega(3.14/30*cos(i/50));
%     cam.changeCamSpeed([0.5*cos(i/20), 1*cos(i/30), 0]);
%     cam.changeCamOmega(3.14/25*cos(i/10));
    sat.updateSatPos(dt);
    cam.updateCamPos(dt);
    mes.getMeasurements(sat,cam);
    ekf.stepEKF(sat,cam,mes,dt);
%     draw(sat,cam,fig,mes);
    draw(sat,cam,fig,mes,ekf);
end 

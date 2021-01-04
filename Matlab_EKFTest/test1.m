close all
clear

lmkN = 5;

cam = camera();
sat = satellite(lmkN);
mes = measurement();
fig = initGraphics(sat,cam,mes);


% for i=1:100
%     cam.translateCam([0,0.1,0]);
%     draw(sat,cam,fig)
% end
% 
% cam.setCamPos([0,0,0]);
% draw(sat,cam,fig)
% cam.setCamAngle(0);
% draw(sat,cam,fig)
% 
% for i=1:150
%     cam.rotateCam(0.05);
%     draw(sat,cam,fig)
% end 
% 
% cam.setCamPos([0,0,0]);
% cam.setCamAngle(0);
% draw(sat,cam,fig)
% 
% for i=1:120
%     sat.rotateSat(0.05);
%     draw(sat,cam,fig)
% end 
% 
% sat.setSatAngle(0);
% draw(sat,cam,fig)
% 
% for i=1:100
%     sat.translateSat([0,-0.11,0]);
%     draw(sat,cam,fig)
% end 

mes.setVariance(0.01,0.01,0.01)
sat.setSatPos([0,10,0]);
sat.setSatAngle(0);
draw(sat,cam,fig,mes)


for i=1:400
    sat.setSatPos([0,10,0] + [2*sin(i/60), 3*sin(i/70), 1*sin(i/80)]);
    sat.setSatAngle(3.14/3*sin(i/50));
    cam.setCamPos([0.5*sin(i/20), 1*sin(i/30), 0]);
    cam.setCamAngle(3.14/25*sin(i/10));
    mes.getMeasurements(sat,cam)
    draw(sat,cam,fig,mes)
    %pause(0.1)
end 

close all
clear

lmkN = 10;

cam = camera();
sat = satellite();
fig = initGraphics(sat,cam);

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

sat.setSatPos([0,10,0]);
sat.setSatAngle(0);
draw(sat,cam,fig)


for i=1:400
    sat.setSatPos([0,10,0] + [2*sin(i/60), 3*sin(i/70), 1*sin(i/80)]);
    sat.setSatAngle(3.14/3*sin(i/50));
    cam.setCamPos([0.5*sin(i/20), 1*sin(i/30), 0]);
    cam.setCamAngle(3.14/25*sin(i/10));
    draw(sat,cam,fig)
end 

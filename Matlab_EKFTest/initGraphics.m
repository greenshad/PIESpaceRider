% create the graphics displaying the camera frame and the relative position
% of the satellite and camera on the x,y plan.
function fig = initGraphics(sat,cam)
fig.fig = figure("name", "EKF graphics",'NumberTitle','off');
set(fig.fig,'WindowStyle','docked')

subplot(1,2,1)
subplot(1,2,2)

fig.fig.Children(1).Title.String = "Relative Position";
fig.fig.Children(1).XLabel.String = 'x position';
fig.fig.Children(1).YLabel.String = 'y position';
fig.fig.Children(1).XLim = [-10,10];
fig.fig.Children(1).YLim = [-10,20];
fig.fig.Children(1).DataAspectRatioMode = "manual";

fig.fig.Children(2).Title.String = "Camera Frame";
fig.fig.Children(2).XLim = [-1,1];
fig.fig.Children(2).YLim = [-1,1];
fig.fig.Children(2).DataAspectRatioMode = "manual";

draw(sat,cam,fig)
end
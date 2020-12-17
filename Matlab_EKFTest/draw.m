function draw(sat,cam,fig)

% relative position
fig.fig.CurrentAxes = fig.fig.Children(1);
cla
hold on
plot(fig.fig.Children(1),cam.camPos(1), cam.camPos(2),"x")
plot(fig.fig.Children(1),cam.camSight(:,1), cam.camSight(:,2))
plot(fig.fig.Children(1),cam.camLogo(:,1), cam.camLogo(:,2))

plot(fig.fig.Children(1),sat.satPos(1), sat.satPos(2),'.')
plot(fig.fig.Children(1),sat.crnPos(:,1), sat.crnPos(:,2))
plot(fig.fig.Children(1),sat.crnPos(:,1), sat.crnPos(:,2),'.')
plot(fig.fig.Children(1),sat.crnPos(:,1), sat.crnPos(:,2),'.')
hold off


% camera frame
fig.fig.CurrentAxes = fig.fig.Children(2);
cla
hold on
drawnow

% plot Sat center
satFramePos = cam.getPointPosInFrame(sat.satPos);
plot(fig.fig.Children(2),satFramePos(1), satFramePos(2),'+')

% plot Sat sides
satCornerFramePos = zeros(size(sat.crnPos,1)+1,2);
for i=1:size(sat.crnPos,1)
    satCornerFramePos(i,:) = cam.getPointPosInFrame(sat.crnPos(i,:));
end
satCornerFramePos(size(sat.crnPos,1)+1,:) = satCornerFramePos(1,:);
plot(fig.fig.Children(2),satCornerFramePos(:,1), satCornerFramePos(:,2))

% plot landmarks positions
for i=1:sat.lmkN
    satLandmarkFramePos = cam.getPointPosInFrame(sat.lmkPos(i,:));
    plot(fig.fig.Children(2),satLandmarkFramePos(1), satLandmarkFramePos(2),'.')
end
hold off
drawnow
end
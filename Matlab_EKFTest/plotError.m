function plotError(Xreal, Xest,P,plotCov)
fig = figure("name", "Error plot",'NumberTitle','off');
set(fig,'WindowStyle','docked')

subplot(2,2,1)
subplot(2,2,2)
subplot(2,2,3)
subplot(2,2,4)

fig.CurrentAxes = fig.Children(4);
fig.Children(4).Title.String = "xSat : real vs est";
fig.Children(4).XLabel.String = 'iterations';
fig.Children(4).YLabel.String = 'xSat';
hold on
plot(Xreal(1,:))
plot(Xest(1,:))
if plotCov
    plot(1:size(P,2), Xest(1,:) + sqrt(P(1,:)),'g')
    plot(1:size(P,2), Xest(1,:) - sqrt(P(1,:)),'g')
end
legend('real', 'est')
hold off

fig.CurrentAxes = fig.Children(3);
fig.Children(3).Title.String = "ySat : real vs est";
fig.Children(3).XLabel.String = 'iterations';
fig.Children(3).YLabel.String = 'ySat';
hold on
plot(Xreal(2,:))
plot(Xest(2,:))
if plotCov
    plot(1:size(P,2), Xest(2,:) + sqrt(P(2,:)),'g')
    plot(1:size(P,2), Xest(2,:) - sqrt(P(2,:)),'g')
end
legend('real', 'est')
hold off

fig.CurrentAxes = fig.Children(2);
fig.Children(2).Title.String = "zSat : real vs est";
fig.Children(2).XLabel.String = 'iterations';
fig.Children(2).YLabel.String = 'zSat';
hold on
plot(Xreal(3,:))
plot(Xest(3,:))
if plotCov
    plot(1:size(P,2), Xest(3,:) + sqrt(P(3,:)),'g')
    plot(1:size(P,2), Xest(3,:) - sqrt(P(3,:)),'g')
end
legend('real', 'est')
hold off

fig.CurrentAxes = fig.Children(1);
fig.Children(1).Title.String = "thetaSat : real vs est";
fig.Children(1).XLabel.String = 'iterations';
fig.Children(1).YLabel.String = 'thetaSat';
hold on
plot(Xreal(4,:))
plot(Xest(4,:))
if plotCov
    plot(1:size(P,2), Xest(4,:) + sqrt(P(4,:)),'g')
    plot(1:size(P,2), Xest(4,:) - sqrt(P(4,:)),'g')
end
legend('real', 'est')
hold off
end
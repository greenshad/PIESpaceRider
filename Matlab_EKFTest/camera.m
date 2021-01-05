% create the camera object. It can move in 3d but can only rotate around
% the z axis. Its field of viex can be changed.
classdef camera < handle
    properties
        camPos
        camTheta
        fov
        foc
        camSight
        camLogo
        camSpeed
        camOmega
    end
    
    methods
        % constructor
        function obj = camera()
            obj.camPos = [0,0,0];
            obj.camTheta = 0*3.14/180;
            obj.camSpeed = [0,0,0];
            obj.camOmega = 0;
            obj.fov = 40*3.14/180;              % camera fov
            obj.foc = 0.5/tan(obj.fov/2);       % camera focal distance
            
            obj.camSight = obj.camPos + [0,0,0;...
                0,obj.foc,0];
            obj.camSight = rotate(obj.camSight, 'zrotate', obj.camTheta, obj.camPos);
            
            obj.camLogo = obj.camPos + [0,0,0;...
                -obj.foc*sin(obj.fov/2), obj.foc, 0;...
                +obj.foc*sin(obj.fov/2), obj.foc, 0;...
                0,0,0];
            obj.camLogo = rotate(obj.camLogo, 'zrotate', obj.camTheta, obj.camPos);
        end
        
        % various functions to move the camera
        function obj = translateCam(obj, vect)
            obj.camPos = obj.camPos + vect;
            obj.camSight = obj.camSight + vect;
            obj.camLogo = obj.camLogo + vect;
        end
        
        function obj = setCamPos(obj, vect)
            obj.camSight = obj.camSight - obj.camPos + vect;
            obj.camLogo = obj.camLogo - obj.camPos + vect;
            obj.camPos = vect;
        end
        
        function obj = rotateCam(obj, theta)
            obj.camSight = rotate(obj.camSight, 'zrotate', theta, obj.camPos);
            obj.camLogo = rotate(obj.camLogo, 'zrotate', theta, obj.camPos);
            obj.camTheta = obj.camTheta + theta;
        end
        
        function obj = setCamAngle(obj, theta)
            obj.camSight = rotate(obj.camSight, 'zrotate', theta - obj.camTheta, obj.camPos);
            obj.camLogo = rotate(obj.camLogo, 'zrotate', theta - obj.camTheta, obj.camPos);
            obj.camTheta = theta;
        end
        
        function obj = changeCamSpeed(obj, vect)
            obj.camSpeed = obj.camSpeed + vect;
        end
        
        function obj = setCamSpeed(obj, vect)
            obj.camSpeed = vect;
        end
        
        function obj = changeCamOmega(obj, omega)
            obj.camOmega = obj.camOmega + omega;
        end
        
        function obj = setCamOmega(obj, omega)
            obj.camOmega = omega;
        end
        
        function obj = updateCameraPos(obj, dt)
            obj.rotateCam(obj.camOmega*dt/2);
            obj.translateCam(obj.camSpeed*dt);
            obj.rotateCam(obj.camOmega*dt/2);
        end
        
        % output a point position on the camera frame
        function framePos = getPointPosInFrame(obj, absPos)
            relPos = rotate(absPos, 'zrotate', -obj.camTheta, obj.camPos) - obj.camPos;
            relativeAngle = [atan(relPos(1)/relPos(2)),...
                atan(relPos(3)/relPos(2))];
            framePos = relativeAngle*2/obj.fov;
            if max(abs(framePos)) > 1 || relPos(2)<0
                framePos = [NaN, NaN];
            end
        end
        
    end
end
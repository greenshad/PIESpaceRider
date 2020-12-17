classdef camera < handle
    properties
        camPos
        camTheta
        fov
        foc
        camSight
        camLogo
    end
    
    methods
        
        function obj = camera()
            obj.camPos = [5,0,0];
            obj.camTheta = 0.5;
            obj.fov = 40*3.14/180;
            obj.foc = 0.5/tan(obj.fov/2);
            
            obj.camSight = obj.camPos + [0,0,0;...
                0,obj.foc,0];
            obj.camSight = rotate(obj.camSight, 'zrotate', obj.camTheta, obj.camPos);
            
            obj.camLogo = obj.camPos + [0,0,0;...
                -obj.foc*sin(obj.fov/2), obj.foc, 0;...
                +obj.foc*sin(obj.fov/2), obj.foc, 0;...
                0,0,0];
            obj.camLogo = rotate(obj.camLogo, 'zrotate', obj.camTheta, obj.camPos);
        end
        
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
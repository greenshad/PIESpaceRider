classdef satellite < handle
    properties
        satPos
        satTheta
        crnPos
        lmkPos
        lmkN
    end
    methods
        function obj = satellite(lmkN)
            obj.lmkN = lmkN;
            obj.satPos = [0,10,0];     % x,y,z position of the center
            obj.satTheta = 0;                % the = rotation
            obj.crnPos = obj.satPos + [-1,0,-1;...
                -1,0,1;...
                1,0,1;...
                1,0,-1];
            obj.crnPos = rotate(obj.crnPos, 'zrotate', obj.satTheta, obj.satPos);
            
            obj.lmkPos = obj.satPos(1:3) + zeros(lmkN,3);
            for i=1:lmkN
                obj.lmkPos(i,1) = obj.lmkPos(i,1) + 2*rand()-1;
                obj.lmkPos(i,3) = obj.lmkPos(i,3) + 2*rand()-1;
            end
            obj.lmkPos = rotate(obj.lmkPos, 'zrotate', obj.satTheta, obj.satPos);
        end
        
        function obj = translateSat(obj, vect)
            obj.satPos = obj.satPos + vect;
            obj.crnPos = obj.crnPos + vect;
            obj.lmkPos = obj.lmkPos + vect;
        end
        
        function obj = setSatPos(obj, vect)
            obj.crnPos = obj.crnPos - obj.satPos + vect;
            obj.lmkPos = obj.lmkPos - obj.satPos + vect;
            obj.satPos = vect;
        end
        
        function obj = rotateSat(obj, theta)
            obj.crnPos = rotate(obj.crnPos, 'zrotate', theta, obj.satPos);
            obj.lmkPos = rotate(obj.lmkPos, 'zrotate', theta, obj.satPos);
            obj.satTheta = obj.satTheta + theta;
        end
        
        function obj = setSatAngle(obj, theta)
            obj.crnPos = rotate(obj.crnPos, 'zrotate', theta - obj.satTheta, obj.satPos);
            obj.lmkPos = rotate(obj.lmkPos, 'zrotate', theta - obj.satTheta, obj.satPos);
            obj.satTheta = theta;
        end
    end
end

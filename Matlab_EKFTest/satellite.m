% Satellite class, a square of dimension 1 that can move in 3d
% but can only rotate around the z axis. It has a certain number of
% landmarks, randomly generated.
classdef satellite < handle
    properties
        satPos
        satTheta
        crnRelPos
        crnPos
        lmkRelPos
        lmkPos
        lmkN
        satSpeed
        satOmega
    end
    methods
        % constructor
        function obj = satellite(lmkN)
            obj.lmkN = lmkN;                    % uses 5 landmarks by default
            obj.satPos = [0,10,0];           % x,y,z position of the center
            obj.satTheta = 0;                % the = rotation around z axis
            obj.satSpeed = [0,0,0];
            obj.satOmega = 0;
            
            obj.crnRelPos = [-1,0,-1;...
                -1,0,1;...
                1,0,1;...
                1,0,-1];
            obj.crnPos = obj.satPos + obj.crnRelPos;
            obj.crnPos = rotate(obj.crnPos, 'zrotate', obj.satTheta, obj.satPos);
            
            % initialise landmarks positions
            obj.lmkRelPos = zeros(obj.lmkN,3);
            for i=1:obj.lmkN
                obj.lmkRelPos(i,1) = 2*rand()-1;
                obj.lmkRelPos(i,3) = 2*rand()-1;
            end
            obj.lmkPos = obj.satPos(1:3) + obj.lmkRelPos;
            obj.lmkPos = rotate(obj.lmkPos, 'zrotate', obj.satTheta, obj.satPos);
        end
        
        
        % various functions to interact with the satellite
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
        
        function obj = changeSatSpeed(obj, vect)
            obj.satSpeed = obj.satSpeed + vect;
        end
        
        function obj = setSatSpeed(obj, vect)
            obj.satSpeed = vect;
        end
        
        function obj = changeSatOmega(obj, omega)
            obj.satOmega = obj.satOmega + omega;
        end
        
        function obj = setSatOmega(obj, omega)
            obj.satOmega = omega;
        end
        
        function obj = updateSatPos(obj, dt)
            obj.rotateSat(obj.satOmega*dt/2);
            obj.translateSat(obj.satSpeed*dt);
            obj.rotateSat(obj.satOmega*dt/2);
        end
    end
end

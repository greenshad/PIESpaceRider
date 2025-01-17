% Measurement class, used to create measurements with a certain level of
% noise from the camera frame.
classdef measurement < handle
    properties
        measSatPos
        measCrnPos
        measLmkPos
        measLmkPnt
        simVarSat
        simVarCrn
        simVarLmk
    end
    methods
        
         % constructor
        function obj = measurement()
            obj.measSatPos = [0,0];          %  no measurements taken
            obj.measCrnPos = [0,0];
            obj.measLmkPos = [0,0];
            obj.measLmkPnt = 0;
            obj.simVarSat = 0;               %  standard variance is zero
            obj.simVarCrn = 0;
            obj.simVarLmk = 0; 
        end
        
        % calculates the measurements from the camera frame
        function obj = getMeasurements(obj,sat,cam)
            
            % creates empty pointer vector
            obj.measLmkPnt = zeros(size(sat.satPos,1) + size(sat.crnPos,1) + sat.lmkN,1);
            
            % measure Sat center
            obj.measSatPos = cam.getPointPosInFrame(sat.satPos) + normrnd(0,obj.simVarSat,[1,2]);
            obj.measLmkPnt(1) = 1;
            
            % measure Sat sides
            satCornerFramePos = zeros(size(sat.crnPos,1),2);
            for i=1:size(sat.crnPos,1)
                satCornerFramePos(i,:) = cam.getPointPosInFrame(sat.crnPos(i,:)) + normrnd(0,obj.simVarCrn,[1,2]);
                obj.measLmkPnt(1+i) = 1+i;
            end
            obj.measCrnPos = satCornerFramePos;

            % measure landmark positions
            satLandmarkFramePos = zeros(size(sat.lmkN,1),2);
            if sat.lmkN == 0
                satLandmarkFramePos = [];
            end
            pntLen = 1+i;
            for i=1:sat.lmkN
                satLandmarkFramePos(i,:) = cam.getPointPosInFrame(sat.lmkPos(i,:)) + normrnd(0,obj.simVarLmk,[1,2]);
                obj.measLmkPnt(pntLen+i) = pntLen+i;
            end
            obj.measLmkPos = satLandmarkFramePos;
        end
        
        % sets the measurements error, uses the deviation: sqrt(Var)
        function obj = setVariance(obj,VarSat,VarCrn,VarLmk)
            obj.simVarSat = VarSat;
            obj.simVarCrn = VarCrn;
            obj.simVarLmk = VarLmk;
        end
        
        % gets the measurements error, uses the deviation: sqrt(Var)
        function [VarSat,VarCrn,VarLmk] = getVariance(obj)
            VarSat = obj.simVarSat;           
            VarCrn = obj.simVarCrn;
            VarLmk = obj.simVarLmk;
        end
    end
    
end
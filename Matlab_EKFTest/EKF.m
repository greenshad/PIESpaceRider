% EKF class, used to create estimate the position of the landmarks from
% noisy measurements. Combined EKF + SLAM approach.

classdef EKF < handle
    properties
        ekfMapsize          %number of all landmarks
        ekfX                % state vector
        ekfP                % state vector covariance
        ekfQ                %system noise covariance
        ekfS                %measurement noise covariance
        ekfF                %measurement noise covariance
        ekfG                %measurement noise covariance
        ekfLmkPnt           %vector with all landmark pointers
        ekfSatPnt           %all pointers for the satellite

    end
    methods
        
         % constructor
        function obj = EKF(sat)
            obj.ekfMapsize = sat.lmkN + 5;  %lmkN + frame + center         
            obj.ekfX = zeros(obj.ekfMapsize,1);         
            obj.ekfP = zeros(obj.ekfMapsize,obj.ekfMapsize);            
            obj.ekfQ = zeros(2,2);              
            obj.ekfS = zeros(2,2);
            obj.ekfF = 1;              
            obj.ekfG = 1;
            obj.ekfLmkPnt = 0;
            obj.ekfSatPnt = 1:8;
        end
        
        % sets the EKF parameters
        function obj = setEkfParam(obj,InitX,InitP,Q,S)
            obj.ekfX = InitX;         
            obj.ekfP = InitP;              
            obj.ekfQ = Q;              
            obj.ekfS = S; 
        end
        
        % gets the EKF parameters
        function [X,P,Q,S] = getEkfParam(obj)
            X = obj.ekfX;         
            P = obj.ekfP;              
            Q = obj.ekfQ;              
            S = obj.ekfS; 
        end
        
        % main EKF computation
        function obj = compEkf(obj,sat,cam)
            %vector with pointers to all used states
            satLmkPnt = [obj.ekfSatPnt, obj.ekfLmkPnt'];
            X = obj.ekfX;
            Pn = obj.ekfP;
            F = obj.ekfF;
            G = obj.ekfG;
            Q = obj.ekfQ;
            
            %PREDICTION
            estimNextState(obj,X);
            Pn1 = F*Pn*F' + G*Q*G';
            
            %CORRECTION
            
            %%% add correction
        end
        
        function obj = estimNextState(obj,X)
            Xn_1 = X;
            Xn_1(1) = Xn_1(1) + dt * Xn(4);     %Xrel
            Xn_1(2) = Xn_1(2) + dt * Xn(5);     %Yrel
            Xn_1(3) = Xn_1(3) + dt * Xn(6);     %Zrel
            Xn_1(7) = Xn_1(7) + dt * Xn(8);     %theta_sat
            Xn_1(9) = Xn_1(9) + dt * Xn(10);    %theta_cam
            obj.ekfX(obj.ekfS) = Xn_1;
        end
        
        function obj = estimLandmark(obj,sat)
            %%% add estimation
        end

        
    end
    
end
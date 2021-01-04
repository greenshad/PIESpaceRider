% EKF class, used to create estimate the position of the landmarks from
% noisy measurements. Combined EKF + SLAM approach.

classdef EKF < handle
    properties
        ekfMapsize          %number of all landmarks
        ekfInitX            %initial state vector
        ekfInitP            %initial state vector covariance
        ekfQ                %system noise covariance
        ekfS                %measurement noise covariance
        ekfLmkPnt           %vector with all landmark pointers

    end
    methods
        
         % constructor
        function obj = EKF(sat)
            obj.ekfMapsize = sat.lmkN + 5;  %lmkN + frame + center         
            obj.ekfInitX = zeros(obj.ekfMapsize,1);         
            obj.ekfInitP = zeros(obj.ekfMapsize,obj.ekfMapsize);            
            obj.ekfQ = zeros(2,2);              
            obj.ekfS = zeros(2,2);               
            obj.ekfLmkPnt = 0;          
        end
        
        % sets the EKF parameters
        function obj = setEkfParam(obj,InitX,InitP,Q,S)
            obj.ekfInitX = InitX;         
            obj.ekfInitP = InitP;              
            obj.ekfQ = Q;              
            obj.ekfS = S; 
        end
        
        % gets the EKF parameters
        function [InitX,InitP,Q,S] = getEkfParam(obj)
            InitX = obj.ekfInitX;         
            InitP = obj.ekfInitP;              
            Q = obj.ekfQ;              
            S = obj.ekfS; 
        end
        
        % main EKF computation
        function obj = compEkf(obj,sat,cam)
            %%% write EKF code here
        end
        
    end
    
end
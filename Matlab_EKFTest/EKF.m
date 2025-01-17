% EKF class, used to create estimate the position of the landmarks from
% noisy measurements. Combined EKF + SLAM approach.

classdef EKF < handle
    properties
        ekfMapsize          %number of all landmarks
        ekfMap              %map of the landmarks position relative to the 
                            % satellite
        ekfX                %state vector
        ekfP                %state vector covariance
        ekfQ                %system noise covariance
        ekfS                %innovation covariance
        ekfR                %measurement noise covariance
        ekfF                %transition matrix
        ekfH                %observation matrix
    end
    methods
        
         % constructor
        function obj = EKF(sat)
            obj.ekfMapsize = sat.lmkN + 5;  %lmkN + frame + center         
            obj.ekfX = zeros(4,1);  %3 relative position, 1 relative angle       
            obj.ekfP = zeros(4);
            obj.ekfQ = zeros(2,2);
            obj.ekfS = zeros(2,2);
            obj.ekfF = 1;
            obj.ekfH = 1;
        end
        
        % sets the EKF parameters
        function obj = setEkfParam(obj,InitX,InitP,Q,R)
            obj.ekfX = InitX;
            obj.ekfP = InitP;
            obj.ekfQ = Q;
            obj.ekfR = R;
        end
        
        % gets the EKF parameters
        function [X,P,Q,R] = getEkfParam(obj)
            X = obj.ekfX;         
            P = obj.ekfP;              
            Q = obj.ekfQ;              
            R = obj.ekfR; 
        end
        
        % main EKF computation
        function obj = stepEKF(obj,sat,cam,mes,dt)
            %vector with pointers to all used states
            X = obj.ekfX;
            Pn = obj.ekfP;
            Q = obj.ekfQ;
            R = obj.ekfR;
            
            map = [[0,0,0] ; sat.lmkRelPos]';               %add the center of the satellite as a lmk
            u = [sat.satSpeed - cam.camSpeed, sat.satOmega - cam.camOmega];
            z = [mes.measSatPos; mes.measLmkPos]';          % add the measurement of the center to the measurements
            
            %PREDICTION
            X = obj.f(X,u,dt);
            X(4) = mod(X(4)+pi,2*pi)-pi;
            
            F = obj.computeF(X,u,dt);
            Pn1 = F*Pn*F' + Q;
            
            %CORRECTION
            
%           correction using landmarks position
            for i=1:size(z,2)
                % find which landmark we're watching
%                 qsdqRsdqsd
                zi = z(:,i);
                mi = map(:,i);
                H = obj.computeH(X,mi,cam.fov);
                
                y = zi - obj.h(X,mi,cam.fov);
                S = H*Pn1*H' + R;
                K = Pn1*H'/S;
                X = X + K*y;
                X(4) = mod(X(4)+pi,2*pi)-pi;
                Pn1 = (eye(size(Pn1))-K*H)*Pn1;
            end
            
            %UPDATE
            obj.ekfX = X;
            obj.ekfP = Pn1;
            end
        
        function X_est = f(obj,X,u,dt)
            X_est = X;
            X_est(1) = X_est(1) + u(1)*dt*cos(u(4)*dt/2) - u(2)*dt*sin(u(4)*dt/2);
            X_est(2) = X_est(2) + u(2)*dt*cos(u(4)*dt/2) + u(1)*dt*sin(u(4)*dt/2);
            X_est(3) = X_est(3) + u(3)*dt;
            X_est(4) = X_est(4) + u(4)*dt;
        end
        
        function F = computeF(obj,X,u,dt)
           F = zeros(size(X,1));
           F(1,1) = 1;
           F(1,4) = -u(1)*dt*sin(u(4)*dt/2) - u(2)*dt*cos(u(4)*dt/2);
           F(2,2) = 1;
           F(2,4) = -u(2)*dt*sin(u(4)*dt/2) + u(1)*dt*cos(u(4)*dt/2);
           F(3,3) = 1;
           F(4,4) = 1;
        end
        
        function zi_est = h(obj,X,mi,fov)
            x = mi(1);
            y = mi(2);
            z = mi(3);
            u = X(1);
            v = X(2);
            w = X(3);
            t = X(4);
            zi_est = zeros(2,1);
            
            xrel = x*cos(t) - y*sin(t) + u;
            yrel = x*sin(t) + y*cos(t) + v;
            zrel = z+w;
            
            zi_est(1) = 2/fov * atan(xrel/yrel);
            zi_est(2) = 2/fov * atan(zrel/yrel);
        end
        
        function H = computeH(obj,X,mi,fov)
            x = mi(1);
            y = mi(2);
            z = mi(3);
            u = X(1);
            v = X(2);
            w = X(3);
            t = X(4);
            H = zeros(2,size(X,1));
            
            H(1,1) = 2/fov * (cos(t)*y+sin(t)*x+v) / (u*u + 2*u*(cos(t)*x-sin(t)*y) + 2*cos(t)*v*y + 2*sin(t)*v*x + v*v + x*x + y*y);
            H(1,2) = -2/fov * (cos(t)*x-sin(t)*y+u) / (v*v + 2*v*(cos(t)*y+sin(t)*x) + 2*cos(t)*u*x - 2*sin(t)*u*y + u*u + x*x + y*y);
            H(1,4) = -2/fov * (cos(t)*cos(t)*(x*x+y*y) + cos(t)*(u*x+v*y) + sin(t)*(sin(t)*(x*x+y*y)-u*y+v*x)) / (2*cos(t)*(u*x+v*y) - 2*sin(t)*(u*y-v*x) + u*u + v*v + x*x + y*y);
            
            
            H(2,2) = -2/fov * (w+z) / (v*v + 2*v*(cos(t)*y+sin(t)*x) - cos(t)*cos(t)*(x*x-y*y) + 2*sin(t)*cos(t)*x*y + w*w + 2*w*z + x*x + z*z);
            H(2,3) = 2/fov * (cos(t)*y+sin(t)*x+v) / (w*w + 2*w*z - cos(t)*cos(t)*(x*x-y*y) + 2*(sin(t)*x+v)*cos(t)*y + 2*sin(t)*v*x + v*v + x*x + z*z);
            H(2,4) = 2/fov * (cos(t)*x-sin(t)*y)*(w+z) / (cos(t)*cos(t)*(x*x-y*y) - 2*(sin(t)*x+v)*cos(t)*y - 2*sin(t)*v*x - v*v - w*w - 2*w*z - x*x - z*z);
        end
        
    end
    
end
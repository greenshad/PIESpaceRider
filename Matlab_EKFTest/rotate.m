function s1 = rotate(s, rAxis,  theta, origin)
R = makehgtform(rAxis, theta);
R = R(1:3,1:3);
center = repmat(origin', 1, size(s,1));
s0 = R*(s'-center) + center;
s1 =s0'; 
end
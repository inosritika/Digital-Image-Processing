% Load the image file and store it as the variable SigImage
SigImage = imread('sig.jpg'); 

% Display the original image
figure, imshow(SigImage);

% Resize the image to 128x128 pixels
I2 = imresize(SigImage, [128, 128]);
figure, imshow(I2);

% Convert the image to grayscale
I3 = rgb2gray(I2);

% Convert the image to double precision
I3 = im2double(I3);

% Binarize the image
I3 = imbinarize(I3);

% Perform morphological thinning
I3 = bwmorph(~I3, 'thin', inf);
I3 = ~I3;
figure, imshow(I3);

% Initialize variables
i = 1;
k = 1;

% Convert image to black and white and thin the image
while i <= 128
    j = 1;
    while j <= 128
        if I3(i, j) == 0
            u(k) = i;
            v(k) = j;
            k = k + 1;
            I3(i, j) = 1;
        end
        j = j + 1;
    end
    i = i + 1;
end

% The curve of the signature
C = [u; v];

% The number of pixels in the signature
N = k - 1;

% Calculate the original x-coordinate center of mass of the image
oub = 0;
for i = 1:N
    oub = oub + C(1, i);
end
oub = oub / N;

% Calculate the original y-coordinate center of mass of the image
ovb = 0;
for i = 1:N
    ovb = ovb + C(2, i);
end
ovb = ovb / N;

% Move the signature to the origin
for i = 1:N
    u(i) = u(i) - oub + 1;
    v(i) = v(i) - ovb + 1;
end

% The new curve of the signature
C = [u; v];

% Calculate the new center of mass
ub = sum(C(1, :)) / N;
vb = sum(C(2, :)) / N;

% Calculate the variances
ubSq = sum((C(1, :) - ub).^2) / N;
vbSq = sum((C(2, :) - vb).^2) / N;

% Calculate the covariance
uvb = 0;
for i = 1:N
    uvb = uvb + (u(i) * v(i));
end
uvb = uvb / N;

% Construct the covariance matrix
M = [ubSq uvb; uvb vbSq];

% Calculate the minimum eigenvalue of the matrix
minIgen = min(abs(eig(M)));

% Construct the matrix for rotation
MI = [ubSq - minIgen uvb; uvb vbSq - minIgen];

% Calculate the rotation angle in degrees
theta = (atan(-MI(1) / MI(2)) * 180) / pi;

% Convert the rotation angle to radians
thetaRad = (theta * pi) / 180;

% Rotate the signature and pass the new coordinates
for i = 1:N
    v(i) = (C(2, i) * cos(thetaRad)) - (C(1, i) * sin(thetaRad));
    u(i) = (C(2, i) * sin(thetaRad)) + (C(1, i) * cos(thetaRad));
end

% The new curve of the signature
C = [u; v];

% Move the signature to its original position
for i = 1:N
    u(i) = round(u(i) + oub - 1);
    v(i) = round(v(i) + ovb - 1);
end
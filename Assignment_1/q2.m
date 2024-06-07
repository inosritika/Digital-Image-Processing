% 1. Clear all variables, close all figures, and clear the command window
clear all;
close all;
clc;

% 2. Read the input grayscale image
RawImage = imread('cameraman.tif');  % Reading Input Raw Image
[row, col] = size(RawImage);
L = 256;  % Upper Limit for the pixel value of the 8-bit Gray Scale Image

% 3. Display the original image
figure();
subplot(2, 2, 1); imshow(RawImage); title('\itRaw Image');

% 4. Negative Transform of the RawImage
NegImage = uint8(zeros(row, col));  % Matrix containing the Negative Transform of the Image
for i = 1:row
    for j = 1:col
        NegImage(i, j) = L - RawImage(i, j) - 1;  % Subtracting the Pixel value from the Maximum Value to get the Negative Transform
    end
end
subplot(2, 2, 2); imshow(NegImage); title('\itNegative Transform');

% 5. Log Transform of the RawImage
LogImage = uint8(zeros(row, col));  % Matrix containing the Log Transform of the Image
for i = 1:row
    for j = 1:col
        LogImage(i, j) = log(double(RawImage(i, j)) + 1) * ((L - 1) / log(L));  % Taking the log transform and multiplying it with the constant
    end
end
subplot(2, 2, 3); imshow(LogImage); title('\itLog Transform');

% 6. AntiLog Transform of the RawImage
AntiLogImage = uint8(zeros(row, col));  % Matrix containing the AntiLog Transform of the Image
for i = 1:row
    for j = 1:col
        AntiLogImage(i, j) = (exp(double(RawImage(i, j))) ^ (log(L) / (L - 1))) - 1;  % Taking the Antilog transform and multiplying it with the constant
    end
end
subplot(2, 2, 4); imshow(AntiLogImage); title('\itAntiLog Transform');

% 7. Gamma Correction using Power Law transform
figure();
Gamma = [0.4, 2.5, 10, 25, 100];  % Array with all Gamma Values
numImages = length(Gamma);
for i = 1:numImages
    GammaImage = uint8(zeros(row, col));
    C = (L - 1) / ((L - 1) ^ Gamma(i));  % Calculating the constant that needs to be multiplied for the Power Law Transform
    for j = 1:row
        for k = 1:col
            GammaImage(j, k) = uint8(C * (double(RawImage(j, k)) ^ Gamma(i)));  % Getting the pixel value after the Gamma Correction
        end
    end
    subplot(2, 3, i); imshow(GammaImage); title(['\itGamma=', num2str(Gamma(i))]);  % Displaying the image
end

% 8. Power of an Image
figure();
Pow = [2, 3, 4];  % Array with all Power Values
numImages = length(Pow);
for i = 1:numImages
    PowImage = uint8(zeros(row, col));
    C = (L - 1) / ((L - 1) ^ Pow(i));
    for j = 1:row
        for k = 1:col
            PowImage(j, k) = uint8(C * (double(RawImage(j, k)) ^ Pow(i)));  % Calculating the Power of each pixel in the image
        end
    end
    subplot(1, 3, i); imshow(PowImage); title(['\itPower=', num2str(Pow(i))]);
end

% 9. Plot Bit-planes of the image
figure();
for i = 1:8
    BitPlane = bitget(RawImage, i);  % Bitget function is used to get the ith bit of a number
    subplot(3, 3, i); imshow(logical(BitPlane)); title(['Bit plane ', num2str(i)]);
end

% 10. Plot the histogram of the original image and apply Histogram equalization
figure();
subplot(2, 2, 1); imshow(RawImage); title('Raw Image');
subplot(2, 2, 2); imhist(RawImage); title('Histogram of the Raw Image');  % Displaying the Histogram of the Raw Image
EqualizedImage = histeq(RawImage);  % Applying Histogram Equalization
subplot(2, 2, 3); imshow(EqualizedImage); title('Equalized Image');
subplot(2, 2, 4); imhist(EqualizedImage); title('Histogram of the Equalized Image');  % Displaying the Histogram of the Equalized Image

% 11. Selective Highlighting of the RawImage
figure();
HighLightedImage = uint8(zeros(row, col));
% Initializing the range that needs to be highlighted
minVal = 120;
maxVal = 200;
for i = 1:row
    for j = 1:col
        x = RawImage(i, j);
        if (x >= minVal) && (x <= maxVal)  % Highlighting only those pixel values whose values lie in the range [120, 200]
            HighLightedImage(i, j) = 255;
        else
            HighLightedImage(i, j) = x;
        end
    end
end
subplot(1, 2, 1); imshow(RawImage); title('\itRaw Image');
subplot(1, 2, 2); imshow(HighLightedImage); title('\itHighlighted Image');
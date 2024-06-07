% Load a test image
image_path = 'C:\Program Files\MATLAB\R2023a\toolbox\images\imdata\llama.jpg';
original_image = imread(image_path);
imshow(original_image)

% Convert to grayscale if necessary
original_image = rgb2gray(original_image);
imshow(original_image)

% a. Calculate Histogram and Implement Histogram Equalization
% Function implementing histogram is written at the end of the file
equalized_image_custom = customHistogramEqualization(original_image);

% Calculate histogram of the original image
histogram_original = imhist(original_image);

% b. Use Built-in Function and Compare Histograms
equalized_image_builtin = histeq(original_image, 256);

% Calculate Mean Squared Error (MSE)
mse_custom_vs_builtin = immse(equalized_image_custom, equalized_image_builtin);

% c. Apply Adaptive Histogram Equalization (CLAHE)
clahe_image = adapthisteq(original_image, 'ClipLimit', 0.02);

% Display original and equalized images side by side
subplot(2, 2, 1); imshow(original_image); title('Original Image');
subplot(2, 2, 2); imshow(equalized_image_custom); title('Custom Histogram Equalization');
subplot(2, 2, 3); imshow(equalized_image_builtin); title('Built-in Histogram Equalization');
subplot(2, 2, 4); imshow(clahe_image); title('CLAHE');

% Calculate Mean Squared Error (MSE) for CLAHE
mse_clahe_vs_builtin = immse(clahe_image, equalized_image_builtin);

% Set the width of the entire figure
figure_width = 1200; % Adjust this value as needed
figure_height = 400; % Adjust this value as needed
figure('Position', [100, 100, figure_width, figure_height]);

% Display histograms
subplot(1, 4, 1); bar(0:255, histogram_original); title('Original Histogram');
subplot(1, 4, 2); bar(0:255, imhist(equalized_image_custom)); title('Custom Histogram');
subplot(1, 4, 3); bar(0:255, imhist(equalized_image_builtin)); title('Built-in Histogram');
subplot(1, 4, 4); bar(0:255, imhist(clahe_image)); title('CLAHE Histogram');

disp(['MSE between Custom and Built-in Histogram Equalization: ', num2str(mse_custom_vs_builtin)]);
disp(['MSE between CLAHE and Built-in Histogram Equalization: ', num2str(mse_clahe_vs_builtin)]);

function equalized_image = customHistogramEqualization(image)
    [h, w] = size(image);
    num_pixels = h * w;
    histogram = zeros(256, 1);
    for i = 1:h
        for j = 1:w
            pixel_value = image(i, j);
            histogram(pixel_value + 1) = histogram(pixel_value + 1) + 1;
        end
    end
    cumulative_histogram = cumsum(histogram) / num_pixels;
    equalized_image = uint8(255 * cumulative_histogram(double(image) + 1));
end
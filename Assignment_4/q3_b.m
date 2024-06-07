clc;
close all;
clear all;

% Load the image
I = imread('cameraman.tif');
I = im2double(I);

m = 1;
for i = 1:8:256
    for j = 1:8:256
        k = 0;
        img = zeros(8, 8);
        
        % Extract 8x8 block
        for x = 0:7
            for y = 0:7
                img(x+1, y+1) = I(i+x, j+y);
            end
        end
        
        % Calculate the expectation of E[xx']
        img_expect = cell(1, 8);
        for l = 1:8
            img_expect{k+1} = img(:, l) * img(:, l)';
            k = k + 1;
        end
        
        imgexp = zeros(8, 8);
        for l = 1:8
            imgexp = imgexp + (1/8) * img_expect{l};
        end
        
        % Calculate the mean
        img_mean = zeros(8, 1);
        for l = 1:8
            img_mean = img_mean + (1/8) * img(:, l);
        end
        
        img_mean_trans = img_mean * img_mean';
        img_covariance = imgexp - img_mean_trans;
        
        % Eigen decomposition
        [v{m}, d{m}] = eig(img_covariance);
        temp = v{m};
        m = m + 1;
        
        for l = 1:8
            v{m-1}(:, l) = temp(:, 8-(l-1));
        end
        
        % Transform the image block
        trans_img1 = zeros(8, 8);
        for l = 1:8
            trans_img1(:, l) = v{m-1} * img(:, l);
        end
        
        % Store the transformed block
        for x = 0:7
            for y = 0:7
                transformed_img(i+x, j+y) = trans_img1(x+1, y+1);
            end
        end
        
        % Apply mask
        mask = ones(8, 8);
        trans_img = trans_img1 .* mask;
        
        % Inverse transform
        inv_trans_img = zeros(8, 8);
        for l = 1:8
            inv_trans_img(:, l) = v{m-1}' * trans_img(:, l);
        end
        
        % Store the inverse transformed block
        for x = 0:7
            for y = 0:7
                inv_transformed_img(i+x, j+y) = inv_trans_img(x+1, y+1);
            end
        end
    end
end

% Display the transformed image
imshow(transformed_img);

figure;
% Display the inverse transformed image
imshow(inv_transformed_img);
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

# Path to Image
path = r'./cat_image.jpg'

# Reading the image
image = cv2.imread(path)
# Displaying the Image
plt.imshow(image)
print("Resolution of image is", image.shape)

# cv2.imshow(window_name, image)

# Creating Identity Matrix
identity_kernel = np.array([[0, 0, 0],
                            [0, 1, 0],
                            [0, 0, 0]])
# Passing image through identity filter
identity_filtered_image = cv2.filter2D(image, ddepth=-1, kernel=identity_kernel)
# Displaying the Image
plt.imshow(identity_filtered_image)

# Defining Kernel size for blurring
ksize = (21, 21)
# Using cv2.blur() method
blur_image = cv2.GaussianBlur(image, ksize, 0)
print(blur_image.shape)
# Displaying the image
plt.imshow(blur_image)

# Kernel size for large_blur would be higher so that image would be more smooth
ksize1 = (101, 101)
# Using cv2.blur() method
blur_image1 = cv2.GaussianBlur(image, ksize1, 0)
print(blur_image1.shape)
# Displaying the image
plt.imshow(blur_image1)

# Sobel filter for edge detection
sobel_image = cv2.Sobel(image, cv2.CV_64F, 1, 1, ksize=21)
# Calculated gradient direction at 45* angle as it gave the most accurate results as
# compared to gradient purely in x and y direction
plt.imshow(sobel_image)

# Applying Laplacian filter with kernel size = 5
laplacian_image = cv2.Laplacian(image, cv2.CV_64F, 5)
print(laplacian_image.shape)
# Displaying the image
plt.imshow(laplacian_image)

# The high pass filter is created by subtracting the Gaussian Blurred image from original image
hpf = cv2.subtract(image, cv2.GaussianBlur(image, (21, 21), 7))
# Displaying the image
plt.imshow(hpf)

# Low frequency image can be obtained by applying the Gaussian Blur on the original filter
# Using cv2.blur() method
low_frequency_image = cv2.GaussianBlur(image, ksize1, 0)
# Displaying the image
plt.imshow(low_frequency_image)

# High frequency image can be created in many ways, here I am subtracting the large_blur image from original image
high_frequency_image = cv2.subtract(image, cv2.GaussianBlur(image, ksize1, 0))
# Displaying the image
plt.imshow(high_frequency_image)

# Creating a hybrid image by adding the low frequency and high frequency images
plt.imshow(cv2.add(low_frequency_image, high_frequency_image))

# Path to Image
path = r'./Human_image.enc'

# Reading the image
image = cv2.imread(path)
# Displaying the Image
plt.imshow(image)
print("Resolution of image is", image.shape)

# Creating Identity Matrix
identity_kernel = np.array([[0, 0, 0],
                            [0, 1, 0],
                            [0, 0, 0]])
# Passing image through identity filter
identity_filtered_image = cv2.filter2D(image, ddepth=-1, kernel=identity_kernel)
# Displaying the Image
plt.imshow(identity_filtered_image)

# Defining Kernel size for blurring
ksize = (21, 21)
# Using cv2.blur() method
blur_image = cv2.GaussianBlur(image, ksize, 0)
print(blur_image.shape)
# Displaying the image
plt.imshow(blur_image)

# Kernel size for large_blur would be higher so that image would be more smooth
ksize1 = (101, 101)
# Using cv2.blur() method
blur_image1 = cv2.GaussianBlur(image, ksize1, 0)
print(blur_image1.shape)
# Displaying the image
plt.imshow(blur_image1)

# Sobel filter for edge detection
sobel_image = cv2.Sobel(image, cv2.CV_64F, 1, 1, ksize=21)
# Calculated gradient direction at 45* angle as it gave the most accurate results as
# compared to gradient purely in x and y direction
plt.imshow(sobel_image)

# Applying Laplacian filter with kernel size = 5
laplacian_image = cv2.Laplacian(image, cv2.CV_64F, 5)
print(laplacian_image.shape)
# Displaying the image
plt.imshow(laplacian_image)

# The high pass filter is created by subtracting the Gaussian Blurred image from original image
hpf = cv2.subtract(image, cv2.GaussianBlur(image, (21, 21), 7))
# Displaying the image
plt.imshow(hpf)

# Low frequency image can be obtained by applying the Gaussian Blur on the original filter
# Using cv2.blur() method
low_frequency_image = cv2.GaussianBlur(image, ksize1, 0)
# Displaying the image
plt.imshow(low_frequency_image)

# High frequency image can be created in many ways, here I am subtracting the large_blur image from original image
high_frequency_image = cv2.subtract(image, cv2.GaussianBlur(image, ksize1, 0))
# Displaying the image
plt.imshow(high_frequency_image)

# Creating a hybrid image by adding the low frequency and high frequency images
plt.imshow(cv2.add(low_frequency_image, high_frequency_image))
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

# Loading the image
image = cv2.imread('coins.jpg', 1)
plt.imshow(image)
plt.show()

# Loading the same image as a grayscale image
gray_image = cv2.imread('coins.jpg', 0)
plt.imshow(gray_image, cmap='gray')
plt.show()

# Blurring the image to identify circles to remove noise using Gaussian filter
blurred_image = cv2.GaussianBlur(gray_image, (7, 7), 13.5)
plt.imshow(blurred_image, cmap='gray')
plt.show()

# Apply Canny edge detection to the image to detect the edges
edges = cv2.Canny(blurred_image, 50, 150)
plt.imshow(edges, cmap='gray')
plt.show()

# As we were to extend our search to 3D parameter space our group has chosen circle
# where the 3 parameters are x, y, r - (x, y) - coordinates of centre and r being the radius of circle
circles = cv2.HoughCircles(image=blurred_image, method=cv2.HOUGH_GRADIENT, dp=1, minDist=80, minRadius=80, maxRadius=300)
circles = np.uint16(np.around(circles))

# Drawing the circles found on the original image
for i in circles[0, :]:
    # Draw the outline of circle
    cv2.circle(image, (i[0], i[1]), i[2], (255, 0, 0), 5)
    # Draw the center of the circle
    cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 5)
plt.imshow(image)
plt.show()

# *******TRYING THIS FOR ANOTHER IMAGE***********

# Loading the image
image2 = cv2.imread('sp.jpg', 1)
plt.imshow(image2)
plt.show()

# Loading the same image as a grayscale image
gray_image2 = cv2.imread('sp.jpg', 0)
plt.imshow(gray_image2, cmap='gray')
plt.show()

# Blurring the image to identify circles to remove noise using Gaussian filter
blurred_image2 = cv2.GaussianBlur(gray_image2, (7, 7), 13.5)
plt.imshow(blurred_image2, cmap='gray')
plt.show()

# Apply Canny edge detection to the image to detect the edges
edges = cv2.Canny(blurred_image2, 50, 150)
plt.imshow(edges, cmap='gray')
plt.show()

# As we were to extend our search to 3D parameter space our group has chosen circle
# where the 3 parameters are x, y, r - (x, y) - coordinates of centre and r being the radius of circle
circles = cv2.HoughCircles(image=blurred_image2, method=cv2.HOUGH_GRADIENT, dp=2, minDist=80, minRadius=10, maxRadius=100)
circles = np.uint16(np.around(circles))

# Drawing the circles found on the original image
for i in circles[0, :]:
    # Draw the outline of circle
    cv2.circle(image2, (i[0], i[1]), i[2], (255, 0, 0), 5)
    # Draw the center of the circle
    cv2.circle(image2, (i[0], i[1]), 2, (0, 0, 255), 5)
plt.imshow(image2)
plt.show()
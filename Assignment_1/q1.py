import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

# Load the image
img = cv2.imread('baby.jpeg', 1)
rows, cols, k = img.shape
img.shape

# Scaling of image
# Taking input of scaling factors along x-axis and y-axis
a = int(input("Scaling along x-axis: "))
b = int(input("Scaling along y-axis: "))

scaled_img = cv2.resize(img, (0, 0), fx=a, fy=b, interpolation=cv2.INTER_LINEAR)

# Used matplotlib to show results in the pdf itself
# cv.imshow() opens a window and shows the image
plt.imshow(cv2.cvtColor(scaled_img, cv2.COLOR_BGR2RGB))
# As opencv loads in BGR format by default, we want to show it in RGB.
plt.show()
scaled_img.shape

# Translation of image
# Taking input for translation along x-axis and y-axis
c = input("Enter shift along x-axis: ")
d = input("Enter shift along y-axis: ")

M = np.float32([[1, 0, c], [0, 1, d]])
# Created a 2x3 matrix to carry out translation of image using matrix multiplication
translated_img = cv2.warpAffine(scaled_img, M, (cols, rows))

# As opencv loads in BGR format by default, we want to show it in RGB.
plt.imshow(cv2.cvtColor(translated_img, cv2.COLOR_BGR2RGB))
plt.show()

# Rotation of image
# Taking inputs of angle of rotation and reference coordinates for rotation
e = int(input("Enter angle of rotation: "))
f = int(input("Enter reference of rotation x-coordinate: "))
g = int(input("Enter reference of rotation y-coordinate: "))

M = cv2.getRotationMatrix2D((f, g), e, 1)
# This function creates the rotation matrix [[cos(e), -sin(e)][cos(e), sin(e)]]
rotated_img = cv2.warpAffine(translated_img, M, (cols, rows))

plt.imshow(cv2.cvtColor(rotated_img, cv2.COLOR_BGR2RGB))
# As opencv loads in BGR format by default, we want to show it in RGB.
plt.show()
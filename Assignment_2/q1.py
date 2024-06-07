import numpy as np
import matplotlib.pyplot as plt
import cv2
from google.colab.patches import cv2_imshow

%matplotlib inline

# Read in the image
image = cv2.imread('/content/combo.jpg')
cv2_imshow(image)

# Use the cvtColor() function to grayscale the resized image
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2_imshow(gray_image)
cv2.waitKey(0)
# Window shown waits for any key pressing event
cv2.destroyAllWindows()

# Define our parameters for Canny
low_threshold = 50
high_threshold = 100
edges = cv2.Canny(gray_image, low_threshold, high_threshold)
cv2_imshow(edges)

# Apply Gaussian blur to reduce noise and improve circle detection
blurred_image = cv2.GaussianBlur(gray_image, (9, 9), 2)

# Define the Hough transform parameters
# Make a blank the same size as our image to draw on
rho = 1
theta = np.pi / 180
threshold = 20
min_line_length = 11
max_line_gap = 11
line_image = np.copy(image)  # creating an image copy to draw lines on

# Run Hough on the edge-detected image
lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

# Iterate over the output "lines" and draw lines on the image copy
for line in lines:
    for x1, y1, x2, y2 in line:
        cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
cv2_imshow(line_image)

# Apply Hough transform to greyscale image
circles = cv2.HoughCircles(blurred_image, cv2.HOUGH_GRADIENT, 1, 20, param1=60, param2=40, minRadius=0, maxRadius=0)
circles = np.uint16(np.around(circles))

# Draw the circles
for i in circles[0, :]:
    # draw the outer circle
    cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)
cv2_imshow(image)
cv2.waitKey(0)
cv2.destroyAllWindows()
import numpy as np
from skimage import io
from skimage.io import imread, imshow
import matplotlib.pyplot as plt

def findRTheta(x1, y1, imgCenter):
    x2, y2 = imgCenter[0], imgCenter[1]
    r = [(x2 - x1), (y2 - y1)]
    if (x2 - x1 != 0):
        return [int(np.rad2deg(np.arctan(int((y2 - y1) / (x2 - x1))))), r]
    else:
        return [0, 0]

def findGradient(x, y):
    if (x != 0):
        return int(np.rad2deg(np.arctan(int(y / x))))
    else:
        return 0

def buildRTable(img):
    rtable = [[0 for x in range(1)] for y in range(90)]  # Creating an empty list
    # r will be calculated corresponding to this point as reference point
    xCenter = int(img.shape[0] / 2)
    yCenter = int(img.shape[1] / 2)
    imgCenter = [xCenter, yCenter]
    filter = 3
    for x in range(img.shape[0] - (filter - 1)):
        for y in range(img.shape[1] - (filter - 1)):
            if (img[x, y] != 0):
                theta, r = findRTheta(x, y, imgCenter)
                if (r != 0):
                    rtable[np.absolute(theta)].append(r)
    for i in range(len(rtable)):
        rtable[i].pop(0)
    return rtable

def findMaxima(accumulator):
    ridx, cidx = np.unravel_index(accumulator.argmax(), accumulator.shape)
    return [accumulator[ridx, cidx], ridx, cidx]

def matchTable(testImage, table):
    # Matching the reference table with the given input Image for testing generalized Hough Transform
    n, m = testImage.shape
    acc = np.zeros((n + 50, m + 50))  # Accumulator array requires some extra space
    for x in range(1, n):
        for y in range(1, m):
            if testImage[x, y] != 0:
                theta = findGradient(x, y)
                vectors = table[theta]
                for vector in vectors:
                    acc[vector[0] + x, vector[1] + y] += 1
    return acc

img = 'kettle.png'
template = imread(img)
testImage = imread('shapes.png')

print("The Shape I am finding using General Hough Transform >>")
plt.figure(figsize=(4, 4))
imshow(template)
plt.title("Kettle")
plt.show()

print("The Image where I am finding the custom shape >>")
plt.figure(figsize=(4, 4))
imshow(testImage)
plt.title("Image with a lot of shapes")
plt.show()

table = buildRTable(template)
acc = matchTable(testImage, table)
val, ridx, cidx = findMaxima(acc)

# Drawing bounding-box in accumulator matrix
for i in range(ridx - 5, ridx + 6):
    acc[i, cidx - 5] = val
    acc[i, cidx + 5] = val
for i in range(cidx - 5, cidx + 6):
    acc[ridx + 5, i] = val
    acc[ridx - 5, i] = val

plt.figure(1)
plt.title("Accumulator")
imshow(acc)
plt.show()

# Drawing bounding-box in original image at the found location
# Calculating the half-width and height of custom shape
boxHeight = np.floor(template.shape[0] / 2) + 1
boxWidth = np.floor(template.shape[1] / 2) + 1

# Calculating coordinates of the box
top = int(max(ridx - boxHeight, 1))
bottom = int(min(ridx + boxHeight, testImage.shape[0] - 1))
left = int(max(cidx - boxWidth, 1))
right = int(min(cidx + boxWidth, testImage.shape[1] - 1))

# Drawing the box
for i in range(top, bottom + 1):
    testImage[i, left] = 255
    testImage[i, right] = 255
for i in range(left, right + 1):
    testImage[top, i] = 255
    testImage[bottom, i] = 255

# Result Image
print("Shape Found >>")
plt.figure(figsize=(5, 5))
imshow(testImage)
plt.title("Shape Found")
plt.show()
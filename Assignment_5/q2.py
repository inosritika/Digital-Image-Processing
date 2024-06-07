# Import necessary libraries
import cv2
import numpy as np
from skimage import io
from skimage.morphology import binary_dilation, binary_erosion, square, rectangle, disk, diamond
from google.colab.patches import cv2_imshow
from PIL import Image
import matplotlib.pyplot as plt

# Reading the image
image = cv2.imread('book1.png')

# Open an image file
input_image_path = '/content/book1.png'
output_image_path = '/content/output_image.png'
image = Image.open(input_image_path)

new_size = (114 * 3, 89 * 3)

# Resize the image
resized_image = image.resize(new_size)
resized_array = np.array(resized_image)

cv2_imshow(resized_array)
cv2.waitKey(0)
cv2.destroyAllWindows()

gray_image = cv2.cvtColor(resized_array, cv2.COLOR_BGR2GRAY)
_, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)

# Iterate through each element in the array
for i in range(binary_image.shape[0]):
    for j in range(binary_image.shape[1]):
        # Check if the pixel value is 255
        if binary_image[i, j] == 255:
            # Change it to 1
            binary_image[i, j] = 1

def pad_binary_image(image, top_padding, bottom_padding, left_padding, right_padding):
    original_height, original_width = image.shape
    # Calculating the new dimensions with padding
    padded_height = original_height + top_padding + bottom_padding
    padded_width = original_width + left_padding + right_padding
    # Creating a new blank image filled with zeros
    padded_image = np.zeros((padded_height, padded_width), dtype=np.uint8)
    # Copying the original binary image to the center of the padded image
    padded_image[top_padding:top_padding + original_height, left_padding:left_padding + original_width] = image
    return padded_image

def count_intersection_pixels(image, struc_ele, x_offset, y_offset):
    # Ensuring that the structuring element fits within the image
    if y_offset + struc_ele.shape[1] - 1 > image.shape[1] or x_offset + struc_ele.shape[0] - 1 > image.shape[0]:
        raise ValueError("Structuring element does not fit within the image at the specified coordinates.")
    # Creating a region of interest (ROI) in the image
    roi = image[x_offset: x_offset + struc_ele.shape[0], y_offset: y_offset + struc_ele.shape[1]]
    # Counting the number of intersection pixels (pixels with a value of 1 in both image and the structuring element)
    intersection_count = np.sum(roi & struc_ele)
    return intersection_count

# Updated dilation function
def updated_dilation(image, s, struc_ele):
    struc_height, struc_width = struc_ele.shape
    struc_x = struc_width // 2
    struc_y = struc_height // 2
    original_height, original_width = image.shape
    resulting_image = np.zeros((original_height, original_width), dtype=np.uint8)
    padded_image = pad_binary_image(image, struc_y, struc_y, struc_x, struc_x)
    # We run on the image and check the cardinality of the 1 pixels when structuring element is placed at each pixel in the image
    # If this cardinality is greater than or equal to s then we keep it 1 else 0
    for x in range(image.shape[0]):  # height
        for y in range(image.shape[1]):  # width
            intersection_count = count_intersection_pixels(padded_image, struc_ele, x, y)
            if intersection_count >= s:
                resulting_image[x, y] = 255
    return resulting_image

# Updated erosion function
def updated_erosion(image, s, struc_ele):
    struc_height, struc_width = struc_ele.shape
    struc_x = struc_width // 2
    struc_y = struc_height // 2
    original_height, original_width = image.shape
    resulting_image = np.zeros((original_height, original_width), dtype=np.uint8)
    padded_image = pad_binary_image(image, struc_y, struc_y, struc_x, struc_x)
    compliment_image = np.logical_not(padded_image).astype(int)
    # We run on the image and check the cardinality of the 1 pixels when structuring element is placed at each pixel in the image
    # If this cardinality is greater than or equal to s then we keep it 1 else 0
    for x in range(image.shape[0]):  # height
        for y in range(image.shape[1]):  # width
            intersection_count = count_intersection_pixels(compliment_image, struc_ele, x, y)
            if intersection_count <= s:
                resulting_image[x, y] = 255
    return resulting_image

# Normal dilation function
def normal_dilation(image, s, struc_ele):
    struc_height, struc_width = struc_ele.shape
    struc_x = struc_width // 2
    struc_y = struc_height // 2
    original_height, original_width = image.shape
    resulting_image = np.zeros((original_height, original_width), dtype=np.uint8)
    padded_image = pad_binary_image(image, struc_y, struc_y, struc_x, struc_x)
    # We run on the image and check the cardinality of the 1 pixels when structuring element is placed at each pixel in the image
    # If this cardinality is greater than or equal to s then we keep it 1 else 0
    for x in range(image.shape[0]):  # height
        for y in range(image.shape[1]):  # width
            intersection_count = count_intersection_pixels(padded_image, struc_ele, x, y)
            if intersection_count >= 1:  # taking intersection greater than or equal to 1
                resulting_image[x, y] = 255
    return resulting_image

# Normal erosion function
def normal_erosion(image, s, struc_ele):
    struc_height, struc_width = struc_ele.shape
    struc_x = struc_width // 2
    struc_y = struc_height // 2
    original_height, original_width = image.shape
    resulting_image = np.zeros((original_height, original_width), dtype=np.uint8)
    padded_image = pad_binary_image(image, struc_y, struc_y, struc_x, struc_x)
    compliment_image = np.logical_not(padded_image).astype(int)
    # We run on the image and check the cardinality of the 1 pixels when structuring element is placed at each pixel in the image
    # If this cardinality is greater than or equal to s then we keep it 1 else 0
    for x in range(image.shape[0]):  # height
        for y in range(image.shape[1]):  # width
            intersection_count = count_intersection_pixels(compliment_image, struc_ele, x, y)
            if intersection_count == 0:
                resulting_image[x, y] = 255
    return resulting_image

def display_images(result1, result2, result3, result4, custom_title):
    # Create a figure with 2 rows and 2 columns
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    # Display images in each subplot with custom titles
    axs[0, 0].imshow(result1, cmap='gray')
    axs[0, 0].set_title(f'Updated Dilation-{custom_title}')

    axs[0, 1].imshow(result3, cmap='gray')
    axs[0, 1].set_title(f'Normal Dilation-{custom_title}')

    axs[1, 0].imshow(result2, cmap='gray')
    axs[1, 0].set_title(f'Updated Erosion-{custom_title}')

    axs[1, 1].imshow(result4, cmap='gray')
    axs[1, 1].set_title(f'Normal Erosion-{custom_title}')

    # Hide the axes labels
    for ax in axs.flat:
        ax.label_outer()

    # Show the plot
    plt.show()

# Structuring elements
square_struc_ele = square(5)
rectangle_struc_ele = rectangle(5, 3)
circle_struc_ele = disk(3)
diamond_struc_ele = diamond(3)
plus_struc_ele = np.array([[0, 0, 1, 0, 0],
                           [0, 0, 1, 0, 0],
                           [1, 1, 1, 1, 1],
                           [0, 0, 1, 0, 0],
                           [0, 0, 1, 0, 0]], dtype=bool)

# Apply updated and normal dilation and erosion with different structuring elements
result1 = updated_dilation(binary_image, 20, square_struc_ele)
result2 = updated_erosion(binary_image, 20, square_struc_ele)
result3 = normal_dilation(binary_image, 1, square_struc_ele)
result4 = normal_erosion(binary_image, 20, square_struc_ele)
display_images(result1, result2, result3, result4, "Square Structuring Element")

result1 = updated_dilation(binary_image, 15, rectangle_struc_ele)
result2 = updated_erosion(binary_image, 10, rectangle_struc_ele)
result3 = normal_dilation(binary_image, 1, rectangle_struc_ele)
result4 = normal_erosion(binary_image, 15, rectangle_struc_ele)
display_images(result1, result2, result3, result4, "Rectangle Structuring Element")

result1 = updated_dilation(binary_image, 20, circle_struc_ele)
result2 = updated_erosion(binary_image, 20, circle_struc_ele)
result3 = normal_dilation(binary_image, 1, circle_struc_ele)
result4 = normal_erosion(binary_image, 40, circle_struc_ele)
display_images(result1, result2, result3, result4, "Circular Structuring Element")

result1 = updated_dilation(binary_image, 20, diamond_struc_ele)
result2 = updated_erosion(binary_image, 20, diamond_struc_ele)
result3 = normal_dilation(binary_image, 1, diamond_struc_ele)
result4 = normal_erosion(binary_image, 40, diamond_struc_ele)
display_images(result1, result2, result3, result4, "Diamond Structuring Element")

result1 = updated_dilation(binary_image, 7, plus_struc_ele)
result2 = updated_erosion(binary_image, 7, plus_struc_ele)
result3 = normal_dilation(binary_image, 1, plus_struc_ele)
result4 = normal_erosion(binary_image, 25, plus_struc_ele)
display_images(result1, result2, result3, result4, "Plus Structuring Element")

def dilate_then_erode(input_image, s1, s2, structuring_element):
    # Perform dilation
    dilated_image = updated_dilation(input_image, s1, structuring_element)
    # Perform erosion on the dilated image
    final_image = updated_erosion(dilated_image, s2, structuring_element)
    return final_image

result1 = dilate_then_erode(binary_image, 20, 20, square_struc_ele)
result2 = dilate_then_erode(binary_image, 15, 10, rectangle_struc_ele)
result3 = dilate_then_erode(binary_image, 20, 20, circle_struc_ele)
result4 = dilate_then_erode(binary_image, 20, 20, diamond_struc_ele)
result5 = dilate_then_erode(binary_image, 7, 7, plus_struc_ele)

# Create a figure with 2 rows and 3 columns
fig, axs = plt.subplots(2, 3, figsize=(15, 10))

# Display images in each subplot with custom titles
axs[0, 0].imshow(result1, cmap='gray')
axs[0, 0].set_title('Square')

axs[0, 1].imshow(result2, cmap='gray')
axs[0, 1].set_title('Rectangle')

axs[0, 2].imshow(result3, cmap='gray')
axs[0, 2].set_title('Circle')

axs[1, 0].imshow(result4, cmap='gray')
axs[1, 0].set_title('Diamond')

axs[1, 1].imshow(result5, cmap='gray')
axs[1, 1].set_title('Plus')

# Hide the axes labels
for ax in axs.flat:
    ax.label_outer()

# Hide the last subplot (if necessary, adjust this based on your layout)
axs[1, 2].axis('off')

# Show the plot
plt.show()
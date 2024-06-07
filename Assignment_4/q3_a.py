import cv2
import numpy as np
from scipy.fftpack import dct, idct
import matplotlib.pyplot as plt
import pywt
import huffman

# Load the input image
original_image = cv2.imread('doc3.jpg', cv2.IMREAD_GRAYSCALE)

# Perform DCT (Discrete Cosine Transform)
dct_image = dct(dct(original_image.T, norm='ortho').T, norm='ortho')

# Quantization
quantization_factor = 0.001
quantized_dct_image = np.round(dct_image / quantization_factor)

# Encode the quantized DCT image
encoded_data = quantized_dct_image.flatten().astype(np.int16)
encoded_data.tofile('encoded_image.bin')

# Decode the DCT image
decoded_dct_image = idct(idct(quantized_dct_image.T, norm='ortho').T, norm='ortho').astype(np.uint8)

# Display the original and decoded images
plt.subplot(1, 3, 1)
plt.imshow(original_image, cmap='gray')
plt.title('Original Image')

plt.subplot(1, 3, 2)
plt.imshow(quantized_dct_image, cmap='gray')
plt.title('Encoded Image')

plt.subplot(1, 3, 3)
plt.imshow(decoded_dct_image, cmap='gray')
plt.title('Decoded Image')

plt.show()

# Load an image using OpenCV
original_image = cv2.imread('doc3.jpg', cv2.IMREAD_GRAYSCALE)

# Perform Haar wavelet transform
coeffs = pywt.dwt2(original_image, 'haar')

# Get the approximation and details coefficients
cA, (cH, cV, cD) = coeffs

# Display the coefficients or perform further processing as needed
cv2.imshow('Approximation (cA)', cA)
cv2.imshow('Horizontal Detail (cH)', cH)
cv2.imshow('Vertical Detail (cV)', cV)
cv2.imshow('Diagonal Detail (cD)', cD)

cv2.waitKey(0)
cv2.destroyAllWindows()

# Load the image using OpenCV
original_image = cv2.imread('doc3.jpg', cv2.IMREAD_GRAYSCALE)

# Calculate pixel frequencies
pixel_frequencies = {}
for row in original_image:
    for pixel_value in row:
        if pixel_value in pixel_frequencies:
            pixel_frequencies[pixel_value] += 1
        else:
            pixel_frequencies[pixel_value] = 1

# Build the Huffman tree
huff_tree = huffman.build_tree(pixel_frequencies)

# Generate Huffman codes
huff_codes = huffman.get_codes(huff_tree)

# Encode the image using Huffman codes
encoded_image = []
for row in original_image:
    encoded_row = [huff_codes[pixel] for pixel in row]
    encoded_image.append(encoded_row)

with open('encoded_image.txt', 'w') as f:
    for row in encoded_image:
        f.write(' '.join(row) + '\n')



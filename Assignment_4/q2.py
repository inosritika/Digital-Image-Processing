import cv2
from PIL import Image
import numpy as np

# Load the input image
input_image = Image.open('doc.jpg')

# Convert the input image to binary (black and white)
binary_image = input_image.convert('1')

# Save the binary image
binary_image.save('result.jpg')

# Get the size of the binary image
image_size = binary_image.size

# Function to perform run-length encoding on a binary image
def rle_encode(image_array):
    shape = image_array.shape
    image_array = image_array.flatten()

    if len(image_array) == 0:
        return "0 0"

    encoded_data = f"{shape[0]} {shape[1]} "
    current_pixel = image_array[0]
    current_length = 1

    for i in range(1, len(image_array)):
        if image_array[i] != current_pixel:
            if current_pixel == True:
                encoded_data += f"{1} {current_length} "
            else:
                encoded_data += f"{0} {current_length} "
            current_pixel = image_array[i]
            current_length = 1
        else:
            current_length += 1

    if current_pixel == True:
        encoded_data += f"{1} {current_length}"
    else:
        encoded_data += f"{0} {current_length}"
    return encoded_data

# Function to decode a run-length encoded string back to an image
def rle_decode(encoded_data):
    arr = [int(x) for x in encoded_data.split()]
    rows = arr[0]
    cols = arr[1]
    data = arr[2:]

    decoded_data = []

    for i in range(0, len(data), 2):
        pixel_value = data[i]
        run_length = data[i + 1]
        decoded_data.extend([pixel_value] * run_length)

    decoded_data = np.array(decoded_data, dtype=np.uint8)
    decoded_image = Image.fromarray(decoded_data.reshape(rows, cols))
    return decoded_image

# Function to encode the binary image using run-length encoding
def rle_encode_image(binary_image):
    image_array = np.array(binary_image)
    encoded_image_data = rle_encode(image_array)
    return encoded_image_data

# Load the input image
input_image = Image.open('doc.jpg')

# Convert the input image to binary (black and white)
binary_image = input_image.convert('1')

# Encode the binary image using run-length encoding
rle_encoded_data = rle_encode_image(binary_image)
# print('RLE encoded image data:', rle_encoded_data)

# Save the encoded data to a text file
with open("encoded_data.txt", "w") as encoded_file:
    encoded_file.write(rle_encoded_data)

# Class to perform G3Fax encoding on a binary image
class G3FaxEncoder:

    def __init__(self, image):
        self.image = image
        self.width = image.width
        self.height = image.height

    # Encode the binary image using G3Fax encoding
    def encode(self):
        bitstream = bytearray()

        # Start of page (SOP) marker
        bitstream.extend([0xFF, 0x00])

        image_data = list(self.image.getdata())

        for y in range(self.height):
            line = image_data[y * self.width: (y + 1) * self.width]
            run_length = 0

            for pixel in line:
                if pixel == 0:  # Black pixel
                    run_length += 1
                else:  # White pixel
                    if run_length > 0:
                        bitstream.extend(self.encode_run_length(run_length))
                    run_length = 0

            # End of line (EOL) marker
            bitstream.extend([0x00, 0x00])

        bitstream.extend([0x01, 0x00])
        return bitstream

    # Encode run length for G3Fax
    def encode_run_length(self, run_length):
        encoded = []
        while run_length >= 0x80:
            encoded.append(0x80 | (run_length & 0x7F))
            run_length >>= 7
        encoded.append(run_length)
        return encoded

# Create an instance of the G3FaxEncoder
g3fax_encoder = G3FaxEncoder(binary_image)

# Encode the image using G3Fax and save it to a binary file
g3fax_bitstream = g3fax_encoder.encode()

with open('g3fax_bitstream.bin', 'wb') as f:
    f.write(g3fax_bitstream)
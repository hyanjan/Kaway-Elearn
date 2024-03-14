import os
import cv2

# Directory containing the images
IMAGE_DIR = './data_letters/5'

# Iterate over each image in the directory
for filename in os.listdir(IMAGE_DIR):
    # Get the full path of the image
    filepath = os.path.join(IMAGE_DIR, filename)
    
    # Check if the file is a regular file
    if os.path.isfile(filepath):
        # Read the image using OpenCV
        image = cv2.imread(filepath)
        
        # Check if the image was successfully read
        if image is not None:
            # Get the width and height of the image
            height, width, _ = image.shape
            
            # Print the size of the image
            print(f"Image: {filename}, Size: {width}x{height}")
        else:
            print(f"Unable to read image: {filename}")
    else:
        print(f"{filename} is not a file")
import os
import cv2

# Path to the directory containing the sample image data
sample_data_dir = 'Vispot'

# Function to process a single image and extract cell information
def process_image(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to segment cells
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find contours of cells
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Count the number of cells identified
    num_cells = len(contours)

    return num_cells

# Function to recursively process images in all subdirectories
def process_images_in_directory(directory):
    # Loop through all files and subdirectories in the directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.tiff'):
                image_path = os.path.join(root.encode('unicode-escape').decode(), filename.encode('unicode-escape').decode())
                num_cells = process_image(image_path)
                print(f'Image: {filename}, Number of cells: {num_cells}')

# Call the function to process images in the sample data directory
process_images_in_directory(sample_data_dir)
import os
import cv2
import sys

# Path to the directory containing the sample image data
sample_data_dir = 'Vispot'

# Function to process a single image and extract cell information
def process_image(image_path):
    # Reading the image
    image = cv2.imread(image_path)

    # Converting the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Applying thresholding to segment cells
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Finding contours of cells
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Counting the number of cells in the image
    num_cells = len(contours)

    # Initializing list to store cell information
    cell_info = []

    # Processing each contour
    for contour in contours:
        # Calculating area and perimeter of the contour
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        # Getting bounding box coordinates
        x, y, w, h = cv2.boundingRect(contour)

        # Appending cell information to the list
        cell_info.append({
            'area': area,
            'perimeter': perimeter,
            'centroid': (x + w // 2, y + h // 2),  # Centroid coordinates
            'bounding_box': (x, y, w, h)  # Bounding box coordinates
        })

    return num_cells, cell_info

# Function to recursively process images in all subdirectories
def process_images_in_directory(directory, output_file):
    # Opening the output file in write mode
    with open(output_file, 'w') as f:
        # Redirecting standard output to the file
        original_stdout = sys.stdout
        sys.stdout = f

        # Initializing a dictionary to store image names and their total cell counts
        image_cell_counts = {}

        # Looping through all files and subdirectories in the directory
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.tiff'):
                    # Construct full path to the image
                    image_path = os.path.join(root, filename)
                    num_cells, _ = process_image(image_path)
                    # Store the total number of cells for the image
                    image_cell_counts[filename] = num_cells

        # Printing the list of images and their total cell counts
        print("List of Images and Total Number of Cells:", file=f)
        for image_name, cell_count in image_cell_counts.items():
            print(f"Image: {image_name} - Total Cells: {cell_count}", file=f)
        print('-' * 100, file=f)  # Add separator before detailed cell information
        print(file=f)  # Add line break before the details

        # Looping through all files and subdirectories in the directory
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.tiff'):
                    # Constructing full path to the image
                    image_path = os.path.join(root, filename)
                    _, cell_info = process_image(image_path)
                    # Printing image header with total number of cells
                    print(f'Image: {filename} - Total Cells: {image_cell_counts[filename]}', file=f)
                    # Outputing cell information for each image
                    for i, cell in enumerate(cell_info):
                        # Printing cell header
                        print(f'  Cell {i + 1}:', file=f)
                        # Print cell properties
                        print(f'    Area: {cell["area"]}', file=f)
                        print(f'    Perimeter: {cell["perimeter"]}', file=f)
                        print(f'    Centroid: {cell["centroid"]}', file=f)
                        print(f'    Bounding Box: {cell["bounding_box"]}', file=f)
                        print(file=f)  # Adding a line break after each cell
                    print('-' * 100, file=f)  # Adding a separator between images

        # Restoring standard output
        sys.stdout = original_stdout

# Defining the output file path
output_file = 'result.txt'

# Calling the function to process images and store the output in the result.txt file
process_images_in_directory(sample_data_dir, output_file)
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

    # Initialize list to store cell information
    cell_info = []

    # Process each contour
    for contour in contours:
        # Calculate area and perimeter of the contour
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        # Get bounding box coordinates
        x, y, w, h = cv2.boundingRect(contour)

        # Append cell information to the list
        cell_info.append({
            'area': area,
            'perimeter': perimeter,
            'centroid': (x + w // 2, y + h // 2),  # Centroid coordinates
            'bounding_box': (x, y, w, h)  # Bounding box coordinates
        })

    return cell_info

# Function to recursively process images in all subdirectories
def process_images_in_directory(directory):
    # Loop through all files and subdirectories in the directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.tiff'):
                image_path = os.path.join(root.encode('unicode-escape').decode(), filename.encode('unicode-escape').decode())
                cell_info = process_image(image_path)
                print(f'Image: {filename}')
                # Output cell information for each image
                for i, cell in enumerate(cell_info):
                    print(f'Cell {i + 1}:')
                    print(f'Area: {cell["area"]}')
                    print(f'Perimeter: {cell["perimeter"]}')
                    print(f'Centroid: {cell["centroid"]}')
                    print(f'Bounding Box: {cell["bounding_box"]}')
                    print()  # Add line break after each cell
                print()  # Add double line break after each image

# Call the function to process images in the sample data directory
process_images_in_directory(sample_data_dir)
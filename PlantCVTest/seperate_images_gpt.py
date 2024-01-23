from plantcv import plantcv as pcv
import cv2

def separate_and_save_plants(image_path, output_dir, num_plants=18):
    # Step 1: Read the image
    img = cv2.imread(image_path)
    img_copy = img.copy()

    # Step 2: Convert to grayscale and threshold (customize these steps as needed)
    gray_img = pcv.rgb2gray(img)
    thresh = pcv.threshold.binary(gray_img, threshold=128, object_type='light')

    # Step 3: Find contours
    contours, _ = pcv.find_objects(img, thresh)

    # Assuming that the plants are the largest 'num_plants' objects
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:num_plants]

    # Step 4: Separate and crop each plant
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        cropped_img = img_copy[y:y+h, x:x+w]

        # Step 5: Save each plant as a separate image
        output_path = f"{output_dir}/plant_{i+1}.jpg"
        cv2.imwrite(output_path, cropped_img)

# Example usage
separate_and_save_plants("multi_image.jpg", "outputs")

from plantcv import plantcv as pcv
import numpy as np
import cv2
import sys

# Read in image data
img, path, filename = pcv.readimage(filename="/mnt/c/Users/13144/Documents/CS 4091/Tutorials/PlantCVTest/multi_image.jpg")

# Convert to grayscale colorspace
a = pcv.rgb2gray_lab(rgb_img=img, channel='a')

# Threshold/segment plants from background
bin_mask = pcv.threshold.binary(gray_img=a, threshold=100, max_value=255, object_type="light")

# Optionally, you might need to clean up the mask
# For example, using pcv.fill or pcv.dilate if necessary

# Find objects (contours) in the binary image
obj_hierarchy, obj_contours = pcv.find_objects(img, bin_mask)
# Iterate over each contour to crop and save the individual plant images
#numpy array of type int32
#of size (3, 4)

print(obj_contours[0])
print(np.min(obj_contours[0], axis=0))
sys.exit(1)

for i, contour in enumerate(obj_contours):
    # Calculate the bounding rectangle manually
        x_min, y_min = np.min(contour, axis=0)
        x_max, y_max = np.max(contour, axis=0)
        w, h = x_max - x_min, y_max - y_min

        # Crop the image around the contour
        crop_img = img[y_min:y_min+h, x_min:x_min+w]

        # Save the cropped image
        crop_filename = f"plant_{i+1}.png"
        cv2.imwrite(crop_filename, crop_img)

    # Optionally, analyze each cropped image as needed
    # For example, you can analyze size, shape, color, etc.

# Save out data to file if needed for individual analysis
# This will depend on how you're analyzing each cropped image
# pcv.outputs.save_results(filename="results.txt", outformat="json")

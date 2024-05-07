from plantcv import plantcv as pcv
import cv2
import numpy as np
from skimage import morphology
from calculate_rois import auto_roi

image_path = "plant_image.jpg"

img, path, filename = pcv.readimage(filename=image_path)

#mask the image with an example mask. Filter out small areas
# Convert to HSV and LAB color spaces
hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lab_image = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

# Define HSV range for filtering using OpenCV
# OpenCV uses 0-180 for Hue, so the values are halved
hsv_min = np.array([int(28/2), int(20/100*255), int(20/100*255)])
hsv_max = np.array([int(144/2), 255, 255])
hsv_mask = cv2.inRange(hsv_image, hsv_min, hsv_max)

# Define LAB range for filtering using OpenCV
# OpenCV uses 0-255 for L, a*, and b*
# Note: 'a' and 'b' ranges need to be shifted from [-128, 127] to [0, 255]
# L is scaled from [0, 100] in LAB to [0, 255] in OpenCV
lab_lower = np.array([int(10/100*255), 0, 132])
lab_upper = np.array([int(90/100*255), 124, 255])
lab_mask = cv2.inRange(lab_image, lab_lower, lab_upper)

# Combine the masks (logical AND) and apply to the original image
combined_mask = cv2.bitwise_and(hsv_mask, lab_mask)

#remove small holes in the image so object detection won't be as bad
# Remove small objects
cleaned_mask = morphology.remove_small_objects(combined_mask, min_size=300)

#generate automatic labels from denoised mask
#create labels for masks that may have plants, count number of objects
labeled_image, number_of_plants = pcv.create_labels(mask=cleaned_mask)

#get the centers and optimal radius size
centers, optimal_radius_size = auto_roi(labeled_image)

#now that this is calculated, use pcv.roi.multi to automatically generate the rois
rois = pcv.roi.multi(img=img, coord=centers, radius=optimal_radius_size)

print(rois)

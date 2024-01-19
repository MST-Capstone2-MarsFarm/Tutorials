import cv2
import numpy as np
from plantcv import plantcv as pcv

# Load the image
class options:
    def __init__(self):
        self.image = "multi_image_image.jpg"
        self.debug = "plot"
        self.writeimg= False 
        self.result = "outputs/plantcv-output.json"
        self.outdir = "outputs" # Store the output in the current directory

# Get options
args = options()

# Set debug to the global parameter 
pcv.params.debug = args.debug

# Read image
img, path, filename = pcv.readimage(filename=args.image)

# Convert RGB to HSV and extract the saturation channel
s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')

# Threshold the saturation image
s_thresh = pcv.threshold.binary(gray_img=s, threshold=85, max_value=255, object_type='dark')

# Median Blur
s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
s_cnt = pcv.median_blur(gray_img=s_thresh, ksize=5)

# Find objects
id_objects, obj_hierarchy = pcv.find_objects(img=img, mask=s_cnt)

# Define region of interest (ROI)
roi1, roi_hierarchy= pcv.roi.rectangle(img=img, x=100, y=100, h=200, w=200)

# Decide which objects to keep
roi_objects, hierarchy, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                              roi_hierarchy=roi_hierarchy,
                                                              object_contour=id_objects, 
                                                              obj_hierarchy=obj_hierarchy,
                                                              roi_type='partial')

# Object combine kept objects
obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy)

# Find shape properties, output shape image (optional)
shape_img = pcv.analyze_object(img=img, obj=obj, mask=mask)

# Output shape data
#pcv.print_results(filename=args.result)

# The output filepath
output_image_filepath = "/mnt/data/shape_img.jpg"

# Save the output
cv2.imwrite(output_image_filepath, shape_img)

output_image_filepath
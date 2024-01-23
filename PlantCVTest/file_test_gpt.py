import cv2
from plantcv import plantcv as pcv
import matplotlib.pyplot as plt
import sys

# Define the options class
class Options:
    def __init__(self):
        self.image = "multi_image.jpg"
        self.debug = "plot"
        self.writeimg = False
        self.result = "outputs/plantcv-output.json"
        self.outdir = "outputs"  # Store the output in the current directory

# Get options
args = Options()

# Set debug to the global parameter 
#pcv.params.debug = args.debug

# Read image
img, _, _ = pcv.readimage(filename=args.image, mode='native')

# Convert RGB to HSV and extract the saturation channel
s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
#s = pcv.rgb2gray_lab(rgb_img=img, channel='a')

# Threshold the saturation image
s_thresh = pcv.threshold.binary(gray_img=s, threshold=120, object_type='dark')

a_fill = pcv.fill(bin_img=s_thresh, size=200)

# The output filepath
output_image_filepath = "outputs/shape_img.jpg"

# Median Blur
#s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)

# Define region of interest (ROI)
roi = pcv.roi.rectangle(img=img, x=100, y=100, h=200, w=200)

# Filter binary image to make a clean mask based on ROI 
# (no longer needs `pcv.find_objects` or `pcv.object_composition`)
mask = pcv.roi.filter(mask=s_thresh, roi=roi, roi_type="partial")

cv2.imwrite("test.png", mask)
sys.exit(1)

labeled_objects, n_obj = pcv.create_labels(mask=mask)

analysis_image = pcv.analyze.size(img=img, labeled_mask=labeled_objects, n_labels=n_obj)

cv2.imwrite("test.png", analysis_image)
sys.exit(1)

# Extract shape traits from plant
shape_img = pcv.analyze.size(img=img,labeled_mask=mask, n_labels=1)

# Output shape data
# pcv.print_results(filename=args.result)

# The output filepath
output_image_filepath = "outputs/shape_img.jpg"

# Save the output image
# Assuming 'analysis_images' is a list of images, you can save the first one or modify as needed
cv2.imwrite(output_image_filepath, analysis_images[0])

output_image_filepath
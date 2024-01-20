import cv2
import numpy as np
from plantcv import plantcv as pcv
import plantcv as pcv_all

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

# Read in image data (no change)
img, path, filename = pcv.readimage(filename="rgb_img.png")

# Covert to grayscale colorspace (no change)
a = pcv.rgb2gray_lab(rgb_img=img, channel='a')

# Threshold/segment plant from background (removed max_value)
bin_mask = pcv.threshold.binary(gray_img=a, threshold=100, object_type="light")

# Define ROI (reduced outputs)
roi = pcv.roi.rectangle(img=img, x=100, y=100, h=100, w=100)

# Filter binary image to make a clean mask based on ROI 
# (no longer needs `pcv.find_objects` or `pcv.object_composition`)
mask = pcv.roi.filter(mask=bin_img, roi=roi, roi_type="partial")

# Extract shape traits from plant
shape_img = pcv.analyze.size(img=img,labeled_mask=mask, n_labels=1)

# Save out data to file
pcv.outputs.save_results(filename="results.txt", outformat="json")
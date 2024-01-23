import cv2
from plantcv import plantcv as pcv
import sys

# Load the image
class options:
    def __init__(self):
        self.image = "multi_image_image.jpg"
        self.debug = "plot"
        self.writeimg= True 
        self.result = "outputs/plantcv-output.json"
        self.outdir = "outputs" # Store the output in the current directory

# Get options
#args = options()

# Set debug to the global parameter 
#pcv.params.debug = args.debug

# Read in image data (no change)
rgb_img, path, filename = pcv.readimage(filename="multi_image.jpg")

s = pcv.rgb2gray_hsv(rgb_img=rgb_img, channel='s')
s_thresh = pcv.threshold.binary(gray_img=s, threshold=120, object_type='dark')

# Fill in small objects if below the "size" threshold
a_fill_image = pcv.fill(bin_img=s_thresh, size=50)
# Flood fill any holes in the leaves (false negative pixels)
a_fill_image = pcv.fill_holes(a_fill_image)

roi1 = pcv.roi.rectangle(img=rgb_img, x=50, y=0, h=a_fill_image.shape[0]-1, w=a_fill_image.shape[1]-1-50)

kept_mask  = pcv.roi.filter(mask=a_fill_image, roi=roi1, roi_type='partial')

cv2.imwrite("test.png", kept_mask)
sys.exit(1)

labeled_objects, n_obj = pcv.create_labels(mask=kept_mask)

analysis_image = pcv.analyze.size(img=img_rgb, labeled_mask=labeled_objects, n_labels=n_obj)


print(labeled_objects.shape)
print(n_obj)


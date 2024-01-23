from plantcv import plantcv as pcv

# Load image and create a binary mask
img, path, filename = pcv.readimage(filename="/mnt/c/Users/13144/Documents/CS 4091/Tutorials/PlantCVTest/multi_image.jpg")
a = pcv.rgb2gray_hsv(rgb_img=img, channel='s')
binary_mask = pcv.threshold.binary(gray_img=a, threshold=85, max_value=255, object_type='dark')

# Identify contours
contours, hierarchy = pcv.find_objects(img, binary_mask)

# Cluster contours and split the image
out = pcv.cluster_contour_splitimg(rgb_img=img, grouped_contour_indices=contours)

# Each element in 'out' is an image containing a single plant
for i, plant_img in enumerate(out):
    pcv.print_image(plant_img, f"plant_{i}.jpg")
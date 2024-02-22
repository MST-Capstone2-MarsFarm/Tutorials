from plantcv import plantcv as pcv
import pandas as pd
from PIL import Image
from parallel_pandas import ParallelPandas

import os, functools, shutil, sys

ParallelPandas.initialize(n_cpu=64, disable_pr_bar = True)

def generate_mask(input_image_path: str, output_mask_folder: str=None):
    try:
        img0, _, img_name = pcv.readimage(filename=input_image_path)
    except:
        return
    a = pcv.rgb2gray_lab(rgb_img=img0, channel='a')
    thresholded_image = pcv.threshold.otsu(gray_img=a, object_type='dark')
    a_fill = pcv.fill(bin_img=thresholded_image, size=50)
    a_fill = pcv.fill_holes(a_fill)
    
    a_fill_bw = a_fill.astype(bool).astype('uint8') * 255
    p = Image.fromarray(a_fill_bw)
    mask_output_path = os.path.join(output_mask_folder, img_name)
    #print(mask_output_path)
    p.save(mask_output_path)
    return 

#get input paths
input_image_folder = sys.argv[1] #quick workardoun for filenames being messed up
output_mask_superfolder = sys.argv[-1]

#ensure input paths exist
assert os.path.isdir(input_image_folder), f"{input_image_folder} is not a directory"
assert os.path.isdir(output_mask_superfolder), f"{output_mask_superfolder} is not a directory"

#wipe outputs folder
base_directory_name = os.path.basename(input_image_folder)
output_mask_folder = os.path.join(output_mask_superfolder, base_directory_name)
if os.path.isdir(output_mask_folder): shutil.rmtree(output_mask_folder, ignore_errors=True)
os.mkdir(output_mask_folder)     

function_prototype = functools.partial(generate_mask, output_mask_folder=output_mask_folder)

file_names = [os.path.join(input_image_folder, file) for file in os.listdir(input_image_folder)]

file_series = pd.Series(file_names)

file_series.p_map(function_prototype)
print(f"Finished {base_directory_name}")
    
from plantcv import plantcv as pcv
import pandas as pd
from PIL import Image
from parallel_pandas import ParallelPandas

ParallelPandas.initialize(disable_pr_bar = True)

def generate_mask(input_image_path: str, output_mask_path: str):
    img, _, img_name = pcv.readimage(filename=input_image_path)
    print(img_name)
    

input_image_path = "/mnt/stor/ceph/csb/marsfarm/projects/marsfarm_image_analysis/inputs/MV1-0043_ 6.1.23 - 6.16.23 (Purple Basil)/2023-05-31_2305.jpg"

generate_mask(input_image_path, "test")
    
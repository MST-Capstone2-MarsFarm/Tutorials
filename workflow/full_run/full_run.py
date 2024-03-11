import pandas as pd
import numpy as np
from plantcv import plantcv as pcv
import cv2
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)

from swifter import set_defaults
from pathlib import Path, PosixPath
from shutil import copy
import os, sys
from time import time

input_folders = [
    Path("/mnt/stor/ceph/csb/marsfarm/projects/inputs/MV1-0039_7.11.23-8.11.23(Tomato)"),
    Path("/mnt/stor/ceph/csb/marsfarm/projects/inputs/MV1-0041_6.2.23-6.20.23(Peas)"),
    Path("/mnt/stor/ceph/csb/marsfarm/projects/inputs/MV1-0043_6.1.23-6.16.23(Purple Basil)")
]

full_input_paths = []
for folder in input_folders:
    full_input_paths.extend(folder.glob('*.jpg'))
full_input_paths.sort()

#create output files and their directories
output_folder_path = Path("/mnt/stor/ceph/csb/marsfarm/projects/leaf_detection/outputs")
def create_output_file(input_file_path: PosixPath):
    output_path = output_folder_path / input_file_path.parent.name / input_file_path.name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return str(output_path)
file_output_paths = [create_output_file(input_file_path) for input_file_path in full_input_paths]
input_str_file_paths = tuple(str(input_path) for input_path in full_input_paths)
#print(file_output_paths)
parameters_df = pd.DataFrame({"Input_Path": input_str_file_paths, "Output_Path": file_output_paths})

def filter_images(input_path: str, output_path: str):
    #plantcv's readimage uses opencv's imread as a backend
    image, _, _ = pcv.readimage(input_path)
    
    # Convert the image from RGB to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the range of green color in HSV
    # Adjusted range of green color in HSV to reduce false positives
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([95, 255, 255])
    
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Bitwise-AND mask and original image to extract green parts
    plant_pixels = cv2.bitwise_and(image, image, mask=mask)

    #convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Count all non-zero (non-black) pixels
    count_non_black = cv2.countNonZero(gray_image)
    
    #using 20k pixels as a lowball starting point
    #trying to make sure we get as many plant photos as possible
    #using shutil.copy to make things quicker
    if count_non_black > 20000:
        copy(input_path, output_path)

#pandarallel apply
#pandarallel took 25 seconds on 1 general node
#27.1345 seconds on head node

#start_time = time()
#parameters_df.parallel_apply(lambda row: filter_images(row['Input_Path'], row['Output_Path']), axis=1)
#print(time() - start_time)

def test_function(arg1, arg2):
    print(f"{arg1}, {arg2}")

from dask_jobqueue import SLURMCluster
from dask.distributed import Client
import dask.dataframe as dd

cluster = SLURMCluster(
    cores=64,
    memory="256 GB",
    walltime = "2-00:00:00",
    name="leaf_identification",
    job_extra=['--partition=general']
)

cluster.adapt(minimum_jobs=1)
client = Client(cluster)




#import swifter
#parameters_df.swifter.apply(lambda row: filter_images(row['Input_Path'], row['Output_Path']), axis=1)


'''from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("example").getOrCreate()

import pyspark.pandas as ps
spark_df = ps.DataFrame({"Input_Path": input_str_file_paths, "Output_Path": file_output_paths})
#took 192 seconds
start_time = time()
spark_df.rdd.apply(lambda row: filter_images(row['Input_Path'], row['Output_Path']), axis=1)
print(time() - start_time)'''

#df['input'].swifter.apply(my_func)
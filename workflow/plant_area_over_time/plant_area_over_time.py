import os, sys, shutil
import numpy as np
from plantcv import plantcv as pcv
import pandas as pd
from parallel_pandas import ParallelPandas
ParallelPandas.initialize(n_cpu=64, disable_pr_bar = True)
import matplotlib.pyplot as plt

from datetime import datetime
from time import mktime

input_folder = "/mnt/stor/ceph/csb/marsfarm/projects/marsfarm_image_analysis/inputs/MV1-0041_6.2.23-6.20.23(Peas)"

def get_area(input_image_path: str):
    img, _, _ = pcv.readimage(filename=input_image_path)
    a = pcv.rgb2gray_lab(rgb_img=img, channel='a')
    thresholded_image = pcv.threshold.otsu(gray_img=a, object_type='dark')
    a_fill = pcv.fill(bin_img=thresholded_image, size=50)
    a_fill = pcv.fill_holes(a_fill)
    
    area = np.count_nonzero(a_fill)
    return area
    


#get filenames, sort them from start
picture_names_list = sorted(os.listdir(input_folder))
time_dates_military = [name.split('.jpg')[0] for name in picture_names_list]
time_dates_stripped = [datetime.strptime(datetime_string, "%Y-%m-%d_%H%M") for datetime_string in time_dates_military]
unix_time_list =  [int(mktime(datetime_object.timetuple())) for datetime_object in time_dates_stripped]
start_time = unix_time_list[0]
unix_times_from_start = [unix_time - start_time for unix_time in unix_time_list]
hours_from_start = [(unix_time // 3600) for unix_time in unix_times_from_start]

file_names = sorted([os.path.join(input_folder, file) for file in os.listdir(input_folder)])

file_names_series = pd.Series(file_names[:100])
areas = file_names_series.p_map(get_area).tolist()
#print(areas)

plt.plot(file_names[:100], areas, marker='o')
plt.savefig('test.png')



#print([picture_names_list[0], picture_names_list[2]])
#print([time_dates_military[0], time_dates_military[2]])
#print([time_dates_stripped[0], time_dates_stripped[2]])
#print([unix_times_from_start[0], unix_times_from_start[2]])
#print(hours_from_start)
#print(file_names)
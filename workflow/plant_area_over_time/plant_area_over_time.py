import os, sys, shutil
import numpy as np
from plantcv import plantcv as pcv
import pandas as pd
from pandarallel import pandarallel
from scipy.signal import lfilter
from copy import deepcopy
pandarallel.initialize(verbose=0, progress_bar = True)

import matplotlib.pyplot as plt
import gc

from datetime import datetime
from time import mktime

input_folder = "/mnt/stor/ceph/csb/marsfarm/projects/marsfarm_image_analysis/inputs/MV1-0041_6.2.23-6.20.23(Peas)"

#function to calculate the area of an image, using the number of pixels as a proxy for area
def get_area(input_image_path: str):
    img, _, _ = pcv.readimage(filename=input_image_path)
    a = pcv.rgb2gray_lab(rgb_img=img, channel='a')
    thresholded_image = pcv.threshold.otsu(gray_img=a, object_type='dark')
    a_fill = pcv.fill(bin_img=thresholded_image, size=50)
    a_fill = pcv.fill_holes(a_fill)
    
    area = np.count_nonzero(a_fill)
    #for memory management
    #del img, a, thresholded_image, a_fill
    return area
    


#get filenames, sort them from start
picture_names_list = sorted(os.listdir(input_folder))
time_dates_military = [name.split('.jpg')[0] for name in picture_names_list]
time_dates_stripped = [datetime.strptime(datetime_string, "%Y-%m-%d_%H%M") for datetime_string in time_dates_military]
unix_time_list =  [int(mktime(datetime_object.timetuple())) for datetime_object in time_dates_stripped]
#calculate the number of hours since the taking of the first image
start_time = unix_time_list[0]
unix_times_from_start = [unix_time - start_time for unix_time in unix_time_list]
hours_from_start = [(unix_time // 3600) for unix_time in unix_times_from_start]

#get file names to calculate areas
file_names = sorted([os.path.join(input_folder, file) for file in os.listdir(input_folder)])
limit_size = -1
file_names_series = pd.Series(file_names)
#print(len(file_names_series))

#calculate the areas
#get from cache if already calculated (as csv file)
if os.path.isfile("areas.csv"): areas = pd.read_csv("areas.csv")['0']
else:
    areas_series = file_names_series.parallel_map(get_area)
    areas_series.to_csv("areas.csv", index=False)
    areas = areas_series.tolist()

graph_dataframe = pd.DataFrame({"area": areas, "hours_from_start": hours_from_start})

#filtered_df = deepcopy(graph_dataframe)

#filter dataframe using difference and iqr instead of relative difference
graph_dataframe['diff'] = graph_dataframe['area'].diff()
graph_dataframe.loc[0, 'diff'] = 0
Q1 = graph_dataframe['diff'].quantile(.25)
Q3 = graph_dataframe['diff'].quantile(.75)
IQR = Q3 - Q1
print(IQR)
filtered_df = graph_dataframe[~((graph_dataframe['diff'] < (Q1 - 1.5 * IQR)) | (graph_dataframe['diff'] > (Q3 + 1.5 * IQR)))]
#print(graph_dataframe['diff'].median())
#print(graph.quan)
#graph_dataframe['diff'].to_csv('diff.csv', index=False)
graph_dataframe['pct_change'] = graph_dataframe['area'].pct_change()
graph_dataframe.loc[0, 'pct_change'] = 0

pct_change_list = graph_dataframe['pct_change'].tolist()

#filter out large spikes in data
up_spike = False
down_spike = False
indeces_to_keep = []
spike_level = .5
for i in range(len(pct_change_list)):
    #up spike
    if pct_change_list[i] > spike_level and not down_spike:
        up_spike = True
    #return to normal from up spike
    elif pct_change_list[i] < -(spike_level * .75) and up_spike:
        up_spike = False 
        indeces_to_keep.append(i)
    #down spike
    elif pct_change_list[i] < -spike_level and not up_spike:
        down_spike = True
    #return to normal from down spike
    elif pct_change_list[i] > (spike_level * .75) and down_spike:
        down_spike = False
        indeces_to_keep.append(i)
    else:
        indeces_to_keep.append(i)
    
#filtered_df = graph_dataframe.iloc[indeces_to_keep]

#graph filtered data

n = len(graph_dataframe)
b = [1.0 / n] * n
a = 1
filtered_df['smoothed'] = lfilter(b, a, filtered_df['area'].tolist())
filtered_df['rolling_mean'] = filtered_df['area'].rolling(window=5).mean()     
#print(pct_change_list)
#filtered_df = graph_dataframe[graph_dataframe['pct_change'].abs() <= 0.5]
#print(filtered_df['pct_change'].tolist())

#since the differentials in time are so small, having a 50% spike margin seems like a somewhat reasonable guess that won't remove normal observations
#condition = graph_dataframe['area'] > 1.5 * graph_dataframe['area'].shift(1)
#filtered_df = graph_dataframe[~condition | graph_dataframe.index.isin([0])]



plt.clf()
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10,8))
fig.suptitle("Plant Area Over Time")

axes[0,0].plot(graph_dataframe['hours_from_start'], graph_dataframe['area'])
axes[0,0].set_title("Raw Results")
axes[0,1].plot(filtered_df['hours_from_start'], filtered_df['area'])
axes[0,0].set_title("50% Difference Removals")
axes[1,0].plot(filtered_df['hours_from_start'], filtered_df['rolling_mean'])
axes[0,0].set_title("50% Difference + Rolling Mean")
axes[1,1].plot(filtered_df['hours_from_start'], filtered_df['smoothed'])
axes[0,0].set_title("50% Difference Smoothed")

for ax in axes.flat:
    ax.set(xlabel="Time (hours)", ylabel="Plant area (pixels)")
plt.tight_layout()

plt.savefig("results.png")
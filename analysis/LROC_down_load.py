# Initialize workspace: 
import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = 353894500
import numpy as np
import h5py
#np.random.seed(42)
import time

# Download file:
fn_pre='NAC_DTM_AESTUUM2'
website='http://lroc.sese.asu.edu/data/LRO-L-LROC-5-RDR-V1.0/LROLRC_2001/DATA/SDP/NAC_DTM/AESTUUM2/'
data_path='../../data/'
for fn in [fn_pre+'.TIF', fn_pre+'.LBL']:
    if os.path.isfile(data_path+fn): 
        print('File {} exist in library!'.format(fn))
    else: 
        s_time = time.time()
        print('File {} does not exist in library. downloading now ...'.format(fn))
        URL = website+fn
        os.sys('wget -P "$data_path" "$URL"')
        #!wget -P "$data_path" "$URL"
        print('Downloaded into {}'.format(data_path+fn))
        print("Time elapsed: {0:.1f} sec".format(time.time() - s_time))
        
# Read source image.
img = Image.open(data_path + fn_pre + '.TIF')
print('Original image. size (shape): {} | mode (bit depth): {}'.format(img.size, img.mode))
# dimensions of source image: [Min long, max long, min lat, max lat] 
# read from Label file: 
import re
file = open(data_path + fn_pre+'.LBL','r')
lines = [line.rstrip('\n') for line in file]
for line in lines:
    if 'MAXIMUM_LATITUDE' in line:
        max_lat=float(re.findall("\d+.\d*",line)[0])
    if 'MINIMUM_LATITUDE' in line:
        min_lat=float(re.findall("\d+.\d*",line)[0])
    if 'EASTERNMOST_LONGITUDE' in line:
        max_lon=float(re.findall("\d+.\d*",line)[0])
    if 'WESTERNMOST_LONGITUDE' in line:
        min_lon=float(re.findall("\d+.\d*",line)[0])
    if 'MAP_SCALE' in line:
        res=float(re.findall("\d+.\d*",line)[0])

source_cdim = [min_lon, max_lon, min_lat, max_lat]
print(source_cdim)
print('map resolution: {} m/pix'.format(res))
# Initialize workspace: 
import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = 353894500
import numpy as np
import h5py
#np.random.seed(42)
import time

# Conversion function: 
def convert16to8bit(img):
    """Transform PIL image of 16-bit to 8-bit"""
    img16=np.asarray(img)
    img16vec=np.concatenate(img16)

    #transformation: 
    min_val = np.min(img16vec)
    dif = (np.max(img16vec)-min_val)
    img8 = np.uint8((img16-min_val)/dif*256)

    return Image.fromarray(img8)

# Download file:
fn='sldem2015_512_00n_30n_000_045.jp2'
website='http://pds-geosciences.wustl.edu/lro/lro-l-lola-3-rdr-v1/lrolol_1xxx/data/sldem2015/tiles/jp2/'
data_path='../data/'
if os.path.isfile(data_path+fn): 
    print('File {} exist in library!'.format(fn))
else: 
    s_time = time.time()
    print('File {} does not exist in library. downloading now ...'.format(fn))
    URL = website+fn
    os.sys('wget -P "$data_path" "$URL"')
    print('Downloaded into {}'.format(data_path+fn))
    print("Time elapsed: {0:.1f} sec".format(time.time() - s_time))

# Read source image.
img = Image.open(data_path + fn)
print('Original image. size (shape): {} | mode (bit depth): {}'.format(img.size, img.mode))
# [Min long, max long, min lat, max lat] dimensions of source image.
source_cdim = [0., 45., 0., 30.]

'''
print('Cropping image...')
s_time=time.time()
box = (0,1800,3600,3600)
ex_box = source_cdim*(np.array(box)/(img.size+img.size))[[0,2,1,3]]
img_cr=img.crop(box)
print('Cropped image. size (shape): {} | mode (bit depth): {}'.format(img_cr.size, img_cr.mode))
print("Time elapsed: {0:.1f} sec".format(time.time() - s_time))
'''

print('Converting from 16-bit to 8-bit...')
s_time = time.time()
con_img = convert16to8bit(img)
print('Converted image. size (shape): {} | mode (bit depth): {}'.format(con_img.size, con_img.mode))
print("Time elapsed: {0:.1f} sec".format(time.time() - s_time))

#fn='sldem2015_512_00n_30n_000_045.jp2'
nfn = data_path + fn[:-4] + '_8bit.png'
con_img.save(nfn)
print('Saved as: ' + nfn)

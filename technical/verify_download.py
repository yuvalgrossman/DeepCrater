# 1. check installation: 
import sys
import os
print(sys.version)
fid=open('requirements.txt','r'); req=fid.readlines(); fid.close()

os.system('pip freeze > technical/inst_pip.txt')
fid=open('technical/inst_pip.txt','r'); inst_pip=fid.read(); fid.close()
os.system('conda list --export > technical/inst_conda.txt')
fid=open('technical/inst_conda.txt','r'); inst_conda=fid.read(); fid.close()

print('Packages installed: \x1b[32m same version \x1b[33m different version \x1b[31m not installed')
for pack in req:
    if pack in inst_pip+inst_conda:
        print("\x1b[32m{}".format(pack))
    elif pack[:pack.find('==')].lower() in inst_pip+inst_conda:
        print("\x1b[33m{}".format(pack))
    else:
        print("\x1b[31m{}".format(pack))

# inst_pip+inst_conda

# 2. download files from zenodo: 
deepmoon_path='../DeepCrater/'
data_path = '../data/'
if deepmoon_path not in sys.path:
    sys.path.append(deepmoon_path)
if data_path not in sys.path:
    sys.path.append(data_path) 
    
# check if exist here and download data from Zenodo: 
Files = ["dev_craters.hdf5", # - Pandas HDFStore of crater locations and sizes for images in the validation dataset.
         "dev_images.hdf5", # - Input DEM images and output targets of the validation dataset.  Also includes each image's longitude/latitude bounds, and the pixel bounds of the global DEM regions cropped to make each image.
         "LunarLROLrocKaguya_118mperpix.png", # - LRO LOLA and Kaguya Terrain Camera DEM Merge, downsampled to 118 m/pixel and 8 bits/pixel.  The original file can be found at: https://astrogeology.usgs.gov/search/map/Moon/LRO/LOLA/Lunar_LRO_LrocKaguya_DEMmerge_60N60S_512ppd.
         "model_keras1.2.2.h5", # - Keras model weights for the DeepMoon CNN, compatible with Keras version 1.2.2.
         "model_keras2.h5", # - Keras model weights for the DeepMoon CNN, compatible with Keras versions >= 2.0.
         "post-processed_sample_images.zip", # - Contains a set of sample images from the test dataset with the Moon DEM image, new identified craters, CNN target predictions, and ground-truth. The new craters from these images were used to estimate the post-processed false positive rate. See Instructions.txt in .zip file for more details.
         "post-processed_test_craters.npy", # - numpy file containing post-processed craters identified by our pipeline on the test set. Each crater entry is arranged as a tuple: (longitude, latitude, radii), where longitude and latitude are in degrees, and radius is in kilometres. 
         "test_craters.hdf5", # - Pandas HDFStore of crater locations and sizes for images in the test dataset.
         "test_images.hdf5", # - Input DEM images and output targets of the test dataset.  Also includes each image's longitude/latitude bounds, and the pixel bounds of the global DEM regions cropped to make each image.
         "train_craters.hdf5", # - Pandas HDFStore of crater locations and sizes for images in the training dataset.
         "train_images.hdf5"] # - Input DEM images and output targets of the training dataset.  Also includes each image's longitude/latitude bounds, and the pixel bounds of the global DEM regions cropped to make each image.]
Files = Files[2:7]
for file in Files: 
  if os.path.isfile(data_path+file): 
    print('File {} exist in library!'.format(file))
  else: 
    print('File {} does not exist in library. downloading now from Zenodo ...'.format(file))
    URL = "https://zenodo.org/record/1133969/files/"+file
    os.system('wget -P "$data_path" "$URL"')
    print('Downloaded into {}'.format(data_path+file))

# download albedo map: 
if not os.path.isfile(data_path+'Clementine_albedo_simp750.jpg'): 
    os.system('wget -P $data_path https://upload.wikimedia.org/wikipedia/commons/e/ea/Clementine_albedo_simp750.jpg')
if not os.path.isfile(data_path+'moonmercator.jpg'):
    os.system('wget -P $data_path http://btc.montana.edu/ceres/worlds/landform/moonmercator.jpg')
#albedo = Image.open(data_path + "/Clementine_albedo_simp750.jpg")
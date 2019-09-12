sudo apt-get update
# install conda: 
mkdir Downloads
cd Downloads
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
cd ..
bash Downloads/Miniconda3-latest-Linux-x86_64.sh

# install pip: 
sudo apt-get install python3-pip
 pip3 install --upgrade pip  
# install anaconda: 
#curl -O https://repo.anaconda.com/archive/Anaconda3-2019.07-Linux-x86_64.sh
#bash Anaconda3*

#clone:
git clone https://github.com/yuvalgrossman/DeepCrater
cd DeepCrater

#install virtualenv:
sudo apt install virtualenv
virtualenv -p python3 deep_crater_env
source deep_crater_env/bin/activate

#install requirements:
conda install Cartopy
pip install h5py==2.6.0
pip install Keras==1.2.2
pip install numpy
pip install opencv-python==3.2.0.6
pip install pandas==0.19.1
pip install Pillow
pip install scikit-image==0.12.3
pip install tables==3.4.2
pip install tensorflow==1.10.0rc0
pip install jupyter

#configure jupyter: 
#jupyter notebook --generate-config
#vi ~/.jupyter/jupyter_notebook_config.py
# add these lines to the file, save and exit:
#c = get_config()
#c.NotebookApp.ip = '*'
#c.NotebookApp.open_browser = False
#c.NotebookApp.port = 7000

#launch jupyter: 
#jupyter-notebook --no-browser --port=7000 &

#python techinical/verify_download.py

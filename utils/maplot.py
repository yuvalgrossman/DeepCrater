import h5py
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

rmoon=1737 #km
kmperdeg = 2*np.pi*rmoon/360 # km per degree transformation

def plot_map_w_scalebar2(ax, train_imgs, im_num, mask=True,colorbar=True):
  im_lims = train_imgs['longlat_bounds']['img_{:02d}'.format(im_num)][...] 
  plt.imshow(train_imgs['input_images'][im_num][...], extent=im_lims, origin='upper', 
             cmap='YlGn', aspect='equal') #, vmin=50, vmax=150
  if colorbar:
    plt.colorbar()
  if mask:
    plt.imshow(1-train_imgs['target_masks'][im_num][...], alpha=0.2, extent=im_lims, origin='upper', cmap='Greys_r', aspect='equal')
# np.cos(np.deg2rad(im_lims[2:].mean()))
  plt.title('Image #{} with target masks'.format(im_num))
  l,r=plt.xlim()
  barlength = 0.3*(r-l)
  bartext = '{:2.1f} km'.format(barlength*kmperdeg)
  bar = AnchoredSizeBar(ax.transData, barlength, bartext, 4)
  ax.add_artist(bar)
  ax.grid()
  return im_lims

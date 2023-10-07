import warnings

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from cartopy import crs as ccrs, feature as cfeature
from scipy.ndimage import gaussian_filter

#  Suppress warnings issued by Cartopy when downloading data files
warnings.filterwarnings('ignore')

from adjustText import adjust_text

from python.deprecated.national_plots import generateNationalPlot

path = '/home/scrump/containers/website/html/goes/model_backgrounds/'

# PLOTTING FUNCTION FOR RADAR DATA
def generateLocalPlot(params):
    projPC = ccrs.PlateCarree()

    #State params allow data to be passed into multiprocessing pool
    state = params['state']

    if state == 'national':
        res = '50m'
    else:
        res = '10m'

    lonW = params['lonW']
    lonE = params['lonE']
    latS = params['latS']
    latN = params['latN']

    #Main projection to view the plot through. Center set to center of bounding coords
    projection = ccrs.LambertConformal(central_longitude=-97.5, central_latitude=40.5)

    #Set size of overall figure and define subplot for model data
    if state == 'national':
        fig = plt.figure(figsize=(10, 8)) # GRAPH SPECIFIC
    else:
        fig = plt.figure(figsize=(10, 9))

    ax = plt.subplot(1, 1, 1, projection=projection)
    
    #Setup gridlines and properties
    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--', x_inline=False, y_inline=False, dms=True)
    gl.ylocator = mticker.FixedLocator([25, 30, 35, 40, 45, 50])
    gl.xlocator = mticker.FixedLocator([-55, -65, -70, -75, -80, -85, -90, -95, -100, -105, -110, -115, -120, -125])
    gl.xlabels_bottom = False
    gl.xlabel_style = {'rotation': 45}
    
    #Setup corner logo
    im = plt.imread('/home/scrump/containers/website/python/model_files/scrump-logo.png')
    
    if state == 'national':
        ax1 = ax.inset_axes([-0.019, 0.01, 0.15, 0.155]) # GRAPH SPECIFIC
    else:
        ax1 = ax.inset_axes([-0.001, 0.01, 0.15, 0.17]) # GRAPH SPECIFIC

    ax1.axis('off')
    ax1.imshow(im, aspect='equal')
    
    #Set map extent and allow matplotlib to adjust extent to maintain aspect ratio
    ax.set_extent([lonW, lonE, latS, latN], crs=projPC) # GRAPH SPECIFIC
    ax.set_aspect('auto')
    
    #Add map background features
    ax.coastlines(resolution=res, color='gray') # GRAPH SPECIFIC
    ax.add_feature(cfeature.STATES, linewidth=0.3, edgecolor='brown', zorder=3) # GRAPH SPECIFIC
    ax.add_feature(cfeature.LAND, zorder=1) # GRAPH SPECIFIC
    ax.add_feature(cfeature.LAKES, zorder=1) # GRAPH SPECIFIC
    ax.add_feature(cfeature.OCEAN, zorder=1) # GRAPH SPECIFIC
    ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='blue', zorder=3) # GRAPH SPECIFIC
    
    #Ensure tight layout of figure, define the complete path and save it
    #fig.tight_layout()
    plt.subplots_adjust(hspace=0,wspace=0)
    final_path = path + state + '.png'

    #Adjust the labels so they don't horribly overlap
    #adjust_text(texts) broken :(

    fig.savefig(final_path, edgecolor='black', dpi=120, transparent=True)
    print('Saving plot to ' + final_path)
    #Clear the whole figure from memory or risk exploding your computer
    plt.clf() #SUPER DUPER IMPORTANT

    return

from state_parameters import state_params as default_state_params

for params in default_state_params:
    generateLocalPlot(params)
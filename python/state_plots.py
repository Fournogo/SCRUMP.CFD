import warnings

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.image as image
from cartopy import crs as ccrs, feature as cfeature

import numpy as np

#  Suppress warnings issued by Cartopy when downloading data files
warnings.filterwarnings('ignore')

import pytz

from adjustText import adjust_text

from national_plots import generateNationalPlot

# PLOTTING FUNCTION FOR RADAR DATA
def generateLocalPlot(params):
    projPC = ccrs.PlateCarree()

    #'GRAPH SPECIFIC' TAG DENOTES SOMETHING UNIQUE TO DIFFERENT GRAPH TYPES. IE RADAR DATA VS TEMPERATURE DATA, DIFFERENT LOCATIONS ETC.
    res = '10m'
    link_list = []
    #State params allow data to be passed into multiprocessing pool
    state = params['state']

    #Use a separate function for plotting the national map since a bunch of things need to be changed
    if state == 'national':
        return generateNationalPlot(params)

    tz = params['tz']
    lonW = params['lonW']
    lonE = params['lonE']
    latS = params['latS']
    latN = params['latN']
    ds = params['ds']

    sample_points = params['sample_points']
    data_unit = params['data_unit']
    cmap = params['cmap'] 
    product = params['product']
    data_min = params['data_min']
    data_max = params['data_max']
    data_label = params['data_label']

    #Standard parameters
    path = params['path']
    USA_cities = params['city_csv']
    description = params['description']

    #Main projection to view the plot through. Center set to center of bounding coords
    projection = ccrs.LambertConformal(central_longitude=-97.5, central_latitude=40.5)
    
    #Main loop to go through each forecast hour
    for step in range(ds.step.size):
        
        #Get the local time zone for the graph
        time = ds['valid_time'].to_index()
        time_utc = time.tz_localize(pytz.UTC) # GRAPH SPECIFIC
        local_tz = pytz.timezone(tz)
        time_local = time_utc.tz_convert(local_tz)

        #Set size of overall figure and define subplot for model data
        fig = plt.figure(figsize=(10,9))
        ax = plt.subplot(1, 1, 1, projection=projection)
        
        #Setup gridlines and properties
        gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--', x_inline=False, y_inline=False, dms=True)
        gl.ylocator = mticker.FixedLocator([25, 30, 35, 40, 45, 50])
        gl.xlocator = mticker.FixedLocator([-55, -65, -70, -75, -80, -85, -90, -95, -100, -105, -110, -115, -120, -125])
        gl.xlabels_bottom = False
        gl.xlabel_style = {'rotation': 45}
        
        #Setup corner logo
        im = plt.imread('/home/scrump/containers/website/python/model_files/scrump-logo.png')
        ax1 = ax.inset_axes([-0.001, 0.01, 0.15, 0.17]) # GRAPH SPECIFIC
        ax1.axis('off')
        ax1.imshow(im, aspect='equal')
        
        #Set map extent and allow matplotlib to adjust extent to maintain aspect ratio
        ax.set_extent([lonW, lonE, latS, latN], crs=projPC) # GRAPH SPECIFIC
        ax.set_aspect('auto')
        
        #Add map background features
        ax.coastlines(resolution=res, color='black') # GRAPH SPECIFIC
        ax.add_feature(cfeature.STATES, linewidth=0.3, edgecolor='brown', zorder=3) # GRAPH SPECIFIC
        ax.add_feature(cfeature.LAND, zorder=1) # GRAPH SPECIFIC
        ax.add_feature(cfeature.LAKES, zorder=1) # GRAPH SPECIFIC
        ax.add_feature(cfeature.OCEAN, zorder=1) # GRAPH SPECIFIC
        ax.add_feature(cfeature.BORDERS, linewidth=0.5, edgecolor='blue', zorder=3) # GRAPH SPECIFIC
        
        #Add scatter plot of city 'dots'
        plt.scatter(x=USA_cities.X, y=USA_cities.Y,
                    color="dodgerblue",
                    s=1,
                    alpha=0.5,
                    transform=projPC,
                    zorder=5)
        
        #Add the label for each city dot
        texts=[]
        #COMMENT ON LINUX csfont = {'fontname': 'Comic Sans MS'}
        for index in range(len(USA_cities.index)):
            
            #Get coordinates of each city in the csv file
            x=USA_cities.iloc[index].X
            y=USA_cities.iloc[index].Y
            
            data_point_text = ""

            if sample_points == True:
                #Find the nearest grid point to the city dot and fetch its value
                abslat = np.abs(ds.isel(step=step).latitude-y) # GRAPH SPECIFIC
                abslon = np.abs(ds.isel(step=step).longitude-(360+x)) # GRAPH SPECIFIC

                absolute_difference = abslat + abslon # GRAPH SPECIFIC

                loc = np.where(absolute_difference == np.min(absolute_difference)) # GRAPH SPECIFIC
                
                sample_point_value = float(ds.isel(step=step).sel(x=loc[1], y=loc[0])[product][0][0]) # GRAPH SPECIFIC
                sample_point_value = round(sample_point_value,1) # GRAPH SPECIFIC
                data_point_text = "\n" + str(sample_point_value) + " " + data_unit

            #Add the city to the list of labels if its on the map but not too close to the edge
            if lonW+3 < x < lonE-3 and latS+3 < y < latN-3:
                texts.append(plt.text(x=USA_cities.iloc[index].X, y=USA_cities.iloc[index].Y,
                            s=USA_cities.iloc[index].NAME + data_point_text, # GRAPH SPECIFIC,
                            color="black",
                            fontsize=8,
                            #COMMENT ON LINUX **csfont,
                            transform=projPC))
        
        #Adjust the labels so they don't horribly overlap
        #adjust_text(texts, on_basemap=True)

        #ADD MODEL DATA TO MAP DEFINE UPPER AND LOWER BOUNDARY OF VALUE
        p = ax.pcolormesh(
            ds.isel(step=step).longitude, # GRAPH SPECIFIC
            ds.isel(step=step).latitude, # GRAPH SPECIFIC
            ds.isel(step=step)[product], # GRAPH SPECIFIC
            vmin=data_min, # GRAPH SPECIFIC
            vmax=data_max, # GRAPH SPECIFIC
            transform=projPC,
            cmap=cmap,
            zorder=2,
        )
        
        #Define the colorbar and its boundaries. Sets colorbar as segmented instead of continuous
        bounds = list(range(data_min-5,data_max+5,5))
        norm = colors.BoundaryNorm(bounds, cmap.N, extend='both')
        plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),
                    ax=ax,
                    orientation='horizontal',
                    pad=0.01,
                    shrink=0.8,
                    label=data_label) # GRAPH SPECIFIC

        #Set the title of the sublot with model description and time, then add product label
        ax.set_title(
            f"{ds.isel(step=step).model.upper()}: {description}\nLocal Time: {time_local[step].strftime('%Y-%m-%d %H:%M:%S')}",
            loc="left",
        )
        
        #Set description to GRIB name of product
        ax.set_title(data_label, loc="right")
        
        #Ensure tight layout of figure, define the complete path and save it
        fig.tight_layout()
        plt.subplots_adjust(hspace=0,wspace=0)
        final_path = path + product + '_' + state + '_' + str(step) + '.png'
        print('Saving plot to ' + final_path)
        fig.savefig(final_path, edgecolor='black', dpi=120, transparent=True)
        
        #Add the path to the saved image to the list of paths to be saved
        link_list.append('goes/model_data/operational/' + product + '_' + state + '_' + str(step) + '.png')
        
        #Clear the whole figure from memory or risk exploding your computer
        plt.clf() #SUPER DUPER IMPORTANT
    return [state, product, link_list]
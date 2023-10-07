import warnings

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.ticker as ticker
from cartopy import crs as ccrs, feature as cfeature
from scipy.ndimage import gaussian_filter

import numpy as np
import pandas as pd
import re

#  Suppress warnings issued by Cartopy when downloading data files
warnings.filterwarnings('ignore')

import pytz

from adjustText import adjust_text

def extract_number(string):
    import re
    match = re.search(r'\d{12}', string)
    
    if match:
        return int(match.group())
    else:
        return 0

def generateNationalPlot(params):
    #Main projection to view the plot through
    projection = ccrs.LambertConformal(central_longitude=-97.5, central_latitude=40.5)
    #These variables consistent across national maps for now
    projPC = ccrs.PlateCarree()
    res = '50m'
    link_list = []

    state = params['state']

    tz = params['tz']
    lonW = params['lonW']
    lonE = params['lonE']
    latS = params['latS']
    latN = params['latN']
    ds = params['ds']
    sample_points = params['sample_points']
    data_unit = params['data_unit']
    cmap = params['cmap']
    model_name = params['model_name']
    product_name = params['product_name']
    forecast = params['forecast']
    data_min = params['data_min']
    data_max = params['data_max']
    data_label = params['data_label']
    lat_index = params['lat_index']
    lon_index = params['lon_index']
    forecast_range = params['forecast_range']
    gaussian = params['gaussian']
    algorithm = params['algorithm']
    prune = params['prune']
    level_increment = params['level_increment']

    #Standard params
    path = params['path']
    USA_cities = params['city_csv']
    description = params['description']

    #Main loop to go through each forecast hour
    for step in range(ds.step.size):

        try:
            fxx = forecast_range[step]
        except:
            fxx = step
        
        #'GRAPH SPECIFIC' TAG DENOTES SOMETHING UNIQUE TO DIFFERENT GRAPH TYPES. IE RADAR DATA VS TEMPERATURE DATA, DIFFERENT LOCATIONS ETC.
        #Get the local time zone for the graph
        time = ds['valid_time'].isel(step=step).values
        time = pd.Timestamp(time)
        time_utc = time.tz_localize(pytz.UTC) # GRAPH SPECIFIC
        local_tz = pytz.timezone(tz)
        time_local = time_utc.tz_convert(local_tz)
        time_string = time.strftime('%Y%m%d%H%M')

        #Set size of overall figure and define subplot for model data
        fig = plt.figure(figsize=(10, 8)) # GRAPH SPECIFIC
        ax = plt.subplot(1, 1, 1, projection=projection)
        
        #Setup gridlines and properties
        gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--', x_inline=False, y_inline=False, dms=True)
        gl.ylocator = mticker.FixedLocator([25, 30, 35, 40, 45, 50])
        gl.xlocator = mticker.FixedLocator([-65, -70, -75, -80, -85, -90, -95, -100, -105, -110, -115, -120, -125])
        gl.xlabels_bottom = False
        gl.xlabel_style = {'rotation': 45}
        
        #Setup corner logo
        im = plt.imread('/home/scrump/containers/website/python/model_files/scrump-logo.png')
        ax1 = ax.inset_axes([0.01,0.01,0.15,0.15])
        ax1.set_aspect('equal', anchor="SW")
        ax1.axis('off')
        ax1.imshow(im, aspect='equal')
        
        #Set map extent and allow matplotlib to adjust extent to maintain aspect ratio
        ax.set_extent([lonW, lonE, latS, latN], crs=projPC)
        ax.set_aspect('auto')
        
        #Add map background features
        ax.coastlines(resolution=res, linewidth=0.4, color='gray') # GRAPH SPECIFIC
        ax.add_feature(cfeature.STATES, linewidth=0.3, edgecolor='brown', zorder=3) # GRAPH SPECIFIC
        #ax.add_feature(cfeature.LAND) GRAPH SPECIFIC
        #ax.add_feature(cfeature.LAKES) GRAPH SPECIFIC
        #ax.add_feature(cfeature.OCEAN) GRAPH SPECIFIC
        ax.add_feature(cfeature.BORDERS, linewidth=0.4, edgecolor='blue', zorder=3) # GRAPH SPECIFIC
        
        #Add scatter plot of city 'dots'
        plt.scatter(x=USA_cities.X, y=USA_cities.Y,
                    color="dodgerblue",
                    s=1,
                    alpha=0.5,
                    transform=projPC)
        
        #Add the label for each city dot
        texts=[]
        #COMMENT ON LINUX csfont = {'fontname': 'Comic Sans MS'}
        for index in range(len(USA_cities.index)):
            
            #Get coordinates of each city in the csv file
            city_x=USA_cities.iloc[index].X
            city_y=USA_cities.iloc[index].Y
            
            data_point_text = ""

            if sample_points == True:
                #Find the nearest grid point to the city dot and fetch its value
                abslat = np.abs(ds.isel(step=step).latitude-city_y) # GRAPH SPECIFIC
                abslon = np.abs(ds.isel(step=step).longitude-(360+city_x)) # GRAPH SPECIFIC

                absolute_difference = abslat + abslon # GRAPH SPECIFIC

                loc = np.where(absolute_difference == np.min(absolute_difference)) # GRAPH SPECIFIC
                
                sample_point_value = float(ds.isel(step=step, **{lat_index: loc[0][0]}, **{lon_index: loc[1][0]})[forecast]) # GRAPH SPECIFIC
                sample_point_value = round(sample_point_value,1) # GRAPH SPECIFIC
                data_point_text = "\n" + str(sample_point_value) + " " + data_unit
            
            #Add the city to the list of labels if its on the map but not too close to the edge
            if lonW+1 < city_x < lonE-1 and latS+1 < city_y < latN-1:
                texts.append(ax.text(x=city_x, y=city_y,
                            s=USA_cities.iloc[index].NAME + data_point_text, # GRAPH SPECIFIC
                            color="black", # MAY NEED TO CONSIDER CHANGING
                            fontsize=8,
                            #COMMENT ON LINUX **csfont,
                            transform=projPC)) 

        data = ds.isel(step=step)[forecast]

        if gaussian == True:
                data = gaussian_filter(data, sigma=1)

        if prune == True:
            pruner = ticker.MaxNLocator(prune = 'lower')
        else:
            pruner = None

        if algorithm == 'pcolormesh':
            #ADD MODEL DATA TO MAP DEFINE UPPER AND LOWER BOUNDARY OF VALUE
            p = ax.pcolormesh(
                ds.isel(step=step).longitude,
                ds.isel(step=step).latitude,
                ds.isel(step=step)[forecast],   
                vmin=data_min, # GRAPH SPECIFIC
                vmax=data_max, # GRAPH SPECIFIC
                transform=projPC,
                cmap=cmap,
                zorder=2,
            )

        else:

            lons = ds.isel(step=step).longitude.values
            lats = ds.isel(step=step).latitude.values
            if np.ndim(lons) == 1 or np.ndim(lats) == 1:
                lons,lats = np.meshgrid(lons,lats)
            
            points = projection.transform_points(projPC, lons, lats)
            xpts = points[:,:,0].flatten().tolist()
            ypts = points[:,:,1].flatten().tolist()
            crs_pts = list(zip(xpts,ypts))
            fig_pts = ax.transData.transform(crs_pts)
            ax_pts = ax.transAxes.inverted().transform(fig_pts)
            x = ax_pts[:,0].reshape(lats.shape)
            y = ax_pts[:,1].reshape(lats.shape)

            mask = (x>=-0.05) & (x<=1.05) & (y>=-0.05) & (y<=1.05)
            
            lons = np.ma.masked_array(lons, ~mask)
            lats = np.ma.masked_array(lats, ~mask)
            data = np.ma.masked_array(data, ~mask)

            if algorithm == 'contourf':

                p = ax.contourf(
                    lons,
                    lats,
                    data,
                    vmin=data_min, # GRAPH SPECIFIC
                    vmax=data_max, # GRAPH SPECIFIC
                    levels=data_max-data_min,
                    transform=projPC,
                    cmap=cmap,
                    zorder=2,
                    **{'locator': pruner},
                    algorithm='threaded',
                    transform_first=True
                )

            if algorithm == 'contour':

                levels = int(round((np.max(data) - np.min(data))/level_increment))

                p = ax.contour(
                    lons,
                    lats,
                    data,
                    levels=levels,
                    transform=projPC,
                    colors='black',
                    zorder=2,
                    algorithm = 'threaded'
                )
            
                ax.clabel(p)
        
        if not algorithm == 'contour':
            #Define the colorbar and its boundaries. Sets colorbar as segmented instead of continuous
            bounds = list(range(data_min-5,data_max+5,5)) # GRAPH SPECIFIC
            norm = colors.BoundaryNorm(bounds, cmap.N, extend='both')
            plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),
                        ax=ax,
                        orientation='horizontal',
                        pad=0.01,
                        shrink=0.8,
                        label=data_label) # GRAPH SPECIFIC

        #Set the title of the sublot with model description and time, then add product label
        ax.set_title(
            f"{ds.isel(step=step).model.upper()}: {description}\nEastern Time: {time_local.strftime('%Y-%m-%d %H:%M:%S')}",  # GRAPH SPECIFIC
            loc="left",
        )
        
        #Set description to GRIB name of product
        ax.set_title(data_label, loc="right") # GRAPH SPECIFIC
        
        #Ensure tight layout of figure, define the complete path and save it
        fig.tight_layout()
        plt.subplots_adjust(hspace=0,wspace=0)
        final_path = path + model_name + '_' + product_name + '_' + forecast + '_' + state + '_' + time_string + '_' + str(fxx) + '.png'
        print('Saving plot to ' + final_path)
        
        #Adjust the labels so they don't horribly overlap
        #adjust_text(texts) broken :(

        fig.savefig(final_path, edgecolor='black', dpi=120, transparent=True)
        
        #Add the path to the saved image to the list of paths to be saved
        link_list.append('goes/model_data/operational/' + model_name + '_' + product_name + '_' + forecast + '_' + state + '_' + time_string + '_' + str(fxx) + '.png')
        
        #Clear the whole figure from memory or risk exploding your computer
        plt.clf() #SUPER DUPER IMPORTANT

    # Sort the string_array using the custom key function
    link_list = sorted(link_list, key=extract_number)

    return [model_name, product_name, forecast, state, link_list]
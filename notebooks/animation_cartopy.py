import numpy as np
from matplotlib import pyplot as plt, animation
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as feat

# %% Define animation Function

def animate_2D_FOCI_cartopy(folder, data_name, var_name, projection_ani = ccrs.PlateCarree(), **kwargs):
    """

    Function to create animations of 2D FOCI model data.
    --------------------------------------------------------------------------------------------------

    reqirements: matplotlib
                 xarray
                 cartopy
                 numpy
    ---------------------------------------------------------------------------------------------------

    ARGS:
        folder: folder the data is stored in.  dtype: raw-string, for raw strings type r''
        data_name: name of the data.  dtype: raw-string
        var_name: name of the variable you want to plot, eg. sosstsst.  dtype: string
    --------------------------------------------------------------------------------------------------

    **KWARGS WITH DEFAULT:

    levels of the counturf-plot: lev = 20

    Missing value of the FOCI output data: miss = 0

    The colormap of the animation: cmap = 'coolwarm'

    Display the timesteps in the title or not: timestep = True

    Set the frames of your animation.
    The default is to animate all timesteps of the given data: frames_ani = len(dat_set[var_name])

    Set the interval in [ms] between the frames of your animation. This property will be changed within the ani.save()
    command later, where you have to set the frames per seconds of the saved animation: interval_ani = 200

    Title of the animation: title_ani = var_name
    """

    # Unpack kwargs and set defaults
    lev = kwargs.get('lev', 20)
    miss = kwargs.get('miss', 0)
    cmap = kwargs.get('cmap', 'coolwarm')
    timestep = kwargs.get('timestep', True)
    title_ani = kwargs.get('title_ani', var_name)

    # Open Data as dataset
    data_path = folder + '\\' + data_name
    print(data_path)
    dat_set = xr.open_mfdataset(data_path)
    # Set miss to NaN
    dat_set[var_name] = dat_set[var_name].where(dat_set[var_name] != miss)

    # Set up the figure and the axes object for the animation
    if projection_ani == ccrs.PlateCarree():
        fig = plt.figure(figsize=[10, 4])
    else:
        fig = plt.figure(figsize=[8, 4])            #The figsize might need be adjusted for projections different
                                                    # from ccrs.Robinson(), since the figsize is not automatically fitted to the
                                                    # Geoaxes objects

    ax = plt.axes(projection=projection_ani)

    # Plot the first timestep of the data and set up the plot
    cax = ax.contourf(dat_set.nav_lon.values, dat_set.nav_lat.values, dat_set[var_name][0,:,:].values,
                      transform=ccrs.PlateCarree(), levels=lev, cmap = cmap)
    ax.coastlines()
    cb = fig.colorbar(cax)
    cb.set_label(var_name)
    ax.add_feature(feat.LAND, zorder=0,
                   edgecolor='#7f7f7f', facecolor='#B1B2B4')
    try:
        gl = ax.gridlines(draw_labels=True)
        gl.xlabels_top = False
        gl.ylabels_right = False
    except:
        ax.gridlines()



    fig.tight_layout()

    #ax.set_xlabel('Longitudes')
    #ax.set_ylabel('Latitudes')

    # Define animation function which updates the figure for every frame
    def animate(frame):

        ax.collections = []
        ax.contourf(dat_set.nav_lon.values, dat_set.nav_lat.values, dat_set[var_name][frame, :, :].values,
                          transform=ccrs.PlateCarree(), levels=lev, cmap = cmap)
        try:
            gl = ax.gridlines(draw_labels=True)
            gl.xlabels_top = False
            gl.ylabels_right = False
        except:
            ax.gridlines()


        if timestep:
            ax.set_title(title_ani + ' Timestep: %i' % frame)
        else:
            ax.set_title(var_name)

    # Create animation object
    interval_ani = kwargs.get('interval_ani', 200)
    frames_ani = kwargs.get('frames_ani', len(dat_set[var_name]))
    ani = animation.FuncAnimation(
        fig,
        animate,
        interval=interval_ani,
        frames=frames_ani)

    return ani

#%%
ani_carto = animate_2D_FOCI_cartopy(folder = r'C:\Users\user\3D Objects\Ausschnitt Daten', data_name= r'1_FOCI1.10-TM028_5d_20000101_20001231_sosstsst.nc',
                        var_name ='sosstsst', projection_ani =ccrs.PlateCarree())
#%%
ani_carto.save('ani_cartopy.mp4', bitrate=-1)
#%%
ani_carto_ice = animate_2D_FOCI_cartopy(folder = r'C:\Users\user\3D Objects\Ausschnitt Daten', data_name= r'1_FOCI1.10-TM028_5d_20000101_20001231_iicethic.nc',
                        var_name ='iicethic', frames_ani=5, projection_ani =ccrs.PlateCarree())
#%%
ani_carto_ice.save('ani_carto_ice.mp4', bitrate=-1)

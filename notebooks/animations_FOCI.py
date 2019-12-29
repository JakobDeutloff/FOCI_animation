# This File contains two animation routines for FOCI model data.
#
# The function animate_2D_FOCI only plots the data on the FOCI model grid.
# The function animate_2D_FOCI_cartopy also uses cartopy for the
# projection of the data, so that you can choose one.
b
from matplotlib import pyplot as plt, animation
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as feat


def animate_2D_FOCI(folder, data_name, var_name, **kwargs):
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

    Set the interval in [ms] between the frames of your animation: interval_ani = 200

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
    dat_set = xr.open_mfdataset(data_path)

    # Set miss to NaN
    dat_set[var_name] = dat_set[var_name].where(dat_set[var_name] != miss)

    # Set up the figure and the axes object for the animation
    fig, ax = plt.subplots()

    # Plot the first timestep of the data and set up the plot
    ax.set_xlabel('Longitudes')
    ax.set_ylabel('Latitudes')
    cax = ax.contourf(dat_set.nav_lon.values[0, :], dat_set.nav_lat.values[:, 0], dat_set[var_name][0, :, :].values,
                      cmap=cmap, levels=lev)

    cb = fig.colorbar(cax)
    cb.set_label(var_name)
    ax.grid()

    # Define animation function which updates the figure for every frame
    def animate(frame):

        ax.collections = []
        ax.contourf(dat_set.nav_lon.values[0, :], dat_set.nav_lat.values[:, 0], dat_set[var_name][frame, :, :].values,
                    cmap=cmap, levels=lev)

        if timestep:
            ax.set_title(title_ani + ' Timestep: %i' % frame)
        else:
            ax.set_title(title_ani)

    # Create animation object
    frames_ani = kwargs.get('frames_ani', len(dat_set[var_name]))
    interval_ani = kwargs.get('interval_ani', 200)
    ani = animation.FuncAnimation(
        fig,
        animate,
        interval=interval_ani,
        frames=frames_ani)

    return ani


def animate_2D_FOCI_cartopy(folder, data_name, var_name, projection_ani=ccrs.PlateCarree(), **kwargs):
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
        projection_ani: The projection you want the data to be plotted in. dytype: cartopy.crs.PROJECTION()
    --------------------------------------------------------------------------------------------------

    **KWARGS WITH DEFAULT:

    levels of the counturf-plot: lev = 20

    Missing value of the FOCI output data: miss = 0

    The colormap of the animation: cmap = 'coolwarm'

    Display the timesteps in the title or not: timestep = True

    Set the frames of your animation.
    The default is to animate all timesteps of the given data: frames_ani = len(dat_set[var_name])

    Set the interval in [ms] between the frames of your animation: interval_ani = 200

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
        fig = plt.figure(figsize=[8, 4])
        # The figsize might need be adjusted for projections different
        # from ccrs.Robinson(), since the figsize is not automatically fitted to the
        # Geoaxes objects

    ax = plt.axes(projection=projection_ani)

    # Plot the first timestep of the data and set up the plot
    cax = ax.contourf(dat_set.nav_lon.values, dat_set.nav_lat.values, dat_set[var_name][0, :, :].values,
                      transform=ccrs.PlateCarree(), levels=lev, cmap=cmap)
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


    # Define animation function which updates the figure every frame
    def animate(frame):

        ax.collections = []
        ax.contourf(dat_set.nav_lon.values, dat_set.nav_lat.values, dat_set[var_name][frame, :, :].values,
                    transform=ccrs.PlateCarree(), levels=lev, cmap=cmap)
        try:
            gl = ax.gridlines(draw_labels=True)
            gl.xlabels_top = False
            gl.ylabels_right = False
        except:
            ax.gridlines()

        if timestep:
            ax.set_title(title_ani + ' Timestep: %i' % frame)
        else:
            ax.set_title(title_ani)

    # Create animation object
    interval_ani = kwargs.get('interval_ani', 200)
    frames_ani = kwargs.get('frames_ani', len(dat_set[var_name]))
    ani = animation.FuncAnimation(
        fig,
        animate,
        interval=interval_ani,
        frames=frames_ani)

    return ani

import numpy as np
from matplotlib import pyplot as plt, animation
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as feat

# %% File SST from Ausschnitt Daten
folder = r'C:\Users\user\OneDrive\Dokumente\Hiwi\FOCI_animation\data'
data_file = folder + '\\' + r'1_FOCI1.10-TM028_5d_20000101_20001231_sosstsst.nc'
data = xr.open_mfdataset(data_file)
data['sosstsst'] = data.sosstsst.where(data.sosstsst != 0)

sst = data.sosstsst
time = data.time_counter
nav_lat = data.nav_lat
nav_lon = data.nav_lon
lat_min = nav_lat.min()
lat_max = nav_lat.max().values
lon_min = nav_lon.min().values
lon_max = nav_lon.max().values
# %% Single Plot
step = data.sel(time_counter=time[0])
step['sosstsst'] = step.sosstsst.where(step.sosstsst != 0)
fig = plt.figure(figsize=[8, 4])
ax = plt.axes(projection=ccrs.Robinson())
plot = ax.contourf(step.nav_lon.values, step.nav_lat.values, step.sosstsst.values, transform=ccrs.PlateCarree(),
                   levels=20)
ax.coastlines()
cb = plt.colorbar(plot)
ax.add_feature(feat.LAND, zorder=0,
               edgecolor='#7f7f7f', facecolor='#B1B2B4')
ax.gridlines(draw_labels=True)
fig.tight_layout()
plt.show()
# %% Animation simple


fig, ax = plt.subplots()

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')


def animate(frame):
    cax = ax.contourf(nav_lon.values[0, :], nav_lat.values[:, 0], sst[0, :, :].values,
                      cmap='coolwarm', levels=20)
    cb = plt.colorbar(cax)
    cb.set_title('SST')
    ax.set_title('Timestep: %i' % frame)


ani = animation.FuncAnimation(
    fig,
    animate,
    frames=5,
)

plt.draw()
plt.show()
ani.save('./animation.mp4', bitrate=-1, fps=1)


# %% Define animation Function

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
            ax.set_title(var_name)

    # Create animation object
    frames_ani = kwargs.get('frames_ani', len(dat_set[var_name]))
    interval_ani = kwargs.get('interval_ani', 200)
    ani = animation.FuncAnimation(
        fig,
        animate,
        interval=interval_ani,
        frames=frames_ani)

    return ani



# %%
ani_FOCI.save('ani_func.mp4', bitrate=-1)
# %% File for SST from task AOD
folder = 'C:\\Users\\user\\OneDrive\\Dokumente\\Hiwi\\FOCI_animation\\data\\'
data_file_course = folder + '1_FOCI1.1-TM005_5d_185902_grid_T_sosstsst.nc'
data_course = xr.open_mfdataset(data_file_course, combine='by_coords')
time = data_course.time_counter
array_course = data_course.mean('time_counter')
fig = plt.figure()
ax = plt.axes(projection=ccrs.PlateCarree())
array_course.sosstsst.plot.contourf(ax=ax, transform=ccrs.AlbersEqualArea())
ax.set_global()
ax.coastlines()
fig.tight_layout()
plt.show()

#%%
import animations_FOCI

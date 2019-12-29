from animation_FOCI import *


# %%
folder = 'C:\\Users\\user\\OneDrive\\Dokumente\\Hiwi\\FOCI_animation\\data\\'
data_file = folder + '1_FOCI1.10-TM028_5d_20000101_20001231_sosstsst.nc'
data = xr.open_mfdataset(data_file)
time = data.time_counter
#%%
step_1 = data.sosstsst.sel(time_counter = time[0])
step_1.plot
plt.show()

#!/usr/bin/env python


#---------------------------------------------------------------------
########testing xarray and glob for time series plots with variables 1990-2020 nc files. #################################
#--------------------------------------------------------------------


import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import glob
from datetime import datetime
from statsmodels.tsa.seasonal import seasonal_decompose

xr.set_options(keep_attrs=True)

path_in = r"/work/malla/ww_leipzig/data_1990_2020/output_1990_2020"
files = glob.glob(path_in + "/*.nc")


import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
URL = 'https://esgf.nccs.nasa.gov/thredds/dodsC/CMIP6.CMIP.NASA-GISS.GISS-E2-1-G.historical.r1i1p1f1.SImon.sithick.gn.sithick.20180827.aggregation.1'
nc = xr.open_dataset(URL)
lat = nc['lat'][:]
lon = nc['lon'][:]
data = nc['sithick'][:, :,:]
data_mean = data.mean(['lat', 'lon']) # wonderful tool to calculate spatial mean by using dim variable names
time = nc['time'].to_dataframe().index
pdtime = time.to_datetimeindex() #convert this index to a pandas.DatetimeIndex
plt.plot(pdtime, data_mean, color='red', linewidth=2, label='SeaIce Thickness')
plt.title('Time Series of Global Mean SeaIce Thickness from CMIP.NASA-GISS.GISS-E2-1-G.historical.r2i1p1f1.SImon.sithick')
plt.xlabel('time (year)')
plt.ylabel('SeaIce Thickness (M)')
plt.show()

# lat= ds['latitude'][:]
# lon= ds['longitude'][:]
# data = ds['pre'][:,:,:]
# data_mean = data.mean(['latitude','longitude'])
# time= ds['time'].to_dataframe().index
# #pdtime= time.to_datetimeindex()
# data_t= data_mean.mean(['time'])
# #plt.plot(time, data_mean, color='red')
# plt.plot(time, data_t, color='green')
# plt.show()

#ds.mean(dim=('latitude','longitude').plot()
#plt.show()

#pre.mean(dim=('latitude', 'longitude')).plot()
#pre.reduce(np.nanpercentile, pre.pre, q=0.75).mean(dim=('latitude', 'longitude')).plot()
#pre.groupby('time.season').mean(dim=('latitude','longitude')).plot(size=6)
#'for seasonal graph'''''''
#plt.show()
#print(pre)

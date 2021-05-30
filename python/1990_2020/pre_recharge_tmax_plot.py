#!/usr/bin/env python

# --------------------------------------------------
#  File:        plot_data.py
#
#  Created:     Mi 12-05-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------

#---------------------------------------------------------------------
########plotting Recharge Precepitation and Tmax> 30 (Heat days)with xarray and for time series plots with variables 1951-2020 nc files. #################################
#--------------------------------------------------------------------



import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import matplotlib.patches as patches

path_in = ("/work/malla/ww_leipzig/data_1990_2020/output_1990_2020")

Heatdays = xr.open_dataset(path_in+"/tmax_ug_1951_2020_gtc30_ysum.nc")
Pre= xr.open_dataset(path_in+"/pre_ug_1951_2020_ysum.nc")
Recharge= xr.open_dataset(path_in+"/recharge_ug_1951_2020_ysum.nc")
#print(Heatdays)

H= Heatdays.tmax.max(dim=["latitude", "longitude"]).to_dataframe()
P=Pre.pre.median(dim=["latitude", "longitude"]).to_dataframe()
R=Recharge.recharge.median(dim=["lat", "lon"]).to_dataframe()

H["Year"]=H.index.year
P["Year"]=P.index.year
R["Year"]=R.index.year
R.reset_index(drop=True, inplace=True)
P.reset_index(drop=True, inplace=True)
H.reset_index(drop=True, inplace=True)

R.set_index(["Year"],inplace=True)
H.set_index(['Year'],inplace=True)
P.set_index(['Year'],inplace=True) 
#print(R)#
data = pd.concat([H,P,R ],axis=1)
#data["year"]= data.index
data.reset_index(level=['Year'], inplace=True) ###making index to another coloumn
#print(data)
data.index.name=None

#print(data) #####created pandas dataframe with all tmax, pre and recharge data##
#data.to_csv("Tmax_pre_rech_yearly")


##########numpy arraay type plotting#########
fig, (ax1, ax2, ax3) = plt.subplots(3,1, sharex=True, figsize=(6,8))
ax1.plot(data.Year, data.pre, label="Precipitation", color="blue")
ax2.plot(data.Year, data.tmax, label="Tmax>30", color="red")
ax3.plot(data.Year, data.recharge, label="Recharge", color="green")
#sns.scatterplot(data.pre, data.recharge,hue= data.Year, size= data.tmax)

#data.plot(subplots=True, figsize=(8,12))
ax1.legend()
ax1.set_title("Yearly sums")
#ax1.set_xlabel()

#######adding text on the plot############################################




##########################################################################
ax2.legend()
ax2.set_ylabel("Number of Days")
ax1.set_ylabel("mm")

ax3.legend()
ax3.set_ylabel("mm")

###ticks###
ax1.xaxis.set_major_locator(MultipleLocator(10))
ax1.xaxis.set_major_formatter('{x:.0f}')

ax1.xaxis.set_minor_locator(AutoMinorLocator(10))
ax3.tick_params(which='minor', length=5)
ax3.tick_params(which='major', length=9)
ax2.tick_params(which='major', length=9)
ax2.tick_params(which='major', length=9)
ax1.tick_params(which='major', length=9)
ax1.tick_params(which='major', length=9)
#plt.show()

#plt.savefig("scatter_pre_recharge_tmax_neu")
plt.savefig("pre_recharge_tmaxspmax_ts_1950_2020.png")

#plt.savefig("/public/malla/Pre_Rech_tmax1.png")

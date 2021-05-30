#!/usr/bin/env python

# --------------------------------------------------
#  File:        plot_data.py
#
#  Created:     Mi 05-05-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------

#---------------------------------------------------------------------
######## xarray for time series plots daily data with years as for variables 1990-2020 nc files. #################################
#--------------------------------------------------------------------



import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

path_in = ("/work/malla/ww_leipzig/data_1990_2020/output_1990_2020/tmax_ug_1951-2020.nc")

nc = xr.open_dataset(path_in)
nc1= nc.tmax.mean(dim=['latitude', 'longitude'])

dataframe= nc1.groupby(nc["time"].dt.dayofyear).min().to_dataframe(name="min")
dataframe["max"]= nc1.groupby(nc["time"].dt.dayofyear).max().values
dataframe["median"]= nc1.groupby(nc["time"].dt.dayofyear).median().values
dataframe["q25"]= nc1.groupby(nc["time"].dt.dayofyear).quantile(.25).values
dataframe["q75"]= nc1.groupby(nc["time"].dt.dayofyear).quantile(.75).values

for year, yearda in nc1.groupby(nc1["time"].dt.year):
    dataframe[year] = pd.Series(index=yearda["time"].dt.dayofyear, data=yearda.values)
print(dataframe.index)
#dataframe.index.name = None
dataframe.reset_index(level=['dayofyear'], inplace=True) ###making index to another coloumn
dataframe.columns = dataframe.columns.map(str)
#print(dataframe)
#dataframe.plot()
#for col in dataframe.columns:
#    print(col)

min1= dataframe["min"]
year2018= dataframe["2018"]
max1=dataframe["max"]
median=dataframe["median"]
q25=dataframe["q25"]
q75= dataframe["q75"]
day=dataframe["dayofyear"]


# dataframe.plot( y=['max','q75','median' ,'q25','min'])
# #plt.plot(dataframe[0:10])
# plt.xlabel('Days in the Year')
# plt.ylabel('Tmax data of years 1951-2020')
# plt.show()
#plt.savefig("/public/malla/plot_variables_timeseries/daily_tmaxofyears.png")

fig, ax= plt.subplots(figsize=(10,6))

ax.set_title("Daily tmax data for years 1951 to 2020")
ax.set_ylabel("Degree Celcius")
ax.set_xlabel("Days in a Year")

ax.plot(day, year2018, color= "#060606", label="2018",ls = '-',linewidth = '1')
ax.plot(day, max1, color= "#A91E20", label="max", linewidth='0.5')
ax.plot(day, q75, color= "#DF4949", label="q75",linewidth='0.5')

ax.plot(day, median, color="#EAF10B", label="median",linewidth='1')

ax.plot(day, q25, color= "#9CD363", label="q25",linewidth='0.5')
ax.plot(day, min1, color= "#50C512", label="min",linewidth='0.5')


ax.fill_between(day, year2018, median,
                where=(year2018> median),
                interpolate=True, alpha=0.25,color="red")

ax.fill_between(day, year2018, median,
                where=(year2018<= median),
                interpolate=True, alpha=0.25, color="blue")
ax.legend()
#plt.show()
fig.savefig("Tmaxdailyforallyears.png")

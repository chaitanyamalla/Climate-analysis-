#!/usr/bin/env python

# --------------------------------------------------
#  File:        plot_data.py
#
#  Created:     Mi 12-05-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------

#---------------------------------------------------------------------
######## 2018 with other Yearly time series plots for different variables 1951-2020 nc files. #################################
#--------------------------------------------------------------------



import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

path_in = ("/work/malla/ww_leipzig/data_1990_2020/output_1990_2020/tmax_ug_1951-2020.nc")

nc = xr.open_dataset(path_in)
nc1= nc.tmax.mean(dim=['latitude', 'longitude'])

dataframe= nc1.groupby(nc["time"].dt.month).sum().to_dataframe("sum")
# dataframe["maximum"]= nc1.groupby(nc["time"].dt.month).max().values
# dataframe["median"]= nc1.groupby(nc["time"].dt.month).median().values
# dataframe["q25"]= nc1.groupby(nc["time"].dt.month).quantile(.25).values
# dataframe["q75"]= nc1.groupby(nc["time"].dt.month).quantile(.75).values

for year, yearda in nc1.groupby(nc1["time"].dt.year):
    monthly_mean = yearda.groupby(yearda["time"].dt.month).mean()
    dataframe[year] = pd.Series(index=monthly_mean["month"], data=monthly_mean.values)
print(dataframe.index)
dataframe= dataframe.drop('sum', axis=1)
#dataframe.index.name = None
dataframe['median']= dataframe.median(axis=1)
dataframe['minimum'] = dataframe.min(axis=1)
dataframe['maximum'] = dataframe.max(axis=1)
dataframe.reset_index(level=['month'], inplace=True) ###making index to another coloumn
dataframe.columns = dataframe.columns.map(str)
#print(dataframe)
#dataframe.plot()
#for col in dataframe.columns:
#    print(col)
dataframe.reset_index(drop=True, inplace=True)
#dataframe.index_name= None
print(dataframe)
min1= dataframe["minimum"]
year2018= dataframe["2018"]
year2017= dataframe["2017"]
year2019= dataframe["2019"]
max1=dataframe["maximum"]
median=dataframe["median"]
# q25=dataframe["q25"]
# q75= dataframe["q75"]
month=dataframe["month"]


# dataframe.plot( y=['max','q75','median' ,'q25','min'])
# #plt.plot(dataframe[0:10])
# plt.xlabel('Days in the Year')
# plt.ylabel('Tmax data of years 1951-2020')
# plt.show()
#plt.savefig("/public/malla/plot_variables_timeseries/daily_tmaxofyears.png")

fig, ax= plt.subplots(figsize=(10,6))

ax.set_title("Tmax monthly mean for years 1951 to 2020")
ax.set_ylabel("degree celcius")
ax.set_xlabel("Months in a Year")
#ax.plot(month, year2019, color= "#0E925C", label="2019",ls = '--',linewidth = '2')
ax.plot(month, year2018, color= "#060606",marker='o', label="2018",ls = '-',linewidth = '2')
#ax.plot(month, year2017, color= "#8A8B76", label="2017",ls = '-.',linewidth = '2')

#ax.plot(month, max1, color= "#A91E20", label="max", linewidth='0.5')
#ax.plot(month, q75, color= "#DF4949", label="q75",linewidth='0.5')

ax.plot(month, median, color="#EAF10B", label="median",linewidth='1')

#ax.plot(month, q25, color= "#9CD363", label="q25",linewidth='0.5')
#ax.plot(month, min1, color= "#50C512", label="min",linewidth='0.5')

ax = dataframe.T.boxplot()


#ax.fill_between(month, year2018, median,
#                where=(year2018> median),
#                interpolate=True, alpha=0.25,color="blue", label="Above median")

#ax.fill_between(month, year2018, median,
#                where=(year2018<= median),
#                interpolate=True, alpha=0.25, color="red", label="Below median")

ax.legend()
plt.show()
#fig.savefig("Tmax_2018 withallyears.png")

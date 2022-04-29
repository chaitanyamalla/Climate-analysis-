#! /usr/bin/env python
# -*- coding: utf-8 -*-
import ufz
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from cftime import num2date, date2num
import pandas as pd
import glob 

from datetime import datetime


def read_data(VAR,filename):
    tmp_data=ufz.readnetcdf(filename, var=VAR)
    return tmp_data



def read_dates(filename):
    timeunit  = ufz.readnetcdf(filename, var='time', attributes=True)['units']
    timecalendar = ufz.readnetcdf(filename, var='time', attributes=True)['calendar']
    times     = ufz.readnetcdf(filename, var='time')
    datetimes=num2date(times,units=timeunit,calendar=timecalendar,only_use_cftime_datetimes=False)
    datetimes=[datetime.date(d) for d in datetimes]


    return datetimes

def calc_metrics(data,dates,round_dig=4):
    tmp_q25, tmp_median, tmp_q75     =np.percentile(data,[25,50,75],axis=(1,2)) # calculates the median
    tmp_max              =np.max(data,axis=(1,2))
    tmp_min              =np.min(data,axis=(1,2))
    tmp_mean             =np.mean(data,axis=(1,2))
    tmp_data=np.column_stack([tmp_min, tmp_q25, tmp_median, tmp_mean, tmp_q75, tmp_max])
    if round_dig != False:
            tmp_data=tmp_data.round(decimals=round_dig)
    tmp_merge=pd.DataFrame(index=dates,data=tmp_data,columns=["min","p25","median","mean","p75","max"])
    return tmp_merge
if __name__ == '__main__':
    inpath="/data/hydmet/WIS_D/ww_leipzig/data_climproj" 
    #outpath="/work/malla/ww_leipzig/data_out/4_indicators/"
    outpath="/work/malla/ww_leipzig/data_out/aET_pet/"
    year_start=1971
    year_end=2098
    timeperiod="{:}_{:}".format(year_start,year_end)
    
    #vars=["SMI"]
    #vars=["pre","tmin","tmax","tavg","aET","recharge","pet"]
    #vars=["tavg","aET","recharge","pet"]
    #vars=["pre", "tmax","tavg"]
    vars=["aET", "pet"]
    met1=["met_001","met_025","met_035","met_057","met_070","met_083","met_086"]
    met2=["met_011","met_015","met_032","met_038","met_044","met_080","met_088"]
    rcp=["rcp26","rcp85"]
    for r in rcp:
        if r == "rcp26":
            mets=met2
        elif r =="rcp85":
            mets=met1

        # for var in vars:
        #     for met in mets:

        #         print("processing: {:}-{:}-{:}".format(var,met,r))
        #         if var == "aET":
        #             filename="{:}/{:}/{:}_daily_ug.nc".format(inpath,met,var)
        #         elif var == "pet":
        #             filename="{:}/{:}/{:}_ug.nc".format(inpath,met,var)
        #         #filename="{:}/{:}/{:}_SM_0_30cm_daily_ug.nc".format(inpath,met,var)
        #         data=read_data(VAR=var,filename=filename)
        #         dates=read_dates(filename=filename)
        #         data_metrics=calc_metrics(data,dates)
        #         #write file: 
        #         #print(data)
        #         data_metrics1=data_metrics.round(1)
        #         data_metrics1.to_csv("{:}daily_spatial_stats/{:}_{:}_ug_{:}_{:}.csv".format(outpath,var,timeperiod,met,r),sep=",",index_label="Datum")


out="/work/malla/ww_leipzig/data_out/aET_pet/rolling30/"
for file in glob.glob("/work/malla/ww_leipzig/data_out/aET_pet/daily_spatial_stats/*.csv"):
    data=pd.read_csv(file)
    df= data.set_index("Datum").rolling(30).sum().round(1)
    outfile=file.replace(".csv","_rolling.csv")
    outfile=outfile.replace("daily_spatial_stats", "rolling30")
    print(outfile)
    df.to_csv(outfile)

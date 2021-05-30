#! /usr/bin/env python
# -*- coding: utf-8 -*-




# --------------------------------------------------
#  File:        plot_data.py
#
#  Created:     Mi 12-05-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce Timeseries from 1971-2099 for individual indicators for HICAM climate ensemble evaluation
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------

import os
import ufz
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import xarray as xr

#def read_data(filename):
#    ls=[]
#    for met_id in range(met_start, met_end+1):
#        tmp_data= xr.open_dataset("{:}/met_{:}/{:}".format(inpath,str(met_id).zfill(3),filename))
#        ls.append(tmp_data)
#    return ls



#if __name__ == '__main__':


inpath="/work/malla/ww_leipzig/data_1971_2099/input_1971_2099/"
met_start=1
met_end=88

for met in range(met_start, met_end+1):
    met_id="met"+'_'+ str(met).zfill(3)

    
    pre_file="/pre_ug.nc"
    data_pre = xr.open_dataset(inpath + met_id + pre_file)
    y_sum = data_pre.groupby('time.year').sum('time')

    fig, p= plt.subplots(figsize=(7,4))
    p =  y_sum.pre.mean(dim=['latitude','longitude']).plot()
    plt.title(met_id)
    plt.ylabel("Yearly Precipitation sum in [mm/yr]")
    plt.ylim(300,1000)
    plt.show()
    #plt.savefig("/work/malla/ww_leipzig/data_1971_2099/output_1971_2099/pre/"+ met_id+".png")
    #plt.clf()
    
#        y_sum= data.groupby('time.year').sum('time')



for met in range(met_start, met_end+1):
    met_id="met"+'_'+ str(met).zfill(3)

    
    tmax_file="/tmax_ug.nc"
    data_tmax = xr.open_dataset(inpath + met_id + tmax_file)
    tmax30days = data_tmax.where(data_tmax > 30).groupby('time.year').count(dim='time')
    fig, tmax_plot = plt.subplots(figsize = (7,4))
    tmax_plot=  tmax30days.tmax.max(dim=['latitude','longitude']).plot()
    plt.title(met_id)
    plt.ylabel("Number of days > 30°C")
    plt.ylim(0,100)
    plt.show()
    #plt.savefig("/work/malla/ww_leipzig/data_1971_2099/output_1971_2099/tmax/"+ met_id+".png")

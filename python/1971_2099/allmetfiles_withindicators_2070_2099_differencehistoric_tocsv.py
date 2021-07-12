#! /usr/bin/env python
# -*- coding: utf-8 -*-




# --------------------------------------------------
#  File:        allmetfiles_withindicators_tocsv.py
#
#  Created:     Di 29-04-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce csv of all METfiles with different indicators to see the far oulier performing METfiles . For time period 2070-2099 minus 1971-2000 (difference)
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


inpath="/work/malla/ww_leipzig/output_periods/"
outpath="/work/malla/ww_leipzig/data_1971_2099/"
met_start=1
met_end=88

pre = []   #yearly
pre_s = []  #summer
pre_w = []   #winter
recharge = []
tmax25 = []
tmax30 = []



def readfile(filename, timeperiod, indicator):
    filename =filename.format(timeperiod)
    data = xr.open_dataset(inpath + met_id + filename)
    if indicator == "pre":
        data_mean = data.pre.mean(dim=["lat", "lon"]).to_dataframe(met_id)
    elif indicator == "recharge":
        data_mean = data.recharge.mean(dim=["lat", "lon"]).to_dataframe(met_id)
    elif indicator == "tmax":
        data_mean = data.tmax.mean(dim=["lat", "lon"]).to_dataframe(met_id)
        
    return data_mean

for met in range(met_start, met_end+1):
    met_id="met"+'_'+ str(met).zfill(3)

    timeperiod = "2070_2099"


    



    pre_y_file1 = readfile("/pre_ug_yearly_{:}_ysum_timmean_fldpctl_difference.nc", timeperiod, "pre")
    pre_w_file1 = readfile("/pre_ug_winter_{:}_ysum_timmean_fldpctl_difference.nc", timeperiod, "pre")
    pre_s_file1 = readfile("/pre_ug_summer_{:}_ysum_timmean_fldpctl_difference.nc", timeperiod, "pre")
    rech_file1 = readfile("/recharge_ug_{:}_ysum_timmean_fldpctl_difference.nc", timeperiod, "recharge")
    tmax25_file1 = readfile("/tmax_ug_gtc25_{:}_ysum_timmean_fldpctl_difference.nc", timeperiod, "tmax")
    tmax30_file1 = readfile("/tmax_ug_gtc30_{:}_ysum_timmean_fldpctl_difference.nc", timeperiod, "tmax")

    pre.append(pre_y_file1.copy())
    pre_w.append(pre_w_file1.copy())
    pre_s.append(pre_s_file1.copy())
    recharge.append(rech_file1.copy())
    tmax25.append(tmax25_file1.copy())
    tmax30.append(tmax30_file1.copy())





def processing(data1, name):
    r = pd.concat(data1, axis=1)
    r["files"]= name
    r = r.set_index("files")
    r = (r.T)
    return r


pre = processing(pre, "pre_yearly")
pre_s = processing(pre_s, "pre_summer")
pre_w = processing(pre_w, "pre_winter")
recharge = processing(recharge, "recharge")
tmax25 = processing(tmax25, "Tmax25[n]")
tmax30 = processing(tmax30, "Tmax30[n]")

data = pre.join([ pre_s, pre_w, recharge, tmax25, tmax30])  #tmax25, pre_s, pre_w,
#print(data)


#######--------------rcps-----------------#########
meta = pd.read_csv("/work/malla/ww_leipzig/MET_list.txt",sep=" ")
met_ids = np.sort(pd.unique(meta["met_id"]))
gcms = np.sort(pd.unique(meta["gcm"]))
rcms = np.sort(pd.unique(meta["inst.rcm"]))
rcps = pd.Series(meta["rcp"], dtype="category")
hms= ['mHM']
rcp = pd.DataFrame(rcps, columns = ['rcp'])
##########----------------------------------------####

data = data.reset_index()
data = data.join(rcp)
print(data)

data.to_csv(outpath + "AllMETfiles_2070_2099_difference_rcp_indicators.csv")

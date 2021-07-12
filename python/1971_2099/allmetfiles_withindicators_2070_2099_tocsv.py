#! /usr/bin/env python
# -*- coding: utf-8 -*-




# --------------------------------------------------
#  File:        allmetfiles_withindicators_tocsv.py
#
#  Created:     Mi 23-04-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce csv of all METfiles with different indicators to see the far oulier performing METfiles 
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


    pre_y_file1 = readfile("/pre_ug_yearly_{:}_ysum_timmean_fldpctl.nc", timeperiod, "pre")
    # pre_y ="/pre_ug_yearly_{:}_ysum_timmean_fldpctl.nc".format(timeperiod)
    # pre_y_file = xr.open_dataset(inpath + met_id + pre_y)
    # pre_y_file1 = pre_y_file.pre.mean(dim=["lat", "lon"]).to_dataframe(met_id)
    
    
    pre_w_file1 = readfile("/pre_ug_halfyear_{:}_ysum_timmean_fldpctl.nc", timeperiod, "pre")
    # pre_w_name ="/pre_ug_halfyear_{:}_ysum_timmean_fldpctl.nc".format(timeperiod)
    # pre_w_file = xr.open_dataset(inpath + met_id + pre_w_name)
    # pre_w_file1 = pre_w_file.pre.mean(dim=["lat", "lon"]).to_dataframe(met_id).astype(float)
    #pre_w_file1= pre_w_file1.apply(pd.to_numeric)
    #pre_w_file1 = pd.to_numeric(pre_w_file1, errors='ignore').to_dataframe(met_id)
    #print(pre_w_file1)

    pre_s_file1 = readfile("/pre_ug_summer_{:}_ysum_timmean_fldpctl.nc", timeperiod, "pre")
    # pre_s_name ="/pre_ug_summer_{:}_ysum_timmean_fldpctl.nc".format(timeperiod)
    # pre_s_file = xr.open_dataset(inpath + met_id + pre_s_name)
    # pre_s_file1 = pre_s_file.pre.mean(dim=["lat", "lon"]).to_dataframe(met_id).astype(float)
 
    


    rech_file1 = readfile("/recharge_ug_{:}_ysum_timmean_fldpctl.nc", timeperiod, "recharge")
    # filename_rech ="/recharge_ug_{:}_ysum_timmean_fldpctl.nc".format(timeperiod)
    # rech_file = xr.open_dataset(inpath + met_id + filename_rech)
    # rech_file1 = rech_file.recharge.mean(dim=["lat", "lon"]).to_dataframe(met_id)

    tmax25_file1 = readfile("/tmax_ug_gtc25_{:}_ysum_timmean_fldpctl.nc", timeperiod, "tmax")
    # filename_tmax25 ="/tmax_ug_gtc25_{:}_ysum_timmean_fldpctl.nc".format(timeperiod)
    # tmax25_file = xr.open_dataset(inpath + met_id + filename_tmax25)
    # tmax25_file1 = tmax25_file.tmax.max(dim=["lat", "lon"]).to_dataframe(met_id)

    tmax30_file1 = readfile("/tmax_ug_gtc30_{:}_ysum_timmean_fldpctl.nc", timeperiod, "tmax")
    # filename_tmax30 ="/tmax_ug_gtc30_{:}_ysum_timmean_fldpctl.nc".format(timeperiod)
    # tmax30_file = xr.open_dataset(inpath + met_id + filename_tmax30)
    # tmax30_file1 = tmax30_file.tmax.max(dim=["lat", "lon"]).to_dataframe(met_id)
    
   
    pre.append(pre_y_file1.copy())
    pre_w.append(pre_w_file1.copy())
    pre_s.append(pre_s_file1.copy())
    recharge.append(rech_file1.copy())
    tmax25.append(tmax25_file1.copy())
    tmax30.append(tmax30_file1.copy())




def processing(data1, name):
    pre = pd.concat(data1, axis=1)
    pre["files"]= name
    pre= pre.set_index("files")
    pre = (pre.T)
    return pre



pre = processing(pre, "pre_yearly")
# pre = pd.concat(pre, axis=1)
# pre["files"]= "pre_yearly"
# pre= pre.set_index("files")
# pre = (pre.T)
pre_s = processing(pre_s, "pre_summer")
# pre_s = pd.concat(pre_s, axis=1)
# pre_s["files"]= "pre_summer"
# pre_s= pre_s.set_index("files")
# pre_s = (pre_s.T)
pre_w = processing(pre_w, "pre_winter")
# pre_w = pd.concat(pre_w, axis=1)
# pre_w["files"]= "pre_winter"
# pre_w= pre_w.set_index("files")
# pre_w = (pre_w.T)

recharge = processing(recharge, "recharge")
# recharge = pd.concat(recharge, axis=1)
# recharge["files"]= "recharge"
# recharge= recharge.set_index("files")
# recharge = (recharge.T)
tmax25 = processing(tmax25, "Tmax25[n]")
# tmax25 = pd.concat(tmax25, axis=1)
# tmax25["files"]= "tmax25(n)"
# tmax25= tmax25.set_index("files")
# tmax25 = (tmax25.T)

tmax30 = processing(tmax30, "Tmax30[n]")
# tmax30 = pd.concat(tmax30, axis=1)
# tmax30["files"]= "tmax30(n)"
# tmax30= tmax30.set_index("files")
# tmax30 = (tmax30.T)

data = pre.join([ pre_s, pre_w, recharge, tmax25, tmax30])  #pre_s, pre_w,
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

#data.to_csv(outpath + "AllMETfiles_2070_2099_rcp_indicators.csv")

 
  


#! /usr/bin/env python
# -*- coding: utf-8 -*-




# --------------------------------------------------
#  File:        plot_data.py
#
#  Created:     Do 22-05-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce Timeseries from 1971-2099 for all 88 MET files   with single indicator for HICAM climate ensemble evaluation
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



outpath= "/work/malla/ww_leipzig/data_1971_2099/output_1971_2099/"
inpath="/work/malla/ww_leipzig/data_1971_2099/input_1971_2099/"
met_start=1
met_end=88

###################--------------pre----------------###############################
# data = []
# for met in range(met_start, met_end+1):
#     met_id="met"+'_'+ str(met).zfill(3)

#     pre_file = "/pre_ug.nc"
#     data_pre = xr.open_dataset(inpath + met_id + pre_file)
#     pre_ysum = data_pre.pre.groupby('time.year').sum('time').mean(dim= ['latitude','longitude']).to_dataframe(met_id)
#     data.append(pre_ysum)
   
# data = pd.concat(data, axis=1)
# data.reset_index(level=['year'], inplace=True) ###making index to another coloumn

# data.to_csv(outpath +'88_METfiles_csv/'+'pre_allMETfiles.csv', index=False)    

# print(data)


###################--------------recharge----------------###############################
# data = []
# for met in range(met_start, met_end+1):
#     met_id="met"+'_'+ str(met).zfill(3)

#     recharge_file = "/recharge_ug.nc"
#     data_re = xr.open_dataset(inpath + met_id + recharge_file)
#     re_ysum = data_re.recharge.groupby('time.year').sum('time').mean(dim= ['lat','lon']).to_dataframe(met_id)
#     data.append(re_ysum)
   
# data = pd.concat(data, axis=1)
# data.reset_index(level=['year'], inplace=True) ###making index to another coloumn

# data.to_csv(outpath +'88_METfiles_csv/'+'recharge_allMETfiles.csv', index=False)    

#print(data)
####################------------tmax > 30 -----------------##########################
data = []
for met in range(met_start, met_end+1):
    met_id="met"+'_'+ str(met).zfill(3)

    
    tmax_file="/tmax_ug.nc"
    data_tmax = xr.open_dataset(inpath + met_id + tmax_file)
    tmax30_ycount = data_tmax.where(data_tmax > 30).tmax.groupby('time.year').count(dim='time').max(dim= ['latitude','longitude']).to_dataframe(met_id)
    data.append(tmax30_ycount)
   
data = pd.concat(data, axis=1)
data.reset_index(level=['year'], inplace=True) ###making index to another coloumn

data.to_csv(outpath +'88_METfiles_csv/'+'Tmax30days_allMETfiles.csv', index=False)    

print(data)
    
####################-----------  pet & aET ----------------################################

# data = []
# for met in range(met_start, met_end+1):
#     met_id="met"+'_'+ str(met).zfill(3)

    
#     #pet_file ="/pet_ug.nc"
#     aET_file ="/aET_ug.nc"
#     #data_pet = xr.open_dataset(inpath + met_id + pet_file)
#     data_aET = xr.open_dataset(inpath + met_id + aET_file)
    
#     #pet_ysum = data_pet.pet.groupby('time.year').sum('time').mean(dim= ['latitude','longitude']).to_dataframe(met_id)
#     aET_ysum = data_aET.aET.groupby('time.year').sum('time').mean(dim= ['lat','lon']).to_dataframe(met_id)
    
#     #aET_ysum = data_aET.groupby('time.year').sum('time')
#     #pet_ysum['empty']= np.nan
#     #data.append(pet_ysum)
#     data.append(aET_ysum)
   
# data = pd.concat(data, axis=1)
# #data.drop(columns= 'empty')
# data.reset_index(level=['year'], inplace=True) ###making index to another coloumn
# #data.to_csv(outpath +'88_METfiles_csv/'+'pet_allMETfiles.csv', index=False)
# data.to_csv(outpath +'88_METfiles_csv/'+'aET_allMETfiles.csv', index=False)    
#     #fig, ax = plt.subplots(figsize=(7,4))
#     #ax = pet_ysum.pet.median(dim=['lat
# print(data)

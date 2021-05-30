#! /usr/bin/env python
# -*- coding: utf-8 -*-




# --------------------------------------------------
#  File:        plot_data.py
#
#  Created:     Do 20-05-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce Timeseries from 1971-2099 for pET and aET indicators for HICAM climate ensemble evaluation
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




inpath="/work/malla/ww_leipzig/data_1971_2099/input_1971_2099/"
met_start=1
met_end=88



####################-----------  aET and pet ----------------################################


for met in range(met_start, met_end+1):
    met_id="met"+'_'+ str(met).zfill(3)

    
    pet_file ="/pet_ug.nc"
    aET_file ="/aET_ug.nc"
    data_pet = xr.open_dataset(inpath + met_id + pet_file)
    data_aET = xr.open_dataset(inpath + met_id + aET_file)
    
    pet_ysum = data_pet.groupby('time.year').sum('time')
    aET_ysum = data_aET.groupby('time.year').sum('time')

    #fig, ax = plt.subplots(figsize=(7,4))
    ax = pet_ysum.pet.median(dim=['latitude','longitude']).plot(label='pet')
    ax = aET_ysum.aET.median(dim=['lat', 'lon']).plot(label='aET')
    
    plt.title(met_id)
    plt.legend(loc=2)
    plt.ylabel("Evapotranspiration [mm/yr]")
    plt.ylim(400,1100)
    #plt.show()

    plt.savefig("/work/malla/ww_leipzig/data_1971_2099/output_1971_2099/pet_aET/"+ met_id+"_aET_pet_ysum_1971_2099_ts"+".png")
    plt.clf()

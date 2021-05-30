#! /usr/bin/env python
# -*- coding: utf-8 -*-




# --------------------------------------------------
#  File:        plot_data.py
#
#  Created:     Mi 14-04-2021
#  Author:      Friedrich Boeing
#  
# --------------------------------------------------
#
#  Description: script to produce scatterplots for HICAM climate ensemble evaluation
#
#  Modified by: Chaitanya Malla
#  Modified date: 21.04.2021
#
# --------------------------------------------------

import os
import ufz
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

def read_data(VAR,filename):
    '''inputs VAR: pre or tavg, filename: .nc files of pre and tavg in specific location.
    outputs: list of pre and tavg values for scatter plot'''
    ls=[]
    for met_id in range(met_start,met_end+1):
        tmp_data=ufz.readnetcdf("{:}/met_{:}/{:}".format(inpath,str(met_id).zfill(3),filename), var=VAR)
        #print(tmp_data.shape) is to look the cell shape. Output is [1,1,1]
        tmp_data=float(tmp_data[0][0])
        ls.append(tmp_data)
        #print(len(ls),ls)
    return ls

# def create_dir(folder):
#     if not os.path.exists(folder):
#         os.mkdir(folder)


if __name__ == '__main__':



    #  meta                    = pd.read_csv("/data/hicam/data/processed/meteo/germany/climproj/euro-cordex/88realizations_mhm/88_main_LUT.txt",sep=" ")
    meta                    = pd.read_csv("MET_list.txt",sep=" ")
    met_ids                 = np.sort(pd.unique(meta["met_id"]))
    # if len(met_ids) < 88: # if not all simulations are in the directory
    #    met_ids                 = np.sort(os.listdir("/work/malla/ww_leipzig/output_periods/"))
    # met_ids                 = ["met_001", "met_002"]

     # list of names of the rcps climate models
    gcms                    = np.sort(pd.unique(meta["gcm"]))
    # list of names of the regional climate models
    rcms            = np.sort(pd.unique(meta["inst.rcm"]))
    # list of names of the hydrological models
    hms                     = ['mHM']
    # list of names of the rcps
    # rcps                    = ['rcp2p6', 'rcp6p0', 'rcp8p5']
    # rcps                    = np.sort(pd.unique(meta["rcp"]))
    rcps                      = pd.Series(meta["rcp"], dtype="category")

    

    inpath="/work/malla/ww_leipzig/output_periods/"
    met_start=1
    met_end=88

    #timeperiod="2021_2050"


    listA = np.array(['1971', '2021', '2036', '2070'], dtype=np.str)
    listB = np.array(['2000', '2050', '2065', '2099'], dtype=np.str)

    # q = list(map(lambda x, y: x+ '_' +y, listA, listB))
    # print (q)
    # for item in zip(listA, listB)

    save_results_to = '/public/malla/plot_pre_tmax/'
    #create_dir(save_results_to)
    
    for i in range(4):
        timeperiod= listA[i]+'_'+ listB[i]
        #print(timeperiod)
        #     timeperiod = item#     print (timeperiod)
    
                       
    
        #filename="pre_ug_halfyear_{:}_ysum_timmean_fldpctl.nc".format(timeperiod)
        #data_winterprecip=read_data(VAR="pre",filename=filename)
        # when fldpctl not computed with cdo
        #data_winterprecip=[[np.median(i)] for i in data_winterprecip]

        #filename="pre_ug_summer_{:}_ysum_timmean_fldpctl.nc".format(timeperiod)
        #data_summerprecip=read_data(VAR="pre",filename=filename)

        filename="pre_ug_yearly_{:}_ysum_timmean_fldpctl.nc".format(timeperiod)
        data_yearlyprecip=read_data(VAR="pre",filename=filename) 

        filename="tmax_ug_gtc25_{:}_ysum_timmean_fldpctl.nc".format(timeperiod)
        data_summerdays=read_data(VAR="tmax",filename=filename)
        # when fldpctl not computed with cdo
        #data_summerdays=[[np.median(i)] for i in data_summerdays]

        #filename="winterpre_summerdays_{:}.png".format(timeperiod)

       

        sns.scatterplot(data_summerdays, data_yearlyprecip, hue= rcps, palette= ["C2", "C0", "k"])
        # plt.scatter(data_summerdays,data_winterprecip,c= rcps)
        plt.xlabel("number of days with tmax > 25°C")
        plt.ylabel("yearly precipitation in mm")
        plt.title(timeperiod)
        plt.xlim(30, 125)
        plt.ylim(550, 950)
        #plt.show()
        # pdList = [data_winterprecip, data_summerdays, rcps]  # List of your dataframes
        # new_df = pd.concat(pdList)
        # sns.scatterplot(data_summerdays, data_winterprecip, hue= rcps)

        #plt.show()

        plt.savefig(save_results_to + timeperiod + '_yearlypre_tmax25' + '.png')
        plt.clf()
     

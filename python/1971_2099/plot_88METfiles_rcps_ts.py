#! /usr/bin/env python
# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        gif_maker.py
#
#  Created:     Mi 14-05-2021
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: ploting single graph from the 88 MET data for each indicator with RCPS included. 
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import matplotlib.patches as patches


inpath= "/work/malla/ww_leipzig/data_1971_2099/output_1971_2099/88_METfiles_csv/"


#indicator = "pre"
indicator = "pre"

#---------------------------------------------------
d = pd.read_csv(inpath+ indicator +"_allMETfiles.csv")

d= d.set_index('year')

# d.reset_index(level=['year'], inplace=True) ###making index to another coloumn
# print(d)
data = d.T
data= data.reset_index( inplace=False) ###adding index numbers
#print(data)

meta = pd.read_csv("/work/malla/ww_leipzig/MET_list.txt",sep=" ")
met_ids = np.sort(pd.unique(meta["met_id"]))
gcms = np.sort(pd.unique(meta["gcm"]))
rcms = np.sort(pd.unique(meta["inst.rcm"]))
rcps = pd.Series(meta["rcp"], dtype="category")
hms= ['mHM']

dat2 = pd.DataFrame(rcps, columns = ['rcp'])


data1 = data.join(dat2)
#print(data1)
data_rcp26 = data1.loc[data1['rcp'] == 'rcp26']
data_rcp45 = data1.loc[data1['rcp'] == 'rcp45']
data_rcp85 = data1.loc[data1['rcp'] == 'rcp85']

#print(data_rcp85.set_index('index').T)
df_rcp26 = data_rcp26.set_index('index').T
df_rcp26 = df_rcp26[:-1]
df_rcp45 = data_rcp45.set_index('index').T
df_rcp45 = df_rcp45[:-1]
df_rcp85 = data_rcp85.set_index('index').T
df_rcp85 = df_rcp85[:-1]
print(type(df_rcp26))

##---------------------df_rcp26-----------##


df_rcp26_q75 = df_rcp26.quantile(q=0.75, axis=1,numeric_only=False).astype(float)
df_rcp26_median = df_rcp26.median(axis=1).astype(float)
df_rcp26_q25 = df_rcp26.quantile(q=0.25, axis=1, numeric_only=False).astype(float)
year_rcp26 = df_rcp26.index.astype(float)



##--------------------df_rcp45------------##

df_rcp45_q75 = df_rcp45.quantile(q=0.75, axis=1, numeric_only=False).astype(float)
df_rcp45_median = df_rcp45.median(axis=1).astype(float)
df_rcp45_q25 = df_rcp45.quantile(q=0.25, axis=1, numeric_only=False).astype(float)
year_rcp45 = df_rcp45.index.astype(float)

##-------------------df_rcp85------------##

df_rcp85_q75 = df_rcp85.quantile(q=0.75, axis=1, numeric_only=False).astype(float)
df_rcp85_median = df_rcp85.median(axis=1).astype(float)
df_rcp85_q25 = df_rcp85.quantile(q=0.25, axis=1, numeric_only=False).astype(float)
year_rcp85 = df_rcp85.index.astype(float)

# df_rcp85_q75= pd.to_numeric(df_rcp85_q75, errors='coerce').fillna(0, downcast='infer')
# df_rcp85_median= pd.to_numeric(df_rcp85_median, errors='coerce').fillna(0, downcast='infer')
# df_rcp85_q25= pd.to_numeric(df_rcp85_q25, errors='coerce').fillna(0, downcast='infer')
# year_rcp85 = pd.to_numeric(year_rcp85, errors='coerce').fillna(0, downcast='infer')
#-----------------------------------------#



fig, (ax1, ax2, ax3)= plt.subplots(3,1,figsize=(10,10))

#ax.set_title(indicator+" yearly sum analysis on Models with RCP 26")
ax1.set_ylabel(indicator+' in [mm/yr]')
ax1.set_title("rcp26")
ax1.plot(year_rcp26, df_rcp26_q75, color= "#F9480B", label=" q75",linewidth='1')
ax1.plot(year_rcp26, df_rcp26_median, color= "#761675", label=" median",linewidth='1')
ax1.plot(year_rcp26, df_rcp26_q25, color= "#095636", label=" q25",linewidth='1')
ax1.set_ylim(450, 900)

# ax1.text(.5,.9,'centered title',
#         horizontalalignment='center',
#         transform=ax1.transAxes)

ax1.fill_between(year_rcp26, df_rcp26_q75, df_rcp26_q25,interpolate=True, alpha=0.25,color="green", label="IQR")
ax1.legend()

ax2.set_ylabel(indicator+' in [mm/yr]')
ax2.set_title("rcp45")
ax2.plot(year_rcp45, df_rcp45_q75, color= "#F9480B", label=" q75",linewidth='1')
ax2.plot(year_rcp45, df_rcp45_median, color= "#761675", label=" median",linewidth='1')
ax2.plot(year_rcp45, df_rcp45_q25, color= "#095636", label=" q25",linewidth='1')
ax2.set_ylim(450, 900)
ax2.fill_between(year_rcp45, df_rcp45_q75, df_rcp45_q25,
                 interpolate=True, alpha=0.25,color="skyblue", label="IQR")
ax2.legend()

ax3.set_ylabel(indicator+' in [mm/yr]')
ax3.set_title("rcp85")
ax3.plot(year_rcp85, df_rcp85_q75, color= "#F9480B", label=" q75",linewidth='1')
ax3.plot(year_rcp85, df_rcp85_median, color="#761675", label=" median",linewidth='1')
ax3.plot(year_rcp85, df_rcp85_q25, color= "#095636", label=" q25",linewidth='1')
ax3.set_ylim(450, 900)
ax3.fill_between(year_rcp85, df_rcp85_q75, df_rcp85_q25,
                 interpolate=True, alpha=0.25,color="orange", label="IQR")

ax3.legend()



plt.show()
#fig.savefig(inpath+"pre_ysum_allMETfiles_rcps_ts.png")

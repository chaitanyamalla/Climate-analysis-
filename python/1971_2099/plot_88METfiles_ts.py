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
#  Description: ploting single graph from the 88 MET data for each indicator. 
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


indicator = "pre"

#---------------------------------------------------
data = pd.read_csv(inpath+ indicator +"_allMETfiles.csv")

min1 = data.min(axis=1)

median = data.median(axis=1)

year = data.year
max1 = data.drop(columns='year').max(axis=1)
q25 = data.quantile(q=0.25, axis=1)
q75 = data.quantile(q=0.75, axis=1)
q90 = data.quantile(q=0.90, axis=1)


#print(max1)
fig, ax= plt.subplots(figsize=(10,6))

ax.set_title(indicator+" yearly sum analysis on the 88 Models")
ax.set_ylabel(indicator+' in [mm/yr]')

ax.plot(year, max1, color= "red", label="max", linewidth='0.5')
ax.plot(year, q90, color= "#0BF389", label="q90",linewidth='1')
ax.plot(year, q75, color= "#F9480B", label="q75",linewidth='1.5')
ax.plot(year, median, color="#761675", label="median",ls = '--',linewidth='1.5')
ax.plot(year, q25, color= "#095636", label="q25",linewidth='1.5')
ax.plot(year, min1, color= "#50C512", label="min",linewidth='1')


ax.fill_between(year, q75, q25,
                interpolate=True, alpha=0.5,color="gold", label="IQR")
#ax.fill_between(year, q25, median,
#                interpolate=True, alpha=0.5,color="#C2F30B", label="below median")


###ticks####
ax.xaxis.set_major_locator(MultipleLocator(10))
#ax.xaxis.set_major_formatter('{x:.0f}')

ax.xaxis.set_minor_locator(AutoMinorLocator(10))
ax.tick_params(which='minor', length=5)
ax.tick_params(which='major', length=9)
#ax.set_xlim(xmin=1971, xmax=2099)
plt.xticks(rotation=70)



ax.legend()
plt.show()
#fig.savefig(inpath+"pre_ysum_allMETfiles_ts.png")

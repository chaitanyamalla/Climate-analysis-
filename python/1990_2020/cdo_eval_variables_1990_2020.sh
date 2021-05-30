#!/bin/sh

###### creating cdo files in folder <<output 1990-2020>> with 6 variables that will be used for timeseries graphs ##############

set -x
set -e

path_int="/work/malla/ww_leipzig/data_1990_2020/data_obs/"
path_out="/work/malla/ww_leipzig/data_1990_2020/output_1990_2020/"


ystart=1990
yend=2020

########precipitation data cutting types###########
cdo yearsum ${path_int}pre_ug_${ystart}-${yend}.nc ${path_out}pre_ug_${ystart}_${yend}_ysum.nc

cdo -yearsum -selseason,ndjfma ${path_int}pre_ug_${ystart}-${yend}.nc ${path_out}pre_ug_${ystart}_${yend}_winterpre_ysum.nc

cdo -yearsum -selseason,mjjaso ${path_int}pre_ug_${ystart}-${yend}.nc ${path_out}pre_ug_${ystart}_${yend}_summerpre_ysum.nc

########tmax data cutting types##################
cdo -yearsum -gtc,25 ${path_int}tmax_ug_${ystart}-${yend}.nc ${path_out}tmax_ug_${ystart}_${yend}_gtc25_ysum.nc

cdo -yearsum -gtc,30 ${path_int}tmax_ug_${ystart}-${yend}.nc ${path_out}tmax_ug_${ystart}_${yend}_gtc30_ysum.nc

########recharge data cutting types############

cdo -yearsum ${path_int}recharge_ug_${ystart}-${yend}.nc ${path_out}recharge_ug_${ystart}_${yend}_ysum.nc



done 

#!/bin/sh

set -x
set -e



path_int="/work/malla/ww_leipzig/input/"
#path_int="/data/hydmet/WIS_D/ww_leipzig/data/"
path_out="/work/malla/ww_leipzig/singlefileoutput/"


met_START=1
met_END=1

cd $path_int

for t in $(seq -f "%03g" $met_START $met_END); do
    met="met_${t}/"
    echo "$met"


    cd $met

    
    cdo -graph,device="png" pre_ug.nc ${path_out}series_test


done

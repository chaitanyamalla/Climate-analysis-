#!/bin/sh

#####  creating all the differnce between history files and future files suitable to WW_leipzig with indicators into output_periods directory############

path_out="/work/malla/ww_leipzig/output_periods/"

met_START=1
met_END=88

cd $path_out

for t in $(seq -f "%03g" $met_START $met_END); do
    met="met_${t}/"
    echo "$met"

    cd $met

    PERIOD_start=("2021" "2036" "2070")
    PERIOD_end=("2050" "2065" "2099")
    #p_start=2070
    #p_end=2099
    i=0
    for p_start in "${PERIOD_start[@]}"; do
        p_end="${PERIOD_end[$i]}"
        echo "evaluate period ${p_start} - ${p_end}"
        i=$(($i + 1))

	#cdo sub ${path_out}${met}pre_ug_halfyear_${p_start}_${p_end}_ysum_timmean_fldpctl.nc pre_ug_halfyear_1971_2000_ysum_timmean_fldpctl.nc ${path_out}${met}pre_ug_halfyear_${p_start}_${p_end}_ysum_timmean_fldpctl_difference.nc

	#cdo sub ${path_out}${met}tavg_ug_gtc25_${p_start}_${p_end}_ysum_timmean_fldpctl.nc tavg_ug_gtc25_1971_2000_ysum_timmean_fldpctl.nc ${path_out}${met}tavg_ug_gtc25_${p_start}_${p_end}_ysum_timmean_fldpctl_difference.nc

	#cdo sub ${path_out}${met}recharge_ug_${p_start}_${p_end}_ysum_timmean_fldpctl.nc recharge_ug_1971_2000_ysum_timmean_fldpctl.nc ${path_out}${met}recharge_ug_${p_start}_${p_end}_ysum_timmean_fldpctl_difference.nc

	#cdo sub ${path_out}${met}tmax_ug_gtc25_${p_start}_${p_end}_ysum_timmean_fldpctl.nc tmax_ug_gtc25_1971_2000_ysum_timmean_fldpctl.nc ${path_out}${met}tmax_ug_gtc25_${p_start}_${p_end}_ysum_timmean_fldpctl_difference.nc
	
	#cdo sub ${path_out}${met}pre_ug_yearly_${p_start}_${p_end}_ysum_timmean_fldpctl.nc pre_ug_yearly_1971_2000_ysum_timmean_fldpctl.nc ${path_out}${met}pre_ug_yearly_${p_start}_${p_end}_ysum_timmean_fldpctl_difference.nc

	cdo sub ${path_out}${met}tmax_ug_gtc30_${p_start}_${p_end}_ysum_timmean_fldpctl.nc tmax_ug_gtc30_1971_2000_ysum_timmean_fldpctl.nc ${path_out}${met}tmax_ug_gtc30_${p_start}_${p_end}_ysum_timmean_fldpctl_difference.nc

    done
    cd ..
   

done

# --------------------------------------------------
#  File:        extract_data.sh
#
#  Created:     Mi 17-03-2021
#  Author:      Friedrich Boeing
#
# --------------------------------------------------
#
#  Description: script to prepare climate projection data for Wasserwerke Leipzig
#
#  Modified:
#  # 2021-04-07 changed names untersuchungsgebiet to ug and versorgungsgebiet to vg
# --------------------------------------------------

set -e
set -x

ml purge # removes all activated modules
ml Anaconda3 # loads Anaconda
# activates conda environment including cdo, nco imagemagick etc
source activate /global/apps/klimabuero/conda_py3.9.2/

create_mask="False" # create the masks
proc_ug="True" # process untersuchungsgebiet ug
proc_vg="True" # process versorgungsgebiet vg
manual="False"
interactive="False"
mets=("met_012" "met_023") # example ensemble members to test data exchange
path_in="/data/hicam/data/processed/meteo/germany/climproj/euro-cordex/88realizations_mhm/"
path_out="./output/"
met_vars=("pre" "tavg" "tmin" "tmax" "pet")
# met_vars=("pre")
# met_vars=("tavg" "tmin" "tmax" "pet")
met_START=1
met_END=88
# execute ' python create_mask...py'
# create two masks for
# 1. vg (smaller one for Wasserwerke Leipzig )
#    Shapefile from Patrick Hartung
# 2. Ug for catchment for recharge estimation
#    Shapefile from Herr Mauder

if [[ $create_mask == "True" ]]; then

    ./create_mask.sh


    cdo setgrid,grid_hicam_ghw mask_untersuchungsgebiet.nc mask_ug_grid.nc
    cdo setgrid,grid_hicam_ghw mask_versorgungsgebiet.nc mask_vg_grid.nc

    cdo sellonlatbox,$extent mask_vg_grid.nc mask_vg_sel.nc
    cdo setmissval,-9999. mask_vg_sel.nc  mask_vg_sel_missval.nc
    cdo setctomiss,0  mask_vg_sel_missval.nc mask_vg_sel_missval2.nc
fi

extent=$(sed -n 2p masks/extent_untersuchungsgebiet)
echo $extent
#  -- loop over meteo variables --------------------


cd $path_out

for met in $(seq -f "%03g" $met_START $met_END); do
    met="met_$met"
    echo "$met"
    if [[ ! -d $met ]]; then
        mkdir $met
    fi
    cd $met
cat > execute.sh <<EOF
set -e
set -x

met_vars=("pre" "tavg" "tmin" "tmax" "pet")
for met_var in "\${met_vars[@]}"; do
# cut out Untersuchungsgebiet ug

if [[ $proc_ug == "True" ]]; then
  cdo sellonlatbox,$extent "$path_in/$met/\${met_var}.nc" tmp_\${met_var}_ug.nc
  nccopy -d 9  tmp_\${met_var}_ug.nc  \${met_var}_ug.nc
fi
if [[ $proc_vg == "True" ]]; then
  # cut out Versorgungsgebiet (subset of Untersuchungsgebiet ug) 
  cdo -O merge tmp_\${met_var}_ug.nc ../../masks/mask_versorgungsgebiet_sel_missval2.nc tmp_ug_merge.nc
  cdo_expr="\${met_var}=(mask==0)?-9999:\${met_var}"
  cdo expr,\$cdo_expr tmp_ug_merge.nc tmp_\${met_var}_vg.nc
  nccopy -d 9  tmp_\${met_var}_vg.nc  \${met_var}_vg.nc
  rm tmp*
fi
done
if [[ $proc_ug == "True" ]]; then
  zip ${met}_climate_ug.zip *ug.nc
fi
if [[ $proc_vg == "True" ]]; then
  zip ${met}_climate_vg.zip *vg.nc
fi

EOF
    chmod 774 execute.sh
    ln -fs ../../submit_slurm.sh
    if [[ $interactive == "True" ]]; then
        ./execute.sh
    fi
    # submit job with sbatch
    if [[ $manual == "False" ]]; then
        sbatch submit_slurm.sh
        echo "submit sbatch job!"
    else
        echo "submit sbatch manually!"
    fi
    cd ..
done

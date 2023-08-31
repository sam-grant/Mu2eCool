#!/bin/zsh

# Define the directory containing the files
ntupleDir="../ntuples/v3.06/"  
logDir="../logs/v3.06/"  

for dir in $ntupleDir $logDir; do 
    for i in 0 1 2 3; do 

        suffix=""
        if [ $dir == $ntupleDir ]; then
            suffix=".root"
        elif [ $dir == $logDir ]; then
            suffix=".log"
        fi

        filepath="${dir}g4beamline_Mu2E_1e7events_Absorber${i}_55mm_fromZ1850_parallel" # "$dir/"*Absorber*".root"; do
        filename=$(basename "$filepath")
        prefix="${filename%%_fromZ*}"
        z_value="${filename#*_fromZ}"
        z_value="${z_value%_parallel.root}"

        new_filename="${prefix}_fromZ${z_value}"
        # replace thickness
        # new_filename="${new_filename//30mm/55mm}"
        new_filename="${new_filename//55mm/l55mm_r100mm}"

        new_filepath="${dir}${new_filename}"

        # if [ $dir == $ntupleDir ]; then
        #     new_filepath="${dir}${new_filename}.root"
        # elif [ $dir == $logDir ]; then
        #     new_filepath="${dir}${new_filename}.log"
        # fi

        mv "$filepath$suffix" "$new_filepath$suffix"
        echo "Renamed: $filepath$suffix -> $new_filepath$suffix"
    done
done

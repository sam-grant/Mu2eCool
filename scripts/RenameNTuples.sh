#!/bin/zsh

# Define the directory containing the files
dir="../ntuples/v3.06/"  

# Loop through the files with the pattern
# for filepath in "$dir/"*Absorber*".root"; do
#     filename=$(basename "$filepath")
#     prefix="${filename%%_fromZ*}"
#     z_value="${filename#*_fromZ}"
#     z_value="${z_value%_parallel.root}"

#     new_filename="${prefix}_20mm_fromZ${z_value}_parallel.root"
#     new_filepath="${directory}/${new_filename}"

#     # mv "$filepath" "$new_filepath"
#     echo "Renamed: $filename -> $new_filename"
# done

for i in 0 1 2 3; do 
    filepath="${dir}/g4beamline_Mu2E_1e7events_Absorber${i}_fromZ1850_parallel_noColl03.root" # "$dir/"*Absorber*".root"; do
    filename=$(basename "$filepath")
    prefix="${filename%%_fromZ*}"
    z_value="${filename#*_fromZ}"
    z_value="${z_value%_parallel.root}"

    new_filename="${prefix}_20mm_fromZ${z_value}_parallel_noColl03.root"
    new_filepath="${dir}${new_filename}"

    mv "$filepath" "$new_filepath"
    echo "Renamed: $filepath -> $new_filepath"
done

# Samuel Grant 2023

input=$1
output=$2
beamFile=$3
absorber=$4
thickness=$5
innerRadius=$6
options=${@:7}

echo "Running: g4bl ${input} histoFile=${output}.root Beam_File=${beamFile} Absorber=${absorber} THICKNESS=${thickness} INNER_RADIUS=${innerRadius} ${options} | tee ${output}.log" 
g4bl ${input} histoFile=${output}.root Beam_File=${beamFile} Absorber=${absorber} THICKNESS=${thickness} INNER_RADIUS=${innerRadius} $options | tee ${output}.log

# echo "Running: g4bl ${input} histoFile=${output}.root Beam_File=${beamFile} $options | tee ${output}.log" 
# g4bl ${input} histoFile=${output}.root Beam_File=${beamFile} $options | tee ${output}.log
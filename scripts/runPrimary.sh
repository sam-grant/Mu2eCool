# Samuel Grant 2023

input=$1
output=$2
firstEvent=$3
numEvents=$4
options=${@:5}

echo "Running: g4bl ${input} histoFile=${output}.root First_Event=${firstEvent} Num_Events=${numEvents} $options | tee ${output}.log" 
g4bl ${input} histoFile=${output} First_Event=${firstEvent} Num_Events=${numEvents} $options | tee ${output}.log
# Samuel Grant 2023

INPUT=$1
NEVENTS=$2
PARTICLE=$3
THICKNESS=$4
MOMENTUM=$5

OUTPUT="g4beamline_Cooling_${NEVENTS}events_${PARTICLE}_${THICKNESS}mm_${MOMENTUM}MeV"
echo "Running: g4bl ${INPUT} NEVENTS=$NEVENTS PARTICLE=$PARTICLE THICKNESS=$THICKNESS MOMENTUM=$MOMENTUM histoFile=${OUTPUT}.root | tee ${OUTPUT}.log" 
g4bl ${INPUT} NEVENTS=${NEVENTS} PARTICLE=${PARTICLE} THICKNESS=${THICKNESS} MOMENTUM=${MOMENTUM} histoFile=${OUTPUT}.root | tee ${OUTPUT}.log

CURRENT_PATH=`pwd` 

cp ${CURRENT_PATH}/${OUTPUT}.root /Users/sgrant/mu2e/Mu2eCool/ntuples/v3.06/CoolingScan/${OUTPUT}.root
cp ${CURRENT_PATH}/${OUTPUT}.log /Users/sgrant/mu2e/Mu2eCool/logs/v3.06/CoolingScan/${OUTPUT}.log

echo "---> Written /Users/sgrant/mu2e/Mu2eCool/ntuples/v3.06/CoolingScan/${OUTPUT}.root"
echo "---> Written /Users/sgrant/mu2e/Mu2eCool/logs/v3.06/CoolingScan/${OUTPUT}.log"
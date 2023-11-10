# Samuel Grant 2023

version="v3.06"
ZNtuple="Z1850" 

echo "---> Sourcing G4beamline setup"
source setup-g4bl-${version}.sh

# Grab the inputs 
input=$1 
nCores=$2
nFiles=$3
totEvents=$4
absorber=$5
thickness=$6
innerRadius=$7
options=${@:8} # Extra options if desired, allows multiple  

echo "Input: $input"
echo "nCores: $nCores"
echo "nFiles: $nFiles"
echo "totEvents: $totEvents"
echo "Version: $version"
echo "Absorber: $absorber"
echo "Thickness: $thickness"
echo "Options: $options"

absorberName=""
if [[ $absorber == 0 ]]; then
  # Don't have a good way of handling this case at the moment 
  absorberName="NoAbsorber"
elif [[ $absorber == 1 ]]; then
  absorberName="PSRing"
elif [[ $absorber == 2 ]]; then
  absorberName="PSRingWedge"
else
  echo "ERROR: absorber not defined"
  exit 0
fi

# Still not clear how to handle 
# foutFileName="g4beamline_${input}_${totEvents}events_${absorberName}_l${thickness}mm_r${innerRadius}mm_from${ZNtuple}"
foutFileName="g4beamline_${input}_${totEvents}events_${absorberName}_l${thickness}mm_r${innerRadius}mm_from${ZNtuple}_noColl_noPbar"

echo "Output format: $foutFileName"

# Prompt the user to check if the options are okay
read -p "Please check these inputs carefully. Proceed? [Y/n]: " choice
if [[ $choice != [Y]* ]]; then
  echo "Aborting. Execution cancelled by user."
  exit 0
fi

# Clear old files
echo "---> Clearing old files"
rm -f g4beamline.*.root 
rm -f g4beamline.*.log

echo "---> Starting..."

# File 0 to N-1
for ((file = 0; file < nFiles; file++)); do 

  # echo "---> File number ${file}" 

  beamFile=""

  if [ $nFiles -gt 1 ]; then
    beamFile="/Users/sgrant/mu2e/Mu2eCool/beamFiles/v3.06/g4beamline_Mu2E_NoAbsorber_${totEvents}events_${ZNtuple}_bm_${file}.txt"
  else
    beamFile="/Users/sgrant/mu2e/Mu2eCool/beamFiles/v3.06/g4beamline_Mu2E_NoAbsorber_${totEvents}events_${ZNtuple}_bm.txt" 
  fi

  if [ -f $beamFile ]; then
    echo "${input}.in g4beamline.${file} ${beamFile} ${absorber} ${thickness} ${innerRadius} ${options}" 
    # echo "${input}_${absorber}.in g4beamline.${file} ${beamFile} ${options}" # "READ_Beam_File=3" "Make_ZNtuple=0" 
  else
    echo "ERROR: $beamFile does not exist!"
    break
  fi

done | xargs -P $nCores -I {} bash -c ". runBeamFile.sh {}"

sleep 1 

rootFile="${foutFileName}.root"
echo "---> Hadding to ${rootFile}"
hadd -f ${rootFile} g4beamline.*.root 
cp ${rootFile} ../ntuples/${version}

sleep 1 

# Setup combined log file
logFile="${foutFileName}.log"

if [ -f $logFile ]; then
  rm -f $logFile && touch $logFile
else
  touch $logFile
fi

# Append all job log files to main
cat `ls g4beamline.*.log | sort -V` >> $logFile
cp $logFile ../logs/${version}

echo "---> Done. Written files to:"
echo "../ntuples/${version}/${rootFile}"
echo "../logs/${version}/${logFile}"
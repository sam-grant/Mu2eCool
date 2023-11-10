# Samuel Grant 2023

version="v3.06"

echo "---> Sourcing G4beamline setup"
source setup-g4bl-${version}.sh

# Grab the inputs 
input=$1 
nCores=$2
nJobs=$3
totEvents=$4
options=${@:5} # Allows multiple options

foutFileName="g4beamline_${input}_${totEvents}events" # _fromZ1800_parallel"

echo "Input: $input"
echo "nCores: $nCores"
echo "nJobs: $nJobs"
echo "Total Events: $totEvents"
echo "Version: $version"
echo "Options: $options"
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

# Per job parameters
firstEvent=1 # 5000001 # 000001 # 8900001 # 1
totEventsTmp=$(echo "$totEvents" | bc) # Needed to handle sci notation, e.g. 1e4
nEventsPerJob=$(( (totEventsTmp + nJobs - 1) / nJobs )) # Use ceil division

echo "---> Target total events: $totEvents"
echo "---> Number of jobs: $nJobs"
echo "---> Number of events per job: $nEventsPerJob"
echo "---> Starting..."

# Job 1 to N, start from 1 otherwise you have to set nJobs n-1 and it messes everything up
for ((job = 1; job <= nJobs; job++)); do 

  echo "---> Job number ${job}; firstEvent=${firstEvent}"

  echo "${input}.in" "g4beamline.${job}" $firstEvent $nEventsPerJob $options

  # Increment the first event number
  ((firstEvent+=$nEventsPerJob))

done | xargs -P $nCores -I {} bash -c ". runPrimary.sh {}"

sleep 1 

rootFile="${foutFileName}.root"
echo "---> Hadding to ${rootFile}"
hadd -f ${rootFile} g4beamline.*.root 
cp ${rootFile} ../ntuples/${version}

sleep 1 

# Setup combined log file
logFile="${foutFileName}.log"
# Append all job log files to main
cat `ls g4beamline.*.log | sort -V` >> $logFile
cp $logFile ../logs/${version}

echo "---> Done. Written files to:"
echo "../ntuples/${version}/${rootFile}"
echo "../logs/${version}/${logFile}"
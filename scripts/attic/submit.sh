input=$1 
nCores=$2
nJobs=$3
totEvents=$4
options=${@:5}  

echo "---> Sourcing G4beamline setup"
source setup-g4bl-${version}.sh

# Clear old files
echo "---> Clearing old files"
rm -f g4beamline.*.root 
rm -f g4beamline.*.log

# Per job parameters
firstEvent=1
totEventsTmp=$(echo "$totEvents" | bc) # Needed to handle sci notation, e.g. 1e4
nEventsPerJob=$(( (totEventsTmp + nJobs - 1) / nJobs )) # Use ceil division

echo "---> Target total events: $totEvents"
echo "---> Number of jobs: $nJobs"
echo "---> Number of events per job: $nEventsPerJob"
echo "---> Starting..."

for ((job = 1; job <= nJobs; job++)); do 

  echo "---> Job number ${job}; firstEvent=${firstEvent}"

  # echo ${input}"_"${ene}"MeV.in" "g4beamline."${job}
  echo "${input}.in" "g4beamline.${job}" $firstEvent $nEventsPerJob $options
  # echo "Mu2E.in" "g4beamline."${job}

  # Increment the first event number (serves as random seed)
  ((firstEvent+=$nEventsPerJob))

done | xargs -P $nCores -I {} bash -c ". run.sh {}"

sleep 1 

foutFileName="g4beamline_${input}_${totEvents}events"

rootFile="${foutFileName}.root"
echo "---> Hadding to ${rootFile}"
hadd -f ${rootFile} g4beamline.*.root 
cp ${rootFile} ../ntuples/${version}

sleep 1 

# Setup main log file
logFile="${foutFileName}.log"
# Append all job log files to main
cat `ls g4beamline.*.log | sort -V` >> $logFile
cp $logFile ../logs/${version}

echo "---> Done. Written files to:"
echo "../ntuples/${version}/${rootFile}"
echo "../logs/${version}/${logFile}"
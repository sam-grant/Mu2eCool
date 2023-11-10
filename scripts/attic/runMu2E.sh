# Tmp script to run with/wout Be target in Mu2E.in for v3.08 and v3.09

# input=$1 
# nCores=$2
# nJobs=$3
# nEvents=$4 
# version=$5  

cd ../run-3.06
. submit.sh Mu2E 3 100 10e4 v3.06
. submit.sh Mu2E_withBeTarget 3 100 10e4 v3.06
cd ../run-3.08
. submit.sh Mu2E 3 100 10e4 v3.08
. submit.sh Mu2E_withBeTarget 3 100 10e4 v3.08
cd ../scripts
# Samuel Grant 2023
# Cooling scan

NCORES=12
INPUT="Cooling.in"

NEVENTS=10000 # per step
THICKNESS_=(1 5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100) # mm
MOMENTUM_=(60 70 80 90 110 120 130 140 150 175 200 225 250 275 300) # MeV
PARTICLE_=("pi-" "mu-") # particles

for PARTICLE in "${PARTICLE_[@]}"; do
	for THICKNESS in "${THICKNESS_[@]}"; do
		for MOMENTUM in "${MOMENTUM_[@]}"; do
			echo $INPUT $NEVENTS $PARTICLE $THICKNESS $MOMENTUM
			# break 3 # Break out of all three nested loops
		done
	done
done | xargs -P $NCORES -I {} bash -c ". runCooling.sh {}"

echo "---> Done <---" 
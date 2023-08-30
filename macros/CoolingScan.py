# Analyse output from cooling scan:
# zero-emittance beam on a Be slab 
# /run-3.06/submitCooling.sh /run-3.06/runCooling.sh /sim/Cooling.in

# External libraries
import pandas as pd
import numpy as np

# Internal libraries
import Utils as ut

g4blVer="v3.06"

# Run scan for a single beam
def RunCoolingScanSingle(nEvents, particle, momentum, thickness_):

	x_ = []
	y_ = []
	xerr_ = []
	yerr_ = []

	# Graph
	graph_ = []

	for thickness in thickness_:

		finName = "../ntuples/"+g4blVer+"/CoolingScan/g4beamline_Cooling_"+str(nEvents)+"events_"+particle+"_"+str(thickness)+"mm_"+str(momentum)+"MeV.root"

		# In/out DataFrames
		df_in = ut.TTreeToDataFrame(finName, "VirtualDetector/DetForward", ut.branchNames)  
		df_out = ut.TTreeToDataFrame(finName, "VirtualDetector/DetBackward", ut.branchNames) 

		if df_out.shape[0] == 0: 
			continue

		# Momentum 
		df_in["P"] = np.sqrt( np.power(df_in["Px"], 2) + np.power(df_in["Py"], 2) + np.power(df_in["Pz"], 2) )
		df_out["P"] = np.sqrt( np.power(df_out["Px"], 2) + np.power(df_out["Py"], 2) + np.power(df_out["Pz"], 2) )

		meanMomIn = np.mean(df_in["P"])
		meanMomOut = np.mean(df_out["P"])

		meanErrMomIn = np.std(df_in["P"]) / len(df_in["P"])
		meanErrMomOut = np.std(df_out["P"]) / len(df_out["P"])

		deltaP = meanMomIn - meanMomOut
		deltaPErr = np.sqrt(pow(meanErrMomIn,2)+pow(meanErrMomOut,2))

		x_.append(thickness)
		y_.append(deltaP)
		xerr_.append(0.00)
		yerr_.append(deltaPErr) # deltaPErr)

	graph_.append( {"x": x_, "y": y_, "xerr": xerr_, "yerr": yerr_} )

	ut.PlotGraph(x_, xerr_, y_, yerr_, title=particle+", "+str(momentum)+" MeV", xlabel="x [mm]", ylabel="$\Delta$ mean momentum [MeV]", fout="../img/"+g4blVer+"/CoolingScan/gr_DeltaPvsX_"+particle+"_"+str(momentum)+".png")

	return

# Run scan for multiple beams
def RunCoolingScanMultiple(nEvents, particle_, momentum_, thickness_):

	for particle in particle_:

		# Container for graphs
		graphs_ = {}

		for momentum in momentum_:

			x_ = []
			y_ = []
			xerr_ = []
			yerr_ = []

			# Graph
			graphs_[momentum] = []

			for thickness in thickness_:

				finName = "../ntuples/"+g4blVer+"/CoolingScan/g4beamline_Cooling_"+str(nEvents)+"events_"+particle+"_"+str(thickness)+"mm_"+str(momentum)+"MeV.root"

				# In/out DataFrames
				df_in = ut.TTreeToDataFrame(finName, "VirtualDetector/DetForward", ut.branchNames)  
				df_out = ut.TTreeToDataFrame(finName, "VirtualDetector/DetBackward", ut.branchNames) 

				# Skip if nothing makes it through the absorber
				if df_in.shape[0] == 0 or df_out.shape[0] == 0: 
					continue

				# Momentum 
				df_in["P"] = np.sqrt( np.power(df_in["Px"], 2) + np.power(df_in["Py"], 2) + np.power(df_in["Pz"], 2) )
				df_out["P"] = np.sqrt( np.power(df_out["Px"], 2) + np.power(df_out["Py"], 2) + np.power(df_out["Pz"], 2) )

				meanMomIn = np.mean(df_in["P"])
				meanMomOut = np.mean(df_out["P"])

				meanErrMomIn = np.std(df_in["P"]) / len(df_in["P"])
				meanErrMomOut = np.std(df_out["P"]) / len(df_out["P"])

				deltaP = meanMomIn - meanMomOut
				deltaPErr = np.sqrt(pow(meanErrMomIn,2)+pow(meanErrMomOut,2))

				x_.append(thickness)
				y_.append(deltaP)
				xerr_.append(0.00)
				yerr_.append(deltaPErr) # deltaPErr)

			graphs_[momentum].append( {"x": x_, "y": y_, "xerr": xerr_, "yerr": yerr_} )

		# print(graphs_)
		title = ""
		if particle=="pi-": title = r"$\pi^{-}$"
		elif particle=="mu-": title = r"$\mu^{-}$"

		ut.PlotGraphOverlay(graphs_, title=ut.GetLatexParticleName(particle), xlabel="x [mm]", ylabel="$\Delta$ momentum [MeV]", fout="../img/"+g4blVer+"/CoolingScan/gr_DeltaPvsX_"+particle+"_MomentumScan.png")

	return

def main():

	nEvents=10000 # per step
	particle_=["pi-", "mu-"]
	thickness_=[1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100] # mm
	momentum_=[75, 100, 125, 150, 175, 200, 225, 250, 275, 300] # MeV

	# ---> pion: 182.31958
	# ---> muon: 82.702324

	# RunCoolingScanSingle(100000, "pi-", 182.31958, [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
	# RunCoolingScanSingle(100000, "mu-", 82.702324, [10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100])

	RunCoolingScanMultiple(nEvents, particle_, momentum_, thickness_) 


if __name__ == "__main__":
    main()
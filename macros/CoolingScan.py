# Analyse output from cooling scan:
# zero-emittance beam on a Be slab 
# /run-3.06/submitCooling.sh /run-3.06/runCooling.sh /sim/Cooling.in

# External libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Internal libraries
import Utils as ut

g4blVer="v3.06"

def PlotGraphWithLine(x, xerr, y, yerr, title=None, xlabel=None, ylabel=None, fout="scatter.png", NDPI=300):

   # Create a scatter plot with error bars using NumPy arrays 

    # Create figure and axes
    fig, ax = plt.subplots()

    # Plot scatter with error bars
    if len(xerr)==0: xerr = [0] * len(x) # Sometimes we only use yerr
    if len(yerr)==0: yerr = [0] * len(y) # Sometimes we only use yerr

    if len(x) != len(y): print("Warning: x has length", len(x),", while y has length", len(y))

    ax.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='o', color='black', markersize=4, ecolor='black', capsize=2, elinewidth=1, linestyle='None')

    # Set title, xlabel, and ylabel
    ax.set_title(title, fontsize=16, pad=10)
    ax.set_xlabel(xlabel, fontsize=14, labelpad=10) 
    ax.set_ylabel(ylabel, fontsize=14, labelpad=10) 

    # Set font size of tick labels on x and y axes
    ax.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
    ax.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size

     # Scientific notation
    if ax.get_xlim()[1] > 9999:
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 9999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax.yaxis.offsetText.set_fontsize(14)

    # Draw line
    ax.axhline(y=50.0, color="grey", linestyle="--", linewidth=1)

    # Ticks every 10 mm
    ax.xaxis.set_major_locator(MultipleLocator(base=10))

    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.clf()
    plt.close()

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

		# deltaP = meanMomIn - meanMomOut
		# deltaPErr = np.sqrt(pow(meanErrMomIn,2)+pow(meanErrMomOut,2))

		x_.append(thickness)
		y_.append(meanMomOut)
		xerr_.append(0.00)
		yerr_.append(meanErrMomOut) # deltaPErr)

	graph_.append( {"x": x_, "y": y_, "xerr": xerr_, "yerr": yerr_} )

	# ut.PlotGraph(x_, xerr_, y_, yerr_, title=ut.GetLatexParticleName(particle)+", "+str(momentum)+" MeV", xlabel="x [mm]", ylabel="Final momentum [MeV]", fout="../img/"+g4blVer+"/CoolingScan/gr_DeltaPvsX_"+particle+"_"+str(momentum)+".png")
	PlotGraphWithLine(x_, xerr_, y_, yerr_, title=ut.GetLatexParticleName(particle)+", "+str(momentum)+" MeV", xlabel="x [mm]", ylabel="Final momentum [MeV]", fout="../img/"+g4blVer+"/CoolingScan/gr_DeltaPvsX_wline_"+particle+"_"+str(momentum)+".png")

	return

# Overlay pions and muons
def RunCoolingScanPionsAndMuonsOverlay(nEvents, particle_, momentum, thickness_):

	# Graphs
	graphs_ = {}

	for particle in particle_:

		x_ = []
		y_ = []
		xerr_ = []
		yerr_ = []

		# Graph
		key = ut.GetLatexParticleName(particle)
		graphs_[key] = []

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

			# deltaP = meanMomIn - meanMomOut
			# deltaPErr = np.sqrt(pow(meanErrMomIn,2)+pow(meanErrMomOut,2))

			x_.append(thickness)
			y_.append(meanMomOut)
			xerr_.append(0.00)
			yerr_.append(meanErrMomOut) # deltaPErr)

		graphs_[key].append( {"x": x_, "y": y_, "xerr": xerr_, "yerr": yerr_} )

	ut.PlotGraphOverlay(graphs_, title=str(momentum)+" MeV", xlabel="x [mm]", ylabel="Final momentum [MeV]", fout="../img/"+g4blVer+"/CoolingScan/gr_DeltaPvsX_ParticleOverlay_"+str(momentum)+"MeV.png")

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
			key = str(momentum)+" MeV"
			graphs_[key] = []

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
				yerr_.append(deltaPErr)

			graphs_[key].append( {"x": x_, "y": y_, "xerr": xerr_, "yerr": yerr_} )

		# print(graphs_)
		title = ""
		if particle=="pi-": title = r"$\pi^{-}$"
		elif particle=="mu-": title = r"$\mu^{-}$"

		ut.PlotGraphOverlay(graphs_, title=ut.GetLatexParticleName(particle), xlabel="x [mm]", ylabel="$\Delta$ momentum [MeV]", fout="../img/"+g4blVer+"/CoolingScan/gr_DeltaPvsX_"+particle+"_MomentumScan.png", offsetLegend=True, useCustomCmap=True)

	return

def main():

	nEvents=10000 # per step
	particle_=["pi-", "mu-"]
	thickness_=[1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100] # mm
	# momentum_=[75, 100, 125, 150, 175, 200, 225, 250, 275, 300] # MeV
	momentum_=[60, 70, 80, 90, 100, 110, 120, 130, 140, 150] 

	# ---> pion: 182.31958
	# ---> muon: 82.702324

	RunCoolingScanSingle(10000, "pi-", 150, thickness_) 
	# RunCoolingScanSingle(10000, "pi-", 100, [1, 5, 10, 15, 25, 20, 35, 30, 35, 40, 45, 50, 55]) # , 60, 70, 80, 90, 100])
	# RunCoolingScanSingle(10000, "mu-", 100, [1, 5, 10, 15, 25, 20, 35, 30, 35, 40, 45, 50, 55]) # [10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100])
	# RunCoolingScanPionsAndMuonsOverlay(10000, ["pi-", "mu-"], 150, [1, 5, 10, 15, 25, 20, 35, 30, 35, 40, 45, 50, 55]) # , 60, 70, 80, 90, 100]) )
	# RunCoolingScanMultiple(nEvents, particle_, momentum_, thickness_) 


if __name__ == "__main__":
    main()
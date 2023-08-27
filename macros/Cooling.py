# See what the beam is doing before and after the absorber 

# Make beam profile plots at a zntuple or VD
# Interested in the relationship between momentum and traverse space, for absorber study

import uproot
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

# Internal libraries
import Utils as ut

from matplotlib.patches import Rectangle

# Globals
g4blVer="v3.06"

particleDict = {
    2212: 'proton',
    211: 'pi+',
    -211: 'pi-',
    -13: 'mu+',
    13: 'mu-'
    # Add more particle entries as needed
    }


def FilterParticles(df, particle): 

	# Filter particles
	if particle in particleDict.values():
		PDGid = list(particleDict.keys())[list(particleDict.values()).index(particle)]
		df = df[df['PDGid'] == PDGid]

	if particle=="no_proton":
		df = df[df['PDGid'] != 2212]

	if particle=="pi-_and_mu-":
		df = df[(df['PDGid'] == -211) | (df['PDGid'] == 13)]

	if particle=="pi+-":
		df = df[(df['PDGid'] == -211) | (df['PDGid'] == 211)]

	if particle=="mu+-":
		df = df[(df['PDGid'] == 13) | (df['PDGid'] == -13)]

	return df

import matplotlib.cm as cm
from matplotlib.colors import ListedColormap
from matplotlib.ticker import ScalarFormatter

def Plot1DOverlayWithStats(hists, nBins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", labels=None, legPos="upper right", errors=True, NDPI=300):

	# Create figure and axes
	fig, ax = plt.subplots()

	# Define a colormap
	# cmap = cm.get_cmap('tab10') # !!deprecated!!

	# Define the colourmap colours
	colours = [
	    # (0., 0., 0.),                                                   # Black
	    (0.12156862745098039, 0.4666666666666667, 0.7058823529411765),  # Blue
	    (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),  # Red
	    (0.17254901960784313, 0.6274509803921569, 0.17254901960784313), # Green
	    (1.0, 0.4980392156862745, 0.054901960784313725),                # Orange
	    (0.5803921568627451, 0.403921568627451, 0.7411764705882353),    # Purple
	    (0.09019607843137255, 0.7450980392156863, 0.8117647058823529),   # Cyan
	    (0.8901960784313725, 0.4666666666666667, 0.7607843137254902),   # Pink
	    (0.5490196078431373, 0.33725490196078434, 0.29411764705882354), # Brown
	    (0.4980392156862745, 0.4980392156862745, 0.4980392156862745),   # Gray 
	    (0.7372549019607844, 0.7411764705882353, 0.13333333333333333)  # Yellow
	]

	# Create the colormap
	cmap = ListedColormap(colours)

	# cmap = cm.get_cmap('tab10')

	# Iterate over the hists and plot each one
	for i, hist in enumerate(hists):
		
		# Calculate statistics
		N, mean, meanErr, stdDev, stdDevErr, underflows, overflows = ut.GetBasicStats(hist, xmin, xmax)
		# Create legend text
		legend_text = f"Entries: {N}\nMean: {ut.Round(mean, 3)}\nStd Dev: {ut.Round(stdDev, 3)}"
		if errors: legend_text = f"Entries: {N}\nMean: {ut.Round(mean, 4)}$\pm${ut.Round(meanErr, 1)}\nStd Dev: {ut.Round(stdDev, 4)}$\pm${ut.Round(stdDevErr, 1)}"
		counts, bin_edges, _ = ax.hist(hist, bins=nBins, range=(xmin, xmax), histtype='step', edgecolor=cmap(i), linewidth=1.0, fill=False, density=False, color=cmap(i), label=r"$\bf{"+labels[i]+"}$"+"\n"+legend_text)

	# Set x-axis limits
	ax.set_xlim(xmin, xmax)

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

	# Add legend to the plot
	ax.legend(loc=legPos, frameon=False, fontsize=12)

	# Save the figure
	plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
	print("---> Written", fout)

	# Clear memory
	plt.close()

def Run(config, branchNames, particle):

	# Setup input 
	finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

	absorber=config.split("_")[2]

	# In/out DataFrames
	df_in = ut.TTreeToDataFrame(finName, "VirtualDetector/BeAbsorber_DetIn", branchNames)  
	df_out = ut.TTreeToDataFrame(finName, "VirtualDetector/BeAbsorber_DetOut", branchNames)  

	# Particle populations
	ut.BarChart(df_in["PDGid"], particleDict, "Entering "+absorber, "", "Counts / particle", fout="../img/"+g4blVer+"/Cooling/bar_In_ParticleFractionCounts_"+particle+"_"+config+".png", percentage=False)
	ut.BarChart(df_out["PDGid"], particleDict, "Exiting "+absorber, "", "Counts / particle", fout="../img/"+g4blVer+"/Cooling/bar_Out_ParticleFractionCounts_"+particle+"_"+config+".png", percentage=False)

	# Filtering
	df_in = FilterParticles(df_in, particle)
	df_out = FilterParticles(df_out, particle)

	# Momentum
	df_in["P"] = np.sqrt( np.power(df_in["Px"], 2) + np.power(df_in["Py"], 2) + np.power(df_in["Pz"], 2) )
	df_out["P"] = np.sqrt( np.power(df_out["Px"], 2) + np.power(df_out["Py"], 2) + np.power(df_out["Pz"], 2) )

	# Radius 
	df_in["R"] = np.sqrt( np.power(df_in["x"], 2) + np.power(df_in["y"], 2) )  
	df_out["R"] = np.sqrt( np.power(df_out["x"], 2) + np.power(df_out["y"], 2) ) 

	ut.Plot1D(df_in["P"], 1375, 0, 1375, "Entering "+absorber+" ("+particle+")", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/Cooling/h1_mom_In_"+particle+"_"+config+".png", underOver=False, errors=True)
	ut.Plot1D(df_out["P"], 1375, 0, 1375, "Exiting "+absorber+" ("+particle+")", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/Cooling/h1_mom_Out_"+particle+"_"+config+".png", underOver=False, errors=True)

	Plot1DOverlayWithStats([df_in["P"], df_out["P"]], 1375, 0, 1375, absorber+" ("+particle+")", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/Cooling/h1_mom_InOut_"+particle+"_"+config+".png", ["Entering", "Exiting"], errors=True)

	# XY
	ut.Plot2D(df_in["x"], df_in["y"], 400, -200, 200, 400, -200, 200, "Entering "+absorber+" ("+particle+")", "x [mm]", "y [mm]", "../img/"+g4blVer+"/Cooling/h2_XY_In_"+particle+"_"+config+".png")
	ut.Plot2D(df_out["x"], df_out["y"], 400, -200, 200, 400, -200, 200, "Exiting "+absorber+" ("+particle+")", "x [mm]", "y [mm]", "../img/"+g4blVer+"/Cooling/h2_XY_Out_"+particle+"_"+config+".png")

	# x vs y vs mom
	ut.Plot3D(df_in['x'], df_in['y'], df_in['P'], 400, -200, 200, 400, -200, 200, 1000, "Entering "+absorber+" ("+particle+")", "x [mm]", "y [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/BeamProfile/h3_XYMom_In_"+particle+"_"+config+".png") 
	ut.Plot3D(df_out['x'], df_out['y'], df_out['P'], 400, -200, 200, 400, -200, 200, 1000, "Exiting "+absorber+" ("+particle+")", "x [mm]", "y [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/BeamProfile/h3_XYMom_Out_"+particle+"_"+config+".png") 

	# Make dispersion plots
	ut.Plot2D(df_in['P'], df_in['x'], 250, 0, 250, 440, -220, 220, "Entering "+absorber+" ("+particle+")", "Momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/Cooling/h2_XvsMom_In_"+particle+"_"+config+".png")
	ut.Plot2D(df_in['P'], df_in['y'], 250, 0, 250, 440, -220, 220, "Entering "+absorber+" ("+particle+")", "Momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/Cooling/h2_YvsMom_In_"+particle+"_"+config+".png")
	
	ut.Plot2D(df_out['P'], df_out['x'], 250, 0, 250, 440, -220, 220, "Exiting "+absorber+" ("+particle+")", "Momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/Cooling/h2_XvsMom_Out_"+particle+"_"+config+".png")
	ut.Plot2D(df_out['P'], df_out['y'], 250, 0, 250, 440, -220, 220, "Exiting "+absorber+" ("+particle+")", "Momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/Cooling/h2_YvsMom_Out_"+particle+"_"+config+".png")

	# ut.Plot2D(df['PT'], df['x'], 200, 0, 200, 440, -220, 220, title, "Tranverse momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XvsMomT_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
	# ut.Plot2D(df['PT'], df['y'], 200, 0, 200, 440, -220, 220, title, "Tranverse momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_YvsMomT_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)

	# ut.Plot2D(df['Pz'], df['x'], 400, -200, 200, 440, -220, 220, title, "Longitundinal momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XvsMomZ_"+ntupleName+"_"+particle+"_"+config+".png" , cb=False)
	# ut.Plot2D(df['Pz'], df['y'], 400, -200, 200, 440, -220, 220, title, "Longitundinal momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_YvsMomZ_"+ntupleName+"_"+particle+"_"+config+".png" , cb=False)

	ut.Plot2D(df_in['P'], df_in['R'], 250, 0, 250, 200, 0, 200, "Entering "+absorber+" ("+particle+")", "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/Cooling/h2_RVsMom_In_"+particle+"_"+config+".png") 
	ut.Plot2D(df_out['P'], df_out['R'], 250, 0, 250, 200, 0, 200, "Exiting "+absorber+" ("+particle+")", "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/Cooling/h2_RVsMom_Out_"+particle+"_"+config+".png")

	return


def PlotGraphOverlay(graph_dict, title=None, xlabel=None, ylabel=None, fout="scatter.png", NDPI=300):

	# Create a scatter plot with error bars using NumPy arrays 

	# Create figure and axes
	fig, ax = plt.subplots()

	# Iterate through the keys (momentum values) in the dictionary
	for label, graph_list in graph_dict.items():
		for graph in graph_list:

			print(label, graph)
            # x = graph['x']
            # y = graph['y']
            # xerr = graph.get('xerr', [])
            # yerr = graph.get('yerr', [])


		# print(graph)

		# x = graph["x"] 
		# y = graph["y"] 
		# xerr = graph["xerr"]
		# yerr = graph["yerr"]

		# # Plot scatter with error bars
		# if len(xerr)==0: xerr = [0] * len(x) # Sometimes we only use yerr
		# if len(yerr)==0: yerr = [0] * len(y) # Sometimes we only use yerr

		# ax.errorbar(grx, y, xerr=xerr, yerr=yerr, fmt='o', color='black', markersize=4, ecolor='black', capsize=2, elinewidth=1, linestyle='None')

	# Set title, xlabel, and ylabel
	ax.set_title(title, fontsize=16, pad=10)
	ax.set_xlabel(xlabel, fontsize=14, labelpad=10) 
	ax.set_ylabel(ylabel, fontsize=14, labelpad=10) 

	# Set font size of tick labels on x and y axes
	ax.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
	ax.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size

	legend = ax.legend(loc="best", frameon=False, fontsize=14) # , bbox_to_anchor=(0.73, 0.99)) 

	# Scientific notation
	if ax.get_xlim()[1] > 9999:
		ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
		ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
		ax.xaxis.offsetText.set_fontsize(14)
	if ax.get_ylim()[1] > 9999:
		ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
		ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		ax.yaxis.offsetText.set_fontsize(14)


	# Save the figure
	plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
	print("---> Written", fout)

	# Clear memory
	plt.clf()
	plt.close()


def CoolingScan(branchNames_, nEvents, particle_, thickness_, momentum_):

	for particle in particle_:

		x_ = []
		y_ = []
		xerr_ = []
		yerr_ = []

		# Container for graphs
		graphs_ = {}

		for momentum in momentum_:

			# Graph
			graphs_[momentum] = []

			for thickness in thickness_:

				finName = "../ntuples/"+g4blVer+"/Cooling/g4beamline_Cooling_"+str(nEvents)+"events_"+particle+"_"+str(thickness)+"mm_"+str(momentum)+"MeV.root"

				# In/out DataFrames
				df_in = ut.TTreeToDataFrame(finName, "VirtualDetector/DetForward", branchNames_)  
				df_out = ut.TTreeToDataFrame(finName, "VirtualDetector/DetBackward", branchNames_) 

				# Momentum 
				df_in["P"] = np.sqrt( np.power(df_in["Px"], 2) + np.power(df_in["Py"], 2) + np.power(df_in["Pz"], 2) )
				df_out["P"] = np.sqrt( np.power(df_out["Px"], 2) + np.power(df_out["Py"], 2) + np.power(df_out["Pz"], 2) )

				meanMomIn = np.mean(df_in["P"])
				meanMomOut = np.mean(df_out["P"])

				stdMomIn = np.std(df_in["P"])
				stdMomOut = np.std(df_out["P"])

				deltaP = meanMomIn - meanMomOut
				deltaPErr = np.sqrt(pow(stdMomIn,2)+pow(stdMomOut,2))

				x_.append(thickness)
				y_.append(deltaP)
				xerr_.append(0.0)
				yerr_.append(deltaPErr)

			graphs_[momentum].append( {"x": x_, "y": y_, "xerr": xerr_, "yerr": yerr_} )

		# print(graphs_)
		PlotGraphOverlay(graphs_)

	return


def main():

	branchNames = [ 
		"x", 
		"y", 
		"z", 
		"Px", 
		"Py",
		"Pz",
		"t",
		"PDGid",
		"EventID",
		"TrackID",
		"ParentID",
		"Weight",
		"InitX",
		"InitY",
		"InitZ"
		]  

	# Run("Mu2E_1e7events_Absorber0_fromZ1850_parallel_noColl03", branchNames, "all") 
	# Run("Mu2E_1e7events_Absorber1_fromZ1850_parallel_noColl03", branchNames, "all") 
	# Run("Mu2E_1e7events_Absorber2_fromZ1850_parallel_noColl03", branchNames, "all") 
	# Run("Mu2E_1e7events_Absorber3_fromZ1850_parallel_noColl03", branchNames, "all") 

	# Run("Mu2E_1e7events_Absorber0_fromZ1850_parallel_noColl03", branchNames, "no_proton") 
	# Run("Mu2E_1e7events_Absorber1_fromZ1850_parallel_noColl03", branchNames, "no_proton") 
	# Run("Mu2E_1e7events_Absorber2_fromZ1850_parallel_noColl03", branchNames, "no_proton") 
	# Run("Mu2E_1e7events_Absorber3_fromZ1850_parallel_noColl03", branchNames, "no_proton") 

	# Run("Mu2E_1e7events_Absorber0_fromZ1850_parallel_noColl03", branchNames, "proton") 
	# Run("Mu2E_1e7events_Absorber1_fromZ1850_parallel_noColl03", branchNames, "proton") 
	# Run("Mu2E_1e7events_Absorber2_fromZ1850_parallel_noColl03", branchNames, "proton") 
	# Run("Mu2E_1e7events_Absorber3_fromZ1850_parallel_noColl03", branchNames, "proton") 

	# Run("Mu2E_1e7events_Absorber0_fromZ1850_parallel_noColl03", branchNames, "pi+-") 
	# Run("Mu2E_1e7events_Absorber1_fromZ1850_parallel_noColl03", branchNames, "pi+-") 
	# Run("Mu2E_1e7events_Absorber2_fromZ1850_parallel_noColl03", branchNames, "pi+-") 
	# Run("Mu2E_1e7events_Absorber3_fromZ1850_parallel_noColl03", branchNames, "pi+-") 

	# Run("Mu2E_1e7events_Absorber0_fromZ1850_parallel_noColl03", branchNames, "mu+-") 
	# Run("Mu2E_1e7events_Absorber1_fromZ1850_parallel_noColl03", branchNames, "mu+-") 
	# Run("Mu2E_1e7events_Absorber2_fromZ1850_parallel_noColl03", branchNames, "mu+-") 
	# Run("Mu2E_1e7events_Absorber3_fromZ1850_parallel_noColl03", branchNames, "mu+-") 

	# Cooling scan from Cooling.in

	nEvents=10000 # per step
	particle_=["pi-", "mu-"]
	thickness_=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100] # mm
	momentum_=[50, 100, 150, 200] # MeV

	CoolingScan(branchNames, nEvents, particle_, thickness_, momentum_)


if __name__ == "__main__":
    main()



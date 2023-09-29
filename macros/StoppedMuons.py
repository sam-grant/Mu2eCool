# Find the origin of stopped muons and analyse their parent pions at a particular ntuple 

# External libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# Internal libraries
import Utils as ut

# Suppress warnings about overwriting a dataframe
pd.options.mode.chained_assignment = None  # default='warn'

# Globals
g4blVer="v3.06"

def Plot1DAnnotated(data, nBins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", legPos="best", stats=True, peak=False, underOver=False, errors=False, norm=False, NDPI=300):
    
	# Create figure and axes
	fig, ax = plt.subplots()

	density = False
	if norm: density=True

	# Plot the histogram with outline
	counts, bin_edges, _ = ax.hist(data, bins=nBins, range=(xmin, xmax), histtype='step', edgecolor='black', linewidth=1.0, fill=False, density=density)

	if norm:
		counts 
	# Set x-axis limits
	ax.set_xlim(xmin, xmax)

	# Calculate statistics
	N, mean, meanErr, stdDev, stdDevErr, underflows, overflows = ut.GetBasicStats(data, xmin, xmax)
	# peak = np.max(counts)
	# peak_bin_edges = bin_edges[i_peak:i_peak + 2]
	# peak = counts[i_peak]
	# peakErr = (bin_edges[1] - bin_edges[0]) / 2
	# N, mean, meanErr, stdDev, stdDevErr = str(N), Round(mean, 3), Round(mean, 3), Round(meanErr, 1), Round(stdDev, 3), Round(stdDevErr, 1) 

	# Create legend text
	legend_text = f"Entries: {N}\nMean: {ut.Round(mean, 3)}\nStd Dev: {ut.Round(stdDev, 3)}"
	# if errors: legend_text = f"Entries: {N}\nMean: {Round(mean, 3)}$\pm${Round(meanErr, 1)}\nStd Dev: {Round(stdDev, 3)}$\pm${Round(stdDevErr, 1)}"
	if errors: legend_text = f"Entries: {N}\nMean: {ut.Round(mean, 4)}$\pm${ut.Round(meanErr, 1)}\nStd Dev: {ut.Round(stdDev, 4)}$\pm${ut.Round(stdDevErr, 1)}"
	# if peak: legend_text += f"\nPeak: {Round(peak, 4)}$\pm${Round(peakErr, 1)}"
	if underOver: legend_text += f"\nUnderflows: {underflows}\nOverflows: {overflows}"

	# legend_text = f"Entries: {N}\nMean: {Round(mean, 3)}$\pm${Round(meanErr, 1)}\nStd Dev: {Round(stdDev, 3)}$\pm${Round(stdDev, 1)}"

	# Add legend to the plot
	if stats: ax.legend([legend_text], loc=legPos, frameon=False, fontsize=14)


	# ax.legend([r"Stopped $\mu^{-}$"], loc="upper right", frameon=False, fontsize=14)

	# ax.set_title(title, fontsize=16, pad=15)
	ax.set_xlabel(xlabel, fontsize=14, labelpad=10) 
	ax.set_ylabel(ylabel, fontsize=14, labelpad=10) 

	# Set font size of tick labels on x and y axes
	ax.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
	ax.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size

    # Scientific notation
    # if ax.get_xlim()[1] > 999:
    #     ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    #     ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    #     ax.xaxis.offsetText.set_fontsize(14)
    # if ax.get_ylim()[1] > 999:
    #     ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    #     ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    #     ax.yaxis.offsetText.set_fontsize(14)

	if ax.get_xlim()[1] > 9999:
		ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
		ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
		ax.xaxis.offsetText.set_fontsize(14)
	if ax.get_ylim()[1] > 9999:
		ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
		ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		ax.yaxis.offsetText.set_fontsize(14)

	# Mark critical geometry 
	ax.axvline(x=1764.5/1e3, color='gray', linestyle='--', linewidth=1) # PT
	ax.axvline(x=3885/1e3, color='gray', linestyle='--', linewidth=1) # TS1
	ax.axvline(x=7929/1e3, color='gray', linestyle='--', linewidth=1) # TS3
	ax.axvline(x=11359/1e3, color='gray', linestyle='--', linewidth=1) # TS5
	ax.axvline(x=13800/1e3, color='gray', linestyle='--', linewidth=1) # ST
	# ax.axvline(x=17964, color='gray', linestyle='--', linewidth=1) # Tracker
	# ax.axvline(x=20394, color='gray', linestyle='--', linewidth=1) # Calo

	# TS3_L =  20643.96933831729
	# TS5_L =  37995.44402692665
	# ST_L =  40436.44402692665

	plt.annotate("PT",
		xy=(1764.5/1e3, plt.ylim()[1]),  # Position of the label
		xytext=(10, 10),  # Offset of the label from the point
		textcoords='offset points',  # Specify offset in points
		va='bottom',  # Vertical alignment of the label
		ha='right',  # Horizontal alignment of the label
		color='gray',  # Color of the label text
		fontsize=14,  # Font size of the label text
		rotation='vertical')  # Rotate the label
	plt.annotate("TS1",
		xy=(3885/1e3, plt.ylim()[1]),  
		xytext=(10, 10),  
		textcoords='offset points',  
		va='bottom',  
		ha='right', 
		color='gray', 
		fontsize=14,  # Font size of the label text
		rotation='vertical')  # Rotate the label
	plt.annotate("TS3",
		xy=(7929/1e3, plt.ylim()[1]), # 7929
		xytext=(10, 10),  
		textcoords='offset points',  
		va='bottom',  
		ha='right', 
		color='gray', 
		fontsize=14,  # Font size of the label text
	rotation='vertical')  # Rotate the label
	plt.annotate("TS5",
		xy=(11359/1e3, plt.ylim()[1]), # 11359
		xytext=(10, 10),  
		textcoords='offset points',  
		va='bottom',  
		ha='right', 
		color='gray', 
		fontsize=14,  # Font size of the label text
		rotation='vertical')  # Rotate the label
	plt.annotate("ST",
		xy=(13800/1e3, plt.ylim()[1]),  # 13800
		xytext=(10, 10),  
		textcoords='offset points',  
		va='bottom',  
		ha='right', 
		color='gray', 
		fontsize=14,  # Font size of the label text
		rotation='vertical')  # Rotate the label

	# Save the figure
	plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
	print("---> Written", fout)

	# Clear memory
	plt.clf()
	plt.close()

# Some things to consider:
# 1) Tracks can pass through the same plane multiple times;
# 2) g4beamline treats a particle resulting from a scatter or an ionisation as child particle, so parents do not neccesarily decay; 
# 3) Both the parent or the child can stop in the target;
# 4) Both the child and parent can originate downstream of the plane of interest.

def RunStoppedMuons(config, ntupleName): 

	# Setup input 
	finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

	# df_Coll_05_DetOut = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_05_DetOut", ut.branchNamesExtended)
	df_prestop = ut.TTreeToDataFrame(finName, "VirtualDetector/prestop", ut.branchNamesExtended)#[:1000]
	df_LostInTarget = ut.TTreeToDataFrame(finName, "NTuple/LostInTarget_Ntuple", ut.branchNamesExtended)#[:1000]
	df_poststop = ut.TTreeToDataFrame(finName, "VirtualDetector/poststop", ut.branchNamesExtended)#[:1000]
	df_ntuple = ut.TTreeToDataFrame(finName, ntupleName, ut.branchNamesExtended)#[:1000]

	# Drop any duplicates
	# Do I need to keep the first one? (It does this automatically)
	df_prestop = df_prestop.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])
	df_LostInTarget = df_LostInTarget.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])
	df_poststop = df_poststop.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])
	df_ntuple = df_ntuple.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])

	# Select forward-going particles 
	df_prestop = df_prestop[df_prestop["Pz"] > 0]
	df_poststop = df_poststop[df_poststop["Pz"] > 0]
	df_ntuple = df_ntuple[df_ntuple["Pz"] > 0]

	# Title and name of df_ntuple
	ntupleName = ntupleName.split("/")[1] 
	ntupleTitle = ntupleName
	if ntupleName[0] == "Z": ntupleTitle = "Z = "+ntupleName[1:]+" mm"
	if ntupleName[6:] == "3_DetIn": ntupleTitle = "Entering TS collimator 3"
	elif ntupleName[6:] == "3_DetOut": ntupleTitle = "Exiting TS collimator 3"
	
	if ntupleName[6:] == "5_DetIn": ntupleTitle = "Entering TS collimator 5"
	elif ntupleName[6:] == "5_DetOut": ntupleTitle = "Exiting TS collimator 5"

	# Add momentum column to DataFrames
	ut.GetTotalMomentum(df_prestop)
	ut.GetTotalMomentum(df_LostInTarget)
	ut.GetTotalMomentum(df_ntuple)



	# Need to translate position, based on where we are along the beamline
	df_trans = df_ntuple 

	if ntupleName[:7] == "Coll_03":
		# x is now z, shifted by z position of collimator 5
		# param Coll_03_up_z=$MECO_G4_zTrans
		# param MECO_G4_zTrans=(5.00+2.929)*1000
		df_trans["x"] = df_ntuple["z"] - (5.00+2.929)*1000 # 082


	if ntupleName[:7] == "Coll_05" or ntupleName == "prestop" or ntupleName == "poststop":
		# x is still x, but shifted by x position of collimator 5
		# param MECO_G4_xTrans=-(2.929+1.950/2.0)*1000
		# param Coll_05_x=-3904+$MECO_G4_xTrans
		df_trans["x"] = df_ntuple["x"] + 3904 + (2.929+1.950/2.0)*1000

	df_ntuple = df_trans

	# Add radial position column 
	ut.GetRadialPosition(df_ntuple)

	# ----------- Stops ----------- 

	# This is cleaner way of selecting stopped muons using Pandas
	df_stops = df_prestop.merge(df_LostInTarget, on=["EventID", "TrackID", "ParentID"], suffixes=("", "_lost"), how="inner")
	# Drop any duplicates
	df_stops = df_stops.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])

	# Drop the "lost" columns
	df_stops = df_stops[df_prestop.columns]

	# ----------- Stopped muons ----------- 

	# Select stopped muons using Pandas
	df_stoppedMuons = ut.FilterParticles(df_prestop, "mu-").merge(ut.FilterParticles(df_LostInTarget, "mu-"), on=["EventID", "TrackID", "ParentID"], suffixes=("", "_lost"), how="inner")
	# Drop any duplicates
	df_stoppedMuons = df_stoppedMuons.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])
	# Drop the "lost" columns
	df_stoppedMuons = df_stoppedMuons[df_prestop.columns]

	# ----------- Non-stops ----------- 

	# Select non-stops using a left join
	df_nonStops = df_prestop.merge(df_stops, on=["EventID", "TrackID", "ParentID"], suffixes=("", "_stopped"), how="left")
	# Select null stopped muons
	df_nonStops = df_nonStops[df_nonStops["x_stopped"].isnull()] 
	# Drop the "stopped" columns
	df_nonStops = df_nonStops[df_nonStops.columns]
	# Drop any duplicates
	df_nonStops = df_nonStops.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])

	# ----------- Non-stopped muons ----------- 

	# Select non-stops using a left join
	df_nonStoppedMuons = ut.FilterParticles(df_prestop, "mu-").merge(ut.FilterParticles(df_stops, "mu-"), on=["EventID", "TrackID", "ParentID"], suffixes=("", "_stopped"), how="left")
	# Select null stopped muons
	df_nonStoppedMuons = df_nonStoppedMuons[df_nonStoppedMuons["x_stopped"].isnull()] 
	# Drop the "stopped" columns
	df_nonStoppedMuons = df_nonStoppedMuons[df_nonStoppedMuons.columns]
	# Drop any duplicates
	df_nonStoppedMuons = df_nonStoppedMuons.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])

	# ----------- Extrapolate stops to plane of interest -----------

	# Orphaned stops, those without parents at the plane of interest
	df_orphanStops = df_ntuple.merge(df_stops, on=["EventID", "TrackID", "ParentID", "PDGid"], suffixes=("", "_atST"), how="inner") 
	# Drop duplicates 
	df_orphanStops = df_orphanStops.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])
	# Drop the ST columns
	df_orphanStops = df_orphanStops[df_ntuple.columns] 

	# Orpaned stopped muons
	df_orphanStoppedMuons = ut.FilterParticles(df_ntuple, "mu-").merge(df_stoppedMuons, on=["EventID", "TrackID", "ParentID", "PDGid"], suffixes=("", "_atST"), how="inner") 
	# Drop duplicates whenever you merge
	df_orphanStoppedMuons = df_orphanStoppedMuons.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])
	# Drop the ST columns
	df_orphanStoppedMuons = df_orphanStoppedMuons[df_ntuple.columns] 

	# Find stopped particle parents
	df_stopsParents = df_ntuple.merge(df_stops, left_on=["EventID", "TrackID"], right_on=["EventID", "ParentID"], suffixes=("", "_child"), how="inner")
	df_stoppedMuonParents = df_ntuple.merge(df_stoppedMuons, left_on=["EventID", "TrackID"], right_on=["EventID", "ParentID"], suffixes=("", "_child"), how="inner")
	# Drop duplicates whenever you merge
	df_stopsParents = df_stopsParents.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])
	df_stoppedMuonParents = df_stoppedMuonParents.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])

	# Sometimes you get both the parent and the child arriving at the ST. This could be due to ionisation or scattering. 
	# We only really care about parents which decay before the ST, so cut out parents with the same PDGid as the child. 
	# Not 100% needed really 
	# df_stopsParents = df_stopsParents[df_stopsParents["PDGid"] != df_stopsParents["PDGid_child"]]
	# df_stoppedMuonParents = df_stoppedMuonParents[df_stoppedMuonParents["PDGid"] != df_stoppedMuonParents["PDGid_child"]]

	# Drop the ST columns
	df_stopsParents = df_stopsParents[df_ntuple.columns]
	df_stoppedMuonParents = df_stoppedMuonParents[df_ntuple.columns]

	# Pion parents
	df_stoppedMuonParentPions = ut.FilterParticles(df_stoppedMuonParents, "pi-") 	

	# ----------- Extrapolate non-stops to plane of interest -----------

	# Orphaned stops, those without parents at the plane of interest
	df_orphanNonStops = df_ntuple.merge(df_nonStops, on=["EventID", "TrackID", "ParentID", "PDGid"], suffixes=("", "_atST"), how="inner") 
	# Drop duplicates 
	df_orphanNonStops = df_orphanNonStops.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])
	# Drop the ST columns
	df_orphanNonStops = df_orphanNonStops[df_ntuple.columns] 

	# Orpaned stopped muons
	df_orphanNonStoppedMuons = ut.FilterParticles(df_ntuple, "mu-").merge(df_nonStoppedMuons, on=["EventID", "TrackID", "ParentID", "PDGid"], suffixes=("", "_atST"), how="inner") 
	# Drop duplicates whenever you merge
	df_orphanNonStoppedMuons = df_orphanNonStoppedMuons.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])
	# Drop the ST columns
	df_orphanNonStoppedMuons = df_orphanNonStoppedMuons[df_ntuple.columns] 

	# Find stopped particle parents
	df_nonStopsParents = df_ntuple.merge(df_nonStops, left_on=["EventID", "TrackID"], right_on=["EventID", "ParentID"], suffixes=("", "_child"), how="inner")
	df_nonStoppedMuonParents = df_ntuple.merge(df_nonStoppedMuons, left_on=["EventID", "TrackID"], right_on=["EventID", "ParentID"], suffixes=("", "_child"), how="inner")
	# Drop duplicates whenever you merge
	df_nonStopsParents = df_nonStopsParents.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])
	df_nonStoppedMuonParents = df_nonStoppedMuonParents.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])

	# Sometimes you get both the parent and the child arriving at the ST. This could be due to ionisation or scattering. 
	# We only really care about parents which decay before the ST, so cut out parents with the same PDGid as the child. 
	# Not 100% needed really 
	# df_nonStopsParents = df_nonStopsParents[df_nonStopsParents["PDGid"] != df_nonStopsParents["PDGid_child"]]
	# df_nonStoppedMuonParents = df_nonStoppedMuonParents[df_nonStoppedMuonParents["PDGid"] != df_nonStoppedMuonParents["PDGid_child"]]

	# Drop the ST columns
	df_nonStopsParents = df_nonStopsParents[df_ntuple.columns]
	df_nonStoppedMuonParents = df_nonStoppedMuonParents[df_ntuple.columns]

	# Pion parents
	df_nonStoppedMuonParentPions = ut.FilterParticles(df_nonStoppedMuonParents, "pi-") 

	# -----------  Identify erroneous rows / double counting -----------

	df_orphanAndParentStops = df_orphanStops[df_orphanStops.isin(df_stopsParents)].dropna()
	df_erroneousOrphanStops = df_orphanStops[~df_orphanStops.isin(df_stops)].dropna()
	df_erroneousStopParents = df_stopsParents[~df_stopsParents.isin(df_stops)].dropna()
	df_orphanAndParentStoppedMuons = df_orphanStoppedMuons[df_orphanStoppedMuons.isin(df_stoppedMuonParents)].dropna()
	df_erroneousOrphanStoppedMuons = df_orphanStoppedMuons[~df_orphanStoppedMuons.isin(df_stoppedMuons)].dropna()
	df_erroneousStoppedMuonParents = df_stoppedMuonParents[~df_stoppedMuonParents.isin(df_stoppedMuons)].dropna()

	if (df_orphanAndParentStops.shape[0] != 0):
		print("!!! WARNING: double counting parents and orphans !!!")
	elif (df_erroneousOrphanStops.shape[0] != 0):
		print("!!! WARNING: orphans counted that do not stop !!!")
	elif (df_erroneousStopParents.shape[0] != 0):
		print("!!! WARNING: parents counted that do not produce a stop !!!")
	elif (df_orphanAndParentStoppedMuons.shape[0] != 0):
		print("!!! WARNING: double counting parents and orphans for stopped muons !!!")
	elif (df_erroneousOrphanStoppedMuons.shape[0] != 0):
		print("!!! WARNING: stopped muon orphans counted that do not stop !!!")
	elif (df_erroneousStoppedMuonParents.shape[0] != 0):
		print("!!! WARNING: stopped muon parents counted that do not produce a stop !!!")

	# Store info 
	stoppingDict = {

					"Info at "+ntupleName : [
						"Entering ST",
						"All stops", 
						"Non-stops",
						"Orphan stops",
						"Parents of stops",
						"---",
						"Muons entering ST",
						"Stopped muons", 
						"Non-stopped muons", 
						"Orphaned stopped muons",
						"Stopped muon parents",
						"Fraction of stopped muons"
					], 

					"Count" : [
						df_prestop.shape[0],
						df_stops.shape[0],
						df_nonStops.shape[0],
						df_orphanStops.shape[0],
						df_stopsParents.shape[0],
						"---",
						ut.FilterParticles(df_prestop, "mu-").shape[0], 
						df_stoppedMuons.shape[0],
						df_nonStoppedMuons.shape[0],
						df_orphanStoppedMuons.shape[0],
						df_stoppedMuonParents.shape[0],
						df_stoppedMuonParents.shape[0]/df_stoppedMuons.shape[0]
					]
				}


	stoppingDict = pd.DataFrame(stoppingDict)
	print(stoppingDict)

	# ----------- All pions and muons at plane of interest ----------- 

	df_allMuons = ut.FilterParticles(df_ntuple, "mu-")
	df_allPions = ut.FilterParticles(df_ntuple, "pi-")


	# ut.Plot1D(df_orphanStoppedMuons["R"], 100, 0, 100, r"Stopped $\mu^{-}$ at "+ntupleTitle , "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_rad_stoppedMuonsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# ut.Plot1D(df_orphanStoppedMuons["P"], 105, 0, 105, r"Stopped $\mu^{-}$ at "+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# # ut.Plot1D(df_orphanStoppedMuons["R"], 250, 0, 250, r"Stopped $\mu^{-}$ at "+ntupleTitle , "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_rad_stoppedMuonsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False) 

	# return

	# ----------- Bar charts for populations -----------

	ut.BarChart(df_stops["PDGid"], ut.latexParticleDict, "All stops", "", "Percentage / particle", fout="../img/"+g4blVer+"/StoppedMuons/bar_Stops_"+config+".png", percentage=True)
	ut.BarChart(df_stopsParents["PDGid"], ut.latexParticleDict, "Stopped particle parents", "", "Percentage / particle", fout="../img/"+g4blVer+"/StoppedMuons/bar_StopParents_"+config+".png", percentage=True)
	# ut.BarChart(df_stoppedMuons["PDGid"], ut.latexParticleDict, r"Stopped $\mu^{-}$", "", "Percentage / particle", fout="../img/"+g4blVer+"/StoppedMuons/bar_StoppedMuons_"+config+".png", percentage=True)
	ut.BarChart(df_orphanStoppedMuons["PDGid"], ut.latexParticleDict, r"Orphan stopped $\mu^{-}$", "", "Percentage / particle", fout="../img/"+g4blVer+"/StoppedMuons/bar_OrphanStoppedMuons_"+config+".png", percentage=True)
	ut.BarChart(df_stoppedMuonParents[df_stoppedMuonParents["PDGid"] != 2212]["PDGid"], ut.latexParticleDict, r"Stopped $\mu^{-}$ parents", "", "Percentage / particle", fout="../img/"+g4blVer+"/StoppedMuons/bar_StoppedMuonParents_"+config+".png", percentage=True)

	# Annotated initial z-position for stopped muons
	Plot1DAnnotated(df_stoppedMuons["InitZ"]/1e3, 143, 0, 14.3, "", "Initial z-position [m]", r"Stopped $\mu^{-}$ (normalised) / 100 mm", "../img/"+g4blVer+"/StoppedMuons/h1_InitZ_annotated_stoppedMuons_"+config+".png", "upper right", stats=False, errors=False, norm=True) 
	# Plot1DAnnotated(df_stoppedMuons["InitZ"], 14300, 0, 14300, "", "Initial z-position [m]", r"Stopped $\mu^{-}$ (normalised) / 100 mm", "../img/"+g4blVer+"/StoppedMuons/h1_InitZ_annotated_stoppedMuons_"+config+".png", "upper right", stats=False, errors=False, norm=True) 

	# ----------- Momentum distributions  ----------- 

	print("\n---> Momentum distributions:")

	# All muons at plane of interest
	ut.Plot1D(df_allMuons["P"], 700, 0, 700, r"$\mu^{-}$ at "+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_muons_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# All pions at plane of interest
	ut.Plot1D(df_allPions["P"], 1400, 0, 1400, r"$\pi^{-}$ at "+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_pions_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# Stopped muon momentum distribution at the target
	ut.Plot1D(df_stoppedMuons["P"], 100, 0, 100, r"Stopped $\mu^{-}$" , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuons_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# Non-stopped muon momentum distribution at the target
	ut.Plot1D(df_nonStoppedMuons["P"], 120, 0, 120, r"Non-stopped $\mu^{-}$" , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_nonStoppedMuons_"+config+".png", "best", errors=True, peak=True, underOver=True) 
	# Stopped muon momentum distribution at the plane of interest
	ut.Plot1D(df_orphanStoppedMuons["P"], 105, 0, 105, r"Stopped $\mu^{-}$ at "+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# Stopped muon parent momentum distribution
	ut.Plot1D(df_stoppedMuonParents["P"], 300, 0, 300, r"Stopped $\mu^{-}$ parents at "+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonsParentsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False)  
	# Stopped muon parent pion momentum distribution
	ut.Plot1D(df_orphanStoppedMuons["P"], 250, 0, 250, r"Stopped $\mu^{-}$ parent $\pi^{-}$ at "+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonsParentPionsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# Non-stopped muon momentum distribution at plane of interest
	# ut.Plot1D(df_orphanNonStoppedMuons["P"], 250, 0, 250, r"Non-stopped $\mu^{-}$ at "+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_nonStoppedMuonsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=True) 
	# Non-stopped muon momentum distribution at plane of interest, R > 90 mm 
	ut.Plot1D(df_orphanNonStoppedMuons["P"], 250, 0, 250, r"Non-stopped $\mu^{-}$ at "+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_nonStoppedMuonsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=True) 
	# Non-stopped muon parent distribution at plane of interest
	ut.Plot1D(df_nonStoppedMuonParents["P"], 250, 0, 250, r"Non-stopped $\mu^{-}$ parents at "+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_nonStoppedMuonParentsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# >90 mm 
	ut.Plot1D(df_nonStoppedMuonParentPions[(df_nonStoppedMuonParentPions["R"]>90) & (df_nonStoppedMuonParentPions["P"]>100)]["P"], 50, 100, 150, r"Non-stopped $\mu^{-}$ parent $\pi^{-}$, $R>90$ mm, "+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_nonStoppedMuonParentPionsAt"+ntupleName+"_above90mmAnd100MeV_"+config+".png", "best", errors=True, peak=True, underOver=True) 

	return

	# Non-stopped muon parent pion distribution at plane of interest
	ut.Plot1D(df_nonStoppedMuonParentPions["P"], 250, 0, 250, r"Non-stopped $\mu^{-}$ parents $\pi^{-}$ at "+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_nonStoppedMuonParentPionsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=True) 
	
	print("\n---> Momentum overlays:")

	# Overlays
	ut.Plot1DOverlay([df_nonStoppedMuons["P"], df_stoppedMuons["P"]], 120, 0, 120, title = r"$\mu^{-}$ at the ST", xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"Non-stopped $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedAndNonStoppedMuonOverlayAtST_"+config+".png") # , includeBlack=False)
	ut.Plot1DOverlay([ut.FilterParticles(df_prestop, "mu-")["P"], df_nonStoppedMuons["P"], df_stoppedMuons["P"]], 120, 0, 120, title = r"$\mu^{-}$ at the ST", xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = ["$\mu^{-}$ entering the ST",  r"Non-stopped $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_prestopMuonsAndStoppedAndNonStoppedMuonOverlayAtST_"+config+".png", includeBlack=True)
	ut.Plot1DRatio([ut.FilterParticles(df_prestop, "mu-")["P"], df_stoppedMuons["P"]], 50, 0, 50, title = r"$\mu^{-}$ at the ST", xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = ["$\mu^{-}$ entering the ST", r"Stopped $\mu^{-}$", r"Non-stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_prestopMuonsAndStoppedMuonRatioAtST_"+config+".png", invertRatio=True) # , ratioTitle="Stopping fraction")
	
	ut.Plot1DOverlay([df_allMuons["P"], df_orphanStoppedMuons["P"]], 700, 0, 700, title = r"$\mu^{-}$ at "+ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = ["All $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_muonOverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)
	ut.Plot1DOverlay([df_allPions["P"], df_stoppedMuonParentPions["P"]], 1400, 0, 1400, title = r"$\pi^{-}$ at "+ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = ["All $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$  "], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_pionOverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)
	
	# ut.Plot1DOverlay([df_allMuons["P"], df_orphanStoppedMuons["P"], ], 700, 0, 700, title = r"$\mu^{-}$ at "+ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = ["All $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_muonOverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)

	# print(df_orphanNonStoppedMuons["z"])
	ut.Plot1DOverlay([df_orphanNonStoppedMuons["P"], df_orphanStoppedMuons["P"]], 120, 0, 120, title = ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"Non-stopped $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonOverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)
	


	# ut.Plot1DOverlay([df_nonStoppedMuonParentPions["P"], df_stoppedMuonParentPions["P"]], 250, 0, 250, title = ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"Non-stopped $\mu^{-}$ parent $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonParentPionOverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)
	ut.Plot1DOverlay([df_nonStoppedMuonParentPions["P"], df_stoppedMuonParentPions["P"]], 200, 0, 200, title = ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"Non-stopped $\mu^{-}$ parent $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonParentPionOverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)

	# ut.Plot1DRatio([df_orphanNonStoppedMuons["P"], df_orphanStoppedMuons["P"]], 120, 0, 120, title = ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"Non-stopped $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonRatioAt"+ntupleName+"_"+config+".png", invertRatio=True)
	# ut.Plot1DRatio([df_nonStoppedMuonParentPions["P"], df_stoppedMuonParentPions["P"]], 250, 0, 250, title = ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"Non-stopped $\mu^{-}$ parent $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonParentPionRatioAt"+ntupleName+"_"+config+".png", invertRatio=True) # , includeBlack=False)

	ut.Plot1DOverlay([df_stoppedMuonParentPions["P"], df_stoppedMuons["P"]], 250, 0, 250, title = ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"Stopped $\mu^{-}$ parent $\pi^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonsAndParentPionsAt"+ntupleName+"_"+config+".png") # , includeBlack=False)


	# Probably dumb
	ut.Plot1DOverlay([df_nonStoppedMuonParentPions["P"], df_stoppedMuonParentPions["P"], df_orphanNonStoppedMuons["P"], df_orphanStoppedMuons["P"]], 250, 0, 250, title = ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"Non-stopped $\mu^{-}$ parent $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$", r"Non-stopped $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppingAndNonStoppingOverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)

	# return

	df_muonsWhichMakeItToPrestop = pd.concat([df_orphanNonStoppedMuons, df_orphanStoppedMuons])
	df_pionsWhichMakeItToPrestop = pd.concat([df_nonStoppedMuonParentPions, df_stoppedMuonParentPions])

	ut.Plot1DOverlay([df_allMuons["P"], df_orphanNonStoppedMuons["P"], df_orphanStoppedMuons["P"]], 250, 0, 250, title = ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"All $\mu^{-}$", r"Non-stopped $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonTripleOverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)
	
	ut.Plot1DOverlay([df_allPions["P"], df_pionsWhichMakeItToPrestop["P"], df_allMuons["P"], df_muonsWhichMakeItToPrestop["P"]], 1200, 0, 1200, title = ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"All $\pi^{-}$", r"Parent $\pi^{-}$ of $\mu^{-}$ reaching ST", r"All $\mu^{-}$", r"$\mu^{-}$ reaching ST"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_particlesMakingItToSTOveraly"+ntupleName+"_"+config+".png") # , includeBlack=False)
	ut.Plot1DOverlay([df_allPions["P"], df_pionsWhichMakeItToPrestop["P"], df_allMuons["P"], df_muonsWhichMakeItToPrestop["P"]], 1200, 0, 1200, title = ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"All $\pi^{-}$", r"Parent $\pi^{-}$ of $\mu^{-}$ reaching ST", r"All $\mu^{-}$", r"$\mu^{-}$ reaching ST"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_particlesMakingItToSTOveraly"+ntupleName+"_logY_"+config+".png", logY=True) # , includeBlack=False)



	# ut.Plot1DOverlay([df_nonStoppedMuonParents[df_nonStoppedMuonParents["R"] > 100]["P"], df_orphanStoppedMuons[df_orphanStoppedMuons["R"] > 100]["P"]], 250, 0, 250, title = "R > 100 mm, "+ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"Non-stopped $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonOverlayAt"+ntupleName+"_highR_"+config+".png") # , includeBlack=False)
	# ut.Plot1DOverlay([df_nonStoppedMuonParentPions[df_nonStoppedMuonParentPions["R"] > 100]["P"], df_stoppedMuonParentPions[df_stoppedMuonParentPions["R"] > 100]["P"]], 250, 0, 250, title = "R > 100 mm, "+ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"Non-stopped $\mu^{-}$ parent $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonParentPionOverlayAt"+ntupleName+"_highR_"+config+".png") # , includeBlack=False)

	# ----------- Radial position distributions  ----------- 

	print("\n---> Radial distributions:")

	# All muons at plane of interest
	ut.Plot1D(df_allMuons["R"], 250, 0, 250, r"$\mu^{-}$ at "+ntupleTitle, "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_rad_muons_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# All pions at plane of interest
	ut.Plot1D(df_allPions["R"], 250, 0, 250, r"$\pi^{-}$ at "+ntupleTitle, "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_rad_pions_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# Stopped muon momentum distribution at the target
	# ut.Plot1D(df_stoppedMuons["R"], 250, 0, 250, r"Stopped $\mu^{-}$", "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_rad_stoppedMuons_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# Stopped muon momentum distribution at the plane of interest
	ut.Plot1D(df_orphanStoppedMuons["R"], 250, 0, 250, r"Stopped $\mu^{-}$ at "+ntupleTitle , "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_rad_stoppedMuonsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# Stopped muon parent momentum distribution
	ut.Plot1D(df_stoppedMuonParents["R"], 250, 0, 250, r"Stopped $\mu^{-}$ parents at "+ntupleTitle , "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_rad_stoppedMuonsParentsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False)  
	# Stopped muon parent pion momentum distribution
	ut.Plot1D(df_stoppedMuonParentPions["R"], 250, 0, 250, r"Stopped $\mu^{-}$ parent $\pi^{-}$ at "+ntupleTitle , "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_rad_stoppedMuonsParentPionsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# Non-stopped muon momentum distribution at plane of interest
	ut.Plot1D(df_orphanNonStoppedMuons["R"], 250, 0, 250, r"Non-stopped $\mu^{-}$ at "+ntupleTitle , "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_rad_nonStoppedMuonsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=True) 
	# Non-stopped muon parent distribution at plane of interest
	ut.Plot1D(df_nonStoppedMuonParents["R"], 250, 0, 250, r"Non-stopped $\mu^{-}$ parents at "+ntupleTitle , "Radial position [mm]", "Counts / mm",  "../img/"+g4blVer+"/StoppedMuons/h1_rad_nonStoppedMuonParentsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=True) 
	# Non-stopped muon parent pion distribution at plane of interest
	ut.Plot1D(df_nonStoppedMuonParentPions["R"], 250, 0, 250, r"Non-stopped $\mu^{-}$ parents $\pi^{-}$ at "+ntupleTitle , "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_rad_nonStoppedMuonParentPionsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=True) 
	
	print("\n---> Radial overlays:")

	# Overlays
	ut.Plot1DOverlay([df_allMuons["R"], df_orphanStoppedMuons["R"]], 250, 0, 250, title = r"$\mu^{-}$ at "+ntupleTitle, xlabel = "Radial position [mm]", ylabel = "Counts / mm", labels = ["All $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_rad_muonOverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)
	ut.Plot1DOverlay([df_allPions["R"], df_stoppedMuonParentPions["R"]], 250, 0, 250, title = r"$\pi^{-}$ at "+ntupleTitle, xlabel = "Radial position [mm]", ylabel = "Counts / mm", labels = ["All $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$  "], fout = "../img/"+g4blVer+"/StoppedMuons/h1_rad_pionOverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)
	
	ut.Plot1DOverlay([df_orphanNonStoppedMuons["R"], df_orphanStoppedMuons["R"]], 120, 0, 120, title = ntupleTitle, xlabel = "Radial position [mm]", ylabel = "Counts / mm", labels = [r"Non-stopped $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_rad_stoppedMuonOverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)
	ut.Plot1DOverlay([df_nonStoppedMuonParentPions["R"], df_stoppedMuonParentPions["R"]], 200, 0, 200, title = ntupleTitle, xlabel = "Radial position [mm]", ylabel = "Counts / mm", labels = [r"Non-stopped $\mu^{-}$ parent $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_rad_stoppedMuonParentPionOverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)

	ut.Plot1DOverlay([df_nonStoppedMuonParentPions["R"], df_stoppedMuonParentPions["R"], df_orphanNonStoppedMuons["R"], df_orphanStoppedMuons["R"]], 250, 0, 250, title = ntupleTitle, xlabel = "Radial position [mm]", ylabel = "Counts / mm", labels = [r"Non-stopped $\mu^{-}$ parent $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$", r"Non-stopped $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_rad_stoppedAndNonStoppedOverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)

	# ut.Plot1DOverlay([df_nonStoppedMuonParents[df_nonStoppedMuonParents["R"] > 100]["P"], df_orphanStoppedMuons[df_orphanStoppedMuons["R"] > 100]["P"]], 250, 0, 250, title = "R > 100 mm, "+ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"Non-stopped $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonOverlayAt"+ntupleName+"_highR_"+config+".png") # , includeBlack=False)
	# ut.Plot1DOverlay([df_nonStoppedMuonParentPions[df_nonStoppedMuonParentPions["R"] > 100]["P"], df_stoppedMuonParentPions[df_stoppedMuonParentPions["R"] > 100]["P"]], 250, 0, 250, title = "R > 100 mm, "+ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = [r"Non-stopped $\mu^{-}$ parent $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonParentPionOverlayAt"+ntupleName+"_highR_"+config+".png") # , includeBlack=False)

	ut.Plot1DOverlay([df_allPions["R"], df_pionsWhichMakeItToPrestop["R"], df_allMuons["R"], df_muonsWhichMakeItToPrestop["R"]], 500, 0, 500, title = ntupleTitle, xlabel = "Radial position [mm]", ylabel = "Counts / mm", labels = [r"All $\pi^{-}$", r"Parent $\pi^{-}$ of $\mu^{-}$ reaching ST", r"All $\mu^{-}$", r"$\mu^{-}$ reaching ST"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_rad_particlesMakingItToSTOveraly"+ntupleName+"_"+config+".png") # , includeBlack=False)
	ut.Plot1DOverlay([df_allPions["R"], df_pionsWhichMakeItToPrestop["R"], df_allMuons["R"], df_muonsWhichMakeItToPrestop["R"]], 750, 0, 750, title = ntupleTitle, xlabel = "Radial position [mm]", ylabel = "Counts / mm", labels = [r"All $\pi^{-}$", r"Parent $\pi^{-}$ of $\mu^{-}$ reaching ST", r"All $\mu^{-}$", r"$\mu^{-}$ reaching ST"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_rad_particlesMakingItToSTOveraly"+ntupleName+"_logY_"+config+".png", logY=True) # , includeBlack=False)
	
	ut.Plot1DOverlay([df_stoppedMuonParentPions["R"], df_orphanStoppedMuons["R"]], 250, 0, 250, title = ntupleTitle,  xlabel = "Radial position [mm]", ylabel = "Counts / mm", labels = [r"Stopped $\mu^{-}$ parent $\pi^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_rad_stoppedMuonsAndParentPionsAt"+ntupleName+"_"+config+".png") # , includeBlack=False)


	#  ----------- Radius vs momentum ----------- 
	
	print("\n---> Momentum vs Radius 2D histograms:")

	ut.Plot2D(df_allPions["P"], df_allPions["R"], 50, 0, 250, 42, 0, 210, r"$\pi^{-}$ at "+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_rad_vs_mom_pions_"+ntupleName+"_"+config+".png")
	ut.Plot2D(df_allMuons["P"], df_allMuons["R"], 50, 0, 250, 42, 0, 210, r"$\mu^{-}$ at $\pi^{-}$"+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_rad_vs_mom_muons_"+ntupleName+"_"+config+".png")

	ut.Plot2D(df_orphanStoppedMuons["P"], df_orphanStoppedMuons["R"], 50, 0, 250, 42, 0, 210, r"Stopped $\mu^{-}$ at "+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_rad_vs_mom_stoppedMuons_"+ntupleName+"_"+config+".png")
	ut.Plot2D(df_stoppedMuonParents["P"], df_stoppedMuonParents["R"], 50, 0, 250, 42, 0, 210, r"Stopped $\mu^{-}$ parents at "+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_rad_vs_mom_stoppedMuonParents_"+ntupleName+"_"+config+".png")
	ut.Plot2D(df_stoppedMuonParentPions["P"], df_stoppedMuonParentPions["R"], 50, 0, 250, 42, 0, 210, r"Stopped $\mu^{-}$ parent $\pi^{-}$ at "+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_rad_vs_mom_stoppedMuonParentPions_"+ntupleName+"_"+config+".png")

	ut.Plot2D(df_orphanNonStoppedMuons["P"], df_orphanNonStoppedMuons["R"], 50, 0, 250, 42, 0, 210, r"Non-stopped $\mu^{-}$ at "+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_rad_vs_mom_nonStoppedMuons_"+ntupleName+"_"+config+".png")
	ut.Plot2D(df_nonStoppedMuonParents["P"], df_nonStoppedMuonParents["R"] , 50, 0, 250, 42, 0, 210, r"Non-stopped $\mu^{-}$ parents at "+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_rad_vs_mom_nonStoppedMuonParents_"+ntupleName+"_"+config+".png")
	ut.Plot2D(df_nonStoppedMuonParentPions["P"], df_nonStoppedMuonParentPions["R"], 50, 0, 250, 42, 0, 210, r"Non-stopped $\mu^{-}$ parent $\pi^{-}$ at "+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_rad_vs_mom_nonStoppedMuonParentPions_"+ntupleName+"_"+config+".png")

	#  ----------- Beam profile ----------- 

	ut.Plot2D(df_orphanStoppedMuons["x"], df_orphanStoppedMuons["y"], 40, -200, 200, 40, -200, 200, r"Stopped $\mu^{-}$ at "+ntupleTitle, "x [mm]", "y [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_x_vs_y_stoppedMuons_"+ntupleName+"_"+config+".png")
	ut.Plot2D(df_stoppedMuonParents["x"], df_stoppedMuonParents["y"], 40, -200, 200, 40, -200, 200, r"Stopped $\mu^{-}$ parents at "+ntupleTitle, "x [mm]", "y [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_x_vs_y_stoppedMuonParents_"+ntupleName+"_"+config+".png")
	ut.Plot2D(df_stoppedMuonParentPions["x"], df_stoppedMuonParentPions["y"], 40, -200, 200, 40, -200, 200, r"Stopped $\mu^{-}$ parent $\pi^{-}$ at "+ntupleTitle, "x [mm]", "y [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_x_vs_y_stoppedMuonParentPions_"+ntupleName+"_"+config+".png")

	ut.Plot2D(df_orphanNonStoppedMuons["x"], df_orphanNonStoppedMuons["y"], 40, -200, 200, 40, -200, 200, r"Non-stopped $\mu^{-}$ at "+ntupleTitle, "x [mm]", "y [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_x_vs_y_nonStoppedMuons_"+ntupleName+"_"+config+".png")
	ut.Plot2D(df_nonStoppedMuonParents["x"], df_nonStoppedMuonParents["y"] , 40, -200, 200, 40, -200, 200, r"Non-stopped $\mu^{-}$ parents at "+ntupleTitle, "x [mm]", "y [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_x_vs_y_nonStoppedMuonParents_"+ntupleName+"_"+config+".png")
	ut.Plot2D(df_nonStoppedMuonParentPions["x"], df_nonStoppedMuonParentPions["y"], 40, -200, 200, 40, -200, 200, r"Non-stopped $\mu^{-}$ parent $\pi^{-}$ at "+ntupleTitle, "x [mm]", "y [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_x_vs_y_nonStoppedMuonParentPions_"+ntupleName+"_"+config+".png")


	return	

def main():

	# RunStoppedMuons("Mu2E_1e7events_ColdParticles_beamloss", "VirtualDetector/Coll_03_DetIn")

	# RunStoppedMuons("Mu2E_1e7events_NoAbsorber_fromZ1850_parallel_partialPSZScan", "NTuple/Z1965")
	# RunStoppedMuons("Mu2E_1e7events_NoAbsorber", "NTuple/Z1850")
	# RunStoppedMuons("Mu2E_1e7events_NoAbsorber_fromZ1850_parallel", "NTuple/Z1850")
	# RunStoppedMuons("Mu2E_1e7events_NoAbsorber_fromZ1850_parallel", "VirtualDetector/Coll_03_DetIn")
	# RunStoppedMuons("Mu2E_1e7events_NoAbsorber_fromZ1850_parallel", "VirtualDetector/Coll_05_DetIn")
	RunStoppedMuons("Mu2E_1e7events_NoAbsorber_fromZ1850_parallel_finePSZScan", "NTuple/Z1915")
	# ../img/v3.06/StoppedMuons/h1_rad_stoppedAndNonStoppedOverlayAtColl_03_DetIn_Mu2E_1e7events_NoAbsorber_fromZ1850_parallel.png
	# RunStoppedMuons("Mu2E_1e7events_NoAbsorber_fromZ1850_parallel", "VirtualDetector/prestop")
    # RunStoppedMuons("Mu2E_1e7events")
    # RunStoppedMuons("Mu2E_1e7events_fromZ1850_parallel_noColl03", "VirtualDetector/Coll_01_DetIn")
    # RunStoppedMuons("Mu2E_1e7events_fromZ1850_parallel", "NTuple/Z1850")
    # RunStoppedMuons("Mu2E_1e7events_fromZ1850_parallel", "NTuple/LostInTarget_Ntuple")
    # RunStoppedMuons("Mu2E_1e7events_fromZ1850_parallel", "VirtualDetector/prestop")
    # RunStoppedMuons("Mu2E_1e7events_Absorber3.1_l90mm_r85mm_fromZ1850_parallel_noColl03", "NTuple/Z1850")
    # RunStoppedMuons("Mu2E_1e7events_Absorber3.1_l90mm_r85mm_fromZ1850_parallel_noColl03", "VirtualDetector/BeAbsorber_DetIn")
	# RunStoppedMuons("Mu2E_1e7events_Absorber3.1_l90mm_r85mm_fromZ1850_parallel_noColl03", "VirtualDetector/BeAbsorber_DetOut")

if __name__ == "__main__":
    main()

# # This is more involved than anticipated. 
# # Really need to know the exact geometry and it's not worth the effort!!!

# def BeamPath(df):

# 	# Parameters from TS_Collimators
# 	MECO_G4_xTrans=-(2.929+1.950/2.0)*1000
# 	MECO_G4_zTrans=(5.00+2.929)*1000

# 	# x, z positions in TS
# 	TS1_x = 0
# 	TS1_z = 3885
# 	TS3_x = 425+MECO_G4_xTrans
# 	TS3_z = 7929
# 	TS5_z = 11359
# 	TS5_x = -3904+MECO_G4_xTrans

# 	# Radii of the TS turns, based on collimator position 
# 	TSR_1 = np.sqrt( pow(TS3_x, 2) + pow(TS3_z - TS1_z, 2) )
# 	TSR_2 = np.sqrt( pow(TS5_x - TS3_x, 2) + pow(TS5_z - TS3_z, 2) )

# 	# Full path length of the "S" turn
# 	TSL_1 = np.pi * TSR_1
# 	TSL_2 = np.pi * TSR_2

# 	print(TSR_1, TSR_2)
# 	print(TSL_1, TSL_2)

# 	print("TS3_L = ", TS1_z + TSL_1)
# 	print("TS5_L = ", TS1_z + TSL_1 + TSL_2)
# 	print("ST_L = ", TS1_z + TSL_1 + TSL_2 + (13800 - TS5_z))


# 	# print(np.pi * abs(TS3_x))
# 	# print(np.pi * (TS3_z - TS1_z))
# 	# print(np.pi * (TS5_z - TS3_z))
# 	# print(np.pi * abs(TS5_x - TS3_x))

# 	# Mask DataFrame 
# 	# mask0 = df["InitZ"] <= TS1_z # PS 
# 	mask1 = (df["InitZ"] >= TS1_z) & (df["InitZ"] < TS3_z) # First TS turn
# 	mask2 = (df["InitZ"] >= TS3_z) & (df["InitZ"] < TS5_z) # Second TS turn
# 	mask3 = df["InitZ"] >= TS5_z # DS 

# 	# df_0 = df[mask0] # PS
# 	df_1 = df[mask1] # First TS turn
# 	df_2 = df[mask2] # Second TS turn
# 	df_3 = df[mask3] # DS

# 	# Calculate the angle of rotation around the curve
# 	# First turn, origin is at (TS1_x, TS1_z), phi is between R and x
# 	# Second turn, origin is at (TS3_x, TS5_z), phi is between R and z
# 	df["Phi"] = 0.0 
# 	# df_0["Phi"] = 0.0
# 	df_1["Phi"] = np.arctan2(df_1["InitZ"]-TS1_z, abs(TS3_x - df_1["InitX"])) 
# 	df_2["Phi"] = np.arctan2(abs(df_2["InitX"]-TS3_x), TS5_z - df_2["InitZ"])

# 	df_1["PhiDeg"] = (180/np.pi) * np.arctan2(df_1["InitZ"]-TS1_z, abs(TS3_x - df_1["InitX"])) 
# 	df_2["PhiDeg"] = (180/np.pi) * np.arctan2(abs(df_2["InitX"]-TS3_x), TS5_z - df_2["InitZ"])

# 	df_3["Phi"] = 0.0 

# 	# Get the radius of the turn
# 	df["TSRadius"] = 0.0
# 	# df_0["TSRadius"] = 0.0
# 	df_1["TSRadius"] = (df_1["InitZ"]-TS1_z) / np.sin(df_1["Phi"]) # abs(TS3_x - df_1["InitX"]) / np.cos(df_1["Phi"])
# 	df_2["TSRadius"] = (TS5_z-df_2["InitZ"]) / np.cos(df_2["Phi"]) # abs(df_2["InitX"]-TS3_x)) / np.sin(df_2["Phi"]) 
# 	df_3["TSRadius"] = 0.0

# 	# Calcuate the arc length of the circle, add it to z to form the beamline position, L
# 	df["InitL"] =  df["InitZ"]
# 	# df_0["InitL"] = df["InitZ"] # Just z
# 	df_1["InitL"] = ( df_1["TSRadius"] * df_1["Phi"] ) + TS1_z # Arc length plus TS1_z
# 	df_2["InitL"] = ( df_2["TSRadius"] * df_2["Phi"] ) + (TSL_1) + TS1_z # Arc length plus first turn plus
# 	df_3["InitL"] = ( df_3["InitZ"] - TS5_z) + (TS1_z + TSL_1 + TSL_2)

# 	print(df_1[:10])
# 	# print(df_2[:10])
# 	# print(df_3[:10])

# 	# unmask
# 	# df[mask0] = df_0
# 	df[mask1] = df_1
# 	# df[mask2] = df_2
# 	# df[mask3] = df_3

# 	# print(df["InitL"].max())

# 	return df

# 	# # print(df_1["PhiDeg"].max())
# 	# # print(df_2["PhiDeg"].max())

# 	# print(df_1[(df_1["InitZ"] >= TS3_z-1) & (df_1["InitZ"] <= TS3_z+1)]["PhiDeg"])
# 	# print(df_2[(df_2["InitZ"] >= TS3_z-1) & (df_2["InitZ"] <= TS3_z+1)]["PhiDeg"])

# 	# return df


# 	# # print(df_1["InitX"].max())
# 	# # print(df_2["InitX"].max()-TS3_x)

# 	# # Calculate the radius of the circle, use pythagoras
# 	# df["TSRadius"] = 0.0
# 	# df_1["TSRadius"] = np.sqrt( pow(df_1["InitX"]+TS3_x, 2) + pow(df_1["InitZ"]-TS1_z, 2) )
# 	# df_2["TSRadius"] = np.sqrt( pow(df_2["InitX"]+TS3_x, 2) + pow(df_1["InitZ"]-TS3_z, 2) )


# 	# return df


# 	# # Calcuate the arc length of the circle, add it to z
# 	# # Define "L", the path length
# 	# df["InitL"] = df["InitZ"]  
# 	# df_1["InitL"] =  ( df_1["TSRadius"] * df_1["Theta"] ) + TS1_z
# 	# df_2["InitL"] =  ( df_2["TSRadius"] * df_2["Theta"] ) + TS3_z

# 	# # # print(df_2[df_2["InitL"].isnan()])
# 	# print(df_1)
# 	# print(df_2)

# 	# df[mask1] = df_1
# 	# df[mask2] = df_2
	
# 	# return df

# 	# # Max path length along TS
# 	# TS5_l = df_2["InitL"].max()


# 	# print(TS5_l)
# 	# # Add this to initial Z minus the Z-length of the TS 
# 	# TS_z = TS5_z - TS1_z # length of the TS in z
# 	# df_3["InitL"] = df_3["InitZ"] + TS5_l - TS_z  

# 	# # Unmask
# 	# df[mask1] = df_1
# 	# df[mask2] = df_2
# 	# df[mask3] = df_3

# 	# return df

	# # Muons that do not stop
	# ut.Plot1D(df_nonStoppedMuons["P"], 250, 0, 250, r"$\mu^{-}$ that do not stop at "+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_muonsThatDoNotStopAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# # Pion parents that do not produce a stop 
	# ut.Plot1D(df_pionParentsThatDoNotProduceAStop["P"], 250, 0, 250, r"Parent $\pi^{-}$ that do not produce a stop at "+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_pionParentsThatDoNotProduceAStopAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False) 

	# # Stopped muon radial distribution at the plane of interest
	# ut.Plot1D(df_orphanStoppedMuons["R"], 200, 0, 200, r"Stopped $\mu^{-}$ at "+ntupleTitle , "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_rad_stoppedMuonsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# # All muons at plane of interest
	# ut.Plot1D(df_allMuons["R"], 250, 0, 250, r"$\mu^{-}$ at "+ntupleTitle , "Radial position [mm]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_rad_mu-_"+config+".png", "best", errors=True, peak=True, underOver=True) 
	# # All pions at plane of interest
	# ut.Plot1D(df_allPions["P"], 250, 0, 250, r"$\pi^{-}$ at "+ntupleTitle , "Radial position [mm]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_rad_pi-_"+config+".png", "best", errors=True, peak=True, underOver=False) 
	# # Stopped muon parent momentum distribution
	# # ut.Plot1D(df_stoppedMuonParents["R"], 250, 0, 250, r"Stopped $\mu^{-}$ parents at "+ntupleTitle , "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_rad_stoppedMuonsParentsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False)  
	# # Stopped muon parent pion momentum distribution
	# ut.Plot1D(df_stoppedMuonParentPions["R"], 200, 0, 200, r"Stopped $\mu^{-}$ parent $\pi^{-}$ at "+ntupleTitle , "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_rad_stoppedMuonsParentPionsAt"+ntupleName+"_"+config+".png", "best", errors=True, peak=True, underOver=False) 

	# ut.Plot2D(df_orphanStoppedMuons["P"], df_orphanStoppedMuons["R"], 50, 0, 250, 41, 0, 210, r"Stopped $\mu^{-}$ at "+ntupleTitle , "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_rad_vs_mom_stoppedMuonsAt"+ntupleName+"_"+config+".png") 
	# ut.Plot2D(df_stoppedMuonParentPions["P"], df_stoppedMuonParentPions["R"], 50, 0, 250, 41, 0, 210, r"Stopped $\mu^{-}$ parent $\pi^{-}$ at "+ntupleTitle , "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_rad_vs_mom_stoppedMuonsParentPionsAt"+ntupleName+"_"+config+".png") 

	# ut.Plot2D(df_allMuons["P"], df_allMuons["R"], 50, 0, 250, 41, 0, 210, r"$\mu^{-}$ at "+ntupleTitle , "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_rad_vs_mom_mu-At"+ntupleName+"_"+config+".png") 
	# ut.Plot2D(df_allPions["P"], df_allPions["R"], 50, 0, 250, 41, 0, 210, r"$\pi^{-}$ at "+ntupleTitle , "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_rad_vs_mom_pi-At"+ntupleName+"_"+config+".png") 

	# ut.Plot2D(df_muonsThatDoNotStop["P"], df_muonsThatDoNotStop["R"], 50, 0, 250, 41, 0, 210,r"Non-stopped $\mu^{-}$ at "+ntupleTitle, "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_rad_vs_mom_noStopMuonsAt"+ntupleName+"_"+config+".png") 
	# ut.Plot2D(df_pionParentsThatDoNotProduceAStop["P"], df_pionParentsThatDoNotProduceAStop["R"], 50, 0, 250, 41, 0, 210, r"Non-stopped $\mu^{-}$ parent $\pi^{-}$ at "+ntupleTitle, "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_rad_vs_mom_noStopPionParentsAt"+ntupleName+"_"+config+".png") 

	# # Overlays
	# ut.Plot1DOverlay([df_allMuons["P"], df_orphanStoppedMuons["P"]], 700, 0, 700, title = r"$\mu^{-}$ at "+ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = ["All $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_mu-OverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)
	# ut.Plot1DOverlay([df_allPions["P"], df_stoppedMuonParentPions["P"]], 1400, 0, 1400, title = r"$\pi^{-}$ at "+ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = ["All $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$  "], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_pi-OverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)

	# ut.Plot1DOverlay([df_allMuons["R"], df_orphanStoppedMuons["R"]], 250, 0, 250, title = r"$\mu^{-}$ at "+ntupleTitle, xlabel = "Radial position [mm]", ylabel = "Counts / mm", labels = ["All $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_rad_mu-OverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)
	# ut.Plot1DOverlay([df_allPions["R"], df_stoppedMuonParentPions["R"]], 250, 0, 250, title = r"$\pi^{-}$ at "+ntupleTitle, xlabel = "Radial position [mm]", ylabel = "Counts / mm", labels = ["All $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$  "], fout = "../img/"+g4blVer+"/StoppedMuons/h1_rad_pi-OverlayAt"+ntupleName+"_"+config+".png") # , includeBlack=False)


	# return

	# # Get stopped muons
	# # df_orphanStoppedMuons = ut.FilterParticles(df_orphanStops, "mu-") 

	# # Identify rows in df_orphanStops that are not in df_stops
	# # df_erroneousOrphanStops = df_orphanStops[~df_orphanStops.isin(df_stops)].dropna()

	# # ----------- Non-stopped muons -----------

	# df_poststopMuons = ut.FilterParticles(df_poststop, "mu-") # Muons that exit the ST

	# # ----------- Extrapolate non-stops to plane of interest -----------

	# # Orphaned non-stopping muons
	# df_orphanNonStops = df_ntuple.merge(df_poststop, on=["EventID", "TrackID", "ParentID", "PDGid"], suffixes=("", "_atST"), how="inner") 
	# df_orphanNonStops = df_orphanNonStops[df_ntuple.columns]
	# df_orphanNonStoppedMuons = ut.FilterParticles(df_orphanNonStops, "mu-")

	# # Find non-stopped particle parents
	# df_nonStopsAndTheirParents = df_ntuple.merge(df_poststop, left_on=["EventID", "TrackID"], right_on=["EventID", "ParentID"], suffixes=("", "_child"), how="inner")
	# df_nonStoppedMuonsAndTheirParents = df_ntuple.merge(df_poststopMuons, left_on=["EventID", "TrackID"], right_on=["EventID", "ParentID"], suffixes=("", "_child"), how="inner")
	
	# # Technically you don't need these, but it makes it a bit easier
	# df_nonStopsParents = df_nonStopsAndTheirParents[df_ntuple.columns]
	# df_nonStoppedMuonParents = df_nonStoppedMuonsAndTheirParents[df_ntuple.columns]
	# df_nonStoppedMuonParentPions = ut.FilterParticles(df_nonStoppedMuonParents, "pi-") 

	# # Store info 
	# stoppingDict = {

	# 				"Info" : [
	# 					"All stops", 
	# 					"Orphan stops at "+ntupleName,
	# 					"Parents of stops at "+ntupleName,
	# 					"Stops - (Orphans + Parents) at "+ntupleName,
	# 					"---",
	# 					"Stopped muons", 
	# 					"Orphaned stopped muons at "+ntupleName,
	# 					"Stopped muon parents at "+ntupleName,
	# 					"Stops - (Orphans + Parents) at "+ntupleName
	# 				], 

	# 				"Count" : [
	# 					df_stops.shape[0],
	# 					df_orphanStops.shape[0],
	# 					df_stopsParents.shape[0],
	# 					df_stops.shape[0] - (df_orphanStops.shape[0]+df_stopsParents.shape[0]),
	# 					"---",
	# 					df_stoppedMuons.shape[0],
	# 					df_orphanStoppedMuons.shape[0],
	# 					df_stoppedMuonParentPions.shape[0],
	# 					df_stoppedMuons.shape[0] - (df_orphanStoppedMuons.shape[0]+df_stoppedMuonParents.shape[0])
	# 				]
	# 			}

	# # print(df_orphanStoppedMuons)

	# stoppingDict = pd.DataFrame(stoppingDict)

	# print(stoppingDict)

	# # print("\n---> All stops:", df_stops.shape[0])
	# # print("---> Orphan stops at", ntupleName, ":", df_orphanStops.shape[0])
	# # print("---> Stops with parents at", ntupleName, ":", df_stopsParents.shape[0]) 

	# # print("---> Stopped muons:", df_stoppedMuons.shape[0])
	# # print("---> Orphan stopped muons at", ntupleName, ":", df_orphanStoppedMuons.shape[0])
	# # print("---> Stopped muon parents at", ntupleName, ":", df_stoppedMuonParents.shape[0]) 

	# # print("---> Stopped muon orphans + parents ", df_orphanStoppedMuons.shape[0]+df_stoppedMuonParents.shape[0])

	# # # How is this possible? 
	# # print("---> Odd extra muon orphans + parents? Some of it is due to duplicates at zntuple but not all:", df_orphanStoppedMuons.shape[0]+df_stoppedMuonParents.shape[0]-df_stoppedMuons.shape[0])

	# return
	
	# # Filter muons and pions at this detector
	# df_allMuons = ut.FilterParticles(df_ntuple, "mu-")
	# df_allPions = ut.FilterParticles(df_ntuple, "pi-")

	# # Muons that do not stop?
	# # df_allMuons not in df_allMuons
	# # df_allPions not in df_stoppedMuonParentPions

	# # More interesting to look at the ones that reach the stopping target and do not stop!!!

	# # Use a left join
	# # df_muonsThatDoNotStop = df_allMuons.merge(df_orphanStoppedMuons, on=["EventID", "TrackID"], suffixes=("", "_stopped"), how="left")
	# # Filter rows where columns from df_orphanStoppedMuons are null
	# # df_muonsThatDoNotStop = df_muonsThatDoNotStop[df_muonsThatDoNotStop["x_stopped"].isnull()] 

	# # Muons that exit the ST
	# df_poststopMuons = ut.FilterParticles(df_poststop, "mu-")

	# # Orphaned non-stopping muons
	# df_orphanNonStops = df_ntuple.merge(df_poststop, on=["EventID", "TrackID", "ParentID", "PDGid"], suffixes=("", "_atST"), how="inner") 
	# df_orphanNonStops = df_orphanNonStops[df_ntuple.columns]
	# df_orphanNonStoppedMuon = ut.FilterParticles(df_orphanNonStops, "mu-")

	# # Non-stop parents
	# df_nonStopsAndTheirParents = df_ntuple.merge(df_poststop, left_on=["EventID", "TrackID"], right_on=["EventID", "ParentID"], suffixes=("", "_child"), how="inner")
	# df_nonStopsAndTheirParents = df_nonStopsAndTheirParents[df_ntuple.columns]

	# # Non-stopped muon parents
	# df_nonStoppedMuonsAndTheirParents = df_ntuple.merge(df_poststopMuons, left_on=["EventID", "TrackID"], right_on=["EventID", "ParentID"], suffixes=("", "_child"), how="inner")
	# df_nonStoppedMuonParents = df_nonStopsAndTheirParents[df_ntuple.columns]

	# # Non-stop parent pions
	# df_nonStoppedMuonParentPions = ut.FilterParticles(df_nonStoppedMuonParents, "pi-")

	# # Particles from plane that exit the ST 
	# # df_nonStoppedMuons = ut.FilterParticles(df_nonStopsAndTheirParents, "mu-")
	# # df_nonStoppedParentPions = ut.FilterParticles(df_nonStopsAndTheirParents, "mu-")

	# # df_nonStops = df_ntuple.merge(df_poststop, on=["EventID", "TrackID", "ParentID", "PDGid"], suffixes=("", "_poststop"), how="inner") 
	# # df_nonStops = df_nonStops(df_ntuple.columns)

	# # Muons from plane that exit the ST 
	# # df_nonStoppedMuons = ut.FilterParticles(df_nonStops, "mu-")
	# # Pions from plane that exit the ST
	# # df_nonStoppedParentPions = ut.FilterParticles(df_nonStops, "mu-")

	# # # Use a left join
	# # df_pionParentsThatDoNotProduceAStop = df_allPions.merge(df_stoppedMuonParentPions, on=["EventID", "TrackID"], suffixes=("", "_stopped"), how="left")
	# # # Filter rows where columns from df_orphanStoppedMuons are null
	# # df_pionParentsThatDoNotProduceAStop = df_pionParentsThatDoNotProduceAStop[df_pionParentsThatDoNotProduceAStop["x_stopped"].isnull()] 

	# ut.BarChart(df_stops["PDGid"], ut.latexParticleDict, "All stops", "", "Percentage / particle", fout="../img/"+g4blVer+"/StoppedMuons/bar_Stops_"+config+".png", percentage=True)
	# ut.BarChart(df_stopsParents["PDGid"], ut.latexParticleDict, "Stopped particle parents", "", "Percentage / particle", fout="../img/"+g4blVer+"/StoppedMuons/bar_StopParents_"+config+".png", percentage=True)
	# ut.BarChart(df_stoppedMuons["PDGid"], ut.latexParticleDict, r"Stopped $\mu^{-}$", "", "Percentage / particle", fout="../img/"+g4blVer+"/StoppedMuons/bar_StoppedMuons_"+config+".png", percentage=True)
	# ut.BarChart(df_orphanStoppedMuons["PDGid"], ut.latexParticleDict, r"Orphan stopped $\mu^{-}$", "", "Percentage / particle", fout="../img/"+g4blVer+"/StoppedMuons/bar_OrphanStoppedMuons_"+config+".png", percentage=True)
	# ut.BarChart(df_stoppedMuonParents["PDGid"], ut.latexParticleDict, r"Stopped $\mu^{-}$ parents", "", "Percentage / particle", fout="../img/"+g4blVer+"/StoppedMuons/bar_StoppedMuonParents_"+config+".png", percentage=True)

	# # Annotated initial z-position for stopped muons 
	# Plot1DAnnotated(df_stoppedMuons["InitZ"]/1e3, 143, 0, 14.3, "", "Initial z-position [m]", r"Stopped $\mu^{-}$ / 100 mm", "../img/"+g4blVer+"/StoppedMuons/h1_InitZ_annotated_stoppedMuons_"+config+".png", "upper right", stats=False, errors=False) 

	# return
	
	# return

	# # Get the parents at the plane of interest
	# df_stoppedMuonParentMuons = df_stoppedMuonsAndTheirParents[df_ntuple.columns]
	# # Orphaned stopped muons 
	# df_orphans = df_ntuple.merge(df_stoppedMuons, on=["EventID", "TrackID", "ParentID", "PDGid"], suffixes=("", "_atST")) # , right_on=["EventID", "TrackID"], suffixes=("_start", "_stop"))
	# df_orphanStoppedMuons = df_orphans[df_ntuple.columns]


	# # print("\n---> Stopped muons:", df_stoppedMuons.shape[0])
	# # print("---> Other stops:", df_stops[df_stops["PDGid"]!=13].shape[0])
	# print("---> Stopped muons and their parents", df_stoppedMuonsAndTheirParents.shape[0]) 
	# print("---> Stopped muon parents at", ntupleName, ":", df_stoppedMuonParentMuons.shape[0]) 
	# print("---> Orpaned stopped muons at", ntupleName, ":", df_orphanStoppedMuons.shape[0]) 
	# print("---> Orpaned stopped muons not at", ntupleName, ":", df_orphans.shape[0] - df_orphanStoppedMuons.shape[0]) 

	# # print("---> Stopped pions?", ntupleName, ":", df_stoppedMuons.shape[0] - (df_stoppedMuonParentMuons.shape[0] + df_orphanStoppedMuons.shape[0]))
	# # print("---> Stopped pions?", ntupleName, ":", df_stops[df_stops["PDGid"]==-211].shape[0] ) 

	# print(df_stoppedMuons[:5]) 
	# print(df_stoppedMuonParentMuons[:5])
	# # print(df_stoppedMuonParentMuons[df_stoppedMuonParentMuons["PDGid"] != -211][:5])
	# print(df_orphanStoppedMuons[:5])

	# # df_children_and_parents = df_stoppedMuons.merge(df_ntuple, left_on=["EventID", "ParentID"], right_on=["EventID", "TrackID"], suffixes=("_child", "_parent"))

	# # Write the df to csv for debugging
	# # print(df_children_and_parents[:10])
	# # csvName = "../txt/"+g4blVer+"/g4beamline_StoppedMuons_parents_and_children.csv" 
	# # df_children_and_parents[:10].to_csv(csvName, index=False) 
	# # csvName = "../txt/"+g4blVer+"/g4beamline_StoppedMuons_orphans.csv" 
	# # df_orphans[:10].to_csv(csvName, index=False) 

	# # print("\n---> Written csv to", csvName)

	# # print(df_children_and_parents["PDGid_parent"])

	# # print(df_children_and_parents["PDGid_parent"])
	# # print(df_children_and_parents["PDGid_child"])

	# # Stopped muon momentum distribution
	# ut.Plot1D(df_stoppedMuons["P"], 100, 0, 100, r"Stopped $\mu^{-}$" , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuons_"+config+".png", "best", errors=True, peak=True) 
	# # Annotated initial z-position 
	# Plot1DAnnotated(df_stoppedMuons["InitZ"]/1e3, 143, 0, 14.3, "", "Initial z position [m]", r"Stopped $\mu^{-}$ / 100 mm", "../img/"+g4blVer+"/StoppedMuons/h1_InitZ_annotated_stoppedMuons_"+config+".png", "upper right", stats=False, errors=False) 


	# return



	# # It does make sense that they would all come from pions, with a couple of exotic decays
	# # , no this doesn't make any sense. why would they have a parent ID equal to the track ID. ParentId would equal parent ID and trackID trackID (some of them are really the same muons)
	# # Do you really need this? Seems a bit messy
	# # 
	# df_stoppedMuonParentMuons = ut.FilterParticles(df_children_and_parents, "mu-")
	# df_stoppedMuonParentPions = ut.FilterParticles(df_children_and_parents, "pi-")

	# print(df_stoppedMuonParentMuons)
	# # print(df_stoppedMuonParentPions.shape[0])

	# # Filter muons and pions at this detector
	# df_allMuons = ut.FilterParticles(df_ntuple, "mu-")
	# df_allPions = ut.FilterParticles(df_ntuple, "pi-")

	# # Total momentum
	# # df_allMuons["P"] = np.sqrt( pow(df_allMuons["Px"],2) + pow(df_allMuons["Py"],2) + pow(df_allMuons["Pz"],2) ) 
	# # df_allPions["P"] = np.sqrt( pow(df_allPions["Px"],2) + pow(df_allPions["Py"],2) + pow(df_allPions["Pz"],2) ) 
	# # df_stoppedMuonParentMuons["P"] = np.sqrt( pow(df_stoppedMuonParentMuons["Px"],2) + pow(df_stoppedMuonParentMuons["Py"],2) + pow(df_stoppedMuonParentMuons["Pz"],2) ) 
	# # df_stoppedMuonParentPions["P"] = np.sqrt( pow(df_stoppedMuonParentPions["Px"],2) + pow(df_stoppedMuonParentPions["Py"],2) + pow(df_stoppedMuonParentPions["Pz"],2) ) 

	# # Radius
	# # df_allMuons["R"] = np.sqrt( pow(df_allMuons["x"],2) + pow(df_allMuons["y"],2) ) 
	# # df_allPions["R"] = np.sqrt( pow(df_allPions["x"],2) + pow(df_allPions["y"],2) ) 
	# # df_stoppedMuonParentMuons["R"] = np.sqrt( pow(df_stoppedMuonParentMuons["x"],2) + pow(df_stoppedMuonParentMuons["y"],2) ) 
	# # df_stoppedMuonParentPions["R"] = np.sqrt( pow(df_stoppedMuonParentPions["x"],2) + pow(df_stoppedMuonParentPions["y"],2) ) 

	# # Compare muons with stopped muons at this detector

	# # Momentum
	# ut.Plot1D(df_allMuons["P"], 200, 0, 200, r"$\mu^{-}$"+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_mu-_"+ntupleName+"_"+config+".png", "best", errors=False) 
	# ut.Plot1D(df_stoppedMuonParentMuons["P"], 200, 0, 200, r"Stopped $\mu^{-}$"+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuons_"+ntupleName+"_"+config+".png", "best", errors=False) 
	# ut.Plot1DOverlay([df_allMuons["P"], df_stoppedMuonParentMuons["P"]], nbins=500, xmin=0, xmax=500, title = r"$\mu^{-}$"+ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = ["All $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonOverlay_"+ntupleName+"_"+config+".png") # , includeBlack=False)
	# # Radius 
	# ut.Plot1D(df_allMuons["R"], 250, 0, 250, r"$\mu^{-}$"+ntupleTitle , "Radius [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_R_mu-_"+ntupleName+"_"+config+".png", "best", errors=False) 
	# ut.Plot1D(df_stoppedMuonParentMuons["R"], 250, 0, 250, r"Stopped $\mu^{-}$"+ntupleTitle , "Radius [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_R_stoppedMuons_"+ntupleName+"_"+config+".png", "best", errors=False) 
	# ut.Plot1DOverlay([df_allMuons["R"], df_stoppedMuonParentMuons["R"]], nbins=250, xmin=0, xmax=250, title = r"$\mu^{-}$"+ntupleTitle, xlabel = "Radius [mm]", ylabel = "Counts / mm", labels = ["All $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_R_stoppedMuonOverlay_"+ntupleName+"_"+config+".png") # , includeBlack=False)
	# # Radius vs momentum 
	# ut.Plot2D(df_allMuons["P"], df_allMuons["R"], 50, 0, 250, 42, 0, 210, r"$\mu^{-}$"+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_RvsMom_mu-_"+ntupleName+"_"+config+".png")
	# ut.Plot2D(df_stoppedMuonParentMuons["P"], df_stoppedMuonParentMuons["R"], 50, 0, 250, 42, 0, 210, r"Stopped $\mu^{-}$"+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_RvsMom_stoppedMuons_"+ntupleName+"_"+config+".png")

	# # Compare pions with stopped muon parent pions at this detector

	# # Momentum
	# ut.Plot1D(df_allPions["P"], 200, 0, 200, r"$\pi^{-}$"+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_pi-_"+ntupleName+"_"+config+".png", "best", errors=False) 
	# ut.Plot1D(df_stoppedMuonParentPions["P"], 200, 0, 200, r"Stopped $\mu^{-}$ parent $\pi^{-}$"+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonParentPi-_"+ntupleName+"_"+config+".png", "best", errors=False) 
	# ut.Plot1DOverlay([df_allPions["P"], df_stoppedMuonParentPions["P"]], nbins=500, xmin=0, xmax=500, title = r"$\pi^{-}$"+ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = ["All $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonParentPionOverlay_"+ntupleName+"_"+config+".png") # , includeBlack=False)
	# # Radius 
	# ut.Plot1D(df_allPions["R"], 250, 0, 250, r"$\pi^{-}$"+ntupleTitle , "Radius [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_R_pi-_"+ntupleName+"_"+config+".png", "best", errors=False) 
	# ut.Plot1D(df_stoppedMuonParentPions["R"], 250, 0, 250, r"Stopped $\mu^{-}$ parent $\pi^{-}$"+ntupleTitle , "Radius [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_R_stoppedMuonsParentPi-_"+ntupleName+"_"+config+".png", "best", errors=False) 
	# ut.Plot1DOverlay([df_allPions["R"], df_stoppedMuonParentPions["R"]], nbins=250, xmin=0, xmax=250, title = r"$\pi^{-}$"+ntupleTitle, xlabel = "Radius [mm]", ylabel = "Counts / mm", labels = ["All $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_R_stoppedMuonParentPionOverlay_"+ntupleName+"_"+config+".png") # , includeBlack=False)
	# # Radius vs momentum 
	# ut.Plot2D(df_allPions["P"], df_allPions["R"], 50, 0, 250, 42, 0, 210, r"$\pi^{-}$"+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_RvsMom_pi-_"+ntupleName+"_"+config+".png")
	# ut.Plot2D(df_stoppedMuonParentPions["P"], df_stoppedMuonParentPions["R"], 50, 0, 250, 42, 0, 210, r"Stopped $\mu^{-}$ parent $\pi^{-}$"+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_RvsMom_stoppedMuonsParentPi-_"+ntupleName+"_"+config+".png")

	# return

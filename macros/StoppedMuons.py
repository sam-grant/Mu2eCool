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

def Plot1DAnnotated(data, nBins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", legPos="best", stats=True, peak=False, underOver=False, errors=False, NDPI=300):
    
	# Create figure and axes
	fig, ax = plt.subplots()

	# Plot the histogram with outline
	counts, bin_edges, _ = ax.hist(data, bins=nBins, range=(xmin, xmax), histtype='step', edgecolor='black', linewidth=1.0, fill=False, density=False)

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

	ax.set_title(title, fontsize=16, pad=10)
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
	ax.axvline(x=1764.5, color='gray', linestyle='--', linewidth=1) # PT
	ax.axvline(x=3885, color='gray', linestyle='--', linewidth=1) # TS1
	ax.axvline(x=7929, color='gray', linestyle='--', linewidth=1) # TS3
	ax.axvline(x=11359, color='gray', linestyle='--', linewidth=1) # TS5
	ax.axvline(x=13800, color='gray', linestyle='--', linewidth=1) # ST
	# ax.axvline(x=17964, color='gray', linestyle='--', linewidth=1) # Tracker
	# ax.axvline(x=20394, color='gray', linestyle='--', linewidth=1) # Calo

	plt.annotate("PT",
		xy=(1764.5, plt.ylim()[1]),  # Position of the label
		xytext=(10, 10),  # Offset of the label from the point
		textcoords='offset points',  # Specify offset in points
		va='bottom',  # Vertical alignment of the label
		ha='right',  # Horizontal alignment of the label
		color='gray',  # Color of the label text
		fontsize=14,  # Font size of the label text
		rotation='vertical')  # Rotate the label
	plt.annotate("TS1",
		xy=(3885, plt.ylim()[1]),  
		xytext=(10, 10),  
		textcoords='offset points',  
		va='bottom',  
		ha='right', 
		color='gray', 
		fontsize=14,  # Font size of the label text
		rotation='vertical')  # Rotate the label
	plt.annotate("TS3",
		xy=(7929, plt.ylim()[1]),  
		xytext=(10, 10),  
		textcoords='offset points',  
		va='bottom',  
		ha='right', 
		color='gray', 
		fontsize=14,  # Font size of the label text
	rotation='vertical')  # Rotate the label
	plt.annotate("TS5",
		xy=(11359, plt.ylim()[1]),  
		xytext=(10, 10),  
		textcoords='offset points',  
		va='bottom',  
		ha='right', 
		color='gray', 
		fontsize=14,  # Font size of the label text
		rotation='vertical')  # Rotate the label
	plt.annotate("ST",
		xy=(13800, plt.ylim()[1]),  
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

def BeamPath(df):

	# Parameters from TS_Collimators
	MECO_G4_xTrans=-(2.929+1.950/2.0)*1000
	MECO_G4_zTrans=(5.00+2.929)*1000

	# x, z positions in TS
	TS1_x = 0
	TS1_z = 3885
	TS3_x = 425+MECO_G4_xTrans
	TS3_z = 7929
	TS5_z = 11359
	TS5_x = -3904+MECO_G4_xTrans

	# Mask DataFrame 
	mask1 = (df["InitZ"] > TS1_z) & (df["InitZ"] <= TS3_z)
	mask2 = (df["InitZ"] > TS3_z) & (df["InitZ"] < TS5_z)

	df_1 = df[mask1] # First turn
	df_2 = df[mask2] # Second turn

	# Calculate the angle between Z and X, theta
	df["Theta"] = 0.0
	df_1["Theta"] = np.arctan2(df_1["InitZ"]-TS1_z, df_1["InitX"]-TS3_x)  
	df_2["Theta"] = np.arctan2(df_2["InitZ"]-TS3_z, df_2["InitX"]-TS3_x) 

	# Calculate the radius of the circle, use pythagoras
	df["TSRadius"] = 0.0
	df_1["TSRadius"] = np.sqrt( pow(df_1["InitX"]-TS3_x, 2) + pow(df_1["InitZ"]-TS1_z, 2) )
	df_2["TSRadius"] = np.sqrt( pow(df_2["InitX"]-TS3_x, 2) + pow(df_1["InitZ"]-TS3_z, 2) )

	# Calcuate the arc length of the circle, add it to z
	# Define "L", the path length
	df["InitL"] = df["InitZ"]  
	df_1["InitL"] =  ( df_1["TSRadius"] * df_1["Theta"] ) + TS1_z
	df_2["InitL"] =  ( df_2["TSRadius"] * df_2["Theta"] ) + TS3_z

	# Unmask
	df[mask1] = df_1
	df[mask2] = df_2

	# TODO:

	# Also need to add the max path length to all the other InitZ!

	# Also adjust x coordinate ...
	# df[df["InitX"] < -250 = 

	return df

def RunStoppedMuons(config, ntupleName): 

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

    df_prestop = ut.TTreeToDataFrame(finName, "VirtualDetector/prestop", ut.branchNamesExtended)
    df_LostInTarget = ut.TTreeToDataFrame(finName, "NTuple/LostInTarget_Ntuple", ut.branchNamesExtended)

    # Stopped muons: muons which are present in prestop and LostInTarget
    # Add the "UniqueID" column sto df_prestop and df_LostInTarget, get the common tracks
    df_prestop['UniqueID'] = 1e6*df_prestop['EventID'] + 1e3*df_prestop['TrackID'] + df_prestop['ParentID'] 
    df_LostInTarget['UniqueID'] = 1e6*df_LostInTarget['EventID'] + 1e3*df_LostInTarget['TrackID'] + df_LostInTarget['ParentID']
    df_stoppedMuons = df_prestop[df_prestop['UniqueID'].isin(df_LostInTarget['UniqueID'])] 

    df_stoppedMuons = ut.FilterParticles(df_stoppedMuons, "mu-")
    df_prestopMuons = ut.FilterParticles(df_prestop, "mu-")

    # Get position coordinates in beam reference frame
    df_stoppedMuons = BeamPath(df_stoppedMuons)
    df_prestopMuons = BeamPath(df_prestopMuons)

    # Momentum
    df_stoppedMuons["P"] = np.sqrt( pow(df_stoppedMuons["Px"],2) + pow(df_stoppedMuons["Py"],2) + pow(df_stoppedMuons["Pz"],2) ) 
    df_prestopMuons["P"] = np.sqrt( pow(df_prestopMuons["Px"],2) + pow(df_prestopMuons["Py"],2) + pow(df_prestopMuons["Pz"],2) ) 

    # Initial radius
    # df_stoppedMuons["InitR"] = np.sqrt( pow(df_stoppedMuons["InitX"],2) + pow(df_stoppedMuons["InitY"],2) ) # + pow(df_stoppedMuons["Pz"],2) ) 

    ut.Plot1D(df_stoppedMuons["P"], 100, 0, 100, r"Stopped $\mu^{-}$" , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuons_"+config+".png", "best", errors=False) 
    # ut.Plot2D(df_stoppedMuons["InitZ"], df_stoppedMuons["Theta"], 143, 0, 14300, int(np.pi), -np.pi/2, np.pi/2, r"Stopped $\mu^{-}$" , "Initial z [mm]", "Theta [rad]", "../img/"+g4blVer+"/StoppedMuons/h2_InitZvsTheta_stoppedMuons_"+config+".png") 
    # ut.Plot1D(df_prestopMuons["P"], 100, 0, 100, r"$\mu^{-}$ entering ST" , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_prestopMuons_"+config+".png", "upper right", errors=False) 
    # ut.Plot1D(df_stoppedMuons["InitZ"], 143, 0, 14300, r"Stopped $\mu^{-}$" , "Initial z [mm]", "Counts / 100 mm", "../img/"+g4blVer+"/StoppedMuons/h1_InitZ_stoppedMuons_"+config+".png", "upper right", errors=False) 
    # ut.Plot1D(df_stoppedMuons["InitX"], 1000, -500, 500, r"Stopped $\mu^{-}$" , "Initial x [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_InitX_stoppedMuons_"+config+".png", "upper right", errors=False) 
    # ut.Plot1D(df_stoppedMuons["InitY"], 500, -250, 250, r"Stopped $\mu^{-}$" , "Initial y [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_InitY_stoppedMuons_"+config+".png", "upper left", errors=False) 
    # ut.Plot1D(df_stoppedMuons["InitR"], 10000, 0, 10000, r"Stopped $\mu^{-}$" , "Initial radius [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_InitR_stoppedMuons_"+config+".png", "upper right", errors=False) 

    # Annotated
    Plot1DAnnotated(df_stoppedMuons["InitL"], 143, 0, 14300, "", "Initial position [mm]", "Counts / 100 mm", "../img/"+g4blVer+"/StoppedMuons/h1_InitL_annotated_stoppedMuons_"+config+".png", "upper right", stats=False, errors=False) 
    Plot1DAnnotated(df_prestopMuons["InitL"], 143, 0, 14300, "", "Initial position [mm]", "Counts / 100 mm", "../img/"+g4blVer+"/StoppedMuons/h1_InitL_annotated_prestopMuons_"+config+".png", "upper right", stats=False, errors=False) 
    
    # What about my cold pions? 

	# Find pion parents for stopped muons, these should all be produced at the PT
    df_ntuple = ut.TTreeToDataFrame(finName, ntupleName, ut.branchNamesExtended)

    # Titles and names
    ntupleName = ntupleName.split("/")[1] 
    ntupleTitle = ", "+ntupleName
    if ntupleName[0] == "Z": ntupleTitle = ", Z = "+ntupleName[1:]+" mm"

    # Merge dataframes
    # look for rows in df_"+ntupleName+" that have the same EventID as df_stoppedMuons, and also have a TrackID which is equal to ParentID in df_stoppedMuons.
    df_stoppedMuonParents = df_ntuple.merge(df_stoppedMuons, left_on=["EventID", "TrackID"], right_on=["EventID", "ParentID"], suffixes=("", "_stoppedMuons"))
    
    # Filter particles of "parents" (some of them are really the same muons)
    df_stoppedMuonParentMuons = ut.FilterParticles(df_stoppedMuonParents, "mu-")
    df_stoppedMuonParentPions = ut.FilterParticles(df_stoppedMuonParents, "pi-")

    # Filter muons and pions at this detector
    df_allMuons = ut.FilterParticles(df_ntuple, "mu-")
    df_allPions = ut.FilterParticles(df_ntuple, "pi-")

    # Total momentum
    df_allMuons["P"] = np.sqrt( pow(df_allMuons["Px"],2) + pow(df_allMuons["Py"],2) + pow(df_allMuons["Pz"],2) ) 
    df_allPions["P"] = np.sqrt( pow(df_allPions["Px"],2) + pow(df_allPions["Py"],2) + pow(df_allPions["Pz"],2) ) 
    df_stoppedMuonParentMuons["P"] = np.sqrt( pow(df_stoppedMuonParentMuons["Px"],2) + pow(df_stoppedMuonParentMuons["Py"],2) + pow(df_stoppedMuonParentMuons["Pz"],2) ) 
    df_stoppedMuonParentPions["P"] = np.sqrt( pow(df_stoppedMuonParentPions["Px"],2) + pow(df_stoppedMuonParentPions["Py"],2) + pow(df_stoppedMuonParentPions["Pz"],2) ) 

    # Radius
    df_allMuons["R"] = np.sqrt( pow(df_allMuons["x"],2) + pow(df_allMuons["y"],2) ) 
    df_allPions["R"] = np.sqrt( pow(df_allPions["x"],2) + pow(df_allPions["y"],2) ) 
    df_stoppedMuonParentMuons["R"] = np.sqrt( pow(df_stoppedMuonParentMuons["x"],2) + pow(df_stoppedMuonParentMuons["y"],2) ) 
    df_stoppedMuonParentPions["R"] = np.sqrt( pow(df_stoppedMuonParentPions["x"],2) + pow(df_stoppedMuonParentPions["y"],2) ) 

    # Compare muons with stopped muons at this detector

    # Momentum
    ut.Plot1D(df_allMuons["P"], 200, 0, 200, r"$\mu^{-}$"+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_mu-_"+ntupleName+"_"+config+".png", "best", errors=False) 
    ut.Plot1D(df_stoppedMuonParentMuons["P"], 200, 0, 200, r"Stopped $\mu^{-}$"+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuons_"+ntupleName+"_"+config+".png", "best", errors=False) 
    ut.Plot1DOverlay([df_allMuons["P"], df_stoppedMuonParentMuons["P"]], nbins=500, xmin=0, xmax=500, title = r"$\mu^{-}$"+ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = ["All $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonOverlay_"+ntupleName+"_"+config+".png") # , includeBlack=False)
    # Radius 
    ut.Plot1D(df_allMuons["R"], 250, 0, 250, r"$\mu^{-}$"+ntupleTitle , "Radius [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_R_mu-_"+ntupleName+"_"+config+".png", "best", errors=False) 
    ut.Plot1D(df_stoppedMuonParentMuons["R"], 250, 0, 250, r"Stopped $\mu^{-}$"+ntupleTitle , "Radius [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_R_stoppedMuons_"+ntupleName+"_"+config+".png", "best", errors=False) 
    ut.Plot1DOverlay([df_allMuons["R"], df_stoppedMuonParentMuons["R"]], nbins=250, xmin=0, xmax=250, title = r"$\mu^{-}$"+ntupleTitle, xlabel = "Radius [mm]", ylabel = "Counts / mm", labels = ["All $\mu^{-}$", r"Stopped $\mu^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_R_stoppedMuonOverlay_"+ntupleName+"_"+config+".png") # , includeBlack=False)
    # Radius vs momentum 
    ut.Plot2D(df_allMuons["P"], df_allMuons["R"], 50, 0, 250, 42, 0, 210, r"$\mu^{-}$"+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_RvsMom_mu-_"+ntupleName+"_"+config+".png")
    ut.Plot2D(df_stoppedMuonParentMuons["P"], df_stoppedMuonParentMuons["R"], 50, 0, 250, 42, 0, 210, r"Stopped $\mu^{-}$"+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_RvsMom_stoppedMuons_"+ntupleName+"_"+config+".png")
   
    # Compare pions with stopped muon parent pions at this detector

    # Momentum
    ut.Plot1D(df_allPions["P"], 200, 0, 200, r"$\pi^{-}$"+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_pi-_"+ntupleName+"_"+config+".png", "best", errors=False) 
    ut.Plot1D(df_stoppedMuonParentPions["P"], 200, 0, 200, r"Stopped $\mu^{-}$ parent $\pi^{-}$"+ntupleTitle , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonParentPi-_"+ntupleName+"_"+config+".png", "best", errors=False) 
    ut.Plot1DOverlay([df_allPions["P"], df_stoppedMuonParentPions["P"]], nbins=500, xmin=0, xmax=500, title = r"$\pi^{-}$"+ntupleTitle, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = ["All $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_mom_stoppedMuonParentPionOverlay_"+ntupleName+"_"+config+".png") # , includeBlack=False)
    # Radius 
    ut.Plot1D(df_allPions["R"], 250, 0, 250, r"$\pi^{-}$"+ntupleTitle , "Radius [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_R_pi-_"+ntupleName+"_"+config+".png", "best", errors=False) 
    ut.Plot1D(df_stoppedMuonParentPions["R"], 250, 0, 250, r"Stopped $\mu^{-}$ parent $\pi^{-}$"+ntupleTitle , "Radius [mm]", "Counts / mm", "../img/"+g4blVer+"/StoppedMuons/h1_R_stoppedMuonsParentPi-_"+ntupleName+"_"+config+".png", "best", errors=False) 
    ut.Plot1DOverlay([df_allPions["R"], df_stoppedMuonParentPions["R"]], nbins=250, xmin=0, xmax=250, title = r"$\pi^{-}$"+ntupleTitle, xlabel = "Radius [mm]", ylabel = "Counts / mm", labels = ["All $\pi^{-}$", r"Stopped $\mu^{-}$ parent $\pi^{-}$"], fout = "../img/"+g4blVer+"/StoppedMuons/h1_R_stoppedMuonParentPionOverlay_"+ntupleName+"_"+config+".png") # , includeBlack=False)
    # Radius vs momentum 
    ut.Plot2D(df_allPions["P"], df_allPions["R"], 50, 0, 250, 42, 0, 210, r"$\pi^{-}$"+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_RvsMom_pi-_"+ntupleName+"_"+config+".png")
    ut.Plot2D(df_stoppedMuonParentPions["P"], df_stoppedMuonParentPions["R"], 50, 0, 250, 42, 0, 210, r"Stopped $\mu^{-}$ parent $\pi^{-}$"+ntupleTitle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/StoppedMuons/h2_RvsMom_stoppedMuonsParentPi-_"+ntupleName+"_"+config+".png")
  
    return	

def main():

    # RunStoppedMuons("Mu2E_1e7events")
    # RunStoppedMuons("Mu2E_1e7events_fromZ1850_parallel_noColl03", "VirtualDetector/Coll_01_DetIn")
    RunStoppedMuons("Mu2E_1e7events_fromZ1850_parallel_noColl03", "NTuple/Z1850")
    # RunStoppedMuons("Mu2E_1e7events_Absorber3.1_l90mm_r85mm_fromZ1850_parallel_noColl03", "NTuple/Z1850")
    # RunStoppedMuons("Mu2E_1e7events_Absorber3.1_l90mm_r85mm_fromZ1850_parallel_noColl03", "VirtualDetector/BeAbsorber_DetIn")
	# RunStoppedMuons("Mu2E_1e7events_Absorber3.1_l90mm_r85mm_fromZ1850_parallel_noColl03", "VirtualDetector/BeAbsorber_DetOut")
if __name__ == "__main__":
    main()
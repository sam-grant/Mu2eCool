# What happens to my <100 MeV pions?

# Analyse cooling effect of the absorber 

# External libraries
import pandas as pd
import numpy as np
from scipy import stats

# Internal libraries
import Utils as ut

# Globals
g4blVer="v3.06"

# def bin(data, bin_width=1.0): 

#     # Bin the data
#     bin_edges = np.arange(min(data), max(data) + bin_width, bin_width)
#     bin_indices = np.digitize(data, bin_edges)
#     bin_counts = np.bincount(bin_indices)

#     return bin_edges, bin_indices, bin_counts

# def GetMode(data):

#     # Bin
#     bin_edges, bin_indices, bin_counts = bin(data)
#     # Get mode index
#     mode_bin_index = np.argmax(bin_counts)
#     # Get mode count
#     mode_count = bin_counts[mode_bin_index]
#     # Get bin width
#     bin_width = bin_edges[mode_bin_index] - bin_edges[mode_bin_index + 1]
#     # Calculate the bin center corresponding to the mode
#     mode_bin_center = (bin_edges[mode_bin_index] + bin_edges[mode_bin_index + 1]) / 2
#     # Mode uncertainty 
#     N = len(data)
#     mode_bin_center_err = np.sqrt(N / (N - mode_count)) * bin_width

#     return mode_bin_center, abs(mode_bin_center_err)

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.colors import ListedColormap

def PlotRatio(hists, nbins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", labels=None, legPos="best", errors=True, NDPI=300, peak=False):

    # Create figure and axes
    fig, ax = plt.subplots()

    if len(hists) > 2: 
        print("PlotRatio requires two input historgrams,", len(hists), "provided")
        # Clear memory
        plt.close()
        return
    # Define a colormap
    # cmap = cm.get_cmap('tab10') # !!deprecated!!

    # Define the colourmap colours
    colours = [                                             # Black
        (0.12156862745098039, 0.4666666666666667, 0.7058823529411765),  # Blue
        (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),  # Red
    ]

    # Create the colormap
    cmap = ListedColormap(colours)

    # Iterate over the hists and plot each one
    for i, hist in enumerate(hists):
        colour = cmap(i)
        # Calculate statistics
        N, mean, meanErr, stdDev, stdDevErr, underflows, overflows = ut.GetBasicStats(hist, xmin, xmax)
        # Create legend text
        legend_text = f"Entries: {N}\nMean: {ut.Round(mean, 3)}\nStd Dev: {ut.Round(stdDev, 3)}"
        if errors: legend_text = f"Entries: {N}\nMean: {ut.Round(mean, 4)}$\pm${ut.Round(meanErr, 1)}\nStd Dev: {ut.Round(stdDev, 4)}$\pm${ut.Round(stdDevErr, 1)}"
        if peak and not errors: legend_text += f"\nPeak: {ut.Round(ut.GetMode(hist, nbins / (xmax - xmin))[0], 3)}"
        if peak and errors: legend_text += f"\nPeak: {ut.Round(ut.GetMode(hist, nbins / (xmax - xmin))[0], 3)}$\pm${ut.Round(ut.GetMode(hist, nbins / (xmax - xmin))[1], 1)}"
        # if errors: legend_text = f"Entries: {N}\nMean: {Round(mean, 4)}$\pm${Round(meanErr, 1)}\nStd Dev: {Round(stdDev, 4)}$\pm${Round(stdDevErr, 1)}"
        counts, bin_edges, _ = ax.hist(hist, bins=nbins, range=(xmin, xmax), histtype='step', edgecolor=colour, linewidth=1.0, fill=False, density=False, color=colour, label=r"$\bf{"+labels[i]+"}$"+"\n"+legend_text)

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

    # Add a ratio plot

    # # Create a subplot for the ratio plot below the main histogram
    # ax2 = plt.axes([ax.get_position().x0, 0.1, ax.get_position().width, 0.25])
    
    # # valid_indices = (bin_edges >= xmin) & (bin_edges <= xmax)
    # h1 = hists[0][(hists[0] >= xmin) & (hists[0] <= xmax)]
    # h2 = hists[1][(hists[1] >= xmin) & (hists[1] <= xmax)]

    # ratio = h1 / h2 # [(hists[0] >= xmin) & (hists[0] <= xmax)] / hists[1][(hists[1] >= xmin) & (hists[1] <= xmax)]
    # valid_indices = (bin_edges >= xmin) & (bin_edges <= xmax)

    # # Plot the ratio histogram
    # # ax2.hist(bin_edges[:-1][valid_indices-1], ratio[valid_indices-1], color='black', linewidth=1.0)
    # # ax2.set_xlim(xmin, xmax)
    # ax2.axhline(y=1.0, color='red', linestyle='--', linewidth=1.0)  # Add a line at y=1.0
    
    # # Customize the ratio plot
    # ax2.set_xlabel(xlabel, fontsize=14, labelpad=10)
    # ax2.set_ylabel("Ratio", fontsize=12, labelpad=10)
    # ax2.tick_params(axis='x', labelsize=14)
    # ax2.tick_params(axis='y', labelsize=10)
    # ax2.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    # ax2.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    # ax2.xaxis.offsetText.set_fontsize(12)

    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.close()

# Group by "UniqueID" and apply a custom function to increment "Weight"
# def increment_weight(group):
#     group['Weight'] = range(1, len(group) + 1)
#     return group


import math 

def GetHelix(df):

	# Transverse radius of curvature in the B field

	# R = p/qBsin(theta) * gamma
	# E_k_T = E_T - E_0 = sqrt(p_T^2 + m_0^2) - m_0
	# E_k=E-E_0=(gamma-1)*m_0*c^2 --> gamma - 1 = E_k / m_0 * c^2 --> gamma = E_k/m_0*c^2 + 1 
	# --> gamma = E_k/m_0 + 1 

	# sin(Theta) = 1 for 2D, since 
	# cos(Theta) = BdotP / (Pmag * Bmag) = 0
	# BdotP = Bx * Px + By * Py + Bz * Pz = 0*Px + 0*Py + Bz*0 = 0

	# —> R = p_T/qB_z * gamma

	# Constants
	m_0 = 139.570 # pi+- rest mass in MeV/c^2
	e = 1.602e-19 # C
	c = 299792458 # m/s

	# Sign of charge 
	df["Sign"] = df["PDGid"].apply(lambda x: math.copysign(1, x))

	# Tranverse momentum, kinetic energy, and gamma
	df["PT"] = np.sqrt( pow(df["Px"], 2) + pow(df["Py"], 2) ) 
	df["EkT"] = np.sqrt(pow(df["PT"], 2) + pow(m_0, 2)) - m_0
	df["gammaT"] = df["EkT"]/m_0 + 1 

	df["LorentzRadius"] = df["gammaT"] *  (df["PT"] / (df["Sign"] * e * df["Bz"]) ) * (1e6 * e / c) * 1e3 # MeV/c -> J and m -> mm

	# Calculate the helical center 
	# We a looking into the helix, it spirals towards us
	# This bit came from ChatGPT, I need to think about it more but it seems to work when testing against the GUI...
	# In particular, I don't understand the signs. 
	# You adjust the x, y coordinates based on the radius of curvature, scaled according to the contribution of Px, Py to the total transverse momentum.
	df["HelixX"] = df["x"] + df["LorentzRadius"] * df["Px"] / df["PT"] # adjust x 
	df["HelixY"] = df["y"] - df["LorentzRadius"] * df["Py"] / df["PT"] # adjust y 
	df["HelixZ"] = df["z"]  # Assuming the magnetic field is along the z-axis

	df["HelixR"] = np.sqrt( pow(df["HelixX"], 2) + pow(df["HelixY"], 2) )

	return df

# Function to increment duplicates
# ChatGPT...
# def increment_duplicates(df, column_name):
#     duplicates = df[df.duplicated(subset=column_name, keep="first")]
    
#     # Dictionary to store mapping of original IDs to new IDs
#     id_mapping = {}
    
#     for index, row in duplicates.iterrows():
#         original_id = row[column_name]
#         new_id = original_id
#         while new_id in df[column_name].tolist():
#             new_id += 1
#         id_mapping[original_id] = new_id

#     df[column_name] = df[column_name].replace(id_mapping)
#     return df

# Function to increment duplicates
def increment_duplicates(df, column_name):
	
    ids = df[column_name].values
    unique_ids, counts = np.unique(ids, return_counts=True)

    duplicate_indices = np.where(counts > 1)[0]
    
    for index in duplicate_indices:
        duplicate_id = unique_ids[index]
        mask = (ids == duplicate_id)
        ids[mask] = np.arange(mask.sum()) + duplicate_id + 1

    df[column_name] = ids
    return df


def RunColdPions(config):

	# Setup input 
	finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

	absorberName = config.split("_")[2] 

	# Read in TTrees
	df_in = ut.TTreeToDataFrame(finName, "VirtualDetector/BeAbsorber_DetIn", ut.branchNamesExtended)
	df_out = ut.TTreeToDataFrame(finName, "VirtualDetector/BeAbsorber_DetOut", ut.branchNamesExtended)

	df_in["UniqueID"] = 1e10*df_in["EventID"] + 1e7*df_in["TrackID"] + 1e4*df_in["ParentID"] + df_in["Weight"] 
	df_out["UniqueID"] = 1e10*df_out["EventID"] + 1e7*df_out["TrackID"] + 1e4*df_out["ParentID"] + df_in["Weight"] 

	# Just take the first 10 events for debugging 
	# df_in = df_in # [:1000]
	# df_out = df_out # 	[:1000]

	# Add momentum column
	df_in["P"] = np.sqrt( pow(df_in["Px"], 2) + pow(df_in["Py"], 2) + pow(df_in["Pz"], 2) ) 
	df_out["P"] = np.sqrt( pow(df_out["Px"], 2) + pow(df_out["Py"], 2) + pow(df_out["Pz"], 2) ) 

	# Add radius column
	df_in["R"] = np.sqrt( pow(df_in["x"], 2) + pow(df_in["y"], 2) ) 
	df_out["R"] = np.sqrt( pow(df_out["x"], 2) + pow(df_out["y"], 2) ) 

	GetHelix(df_in)
	GetHelix(df_out)

	# print(df_out["LorentzRadius"])

	df_in = ut.FilterParticles(df_in, "pi-")
	df_out = ut.FilterParticles(df_out, "pi-")

	# Filter 0-100 MeV
	df_in = df_in[df_in["P"] <= 100]
	df_out = df_out[df_out["P"] <= 100]

	# Remove rows with duplicate UniqueID values
	# This is a bug in G4beamline as far as I can tell...
	# df_in = df_in.drop_duplicates(subset="UniqueID", keep="first")
	# df_out = df_out.drop_duplicates(subset="UniqueID", keep="first")

	df_in = increment_duplicates(df_in, "UniqueID")
	df_out = increment_duplicates(df_out, "UniqueID")

	print(df_in)

	# Handle duplicate events 
	# Group by "UniqueID" and increment each duplicate 
	# df_in['Weight'] = df_in.groupby('UniqueID').cumcount() + 1
	# df_out['Weight'] = df_out.groupby('UniqueID').cumcount() + 1

	# df_in = df_in.groupby('UniqueID').apply(increment_weight)
	# df_out = df_out.groupby('UniqueID').apply(increment_weight)

	# # Update UniqueID
	# df_in["UniqueID"] = 1e10*df_in["EventID"] + 1e7*df_in["TrackID"] + 1e4*df_in["ParentID"] + df_in["Weight"] 
	# df_out["UniqueID"] = 1e10*df_out["EventID"] + 1e7*df_out["TrackID"] + 1e4*df_out["ParentID"] + df_in["Weight"] 


	# Pions that enter the <100 MeV but do not exit 
	df_lostPions = df_in[~df_in['UniqueID'].isin(df_out['UniqueID'])]
	# Pions that exit <100 MeV after entering <100 MeV
	df_oldPions = df_out[df_out['UniqueID'].isin(df_in['UniqueID'])] 
	# Pions that exit <100 MeV but do not enter <100 MeV
	df_newPions = df_out[~df_out['UniqueID'].isin(df_in['UniqueID'])] 

	# Pions that are present in out, but not old, new, or lost
	df_anomalousPions = df_out[
	    (~df_out['UniqueID'].isin(df_oldPions['UniqueID'])) &
	    (~df_out['UniqueID'].isin(df_newPions['UniqueID'])) &
	    (~df_out['UniqueID'].isin(df_lostPions['UniqueID']))
	]

	# print(df_in[:5])
	# print(df_out[:5])
	# print(df_oldPions[:5])
	# print(df_lostPions[:5])
	# print(df_newPions[:5])

	print("in =", df_in.shape[0])
	print("out =", df_out.shape[0])
	print("out - in =", df_out.shape[0]-df_in.shape[0])
	print("old =", df_oldPions.shape[0])
	print("lost =", df_lostPions.shape[0])
	print("new =", df_newPions.shape[0])
	print("new - lost =", df_newPions.shape[0] - df_lostPions.shape[0])

	# This should equal out-in? right?
	print("---> these should all be zero...")
	print("(out - in) - (new - lost) =", (df_out.shape[0]- df_in.shape[0]) - (df_newPions.shape[0] - df_lostPions.shape[0]))
	print("out  - (in + (new - lost)) = ", df_out.shape[0] - (df_in.shape[0] + (df_newPions.shape[0] - df_lostPions.shape[0])))
	print("anomalous =", df_anomalousPions.shape[0])

	# So then what about those muons that are present in out, but not old, new, or lost?

	# print(df_in.shape[0], df_out.shape[0], df_out.shape[0]-df_in.shape[0])
	# print(df_lostPions.shape[0], df_oldPions.shape[0], df_newPions.shape[0]) 

	# # The number (entering + lost) - exiting
	# print((df_oldPions.shape[0]+df_lostPions.shape[0])-df_newPions.shape[0])

	# Pions below 100 MeV that exit the detector <100 MeV but do not enter <100 MeV
	# df_a = df_out[df_out['UniqueID'].isin(df_in['UniqueID'])]
	# df_b = df_out[~df_out['UniqueID'].isin(df_in['UniqueID'])]

	# print(len(df_in["P"]), len(df_out["P"]), len(df_out["P"])-len(df_in["P"]), len(df_a["P"]))
	# print(df_in.shape[0], df_out.shape[0], df_out.shape[0]-df_in.shape[0])
	# print(df_a.shape[0], df_b.shape[0], df_a.shape[0]+df_b.shape[0])

	# Momentum 
	# ut.Plot1D(df_in["P"], 100, 0, 100, "", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdPions/h1_Mom_In_xmax100MeV_pi-_"+config+".png")
	# ut.Plot1D(df_out["P"], 100, 0, 100, "", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdPions/h1_Mom_Out_xmax100MeV_pi-_"+config+".png")

	ut.Plot1D(df_in["P"], 100, 0, 100, "In", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdPions/h1_Mom_In_xmax100MeV_pi-_"+config+".png")
	ut.Plot1D(df_out["P"], 100, 0, 100, "Out", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdPions/h1_Mom_Out_xmax100MeV_pi-_"+config+".png")


	# df_diff = df_out - df_in

	ut.Plot1D(df_oldPions["P"], 100, 0, 100, "Old", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdPions/h1_Mom_lost_pi-_"+config+".png")
	ut.Plot1D(df_lostPions["P"], 100, 0, 100, "Lost", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdPions/h1_Mom_lost_pi-_"+config+".png")
	ut.Plot1D(df_newPions["P"], 100, 0, 100, "New", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdPions/h1_Mom_new_pi-_"+config+".png")

	ut.Plot1DOverlay([df_oldPions["P"], df_lostPions["P"], df_newPions["P"]], nbins=100, xmin=0, xmax=100, title = r"$\pi^{-}$, "+absorberName+", <100 MeV", xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = ["Old", "Lost", "New"], fout = "../img/"+g4blVer+"/ColdPions/h1_mom_oldLostNewPi-_"+config+".png", legPos="best") # , includeBlack=False)
	
	ut.Plot1DOverlay([df_oldPions["R"], df_lostPions["R"], df_newPions["R"]], nbins=220, xmin=0, xmax=220, title = r"$\pi^{-}$, "+absorberName+", <100 MeV", xlabel = "Radial position [mm]", ylabel = "Counts / mm", labels = ["Old", "Lost", "New"], fout = "../img/"+g4blVer+"/ColdPions/h1_rad_oldLostNewPi-_"+config+".png", legPos="best") # , includeBlack=False)

	ut.Plot1DOverlay([df_oldPions["HelixR"], df_lostPions["HelixR"], df_newPions["HelixR"]], nbins=220, xmin=0, xmax=220, title = r"$\pi^{-}$, "+absorberName+", <100 MeV", xlabel = "Radial position of the helical centre [mm]", ylabel = "Counts / mm", labels = ["Old", "Lost", "New"], fout = "../img/"+g4blVer+"/ColdPions/h1_HelixR_oldLostNewPi-_"+config+".png", legPos="best") # , includeBlack=False)


	return

def main():

    # RunColdPions("Mu2E_1e7events_Absorber3_l55mm_r100mm_fromZ1850_parallel") 
    RunColdPions("Mu2E_1e7events_Absorber3_fromZ1850_parallel_noColl03") 

if __name__ == "__main__":
    main()
# Samuel Grant 2023
# Write cooled off muons and pions to an ntuple

# External libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# Suppress warnings about overwriting a dataframe
pd.options.mode.chained_assignment = None  # default='warn'

# Internal libraries
import Utils as ut

# Globals
g4blVer="v3.06"

def Plot1DAnnotated(data, nBins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", legPos="best", stats=False, peak=False, underOver=False, errors=False, norm=False, NDPI=300):
    
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

from matplotlib.colors import LogNorm 

def Plot2DAnnotated(x, y, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", cb=True, NDPI=300):

    # Create 2D histogram
    hist, x_edges, y_edges = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])

    # Set up the plot
    fig, ax = plt.subplots()

    # Plot the 2D histogram
    im = ax.imshow(hist.T, cmap='inferno', extent=[xmin, xmax, ymin, ymax], aspect='auto', origin='lower', norm=LogNorm(vmin=1, vmax=np.max(hist))) # vmax=np.max(hist))

    # Add colorbar
    if cb:
        plt.colorbar(im)

    plt.title(title, fontsize=16, pad=10)
    plt.xlabel(xlabel, fontsize=14, labelpad=10)
    plt.ylabel(ylabel, fontsize=14, labelpad=10)

    # Scientific notation for x and y axes if values are too large
    if ax.get_xlim()[1] > 999:
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
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
    
    # Add other annotations as needed
    # Example:
    # ax.annotate("Annotation Text", xy=(x_coord, y_coord), xytext=(text_x, text_y),
    #             textcoords='offset points', fontsize=14, color='gray')

    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.close()

    return


from matplotlib.colors import ListedColormap

def Plot1DAnnotatedOverlay(hists, nbins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, labels = [], fout="hist.png", legPos="best", includeBlack=False, NDPI=300): # stats=False, peak=False, underOver=False, errors=False, norm=False, NDPI=300):
    
    # Create figure and axes
    fig, ax = plt.subplots()

    # Define the colourmap colours
    colours = [
        (0., 0., 0.),                                                   # Black
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
        colour = cmap(i)
        if not includeBlack: colour = cmap(i+1)
        counts, bin_edges, _ = ax.hist(hist, bins=nbins, range=(xmin, xmax), histtype='step', edgecolor=colour, linewidth=1.0, fill=False, density=False, color=colour, label=labels[i]) 

    # Add legend to the plot
    ax.legend(loc=legPos, frameon=True, fontsize=14)


    # ax.legend([r"Stopped $\mu^{-}$"], loc="upper right", frameon=False, fontsize=14)

    # ax.set_title(title, fontsize=16, pad=15)
    ax.set_xlabel(xlabel, fontsize=14, labelpad=10) 
    ax.set_ylabel(ylabel, fontsize=14, labelpad=10) 

    # Set font size of tick labels on x and y axes
    ax.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
    ax.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size

    if ax.get_xlim()[1] > 999:
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 999:
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

# Basically just analyse the beamlossnutple. Where do they die? 
# Use StoppedMuons.py to check on stopped muons
def RunFilter(df):
    # Drop any duplicates
    df = df.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"]) 
    # Filter upstream particles
    df = df[df["Pz"]>0]
    return df

def RunColdParticlesBeamLoss(config): 

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"
 
    # Read in TTrees
    df_beamloss = ut.TTreeToDataFrame(finName, "NTuple/BeamLoss", ut.branchNamesExtended)
    df_TS1 = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_01_DetIn", ut.branchNamesExtended)
    df_TS3 = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_03_DetIn", ut.branchNamesExtended)
    df_TS5 = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_05_DetIn", ut.branchNamesExtended)
    df_prestop = ut.TTreeToDataFrame(finName, "VirtualDetector/prestop", ut.branchNamesExtended)

    print("Total", )
    print("Fraction making it ST", df_prestop.shape[0])
    z_TS1 = np.mean(df_TS1["z"])
    z_TS3 = np.mean(df_TS3["z"])
    z_TS5 = np.mean(df_TS5["z"])

    # param Coll_03_up_z=$MECO_G4_zTrans
    # param MECO_G4_zTrans=(5.00+2.929)*1000
    # param MECO_G4_xTrans=-(2.929+1.950/2.0)*1000
    # param Coll_05_x=-3904+$MECO_G4_xTrans

    df_beamloss_TS1 = df_beamloss[(df_beamloss["z"] > z_TS1-50) & (df_beamloss["z"] < z_TS1+50)]
    df_beamloss_TS3 = df_beamloss[(df_beamloss["z"] > z_TS3-50) & (df_beamloss["z"] < z_TS3+50)]
    df_beamloss_TS5 = df_beamloss[(df_beamloss["z"] > z_TS5-50) & (df_beamloss["z"] < z_TS5+50)]

    # x is now z, shifted by z position of collimator 3
    df_beamloss_TS3["x"] = df_beamloss_TS3["z"] - (5.00+2.929)*1000

    # x is still x, but shifted by x position of collimator 5
    df_beamloss_TS5["x"] = df_beamloss_TS5["x"] + 3904 + (2.929+1.950/2.0)*1000

    ut.Plot2D(ut.FilterParticles(df_beamloss_TS1, "pi-")["x"], ut.FilterParticles(df_beamloss_TS1, "pi-")["y"], 50, -250, 250, 50, -250, 250, r"TS1, $\pi^{-}$", "x [mm]", "y [mm]", fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h2_xy_pions_TS1_"+config+".png") # , stats=True) ) )
    ut.Plot2D(ut.FilterParticles(df_beamloss_TS3, "pi-")["x"], ut.FilterParticles(df_beamloss_TS3, "pi-")["y"], 50, -250, 250, 50, -250, 250, r"TS3, $\pi^{-}$", "x [mm]", "y [mm]", fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h2_xy_pions_TS3_"+config+".png") # , stats=True) ) )
    ut.Plot2D(ut.FilterParticles(df_beamloss_TS5, "pi-")["x"], ut.FilterParticles(df_beamloss_TS5, "pi-")["y"], 50, -250, 250, 50, -250, 250, r"TS5, $\pi^{-}$", "x [mm]", "y [mm]", fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h2_xy_pions_TS5_"+config+".png") # , stats=True) ) )
  
    ut.Plot2D(ut.FilterParticles(df_beamloss_TS1, "mu-")["x"], ut.FilterParticles(df_beamloss_TS1, "mu-")["y"], 50, -250, 250, 50, -250, 250, r"TS1, $\mu^{-}$", "x [mm]", "y [mm]", fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h2_xy_muons_TS1_"+config+".png") # , stats=True) ) )
    ut.Plot2D(ut.FilterParticles(df_beamloss_TS3, "mu-")["x"], ut.FilterParticles(df_beamloss_TS3, "mu-")["y"], 50, -250, 250, 50, -250, 250, r"TS3, $\mu^{-}$", "x [mm]", "y [mm]", fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h2_xy_muons_TS3_"+config+".png") # , stats=True) ) )
    ut.Plot2D(ut.FilterParticles(df_beamloss_TS5, "mu-")["x"], ut.FilterParticles(df_beamloss_TS5, "mu-")["y"], 50, -250, 250, 50, -250, 250, r"TS5, $\mu^{-}$", "x [mm]", "y [mm]", fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h2_xy_muons_TS5_"+config+".png") # , stats=True) ) )

    # if df_beamloss["z"] == z_TS3: = "Coll_03":
    #     # x is now z, shifted by z position of collimator 5
    #     # param Coll_03_up_z=$MECO_G4_zTrans
    #     # param MECO_G4_zTrans=(5.00+2.929)*1000
    #     df_trans["x"] = df["z"] - (5.00+2.929)*1000 # 082
    #     df = df_trans

    # if ntupleName[:7] == "Coll_05" or ntupleName == "prestop" or ntupleName == "poststop":
    #     # x is still x, but shifted by x position of collimator 5
    #     # param MECO_G4_xTrans=-(2.929+1.950/2.0)*1000
    #     # param Coll_05_x=-3904+$MECO_G4_xTrans
    #     df_trans["x"] = df["x"] + 3904 + (2.929+1.950/2.0)*1000
    #     df = df_trans 


    # Collimator plots
    
    # ut.Plot2D(ut.FilterParticles(df_TS3, "pi-")["x"], ut.FilterParticles(df_TS3, "pi-")["y"], 400, -200, 200, 400, -200, 200, r"$\pi^{-}$", "x [mm]", "y [mm]", fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h2_xy_pions_TS3_"+config+".png") # , stats=True) ) )
    # ut.Plot2D(ut.FilterParticles(df_TS5, "pi-")["x"], ut.FilterParticles(df_TS5, "pi-")["y"], 400, -200, 200, 400, -200, 200, r"$\pi^{-}$", "x [mm]", "y [mm]", fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h2_xy_pions_TS5_"+config+".png") # , stats=True) ) )
    
    # ut.Plot2D(ut.FilterParticles(df_TS1, "mu-")["x"], ut.FilterParticles(df_TS1, "mu-")["y"], 400, -200, 200, 400, -200, 200, r"$\mu^{-}$", "x [mm]", "y [mm]", fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h2_xy_muons_TS1_"+config+".png") # , stats=True) ) )
    # ut.Plot2D(ut.FilterParticles(df_TS3, "mu-")["x"], ut.FilterParticles(df_TS3, "mu-")["y"], 400, -200, 200, 400, -200, 200, r"$\mu^{-}$", "x [mm]", "y [mm]", fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h2_xy_muons_TS3_"+config+".png") # , stats=True) ) )
    # ut.Plot2D(ut.FilterParticles(df_TS5, "mu-")["x"], ut.FilterParticles(df_TS5, "mu-")["y"], 400, -200, 200, 400, -200, 200, r"$\mu^{-}$", "x [mm]", "y [mm]", fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h2_xy_muons_TS5_"+config+".png") # , stats=True) ) )

    # Some plots
    # ut.Plot1D(df_beamloss["z"]/1e3, 143, 0, 14.3, "Beam loss", "z-position [MeV]", "Counts / 100 mm", "../img/"+g4blVer+"/ColdParticleBeamLoss/h1_z_"+config+".png") # , stats=True) 
    Plot1DAnnotated(df_beamloss["z"]/1e3, 143, 0, 14.3, "", "Beam loss z-position [m]", "Counts / 100 mm", "../img/"+g4blVer+"/ColdParticleBeamLoss/h1_z_annoted_"+config+".png") # , stats=True) )
    Plot1DAnnotatedOverlay([ut.FilterParticles(df_beamloss, "pi-")["z"]/1e3, ut.FilterParticles(df_beamloss, "mu-")["z"]/1e3], 143, 0, 14.3, "", "Beam loss z-position [m]", "Counts / 100 mm", [r"$\pi^{-}$", r"$\mu^{-}$"], "../img/"+g4blVer+"/ColdParticleBeamLoss/h1_z_annoted_overlay_"+config+".png") # , legPos="upper left") # , stats=True) )
    Plot1DAnnotatedOverlay([df_beamloss["z"]/1e3, ut.FilterParticles(df_beamloss, "pi-")["z"]/1e3, ut.FilterParticles(df_beamloss, "mu-")["z"]/1e3], 143, 0, 14.3, "", "Beam loss z-position [m]", "Counts / 100 mm", ["All", r"$\pi^{-}$", r"$\mu^{-}$"], "../img/"+g4blVer+"/ColdParticleBeamLoss/h1_z_annoted_tripleOverlay_"+config+".png", includeBlack=True) # , legPos="upper left") # , stats=True) )

    ut.Plot1D(df_beamloss["y"], 1000, -500, 500, fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h1_y_"+config+".png", underOver=True)
    # ut.Plot2DAnnotated(df_beamloss["z"], df_beamloss["y"], 1430, 0, 14300, 100, -500, 500, "", "Beam loss z-position [mm]", "Beam loss y-position [mm]", fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h2_zy_annoted_"+config+".png")
  
    Plot2DAnnotated(ut.FilterParticles(df_beamloss, "pi-")["z"]/1e3, ut.FilterParticles(df_beamloss, "pi-")["y"], 143, 0, 14.3, 120, -300, 300, "", "Beam loss z-position [mm]", "Beam loss y-position [mm]", fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h2_zy_pions_annoted_"+config+".png")
    Plot2DAnnotated(ut.FilterParticles(df_beamloss, "mu-")["z"]/1e3, ut.FilterParticles(df_beamloss, "mu-")["y"], 143, 0, 14.3, 120, -300, 300, "", "Beam loss z-position [mm]", "Beam loss y-position [mm]", fout="../img/"+g4blVer+"/ColdParticleBeamLoss/h2_zy_muons_annoted_"+config+".png")

    return

def main():

    RunColdParticlesBeamLoss("Mu2E_1e7events_PSRingWedge_l25mm_r110mm_fromZ1850_ColdParticles")

if __name__ == "__main__":
    main()
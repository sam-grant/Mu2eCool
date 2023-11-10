# Samuel Grant 2023
# Analyse cooling effect of the absorber 

# External libraries
import pandas as pd
import numpy as np
from scipy import stats

# Internal libraries
import Utils as ut

# Globals
g4blVer="v3.06"

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

def RunAbsorberCooling(config, dim=""):

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

    absorberName = config.split("_")[2] 
    # absorberName = absorberName[:1]+" "+absorberName[2:]
    # thickness = config.split("_")[3] 
    # thickness = thickness[:2]+" "+thickness[2:]
 
    # Read in TTrees
    df_BeAbsorber_DetIn = ut.TTreeToDataFrame(finName, "VirtualDetector/BeAbsorber_DetIn", ut.branchNames)
    df_BeAbsorber_DetOut = ut.TTreeToDataFrame(finName, "VirtualDetector/BeAbsorber_DetOut", ut.branchNames)

    # Add momentum column
    df_BeAbsorber_DetIn["P"] = np.sqrt( pow(df_BeAbsorber_DetIn["Px"], 2) + pow(df_BeAbsorber_DetIn["Py"], 2) + pow(df_BeAbsorber_DetIn["Pz"], 2) ) 
    df_BeAbsorber_DetOut["P"] = np.sqrt( pow(df_BeAbsorber_DetOut["Px"], 2) + pow(df_BeAbsorber_DetOut["Py"], 2) + pow(df_BeAbsorber_DetOut["Pz"], 2) ) 

    # Add Radial position column
    df_BeAbsorber_DetIn["R"] = np.sqrt( pow(df_BeAbsorber_DetIn["x"], 2) + pow(df_BeAbsorber_DetIn["y"], 2) ) 
    df_BeAbsorber_DetOut["R"] = np.sqrt( pow(df_BeAbsorber_DetOut["x"], 2) + pow(df_BeAbsorber_DetOut["y"], 2) ) 

    # # Select forward going particles 
    # df_BeAbsorber_DetIn = df_BeAbsorber_DetIn[df_BeAbsorber_DetIn["Pz"] > 0]
    # df_BeAbsorber_DetOut = df_BeAbsorber_DetOut[df_BeAbsorber_DetOut["Pz"] > 0]

    # Drop any duplicates 
    df_BeAbsorber_DetIn = df_BeAbsorber_DetIn.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"], keep="first")
    df_BeAbsorber_DetOut = df_BeAbsorber_DetOut.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"], keep="first")

    # ------ Stats ------
    # meanMom_BeAbsorber_DetIn, meanMomErr_BeAbsorber_DetIn = np.mean(df_BeAbsorber_DetIn["P"]), np.std(df_BeAbsorber_DetOut["P"])/len(df_BeAbsorber_DetOut["P"])
    # meanMom_BeAbsorber_DetOut, meanMomErr_BeAbsorber_DetOut = np.mean(df_BeAbsorber_DetOut["P"]), np.std(df_BeAbsorber_DetOut["P"])/len(df_BeAbsorber_DetOut["P"])

    # 
    df_cooling = {
        # "Particle": ["All", "proton", "pi+", "pi-", "mu+", "mu-"],
        "Particle": ["pi-", "mu-"],
        "Entering (mean)": [],
        "Entering (mean err)": [],
        "Exiting (mean)": [],
        "Exiting (mean err)": [],
        "Delta (mean)": [],
        "Delta (mean err)": [],
        "Entering (mode)": [],
        "Entering (mode err)": [],
        "Exiting (mode)": [],
        "Exiting (mode err)": [],
        "Delta (mode)": [],
        "Delta (mode err)": []
    }

    # Loop through particles
    # particle_ = ["All", "proton", "pi+", "pi-", "mu+", "mu-"]

    i_xmax = 0 
    # xmax_ = [1250, 1250, 750, 750, 275, 275] 
    xmax_ = [750, 275] 

    for particle in df_cooling["Particle"]: 

        print("\n--->",particle)

        title = ut.GetLatexParticleName(particle)+", "+dim

        in_ = ut.FilterParticles(df_BeAbsorber_DetIn, particle)
        out_ = ut.FilterParticles(df_BeAbsorber_DetOut, particle)

        ut.Plot1D(in_["P"], 750, 0, 750, "pions in", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/AbsorberCooling/h1_Mom_In_"+particle+"_"+config+".png")

        # Momentum 
        ut.Plot1DOverlayWithStats([in_["P"], out_["P"]], int(xmax_[i_xmax]), 0, xmax_[i_xmax], title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/AbsorberCooling/h1_Mom_InOut_"+particle+"_"+config+".png", ["Entering", "Exiting"], errors=False, peak=True)
        ut.Plot1DOverlayWithStats([in_["P"], out_["P"]], 50, 0, 50, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/AbsorberCooling/h1_Mom_InOut_xmax50MeV_"+particle+"_"+config+".png", ["Entering", "Exiting"], errors=False, peak=False , legPos="best")
        ut.Plot1DOverlayWithStats([in_["P"], out_["P"]], 100, 0, 100, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/AbsorberCooling/h1_Mom_InOut_xmax100MeV_"+particle+"_"+config+".png", ["Entering", "Exiting"], errors=False, peak=False, legPos="best")
        # ut.Plot1DOverlayWithStats([in_["P"], out_["P"]], 125, 0, 125, title", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/AbsorberCooling/h1_Mom_InOut_xmax125MeV_"+particle+"_"+config+".png", ["Entering", "Exiting"], peak=False, legPos="best")
        # ut.Plot1DRatio([in_["P"], out_["P"]], 50, 0, 50, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/AbsorberCooling/h1_ratio_Mom_InOut_xmax50MeV_"+particle+"_"+config+".png", ["Entering", "Exiting"], peak=False, legPos="best", invertRatio=True, stats=True, errors=True, limitRatio=True, ratioMin=0, ratioMax=1.99)
        # ut.Plot1DRatio([in_["P"], out_["P"]], 50, 0, 50, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/AbsorberCooling/h1_ratio_Mom_InOut_xmax50MeV_"+particle+"_"+config+".png", ["Entering", "Exiting"], peak=False, legPos="best", invertRatio=True, stats=True, errors=True, limitRatio=True, ratioMin=0, ratioMax=1.99)
        # ut.Plot1DRatio([in_["P"], out_["P"]], 100, 0, 100, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/AbsorberCooling/h1_ratio_Mom_InOut_xmax100MeV_"+particle+"_"+config+".png", ["Entering", "Exiting"], peak=False, legPos="best", invertRatio=True, stats=True, errors=True, limitRatio=True, ratioMin=0, ratioMax=1.99)
        # PlotRatio([in_["P"], out_["P"]], 100, 0, 100, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/AbsorberCooling/h1_ratio_Mom_InOut_xmax100MeV_"+particle+"_"+config+".png", ["Entering", "Exiting"], peak=False, legPos="best")

        # Radial position
        ut.Plot1DOverlayWithStats([in_["R"], out_["R"]], 250, 0, 250, title, "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/AbsorberCooling/h1_R_InOut_"+particle+"_"+config+".png", ["Entering", "Exiting"], peak=True)
        ut.Plot1DOverlayWithStats([in_[in_["P"] < 50]["R"], out_[out_["P"] < 50]["R"]], 250, 0, 250, title+", <50 MeV", "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/AbsorberCooling/h1_R_InOut_xmax50MeV_"+particle+"_"+config+".png", ["Entering", "Exiting"], errors=False, peak=False, legPos="best")
        ut.Plot1DOverlayWithStats([in_[in_["P"] < 100]["R"], out_[out_["P"] < 100]["R"]], 250, 0, 250, title+", <50 MeV", "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/AbsorberCooling/h1_R_InOut_xmax100MeV_"+particle+"_"+config+".png", ["Entering", "Exiting"], errors=False, peak=False, legPos="best")

        # ut.Plot1DRatio([in_["R"], out_["R"]],  200, 0, 200, title, "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/AbsorberCooling/h1_ratio_rad_InOut_"+particle+"_"+config+".png", ["Entering", "Exiting"], peak=False, legPos="best", invertRatio=True, stats=True, errors=True, limitRatio=False, ratioMin=0, ratioMax=1.99)
        # ut.Plot1DRatio([in_[in_["P"] < 50]["R"], out_[out_["P"] < 50]["R"]], 200, 0, 200, title+", <50 MeV", "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/AbsorberCooling/h1_ratio_rad_InOut_xmax50MeV_"+particle+"_"+config+".png", ["Entering", "Exiting"], peak=False, legPos="best", invertRatio=True, stats=True, errors=True, limitRatio=False, ratioMin=0, ratioMax=1.99)
        # ut.Plot1DRatio([in_[in_["P"] < 100]["R"], out_[out_["P"] < 100]["R"]], 200, 0, 200, title+", <100 MeV", "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/AbsorberCooling/h1_ratio_rad_InOut_xmax100MeV_"+particle+"_"+config+".png", ["Entering", "Exiting"], peak=False, legPos="best", invertRatio=True, stats=True, errors=True, limitRatio=False, ratioMin=0, ratioMax=1.99)
        # # ut.Plot1DOverlayWithStats([in_[in_["P"] < 100]["R"], out_[out_["P"] < 100]["R"]], 250, 0, 250, title+", <100 MeV", "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/AbsorberCooling/h1_R_InOut_xmax100MeV_"+particle+"_"+config+".png", ["Entering", "Exiting"], peak=False, legPos="best")
        # ut.Plot1DOverlayWithStats([in_[in_["P"] < 125]["R"], out_[out_["P"] < 125]["R"]], 250, 0, 250, title+", <125 MeV", "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/AbsorberCooling/h1_R_InOut_xmax125MeV_"+particle+"_"+config+".png", ["Entering", "Exiting"], peak=False, legPos="best")

        # 2D
        # ut.Plot2D(in_["P"], in_["R"], 50, 0, 250, 42, 0, 210, title+", entering", "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/AbsorberCooling/h2_RvsMom_In_"+particle+"_"+config+".png")
        # ut.Plot2D(out_["P"], out_["R"], 50, 0, 250, 42, 0, 210, title+", exiting", "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/AbsorberCooling/h2_RvsMom_Out_"+particle+"_"+config+".png")

        # Percentage gain 
        N_in = 0.0
        N_out = 0.0

        if particle=="pi-":

            # N_in = in_[in_["P"]<100].shape[0]
            # N_out = out_[out_["P"]<100].shape[0]
            N_in = in_[(in_["P"]<100) & (in_["R"]<150)].shape[0]
            N_out = out_[(out_["P"]<100) & (out_["R"]<150)].shape[0]

        elif particle=="mu-":

            N_in = in_[in_["P"]<50].shape[0]
            N_out = out_[out_["P"]<50].shape[0]

            N_in = in_[(in_["P"]<50) & (in_["R"]<150)].shape[0]
            N_out = out_[(out_["P"]<50) & (out_["R"]<150)].shape[0]

        Nerr_in = np.sqrt(N_in)
        Nerr_out = np.sqrt(N_out)

        gain = (N_out - N_in) / N_in
        gainErr = np.abs(gain) * np.sqrt((Nerr_in / N_out)**2 + (Nerr_out / N_out)**2) # Should be about right

        print(particle,"percentage gain =", gain*100, "+-", gainErr*100)

        continue

        in_ = in_["P"]
        out_ = out_["P"]

        meanIn = np.mean(in_)
        meanOut = np.mean(out_)
        deltaMean = np.mean(in_) - meanOut
        rmsIn = np.std(in_)
        rmsOut = np.std(out_)
        meanErrIn = rmsIn / np.sqrt(len(in_))
        meanErrOut = rmsOut / np.sqrt(len(out_))
        deltaMeanErr = np.sqrt( pow(meanErrIn, 2) + pow(meanErrOut, 2))

        modeIn, modeInErr = ut.GetMode(in_)
        modeOut, modeOutErr = ut.GetMode(out_)
        deltaMode = modeIn - modeOut
        deltaModeErr = np.sqrt( pow(modeInErr, 2) + pow(modeOutErr, 2))

        # Bin the data
        # bin_edges, bin_indices, bin_counts = bin(meanIn)
        # mode_bin_index = np.argmax(bin_counts)
        # # Calculate the bin center corresponding to the mode
        # mode_bin_center = (bin_edges[mode_bin_index] + bin_edges[mode_bin_index + 1]) / 2

        # Fill results dict
        df_cooling["Entering (mean)"].append(meanIn)
        df_cooling["Entering (mean err)"].append(meanErrIn)
        df_cooling["Exiting (mean)"].append(meanOut)
        df_cooling["Exiting (mean err)"].append(meanErrOut)
        df_cooling["Delta (mean)"].append(deltaMean)
        df_cooling["Delta (mean err)"].append(deltaMeanErr) 

        df_cooling["Entering (mode)"].append(modeIn)
        df_cooling["Entering (mode err)"].append(modeInErr)
        df_cooling["Exiting (mode)"].append(modeOut)
        df_cooling["Exiting (mode err)"].append(modeOutErr)
        df_cooling["Delta (mode)"].append(deltaMode)
        df_cooling["Delta (mode err)"].append(deltaModeErr) 
        # coolingDict["Entering"].append()

        i_xmax += 1


    return

    df_cooling = pd.DataFrame(df_cooling)

    print("---> Cooling results:\n", df_cooling)

    return

def main():

    # RunAbsorberCooling("Mu2E_1e7events_AbsorberB_l25mm_r90mm_fromZ1850_parallel", "L = 25 mm, $R_{i}$ = 90 mm")
    # RunAbsorberCooling("Mu2E_1e7events_AbsorberB_l45mm_r90mm_fromZ1850_parallel", "L = 35 mm, $R_{i}$ = 90 mm")
    # RunAbsorberCooling("Mu2E_1e7events_AbsorberB_l65mm_r90mm_fromZ1850_parallel", "L = 65 mm, $R_{i}$ = 90 mm")
    # RunAbsorberCooling("Mu2E_1e7events_AbsorberC_l25mm_r127mm_fromZ1850_parallel", "L = 25 mm, $R_{i}$ = 127 mm")
    # RunAbsorberCooling("Mu2E_1e7events_AbsorberC_l45mm_r127mm_fromZ1850_parallel", "L = 35 mm, $R_{i}$ = 127 mm")
    # RunAbsorberCooling("Mu2E_1e7events_AbsorberC_l65mm_r127mm_fromZ1850_parallel", "L = 65 mm, $R_{i}$ = 127 mm")

    RunAbsorberCooling("Mu2E_1e7events_AbsorberD_l25mm_r110mm_fromZ1850_parallel", "L = 25 mm, $R_{i}$ = 110 mm")
    # RunAbsorberCooling("Mu2E_1e7events_AbsorberD_l45mm_r110mm_fromZ1850_parallel", "L = 45 mm, $R_{i}$ = 110 mm")
    # RunAbsorberCooling("Mu2E_1e7events_AbsorberD_l65mm_r110mm_fromZ1850_parallel", "L = 65 mm, $R_{i}$ = 110 mm")

    # RunAbsorberCooling("Mu2E_1e7events_AbsorberA_l65mm_r100mm_fromZ1850_parallel", "L = 65 mm, $R_{i}$ = 100 mm")
    # RunAbsorberCooling("Mu2E_1e7events_AbsorberA_l50mm_r100mm_fromZ1850_parallel", "L = 50 mm, $R_{i}$ = 100 mm")
    # RunAbsorberCooling("Mu2E_1e7events_AbsorberA_l30mm_r100mm_fromZ1850_parallel", "L = 50 mm, $R_{i}$ = 100 mm")

    # RunAbsorberCooling("Mu2E_1e7events_AbsorberB_l65mm_r100mm_fromZ1850_parallel", "L = 65 mm, $R_{i}$ = 100 mm")
    # RunAbsorberCooling("Mu2E_1e7events_AbsorberB_l50mm_r100mm_fromZ1850_parallel", "L = 50 mm, $R_{i}$ = 100 mm")
    # RunAbsorberCooling("Mu2E_1e7events_AbsorberB_l30mm_r100mm_fromZ1850_parallel", "L = 30 mm, $R_{i}$ = 100 mm")
    # RunAbsorberCooling("Mu2E_1e7events_AbsorberB_l25mm_r100mm_fromZ1850_parallel", "L = 25 mm, $R_{i}$ = 100 mm")
    # RunAbsorberCooling("Mu2E_1e7events_AbsorberB_l20mm_r100mm_fromZ1850_parallel", "L = 20 mm, $R_{i}$ = 100 mm")

if __name__ == "__main__":
    main()
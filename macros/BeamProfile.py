# Samuel Grant 2023
# Make beam profile plots at a zntuple or VD
# Interested in the relationship between momentum and traverse space, for absorber study

import uproot
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np
import h5py

# Internal libraries
import Utils as ut

from matplotlib.patches import Rectangle

# Globals
g4blVer="v3.06"

# ---- Start of plotting functions ---- 

# def Plot2DCustomLine(x, y, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", NDPI=300):

#     # Create 2D histogram
#     hist, x_edges, y_edges = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])

#     # Set up the plot
#     fig, ax = plt.subplots()

#     # Plot the 2D histogram
#     im = ax.imshow(hist.T, cmap="inferno", extent=[xmin, xmax, ymin, ymax], aspect="auto", origin="lower", vmax=np.max(hist)) # , norm=cm.LogNorm())

#     # Add colourbar
#     plt.colorbar(im)

#     plt.title(title)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)

#     # Format main plot axes
#     # ax1.set_title(title, fontsize=16, pad=10)
#     # ax1.set_xlabel(xlabel, fontsize=14, labelpad=10) 
#     # ax1.set_ylabel(ylabel, fontsize=14, labelpad=10) 

#     # # Set font size of tick labels on x and y axes
#     # ax1.tick_params(axis="x", labelsize=14)  # Set x-axis tick label font size
#     # ax1.tick_params(axis="y", labelsize=14)  # Set y-axis tick label font size

#     # Define the function y = 2x
#     m = 2 # gradient
#     b = 75 # x-intercept
#     c = -b*m

#     x_values = np.linspace(x_edges[0], x_edges[-1], nBinsX)
#     y_values = m * x_values + c

#     # Mask y_values to only include values within the original y range
#     x_values = np.ma.masked_outside(x_values, xmin, xmax)
#     y_values = np.ma.masked_outside(y_values, ymin, ymax)

#     # Plot the line on the histogram
#     plt.plot(x_values, y_values, color="white", linestyle="--", label="y = 2x")
    
#     # Create a Rectangle patch
#     # box = Rectangle((xBoxMin, yBoxMin), width=(xmax - xBoxMin), height=(ymax - yBoxMin), fill=False, hatch="/", edgecolor="white", linestyle="--", linewidth=1)

#     # Add the Rectangle patch to the plot
#     # ax.add_patch(box)

#     # Scientific notation
#     if ax.get_xlim()[1] > 9999:
#         ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
#         ax.ticklabel_format(style="sci", axis="x", scilimits=(0,0))
#         ax.xaxis.offsetText.set_fontsize(14)
#     if ax.get_ylim()[1] > 9999:
#         ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
#         ax.ticklabel_format(style="sci", axis="y", scilimits=(0,0))
#         ax.yaxis.offsetText.set_fontsize(14)

#     plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
#     print("---> Written", fout)

#     # Clear memory
#     plt.close()

def Plot2DCustomBox(x, y, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", NDPI=300):

    # Create 2D histogram
    hist, x_edges, y_edges = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])

    # Set up the plot
    fig, ax = plt.subplots()

    # Plot the 2D histogram
    im = ax.imshow(hist.T, cmap="inferno", extent=[xmin, xmax, ymin, ymax], aspect="auto", origin="lower", vmax=np.max(hist)) # , norm=cm.LogNorm())

    # Add colourbar
    plt.colorbar(im)

    # Format axes
    plt.title(title, fontsize=16, pad=10)
    plt.xlabel(xlabel, fontsize=14, labelpad=10)
    plt.ylabel(ylabel, fontsize=14, labelpad=10) 

    # Draw line
    ax.axvline(x=50.0, color="white", linestyle="--", linewidth=1)
    ax.axhline(y=85.0, color="white", linestyle="--", linewidth=1)
    
    # Scientific notation
    if ax.get_xlim()[1] > 9999:
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style="sci", axis="x", scilimits=(0,0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 9999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style="sci", axis="y", scilimits=(0,0))
        ax.yaxis.offsetText.set_fontsize(14)

    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.close()

from matplotlib.patches import Circle

def Plot2DCustomCircle(x, y, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", radius=100, NDPI=300):

    # Create 2D histogram
    hist, x_edges, y_edges = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])

    # Set up the plot
    fig, ax = plt.subplots()

    # Plot the 2D histogram
    im = ax.imshow(hist.T, cmap="inferno", extent=[xmin, xmax, ymin, ymax], aspect="auto", origin="lower", vmax=np.max(hist)) # , norm=cm.LogNorm())

    # Add colourbar
    plt.colorbar(im)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Scientific notation
    if ax.get_xlim()[1] > 999:
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style="sci", axis="x", scilimits=(0,0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style="sci", axis="y", scilimits=(0,0))
        ax.yaxis.offsetText.set_fontsize(14)

    circle = Circle((0, 0), radius=radius, fill=False, edgecolor="white", linestyle="--", linewidth=1)
    ax.add_patch(circle)

    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.close()

def Plot3DCustomCircle(x, y, z, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0, zmax=1.0, title=None, xlabel=None, ylabel=None, zlabel=None, fout="3d_plot.png", contours=False, radius=100, NDPI=300):

    # Create a 2D histogram in xy, with the average z values on the colorbar
    hist_xy, x_edges_xy, y_edges_xy = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]], weights=z)
    # Calculate the histogram bin counts
    hist_counts, _, _ = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])
    # Avoid division by zero and invalid values
    non_zero_counts = hist_counts > 0
    hist_xy[non_zero_counts] /= hist_counts[non_zero_counts]

    # Set up the plot

    fig, ax = plt.subplots()

    # Plot the 2D histogram
    im = ax.imshow(hist_xy.T, cmap="inferno", extent=[xmin, xmax, ymin, ymax], aspect="auto", origin="lower", vmax=zmax) # z.max()) # , norm=cm.LogNorm())

    # Add colourbar
    cbar = plt.colorbar(im) # , ticks=np.linspace(zmin, zmax, num=10)) 

    # Add contour lines to visualize bin boundaries
    if contours:
        contour_levels = np.linspace(zmin, zmax, num=nBinsZ)
        print(contour_levels)
        # ax.contour(hist_xy.T, levels=[66], extent=[xmin, xmax, ymin, ymax], colors="white", linewidths=0.7)
        ax.contour(hist_xy.T, levels=contour_levels, extent=[xmin, xmax, ymin, ymax], colors="white", linewidths=0.7)

    # Draw a circle with radius 100 mm (Absorber1)
    # circle_center = (0, 0)
    # circle_radius = 50
    circle = Circle((0, 0), radius=radius, fill=False, edgecolor="white", linestyle="--", linewidth=1)
    ax.add_patch(circle)

    plt.title(title, fontsize=16, pad=10)
    plt.xlabel(xlabel, fontsize=14, labelpad=10)
    plt.ylabel(ylabel, fontsize=14, labelpad=10)
    cbar.set_label(zlabel, fontsize=14, labelpad=10)

    # Scientific notation
    if ax.get_xlim()[1] > 999:
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style="sci", axis="x", scilimits=(0,0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style="sci", axis="y", scilimits=(0,0))
        ax.yaxis.offsetText.set_fontsize(14)
    # if ax.get_zlim()[1] > 999:
    #     ax.zaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    #     ax.ticklabel_format(style="sci", axis="z", scilimits=(0,0))
    #     ax.zaxis.offsetText.set_fontsize(14)

    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.close()

    return

# ---- End of plotting functions ----  

import math

def RunBeamProfile(config, ntupleName, particle, maxMom = 500):

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"
    df = ut.TTreeToDataFrame(finName, ntupleName, ut.branchNamesExtended)  

    # Titles and names
    ntupleName = ntupleName.split("/")[1] 
    title = ut.GetLatexParticleName(particle) # 
    if ntupleName[0] == "Z": title += ", Z = "+ntupleName[1:]+" mm" # title += ", Z = "+ntupleName[1:]+" mm"
    else: title += ", "+ntupleName # ", "+ntupleName

    # Particle populations
    ut.BarChart(df["PDGid"], ut.particleDict, title, "", "Percentage / particle", fout="../img/"+g4blVer+"/BeamProfile/bar_ParticleFractionPecentage_"+ntupleName+"_"+config+".png", percentage=True)
    ut.BarChart(df["PDGid"], ut.particleDict, title, "", "Counts / particle", fout="../img/"+g4blVer+"/BeamProfile/bar_ParticleFractionCounts_"+ntupleName+"_"+config+".png", percentage=False)

    # Upstream / downstream particles
    # df_upstream = df[df["Pz"] > 0]
    # df_downstream = df[df["Pz"] < 0]
    # ut.BarChart(df_upstream["PDGid"], particleDict, config+", "+title+", upstream", "", "Counts / particle", fout="../img/"+g4blVer+"/BeamProfile/bar_ParticleFractionCountsUpstream_"+ntupleName+"_"+config+".png", percentage=False)
    # ut.BarChart(df_downstream ["PDGid"], particleDict, config+", "+title+", downstream", "", "Counts / particle", fout="../img/"+g4blVer+"/BeamProfile/bar_ParticleFractionCountsDownstream_"+ntupleName+"_"+config+".png", percentage=False)

    # Duplicate tracks
    # df["UniqueID"] = 1e6*df["EventID"] + 1e3*df["TrackID"] + df["ParentID"] 
    # unique_df = df.drop_duplicates(subset=["UniqueID"])
    # ut.BarChart(unique_df["PDGid"], particleDict, config+", "+title, "", "Counts / particle", fout="../img/"+g4blVer+"/BeamProfile/bar_ParticleFractionCountsUniqueTracks_"+ntupleName+"_"+config+".png", percentage=False)

    # Filter particles
    df = ut.FilterParticles(df, particle)

    print(df.shape[0])

    # Need to translate position, based on where we are along the beamline
    df_trans = df 

    if ntupleName[:7] == "Coll_03":
        # x is now z, shifted by z position of collimator 3
        # param Coll_03_up_z=$MECO_G4_zTrans
        # param MECO_G4_zTrans=(5.00+2.929)*1000
        df_trans["x"] = df["z"] - (5.00+2.929)*1000 # 082
        df = df_trans

    if ntupleName[:7] == "Coll_05" or ntupleName == "prestop" or ntupleName == "poststop":
        # x is still x, but shifted by x position of collimator 5
        # param MECO_G4_xTrans=-(2.929+1.950/2.0)*1000
        # param Coll_05_x=-3904+$MECO_G4_xTrans
        df_trans["x"] = df["x"] + 3904 + (2.929+1.950/2.0)*1000
        df = df_trans 

    # Momentum 
    df["P"] = np.sqrt( pow(df["Px"],2) + pow(df["Py"],2) + pow(df["Pz"],2) ) 
    # Radius 
    df["R"] = np.sqrt( pow(df["x"],2) + pow(df["y"],2)) 
    # Tranvserse momentum 
    df["PT"] = np.sqrt( pow(df["Px"],2) + pow(df["Py"],2) ) 
    # Helix parameters
    ut.GetHelix(df)

    ut.Plot1D(df["P"], int(maxMom), 0, maxMom, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamProfile/h1_mom_"+ntupleName+"_"+particle+"_"+config+".png", errors=False, underOver=True)

    return

    # ut.Plot1D(df["R"]/df["P"], 250, 0, 1, title, "R/p [mm/MeV]", "Counts", "../img/"+g4blVer+"/BeamProfile/h1_rad_over_mom_"+ntupleName+"_"+particle+"_"+config+".png")
    # ut.Plot1D(np.log(df["R"]/df["P"]), 250, -10, 10, title, "Log(R/p)", "Counts", "../img/"+g4blVer+"/BeamProfile/h1_log_rad_over_mom_"+ntupleName+"_"+particle+"_"+config+".png")
    # ut.Plot2D(df[(np.log(df["R"]/df["P"]) > -.5) & (np.log(df["R"]/df["P"]) < .5)]["P"], df[(np.log(df["R"]/df["P"]) > -.5) & (np.log(df["R"]/df["P"]) < .5)]["R"], 250, 0, 250, 210, 0, 210, title, "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RvsMom_cut_"+ntupleName+"_"+particle+"_"+config+".png")

    # return

    # ut.Plot1D(df[(df["R"] > 100)]["P"], 500, 0, maxMom, title+", R > 100 mm", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamProfile/h1_mom_above100mm_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)

    # ut.Plot3D(df["x"], df["y"], df["P"], 100, -300, 300, 100, -300, 300, maxMom, title, "x [mm]", "y [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/BeamProfile/h3_XYMom_"+ntupleName+"_"+particle+"_"+config+".png", contours=False)
    # ut.Plot3D(df["x"], df["y"], df["P"], 100, -300, 300, 100, -300, 300, maxMom, "Entering TS collimator 1", "x [mm]", "y [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/BeamProfile/h3_XYMom_"+ntupleName+"_"+particle+"_"+config+".png", contours=False)
    # ut.Plot3D(df["x"], df["y"], df["P"], 100, -300, 300, 100, -300, 300, maxMom, "Entering TS collimator 3", "x [mm]", "y [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/BeamProfile/h3_XYMom_"+ntupleName+"_"+particle+"_"+config+".png", contours=False)
    # ut.Plot3D(df["x"], df["y"], df["P"], 100, -300, 300, 100, -300, 300, maxMom, "Entering TS collimator 5", "x [mm]", "y [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/BeamProfile/h3_XYMom_"+ntupleName+"_"+particle+"_"+config+".png", contours=False)
    ut.Plot3D(df["x"], df["y"], df["P"], 100, -300, 300, 100, -300, 300, maxMom, "Entering ST", "x [mm]", "y [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/BeamProfile/h3_XYMom_"+ntupleName+"_"+particle+"_"+config+".png", contours=False)
    Plot3DCustomCircle(df["x"], df["y"], df["P"], 100, -300, 300, 100, -300, 300, 600, title, "x [mm]", "y [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/BeamProfile/h3_XYMom_wcirc_"+ntupleName+"_"+particle+"_"+config+".png", contours=False, radius=200)
    # Momentum and radial distributions
    # ut.Plot1D(df["P"], 500, 0, maxMom, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamProfile/h1_mom_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)

    ut.Plot1D(df[df["R"] > 100]["P"], 500, 0, maxMom, title+", R > 100 mm", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamProfile/h1_mom_above100mm_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)
    # ut.Plot1DWithGaussFit(df["P"], 500, 0, maxMom, 100, 85, 50, 50, 100, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamProfile/h1_mom_wGausFit_"+ntupleName+"_"+particle+"_"+config+".png", errors=True) # , peak=True)

    ut.Plot1D(df["R"], 500, 0, 500, title, "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/BeamProfile/h1_rad_"+ntupleName+"_"+particle+"_"+config+".png", errors=True)
    ut.Plot1D(df[df["P"] < 50]["R"], 250, 0, 250, title+", <50 MeV", "Radius [mm]", "Counts / mm", "../img/"+g4blVer+"/BeamProfile/h1_rad_below50MeV_"+ntupleName+"_"+particle+"_"+config+".png", errors=True)

    ut.Plot1D(df["HelixR"], 500, 0, 500, title, "Radial position of helical axis [mm]", "Counts / mm", "../img/"+g4blVer+"/BeamProfile/h1_helix_rad_"+ntupleName+"_"+particle+"_"+config+".png", errors=True)

    # return

    # Tranvserse position
    # ut.Plot2D(df["x"], df["y"], 400, -200, 200, 400, -200, 200, title, "x [mm]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XvsY_"+ntupleName+"_"+particle+"_"+config+".png") 
    ut.Plot2D(df["x"], df["y"], 40, -200, 200, 40, -200, 200, title, "x [mm]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XvsY_"+ntupleName+"_"+particle+"_"+config+".png") 
    ut.Plot2D(df[df["P"] < 50]["x"], df[df["P"] < 50]["y"], 40, -200, 200, 40, -200, 200, title+", <50 MeV", "x [mm]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XvsY_below50MeV_"+ntupleName+"_"+particle+"_"+config+".png") 

    # Make 2D dispersion plots
    ut.Plot2D(df["P"], df["x"], 250, 0, 250, 440, -220, 220, title, "Momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XvsMom_"+ntupleName+"_"+particle+"_"+config+".png") 
    # ut.Plot2D(df["P"], df["y"], 250, 0, 250, 440, -220, 220, title, "Momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_YvsMom_"+ntupleName+"_"+particle+"_"+config+".png") 
    ut.Plot2D(df["P"], df["y"], 100, 0, 100, 225, -25, 200, title, "Momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_YvsMom_"+ntupleName+"_"+particle+"_"+config+".png") 

    # x_, xerr_, y_, yerr_ = ut.ProfileX(df["P"], df["y"], 100, 0, 100, 225, -25, 200)
    # ut.PlotGraph(x_, xerr_, y_, yerr_, title, "Average momentum [MeV] / mm", "Average y [mm] / MeV", "../img/"+g4blVer+"/BeamProfile/px_YvsMom_"+ntupleName+"_"+particle+"_"+config+".png")

    ut.Plot2D(df["PT"], df["x"], 200, 0, 200, 440, -220, 220, title, "Tranverse momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XvsMomT_"+ntupleName+"_"+particle+"_"+config+".png") 
    ut.Plot2D(df["PT"], df["y"], 200, 0, 200, 440, -220, 220, title, "Tranverse momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_YvsMomT_"+ntupleName+"_"+particle+"_"+config+".png") 

    ut.Plot2D(df["Pz"], df["x"], 400, -200, 200, 440, -220, 220, title, "Longitundinal momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XvsMomZ_"+ntupleName+"_"+particle+"_"+config+".png")
    ut.Plot2D(df["Pz"], df["y"], 400, -200, 200, 440, -220, 220, title, "Longitundinal momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_YvsMomZ_"+ntupleName+"_"+particle+"_"+config+".png")

    ut.Plot2D(df["P"], df["R"], 250, 0, 250, 210, 0, 210, title, "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RvsMom_"+ntupleName+"_"+particle+"_"+config+".png")
    ut.Plot2D(df["PT"], df["R"], 200, 0, 200, 210, 0, 210, title, "Tranverse momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RvsMomT_"+ntupleName+"_"+particle+"_"+config+".png")

    ut.Plot2D(df["P"], df["HelixR"], 250, 0, 250, 210, 0, 210, title, "Momentum [MeV]", "Radial position of helical axis [mm]", "../img/"+g4blVer+"/BeamProfile/h2_helix_rad_vs_mom_"+ntupleName+"_"+particle+"_"+config+".png")
    # ut.Plot2D(df["PT"], df["R"], 200, 0, 200, 210, 0, 210, title, "Tranverse momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RvsMomT_"+ntupleName+"_"+particle+"_"+config+".png")

    # P/R and Log(P/R)

    ut.Plot1D(df["R"]/df["P"], 250, 0, 1, title, "R/p [mm/MeV]", "Counts", "../img/"+g4blVer+"/BeamProfile/h1_rad_over_mom_"+ntupleName+"_"+particle+"_"+config+".png")
    ut.Plot1D(np.log(df["R"]/df["P"]), 250, -10, 10, title, "Log(R/p)", "Counts", "../img/"+g4blVer+"/BeamProfile/h1_log_rad_over_mom_"+ntupleName+"_"+particle+"_"+config+".png")
    # ut.Plot2D(df[(np.log(df["R"]/df["P"]) > -5.0) & (np.log(df["R"]/df["P"]) < 2.5)]["P"], df[(np.log(df["R"]/df["P"]) > -5.0) & (np.log(df["R"]/df["P"]) < -2.5)]["R"], 250, 0, 250, 210, 0, 210, title, "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RvsMom_cut_"+ntupleName+"_"+particle+"_"+config+".png")
    # ---- Special plots for illustration ----

    Plot2DCustomBox(df["P"], df["R"], 250, 0, 250, 200, 0, 200, title, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RvsMom_wline_"+ntupleName+"_"+particle+"_"+config+".png")
    ut.Plot2D(df["P"], df["R"], 50, 0, 250, 40, 0, 200, title, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RvsMom_coarseBinning_"+ntupleName+"_"+particle+"_"+config+".png")
    Plot2DCustomBox(df["P"], df["R"], 50, 0, 250, 40, 0, 200, title, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RvsMom_wline_coarseBinning_"+ntupleName+"_"+particle+"_"+config+".png")

    # x vs y vs mom
    ut.Plot3D(df["x"], df["y"], df["P"], 100, -300, 300, 100, -300, 300, maxMom, title, "x [mm]", "y [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/BeamProfile/h3_XYMom_"+ntupleName+"_"+particle+"_"+config+".png", contours=False)
    Plot3DCustomCircle(df["x"], df["y"], df["P"], 80, -200, 200, 80, -200, 200, maxMom, title, "x [mm]", "y [mm]", "Mean momentum [MeV]", "../img/"+g4blVer+"/BeamProfile/h3_XYMom_wcirc_"+ntupleName+"_"+particle+"_"+config+".png", contours=False, radius=80)

    # Slice momentum 
    for i in range(0, 201, 50):

        # Upper bound
        j = i+50 

        # Create a new array filled with zeros
        momCut = np.zeros_like(df["P"])

        # Cut momentum while preserving the structure of mom array
        momCut[(df["P"] >= i) & (df["P"] < j)] = df["P"][(df["P"] >= i) & (df["P"] < j)]

        ut.Plot2D(df[(df["P"] >= i) & (df["P"] < j)]["x"], df[(df["P"] >= i) & (df["P"] < j)]["y"], 40, -200, 200, 40, -200, 200, title+":\n "+str(int(i))+"< p [MeV] < "+str(j), "x [mm]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/MomSlices/h2_XY_"+ntupleName+"_"+particle+"_"+config+"_"+str(int(i))+"_"+str(int(j))+"MeV.png")
        Plot2DCustomCircle(df[(df["P"] >= i) & (df["P"] < j)]["x"], df[(df["P"] >= i) & (df["P"] < j)]["y"], 40, -200, 200, 40, -200, 200, title+":\n "+str(int(i))+"< p [MeV] < "+str(j), "x [mm]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/MomSlices/h2_XY_wcirc_"+ntupleName+"_"+particle+"_"+config+"_"+str(int(i))+"_"+str(int(j))+"MeV.png", radius=85)

    # Radius verus momentum 2D
    ut.Plot2D(df["P"], df["R"], 250, 0, 250, 200, 0, 200, title, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RadiusVsMom_"+ntupleName+"_"+particle+"_"+config+".png")
    # Plot2DCustomBox(df["P"], df["R"], 250, 0, 250, 200, 0, 200, title, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RadiusVsMom_wline_"+ntupleName+"_"+particle+"_"+config+".png")
    # Plot2DCustomBox(df["P"], df["R"], 25, 0, 25, 20, 0, 200, title, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RadiusVsMom_wline_"+ntupleName+"_"+particle+"_"+config+".png")

    # xProfile of momentum versus radius
    # x_, xerr_, y_, yerr_, yrms_ = ut.ProfileX(df["P"], df["R"], 250, 0, 250, 200, 0, 200)
    x_, xerr_, y_, yerr_, yrms_ = ut.ProfileX(df[df["P"]<=150]["R"], df[df["P"]<=150]["P"], 200, 0, 200, 250, 0, 250)

    ut.PlotGraph(x_, xerr_, y_, yerr_, title, "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/BeamProfile/px_RadiusVsMom_"+ntupleName+"_"+particle+"_"+config+".png")

    # Create an HDF5 file
    h5File = "../h5/"+g4blVer+"/BeamProfile/dispersion_reversed_150MeVcut_"+ntupleName+"_"+particle+"_"+config+".h5"

    with h5py.File(h5File, "w") as hf:
        # Create datasets for x_, xerr_, y_, and yerr_
        hf.create_dataset("x_", data=x_)
        hf.create_dataset("xerr_", data=xerr_)
        hf.create_dataset("y_", data=y_)
        hf.create_dataset("yerr_", data=yerr_)
        hf.create_dataset("yrms_", data=yrms_)

    print("---> Written", h5File)

    return

def main():

    RunBeamProfile("Mu2E_1e7events_PSRingWedge_l25mm_r110mm_fromZ1850", "VirtualDetector/prestop", "e-", 100)
    RunBeamProfile("Mu2E_1e7events_PSRingWedge_l25mm_r110mm_fromZ1850_noColl_noPbar", "VirtualDetector/prestop", "e-", 100)

if __name__ == "__main__":
    main()
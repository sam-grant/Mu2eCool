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

def Plot2DCustomLine(x, y, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", NDPI=300):

    # Create 2D histogram
    hist, x_edges, y_edges = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])

    # Set up the plot
    fig, ax = plt.subplots()

    # Plot the 2D histogram
    im = ax.imshow(hist.T, cmap='inferno', extent=[xmin, xmax, ymin, ymax], aspect='auto', origin='lower', vmax=np.max(hist)) # , norm=cm.LogNorm())

    # Add colourbar
    plt.colorbar(im)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Format main plot axes
    # ax1.set_title(title, fontsize=16, pad=10)
    # ax1.set_xlabel(xlabel, fontsize=14, labelpad=10) 
    # ax1.set_ylabel(ylabel, fontsize=14, labelpad=10) 

    # # Set font size of tick labels on x and y axes
    # ax1.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
    # ax1.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size

    # Define the function y = 2x
    m = 2 # gradient
    b = 75 # x-intercept
    c = -b*m

    x_values = np.linspace(x_edges[0], x_edges[-1], nBinsX)
    y_values = m * x_values + c

    # Mask y_values to only include values within the original y range
    x_values = np.ma.masked_outside(x_values, xmin, xmax)
    y_values = np.ma.masked_outside(y_values, ymin, ymax)

    # Plot the line on the histogram
    plt.plot(x_values, y_values, color='white', linestyle="--", label='y = 2x')
    

    
    # Create a Rectangle patch
    # box = Rectangle((xBoxMin, yBoxMin), width=(xmax - xBoxMin), height=(ymax - yBoxMin), fill=False, hatch="/", edgecolor='white', linestyle='--', linewidth=1)

    # Add the Rectangle patch to the plot
    # ax.add_patch(box)

    # Scientific notation
    if ax.get_xlim()[1] > 999:
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax.yaxis.offsetText.set_fontsize(14)

    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.close()

def Plot2DCustomBox(x, y, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", NDPI=300):

    # Create 2D histogram
    hist, x_edges, y_edges = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])

    # Set up the plot
    fig, ax = plt.subplots()

    # Plot the 2D histogram
    im = ax.imshow(hist.T, cmap='inferno', extent=[xmin, xmax, ymin, ymax], aspect='auto', origin='lower', vmax=np.max(hist)) # , norm=cm.LogNorm())

    # Add colourbar
    plt.colorbar(im)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Format main plot axes
    # ax1.set_title(title, fontsize=16, pad=10)
    # ax1.set_xlabel(xlabel, fontsize=14, labelpad=10) 
    # ax1.set_ylabel(ylabel, fontsize=14, labelpad=10) 

    # # Set font size of tick labels on x and y axes
    # ax1.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
    # ax1.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size


    ax.axvline(x=50.0, color='white', linestyle='--', linewidth=1)
    ax.axhline(y=100.0, color='white', linestyle='--', linewidth=1)

    xBoxMin = 0.0
    yBoxMin = 100.0
    
    # Create a Rectangle patch
    # box = Rectangle((xBoxMin, yBoxMin), width=(xmax - xBoxMin), height=(ymax - yBoxMin), fill=False, hatch="/", edgecolor='white', linestyle='--', linewidth=1)

    # Add the Rectangle patch to the plot
    # ax.add_patch(box)

    # Scientific notation
    if ax.get_xlim()[1] > 999:
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax.yaxis.offsetText.set_fontsize(14)

    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.close()

def Plot2DCustomBox2(x, y, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", NDPI=300):

    # Create 2D histogram
    hist, x_edges, y_edges = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])

    # Set up the plot
    fig, ax = plt.subplots()

    # Plot the 2D histogram
    im = ax.imshow(hist.T, cmap='inferno', extent=[xmin, xmax, ymin, ymax], aspect='auto', origin='lower', vmax=np.max(hist)) # , norm=cm.LogNorm())

    # Add colourbar
    plt.colorbar(im)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Format main plot axes
    # ax1.set_title(title, fontsize=16, pad=10)
    # ax1.set_xlabel(xlabel, fontsize=14, labelpad=10) 
    # ax1.set_ylabel(ylabel, fontsize=14, labelpad=10) 

    # # Set font size of tick labels on x and y axes
    # ax1.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
    # ax1.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size


    # ax.axvline(x=50.0, color='white', linestyle='--', linewidth=1)
    ax.axhline(y=100.0, color='white', linestyle='--', linewidth=1)
    ax.axhline(y=-100.0, color='white', linestyle='--', linewidth=1)

    xBoxMin = 0.0
    yBoxMin = 100.0
    
    # Create a Rectangle patch
    # box = Rectangle((xBoxMin, yBoxMin), width=(xmax - xBoxMin), height=(ymax - yBoxMin), fill=False, hatch="/", edgecolor='white', linestyle='--', linewidth=1)

    # Add the Rectangle patch to the plot
    # ax.add_patch(box)

    # Scientific notation
    if ax.get_xlim()[1] > 999:
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
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
    im = ax.imshow(hist.T, cmap='inferno', extent=[xmin, xmax, ymin, ymax], aspect='auto', origin='lower', vmax=np.max(hist)) # , norm=cm.LogNorm())

    # Add colourbar
    plt.colorbar(im)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Scientific notation
    if ax.get_xlim()[1] > 999:
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax.yaxis.offsetText.set_fontsize(14)

    circle = Circle((0, 0), radius=radius, fill=False, edgecolor='white', linestyle='--', linewidth=1)
    ax.add_patch(circle)

    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.close()

# def Plot2DCustomCurve(x, y, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", radius=100, NDPI=300):

#     # Create 2D histogram
#     hist, x_edges, y_edges = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])

#     # Set up the plot
#     fig, ax = plt.subplots()

#     # Plot the 2D histogram
#     im = ax.imshow(hist.T, cmap='inferno', extent=[xmin, xmax, ymin, ymax], aspect='auto', origin='lower', vmax=np.max(hist)) # , norm=cm.LogNorm())

#     # Add colourbar
#     plt.colorbar(im)

#     plt.title(title)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)

#     # Scientific notation
#     if ax.get_xlim()[1] > 999:
#         ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
#         ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
#         ax.xaxis.offsetText.set_fontsize(14)
#     if ax.get_ylim()[1] > 999:
#         ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
#         ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#         ax.yaxis.offsetText.set_fontsize(14)

#     circle = Circle((0, 0), radius=radius, fill=False, edgecolor='white', linestyle='--', linewidth=1)
#     ax.add_patch(circle)

#     plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
#     print("---> Written", fout)

#     # Clear memory
#     plt.close()

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
    im = ax.imshow(hist_xy.T, cmap='inferno', extent=[xmin, xmax, ymin, ymax], aspect='auto', origin='lower', vmax=zmax) # z.max()) # , norm=cm.LogNorm())

    # Add colourbar
    cbar = plt.colorbar(im) # , ticks=np.linspace(zmin, zmax, num=10)) 

    # Add contour lines to visualize bin boundaries
    if contours:
        contour_levels = np.linspace(zmin, zmax, num=nBinsZ)
        print(contour_levels)
        # ax.contour(hist_xy.T, levels=[66], extent=[xmin, xmax, ymin, ymax], colors='white', linewidths=0.7)
        ax.contour(hist_xy.T, levels=contour_levels, extent=[xmin, xmax, ymin, ymax], colors='white', linewidths=0.7)

    # Draw a circle with radius 100 mm (Absorber1)
    # circle_center = (0, 0)
    # circle_radius = 50
    circle = Circle((0, 0), radius=radius, fill=False, edgecolor='white', linestyle='--', linewidth=1)
    ax.add_patch(circle)

    plt.title(title, fontsize=16, pad=10)
    plt.xlabel(xlabel, fontsize=14, labelpad=10)
    plt.ylabel(ylabel, fontsize=14, labelpad=10)
    cbar.set_label(zlabel, fontsize=14, labelpad=10)

    # Scientific notation
    if ax.get_xlim()[1] > 999:
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax.yaxis.offsetText.set_fontsize(14)
    # if ax.get_zlim()[1] > 999:
    #     ax.zaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    #     ax.ticklabel_format(style='sci', axis='z', scilimits=(0,0))
    #     ax.zaxis.offsetText.set_fontsize(14)

    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.close()

    return

def Run(config, branchNames, ntupleName, particle):

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

    df = ut.TTreeToDataFrame(finName, ntupleName, branchNames)  

    ntupleName = ntupleName.split("/")[1] 

    # Filter upstream particles 
    # df = df[df['Pz'] > 0]



    title = particle+", Z = "+ntupleName[1:]+" mm"

    # Particle populations
    ut.BarChart(df['PDGid'], particleDict, config+", "+title, "", "Percentage / particle", fout="../img/"+g4blVer+"/BeamProfile/bar_ParticleFractionPecentage_"+ntupleName+"_"+config+".png", percentage=True)
    ut.BarChart(df['PDGid'], particleDict, config+", "+title, "", "Counts / particle", fout="../img/"+g4blVer+"/BeamProfile/bar_ParticleFractionCounts_"+ntupleName+"_"+config+".png", percentage=False)

    # Upstream / downstream particles?

    df_upstream = df[df['Pz'] > 0]
    df_downstream = df[df['Pz'] < 0]

    ut.BarChart(df_upstream['PDGid'], particleDict, config+", "+title+", upstream", "", "Counts / particle", fout="../img/"+g4blVer+"/BeamProfile/bar_ParticleFractionCountsUpstream_"+ntupleName+"_"+config+".png", percentage=False)
    ut.BarChart(df_downstream ['PDGid'], particleDict, config+", "+title+", downstream", "", "Counts / particle", fout="../img/"+g4blVer+"/BeamProfile/bar_ParticleFractionCountsDownstream_"+ntupleName+"_"+config+".png", percentage=False)

    # Duplicate tracks?

    df['UniqueID'] = 1e6*df['EventID'] + 1e3*df['TrackID'] + df['ParentID'] 

    unique_df = df.drop_duplicates(subset=['UniqueID'])

    ut.BarChart(unique_df['PDGid'], particleDict, config+", "+title, "", "Counts / particle", fout="../img/"+g4blVer+"/BeamProfile/bar_ParticleFractionCountsUniqueTracks_"+ntupleName+"_"+config+".png", percentage=False)

    df = unique_df

    # df = df[df['Pz'] > 0]

    print("proton =", df[df['PDGid'] == 2212].shape[0])
    print("anti_proton =", df[df['PDGid'] == -2212].shape[0])
    print("pi+ =", df[df['PDGid'] == 211].shape[0])
    print("pi- =", df[df['PDGid'] == -211].shape[0])
    print("mu+ =", df[df['PDGid'] == -13].shape[0])
    print("mu- =", df[df['PDGid'] == 13].shape[0])

    # return

    # Filter particles
    PDGid = 0

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
        df = df[(df['PDGid'] == -13) | (df['PDGid'] == 13)]

    # Momentum and radial distributions 
    df.loc[:, 'P'] = np.sqrt( np.power(df["Px"],2) + np.power(df["Py"],2) + np.power(df["Pz"],2) ) 
    df.loc[:, 'R'] = np.sqrt( np.power(df['x'],2) + np.power(df['y'],2)) 
    # Tranvserse momentum 
    df.loc[:, 'PT'] = np.sqrt( np.power(df["Px"],2) + np.power(df["Py"],2) ) 

    # Make dispersion plots
    ut.Plot2D(df['P'], df['x'], 250, 0, 250, 440, -220, 220, title, "Momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XvsMom_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
    ut.Plot2D(df['P'], df['y'], 250, 0, 250, 440, -220, 220, title, "Momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_YvsMom_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)

    ut.Plot2D(df['PT'], df['x'], 200, 0, 200, 440, -220, 220, title, "Tranverse momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XvsMomT_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
    ut.Plot2D(df['PT'], df['y'], 200, 0, 200, 440, -220, 220, title, "Tranverse momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_YvsMomT_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)

    ut.Plot2D(df['Pz'], df['x'], 400, -200, 200, 440, -220, 220, title, "Longitundinal momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XvsMomZ_"+ntupleName+"_"+particle+"_"+config+".png" , cb=False)
    ut.Plot2D(df['Pz'], df['y'], 400, -200, 200, 440, -220, 220, title, "Longitundinal momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_YvsMomZ_"+ntupleName+"_"+particle+"_"+config+".png" , cb=False)

    ut.Plot2D(df['P'], df['R'], 250, 0, 250, 210, 0, 210, title, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RVsMom_"+ntupleName+"_"+particle+"_"+config+".png", cb=True)

    # ---- Special plots for illustration ----

    # Plot2DCustomBox(df['P'], df['R'], 250, 0, 250, 200, 0, 200, particle+" at "+ntupleName, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RVsMom_wline_"+ntupleName+"_"+particle+"_"+config+".pdf")
    # Plot2DCustomBox2(df['P'], df['x'], 500, 0, 500, 250, -250, 250, title, "Momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XvsMom_wline_"+ntupleName+"_"+particle+"_"+config+".pdf") # df['P'], df['R'], 250, 0, 250, 200, 0, 200, particle+" at "+ntupleName, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RVsMom_wline_"+ntupleName+"_"+particle+"_"+config+".pdf")
    # Plot2DCustomBox2(df['P'], df['y'], 500, 0, 500, 250, -250, 250, title, "Momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_YvsMom_wline_"+ntupleName+"_"+particle+"_"+config+".pdf") # df['P'], df['R'], 250, 0, 250, 200, 0, 200, particle+" at "+ntupleName, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RVsMom_wline_"+ntupleName+"_"+particle+"_"+config+".pdf")

    return

    # x vs y vs mom
    ut.Plot3D(df['x'], df['y'], df['P'], 80, -200, 200, 80, -200, 200, 250, particle+" at "+ntupleName, "x [mm]", "y [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/BeamProfile/h3_XYMom_"+ntupleName+"_"+particle+"_"+config+".pdf", contours=False)
    

    
    # Plot2DCustomLine(df['P'], df['R'], 250, 0, 250, 200, 0, 200, particle+" at "+ntupleName, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RadiusVsMom_wcutline_"+ntupleName+"_"+particle+"_"+config+".png")
    Plot3DCustomCircle(df['x'], df['y'], df['P'], 80, -200, 200, 80, -200, 200, 250, particle+" at "+ntupleName, "x [mm]", "y [mm]", "Mean momentum [MeV]", "../img/"+g4blVer+"/BeamProfile/h3_XYMom_wcirc_"+ntupleName+"_"+particle+"_"+config+".pdf", contours=False, radius=100)

    return

    # Momentum and radial distributions
    ut.Plot1D(df['P'], 500, 0, 500, particle+" at "+ntupleName, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamProfile/h1_mom_"+ntupleName+"_"+particle+"_"+config+".pdf") # , errors=True)
    ut.Plot1D(df['R'], 300, 0, 300, particle+" at "+ntupleName, "Radus [mm]", "Counts / mm", "../img/"+g4blVer+"/BeamProfile/h1_rad_"+ntupleName+"_"+particle+"_"+config+".pdf") # , errors=True)


    # Transverse beam profile in position and momentum 
    ut.Plot2D(df['x'], df['y'], 400, -200, 200, 400, -200, 200, particle+" at "+ntupleName, "x [mm]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XY_"+ntupleName+"_"+particle+"_"+config+".pdf")
    # ut.Plot2DWith1DProj(df['x'], df['y'], 400, -200, 200, 400, -200, 200, particle+" at "+ntupleName, "x [mm]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XY_wproj_"+ntupleName+"_"+particle+"_"+config+".pdf")
    # ut.Plot2D(df['Px'], df['Py'], 400, -200, 200, 400, -200, 200, particle+" at "+ntupleName, "Px [mm]", "Py [mm]", "../img/"+g4blVer+"/BeamProfile/h2_MomXY_"+ntupleName+"_"+particle+"_"+config+".pdf")
    # ut.Plot2DWith1DProj(df['Px'], df['Py'], 400, -200, 200, 400, -200, 200, particle+" at "+ntupleName, "Px [mm]", "Py [mm]", "../img/"+g4blVer+"/BeamProfile/h2_MomXY_wproj_"+ntupleName+"_"+particle+"_"+config+".pdf")

    # Slice momentum 
    for i in range(0, 201, 50):

        # Upper bound
        j = i+50 

        # Create a new array filled with zeros
        momCut = np.zeros_like(df['P'])

        # Cut momentum while preserving the structure of mom array
        momCut[(df['P'] >= i) & (df['P'] < j)] = df['P'][(df['P'] >= i) & (df['P'] < j)]

        # ut.Plot2D(df[(df['P'] >= i) & (df['P'] < j)]['x'], df[(df['P'] >= i) & (df['P'] < j)]['y'], 400, -200, 200, 400, -200, 200, particle+" at "+ntupleName+":\n "+str(int(i))+"< p [MeV] < "+str(j), "x [mm]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XY_"+ntupleName+"_"+particle+"_"+config+"_"+str(int(i))+"_"+str(int(j))+"MeV.pdf")
        # Plot2DCustomCircle(df[(df['P'] >= i) & (df['P'] < j)]['x'], df[(df['P'] >= i) & (df['P'] < j)]['y'], 400, -200, 200, 400, -200, 200, particle+" at "+ntupleName+":\n "+str(int(i))+"< p [MeV] < "+str(j), "x [mm]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_XY_wcirc_"+ntupleName+"_"+particle+"_"+config+"_"+str(int(i))+"_"+str(int(j))+"MeV.pdf", radius=100)
        # Plot3DCustomCircle(df['x'], df['y'], momCut, 80, -200, 200, 80, -200, 200, j, particle+" at "+ntupleName+":\n "+str(int(i))+"< p [MeV] < "+str(j), "x [mm]", "y [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/BeamProfile/h3_XYMom_wcirc_"+ntupleName+"_"+particle+"_"+config+"_"+str(int(i))+"_"+str(int(j))+"MeV.pdf", contours=False, radius=100)

    # Radius verus momentum 2D
    ut.Plot2D(df['P'], df['R'], 250, 0, 250, 200, 0, 200, particle+" at "+ntupleName, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RadiusVsMom_"+ntupleName+"_"+particle+"_"+config+".pdf")
    Plot2DCustomBox(df['P'], df['R'], 250, 0, 250, 200, 0, 200, particle+" at "+ntupleName, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RadiusVsMom_wline_"+ntupleName+"_"+particle+"_"+config+".pdf")
    # Plot2DWith1DProjCustom(mom, rad, 250, 0, 250, 200, 0, 200, particle+" at "+ntupleName, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/BeamProfile/h2_RadiusVsMom_wproj_wline_"+particle+"_"+config+".pdf")

    # Momentum versus transverse position 
    # ut.Plot2D(df['P'], df['x'], 250, 0, 250, 400, -200, 200, particle+" at "+ntupleName, "Momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/BeamProfile/h2_MomVsX_"+ntupleName+"_"+particle+"_"+config+".pdf")
    # ut.Plot2DWith1DProj(df['P'], df['x'], 250, 0, 250, 400, -200, 200, particle+" at "+ntupleName, "Momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/BeamProfile/h2_MomVsX_wproj_"+ntupleName+"_"+particle+"_"+config+".pdf")
    # ut.Plot2D(df['P'], df['y'], 250, 0, 250, 400, -200, 200, particle+" at "+ntupleName, "Momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_MomVsY_"+ntupleName+"_"+particle+"_"+config+".pdf")
    # ut.Plot2DWith1DProj(df['P'], df['y'], 250, 0, 250, 400, -200, 200, particle+" at "+ntupleName, "Momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/BeamProfile/h2_MomVsY_wproj_"+ntupleName+"_"+particle+"_"+config+".pdf")


    # 

    # xProfile of momentum versus radius
    xProfile, xProfileErrors = ut.ProfileX(df['P'], df['R'], 250, 0, 250, 200, 0, 200)
    # ut.PlotGraph(xProfile, xProfileErrors, particle+" at "+ntupleName, "Mean radius [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/BeamProfile/px_RadiusVsMom_"+ntupleName+"_"+particle+"_"+config+".pdf")

    return

def RunParticleMomentum(config, branchNames, ntupleName):

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

    # Get data
    df = ut.TTreeToDataFrame(finName, ntupleName, branchNames)  

    df = df[df['Pz'] > 0]

    ntupleName = ntupleName.split("/")[1] 

    df["P"] = np.sqrt( np.power(df["Px"], 2) + np.power(df["Py"], 2) + np.power(df["Pz"], 2) )

    df_proton = df[df["PDGid"] == 2212]
    df_pion = df[ (df['PDGid'] == -211) | (df['PDGid'] == 211) ]
    df_muon = df[ (df['PDGid'] == 13) | (df['PDGid'] == -13) ]

    ut.Plot1DOverlay([df["P"], df_proton["P"], df_pion["P"], df_muon["P"]], nbins=1350, xmin=0, xmax=1350, title = ntupleName, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = ["All", "$p$", "$\pi^{\pm}$", "$\mu^{\pm}$"], fout = "../img/"+g4blVer+"/BeamProfile/h1_ParticleMomentumOverlay_"+ntupleName+"_"+config+".png")

    print("Mean momentum [MeV]:")
    print("---> all:", np.mean(df["P"]))
    print("---> proton:", np.mean(df_proton["P"])) 
    print("---> pion:", np.mean(df_pion["P"]))
    print("---> muon:", np.mean(df_muon["P"]))

    print("RMS momentum [MeV]:")
    print("---> all:", np.std(df["P"]))
    print("---> proton:", np.std(df_proton["P"])) 
    print("---> pion:", np.std(df_pion["P"]))
    print("---> muon:", np.std(df_muon["P"]))


    # print("Peak momentum [MeV]:")
    # print("---> all:", df["P"].value_counts().idxmax())
    # print("---> proton:", df_proton["P"].value_counts().idxmax())
    # print("---> pion:", df_pion["P"].value_counts().idxmax())
    # print("---> muon:", df_muon["P"].value_counts().idxmax())

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

    # config="Mu2E_1e7events_fromZ1800_parallel"
    config="Mu2E_1e7events_fromZ2265_parallel"

    # config="Mu2E_1e7events" # _ManyZNTuple1"
    # config="Mu2E_1e7events_fromZ1800_parallel"
    # config="Mu2E_1e7events_fromZ1800_parallel"
    # config="Mu2E_1e7events_fromZ2265_parallel" 
    # config="Mu2E_1e7events_fromZ1800_parallel" 

    ntupleName="NTuple/Z2265" # 965"

    # ntupleName="NTuple/Z1850" # 965"
    # ntupleName="NTuple/Z3265"
    # ntupleName="VirtualDetector/BeAbsorber_DetIn"
    # config="Mu2E_1e7events_Absorber0_fromZ2265_parallel" 
    # config="Mu2E_1e7events_Absorber1_fromZ2265_parallel" 

    # Run(config, branchNames, ntupleName, "all") 
    # Run(config, branchNames, ntupleName, "no_proton") 
    # # Run(config, branchNames, ntupleName, "pi-_and_mu-") 
    # Run(config, branchNames, ntupleName, "proton") 
    # Run(config, branchNames, ntupleName, "pi+") 
    # Run(config, branchNames, ntupleName, "pi-") 
    # Run(config, branchNames, ntupleName, "mu+") 
    # Run(config, branchNames, ntupleName, "mu-") 
    # Run("Mu2E_1e7events", branchNames, ntupleName, "no_proton") 
    # Run("Mu2E_1e7events_fromZ1800_parallel", branchNames, ntupleName, "no_proton") 

    # Run("Mu2E_1e7events_Z1850", branchNames, ntupleName, "no_proton") 

    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel", branchNames, ntupleName)
    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel", branchNames, "NTuple/Z1850")
    # RunParticleMomentum("Mu2E_1e7events_Absorber0_fromZ1850_parallel", branchNames, "NTuple/Z1850") # "VirtualDetector/BeAbsorber_DetIn")
    # RunParticleMomentum("Mu2E_1e7events_Absorber0_fromZ1850_parallel_noColl03", branchNames, "NTuple/Z1850") # "VirtualDetector/BeAbsorber_DetIn")
    # RunParticleMomentum("Mu2E_1e7events_Absorber0_fromZ1850_parallel", branchNames, "VirtualDetector/BeAbsorber_DetIn")

    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel", branchNames, "NTuple/Z1850")
    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel", branchNames, "VirtualDetector/Coll_01_DetIn")
    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel", branchNames, "VirtualDetector/Coll_01_DetOut")
    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel", branchNames, "VirtualDetector/Coll_03_DetIn")
    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel", branchNames, "VirtualDetector/Coll_03_DetOut")
    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel", branchNames, "VirtualDetector/Coll_05_DetIn")
    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel", branchNames, "VirtualDetector/Coll_05_DetOut")
    RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel", branchNames, "VirtualDetector/prestop")

    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel_noColl03", branchNames, "NTuple/Z1850")
    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel_noColl03", branchNames, "VirtualDetector/Coll_01_DetIn")
    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel_noColl03", branchNames, "VirtualDetector/Coll_01_DetOut")
    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel_noColl03", branchNames, "VirtualDetector/Coll_03_DetIn")
    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel_noColl03", branchNames, "VirtualDetector/Coll_03_DetOut")
    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel_noColl03", branchNames, "VirtualDetector/Coll_05_DetIn")
    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel_noColl03", branchNames, "VirtualDetector/Coll_05_DetOut")
    # RunParticleMomentum("Mu2E_1e7events_fromZ1850_parallel_noColl03", branchNames, "VirtualDetector/prestop")


if __name__ == "__main__":
    main()



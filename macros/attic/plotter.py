import uproot
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import h5py

# Enable LaTeX rendering
plt.rcParams["text.usetex"] = True

# Make branch names global
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
    "Weight"
]  

import math

def Round(value, sf):
    if value == 0:
        return 0
    power = math.floor(math.log10(abs(value)))
    factor = 10 ** (power - sf + 1)
    rounded = math.ceil(value / factor) * factor
    return rounded


def GetBasicStats(data):

    N = len(data)                      
    mean = np.mean(data)  
    meanErr = stats.sem(data) # Mean error (standard error of the mean from scipy)
    stdDev = np.std(data) # Standard deviation
    stdDevErr = np.sqrt(stdDev**2 / (2*N)) # Standard deviation error assuming normal distribution

    return N, mean, meanErr, stdDev, stdDevErr

def plot1D(data, nBins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", NDPI=300):
    
    # Create figure and axes
    fig, ax = plt.subplots()

    # Plot the histogram with outline
    counts, bin_edges, _ = ax.hist(data, bins=nBins, range=(xmin, xmax), histtype='step', edgecolor='black', linewidth=1.0, fill=False, density=False)

    # Set x-axis limits
    ax.set_xlim(xmin, xmax)

    # Calculate statistics
    N, mean, meanErr, stdDev, stdDevErr = GetBasicStats(data)

    # Error SF should always be zero
    # errSF = 1

    # Round the errors to the specified number of significant figures
    # roundedMeanErr = Round(meanErr, errSF)
    # roundedStdDevErr = Round(stdDevErr, errSF)

    # print("---> Rounding", meanErr, roundedMeanErr)

    # Determine the number of decimal places for the errors
    # meanDecimals = -int(np.floor(np.log10(abs(roundedMeanErr))))
    # stdDevDecimals = -int(np.floor(np.log10(abs(roundedStdDevErr))))

    # Round the value using the determined number of decimal places
    # roundedMean = round(mean, meanDecimals)
    # roundedStdDev = round(stdDev, stdDevDecimals)

    # Create legend text
    # legend_text = f"Entries: {N}\nMean: {roundedMean:.{meanDecimals}f}±{roundedMeanErr:.{errSF}f}\nStd Dev: {roundedStdDev:.{stdDevDecimals}f}±{roundedStdDevErr:.{errSF}f}"
    # legend_text = f"Entries: {N}\nMean: {mean:.{meanDecimals}f}±{roundedMeanErr:.{errSF}f}\nStd Dev: {roundedStdDev:.{stdDevDecimals}f}±{roundedStdDevErr:.{errSF}f}"

    legend_text = f"Entries: {N}\nMean: {mean:.3g}$\pm${meanErr:.1g}\nStd Dev: {stdDev:.3g}$\pm${stdDevErr:.1g}"
    # legend_text = f"Entries: {N}\nMean: {mean:.3g}\nStd Dev: {stdDev:.3g}"


    # Add legend to the plot
    ax.legend([legend_text], loc="upper left", frameon=False)

    ax.set_title(title)
    ax.set_xlabel(xlabel) 
    ax.set_ylabel(ylabel) 
    
    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.clf()
    plt.close()

def plot2D(x, y, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", NDPI=300):

    # Create 2D histogram
    hist, x_edges, y_edges = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])

    # Set up the plot
    fig, ax = plt.subplots()

    # Plot the 2D histogram
    im = ax.imshow(hist.T, cmap='inferno', extent=[xmin, xmax, ymin, ymax], aspect='auto', origin='lower', vmax=np.max(hist)) # , norm=cm.LogNorm())

    # Add colorbar
    plt.colorbar(im)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.close()

def plot2DWith1DProj(x, y, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", NDPI=300):

    # Create 2D histogram
    hist, x_edges, y_edges = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])

    # Set up the plot
    fig = plt.figure(figsize=(8, 10))
    gs = fig.add_gridspec(2, 2, width_ratios=[4, 1], wspace=0.1, hspace=0.1)

    # Plot the 2D histogram with a logarithmic color scale
    ax1 = fig.add_subplot(gs[0, 0])
    im = ax1.imshow(hist.T, cmap='inferno', extent=[xmin, xmax, ymin, ymax], aspect='auto', origin='lower')

    # Format main plot axes
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)

    # Add colorbar
    ax_cb = fig.add_subplot(gs[0, 1])
    cbar = plt.colorbar(im, cax=ax_cb)
    cbar.ax.set_position(cbar.ax.get_position().shrunk(0.25, 1))
    cbar.ax.set_position(cbar.ax.get_position().translated(0.10, 0))

    # Project the 2D histogram onto the x-axis
    hist_x = np.sum(hist, axis=1)
    bin_centers_x = (x_edges[:-1] + x_edges[1:]) / 2

    # Plot the 1D histogram along the x-axis
    ax2 = fig.add_subplot(gs[1, 0], sharex=ax1)
    counts, bin_edges, _ = ax2.hist(x, bins=nBinsX, range=(xmin, xmax), histtype='step', edgecolor='black', linewidth=1.0, fill=False)

    # Turn off tick numbering for y-axis
    ax2.yaxis.set_ticklabels([])
    # ax2.yaxis.set_ticklabels([])
    ax2.tick_params(axis='y', which='major', length=0)  # Hide tick markers
    # ax2.axis('off')

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_visible(True)

    # Set the position of ax2 while maintaining the same width and adjusting the height
    ax2.set_position([ax1.get_position().x0, ax1.get_position().y0 + ax1.get_position().height + 0.01, ax1.get_position().width, ax1.get_position().height / 5])

    # Project the 2D histogram onto the y-axis
    hist_y = np.sum(hist, axis=0)
    bin_centers_y = (y_edges[:-1] + y_edges[1:]) / 2

    # Plot the 1D histogram along the y-axis (rotated +90 degrees)
    ax3 = fig.add_subplot(gs[1, 1], sharey=ax1)
    counts, bin_edges, _ = ax3.hist(y, bins=nBinsY, range=(ymin, ymax), histtype='step', edgecolor='black', linewidth=1.0, fill=False, orientation='horizontal')

    # Turn off tick numbering for x-axis
    # ax3.axis('off')
    ax3.xaxis.set_ticklabels([])
    # ax3.yaxis.set_ticklabels([])

    ax3.tick_params(axis='x', which='major', length=0)  # Hide tick markers


    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_visible(True)
    ax3.spines['bottom'].set_visible(False)

    # Set the position of ax3 while maintaining the same height and adjusting the width
    ax3.set_position([ax1.get_position().x0 + ax1.get_position().width + 0.01, ax1.get_position().y0, ax1.get_position().width / 5, ax1.get_position().height])

    # Format main plot axes
    # ax1.axis('on')
    # ax1.set_xlabel(xlabel)
    # ax1.set_ylabel(ylabel)

    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.close()

def read(finName, treeName):

    print("\n---> Reading...")

    # Open the ROOT file
    fin = uproot.open(finName)
    
    print("---> Got input file ", finName, ", ", (fin))

    # Get tree
    tree = fin[treeName]

    print("---> Got tree ", str(tree))

    # Create an empty dictionary to store the selected columns as NumPy arrays
    branchData = {}

    # Iterate over the specified column names
    for branchName in branchNames:
        # Check if the column name exists in the TTree
        if branchName in tree:

            branchData[branchName] = tree[branchName].array(library="np")

    # Create the DataFrame directly from the dictionary of column data
    df = pd.DataFrame(branchData)

    print("---> Reading done, closing input file...")

    print("\n---> DataFrame:\n", df)

    # Close the ROOT file
    fin.close()

    # Return the DataFrame
    return df

def run(): # ene):

    g4blVersion="v3.08"
    nEvents="10e3"
    # ene=en
    stepSize="" # _maxStep50e-3"

    print("\n--->Running at "+str(ene)+"MeV")

    # finName = "../plots/g4beamline_pi-_"+str(ene)+"MeV_10e4events.root" 
    finName = "../plots/"+g4blVersion+"/g4beamline_pi-_"+str(ene)+"MeV_"+nEvents+"events"+stepSize+".root"

    # Access the TTree
    dfForward = read(finName, "VirtualDetector/DetForward")
    dfBackward = read(finName, "VirtualDetector/DetBackward")


    # Put this before filtering the whole DataFrame, so you can count other particles if you like
    nPiMinusForward = dfForward[dfForward['PDGid'] == -211].shape[0]
    print("Number of pi- at forward detector =", nPiMinusForward)

    nPiMinusBackward = dfBackward[dfBackward['PDGid'] == -211].shape[0]
    print("Number of pi- at backward detector =", nPiMinusBackward)

    # Check what other particles we have
    # filtered_df = dfForward[~dfForward['PDGid'].isin([5, 8, 11, -11, 13, -14, 14, -12, 13, 22, -211, -221, 2112, 2112.])]
    # print(filtered_df['PDGid'])

    # TODO: make this more sophisticated, with if statements and PDGids and so on
    particleFlag = "pi-"

    # Filter 
    if particleFlag=="pi-": 
        dfForward = dfForward[dfForward['PDGid'] == -211]
        dfBackward= dfBackward[dfBackward['PDGid'] == -211]

    timeForward = dfForward["t"]
    timeBackward = dfBackward["t"]   

    xForward = dfForward["x"]
    xBackward = dfBackward["x"]  

    yForward = dfForward["y"]
    yBackward = dfBackward["y"]  

    momForward = np.sqrt( pow(dfForward["Px"],2) + pow(dfForward["Py"],2) + pow(dfForward["Pz"],2) )
    momBackward = np.sqrt( pow(dfBackward["Px"],2) + pow(dfBackward["Py"],2) + pow(dfBackward["Pz"],2) )

    plot1D(momForward, 550, 0, 550, r""+g4blVersion+", forward detector, "+str(ene)+" MeV beam, $\pi^{-}$ only" , "Momentum [MeV]", "Events / MeV", "../img/"+g4blVersion+"/h1_mom_detForward_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")
    plot1D(momBackward, 550, 0, 550, r""+g4blVersion+", backward detector, $\pi^{-}$ only", "Momentum [MeV]", "Events / MeV", "../img/"+g4blVersion+"/h1_mom_detBackward_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")
    
    # Zoom in on 50 MeV peak
    plot1D(momBackward, 100, 49, 50, r""+g4blVersion+", backward detector, "+str(ene)+" MeV beam, $\pi^{-}$ only", "Momentum [MeV]", "Events", "../img/"+g4blVersion+"/h1_mom_detBackward_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV"+stepSize+"_zoom.pdf")

    plot1D(xForward, 220, -1100, 1100, r""+g4blVersion+", forward detector, "+str(ene)+" MeV beam, $\pi^{-}$ only", "x[mm]", "Events / 10 mm", "../img/"+g4blVersion+"/h1_x_detForward_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")
    plot1D(xBackward, 220, -1100, 1100, r""+g4blVersion+", backward detector, "+str(ene)+" MeV beam, $\pi^{-}$ only", "x [mm]", "Events / 10 mm", "../img/"+g4blVersion+"/h1_x_detBackward_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")

    plot1D(yForward, 220, -1100, 1100,  r""+g4blVersion+", forward detector, "+str(ene)+" MeV beam, $\pi^{-}$ only", "y [mm]" , "Events / 10 mm", "../img/"+g4blVersion+"/h1_y_detForward_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")
    plot1D(yBackward, 220, -1100, 1100,  r""+g4blVersion+", backward detector, "+str(ene)+" MeV beam, $\pi^{-}$ only", "y [mm]", "Events / 10 mm", "../img/"+g4blVersion+"/h1_y_detBackward_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")

    plot2D(xForward, yForward, 110, -550, 550, 110, -550, 550, r""+g4blVersion+", forward detector, "+str(ene)+" MeV beam, $\pi^{-}$ only", "x [mm]", "y [mm]", "../img/"+g4blVersion+"/h2_xy_detForward_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")
    plot2D(xBackward, yBackward, 110, -550, 550, 110, -550, 550, r""+g4blVersion+", backward detector, "+str(ene)+" MeV beam, $\pi^{-}$ only", "x [mm]", "y [mm]", "../img/"+g4blVersion+"/h2_xy_detBackward_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")

    plot2DWith1DProj(xForward, yForward, 110, -550, 550, 110, -550, 550, r""+g4blVersion+", forward detector, "+str(ene)+" MeV beam, $\pi^{-}$ only", "x [mm]", "y [mm]", "../img/"+g4blVersion+"/h2_xy_xProj_detForward_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")
    plot2DWith1DProj(xBackward, yBackward, 110, -550, 550, 110, -550, 550, r""+g4blVersion+", backward detector, "+str(ene)+" MeV beam, $\pi^{-}$ only", "x [mm]", "y [mm]", "../img/"+g4blVersion+"/h2_xy_xProj_detBackward_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")

    # Write everything to hdf5 file
    foutName = "../plots/"+g4blVersion+"/g4beamlinePlots_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV_10e4events"+stepSize+".0.h5"

    fout = h5py.File(foutName, "w")

    # Write the histograms to the HDF5 file
    fout.create_dataset("momForward", data=momForward)
    fout.create_dataset("momBackward", data=momBackward)
    fout.create_dataset("xForward", data=xForward)
    fout.create_dataset("xBackward", data=xBackward)
    fout.create_dataset("yForward", data=yForward)
    fout.create_dataset("yBackward", data=yBackward)

    # Close the HDF5 file
    fout.close()

    print("---> Written", foutName)

    return 

def main():

    run()

    # for ene in range(100,1100,100):
    #     run(ene) 

if __name__ == "__main__":
    main()
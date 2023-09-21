# Common custom functions for plotting, reading data, and other things
# Sam Grant (June 2023)

# ---------------------------------
# Calculations and value formatting
# ---------------------------------

import math
import numpy as np
from scipy import stats
from scipy.stats import norm
from scipy.optimize import curve_fit

def Round(value, sf):

    if value == 0.00:
        return "0"
    elif math.isnan(value):
        return "NaN"
    else:

        # Determine the order of magnitude
        magnitude = math.floor(math.log10(abs(value))) + 1

        # Calculate the scale factor
        scale_factor = sf - magnitude

        # Truncate the float to the desired number of significant figures
        truncated_value = math.trunc(value * 10 ** scale_factor) / 10 ** scale_factor

        # Convert the truncated value to a string
        truncated_str = str(truncated_value).rstrip('0').rstrip('.')

        return truncated_str

# Stats for histograms tends to assume a normal distribution
# ROOT does the same thing with TH1
def GetBasicStats(data, xmin, xmax):

    filtered_data = data[(data >= xmin) & (data <= xmax)]  # Filter data within range

    N = len(filtered_data)                      
    mean = np.mean(filtered_data)  
    meanErr = stats.sem(filtered_data) # Mean error (standard error of the mean from scipy)
    stdDev = np.std(filtered_data) # Standard deviation
    stdDevErr = np.sqrt(stdDev**2 / (2*N)) # Standard deviation error assuming normal distribution
    underflows = len(data[data < xmin]) # Number of underflows
    overflows = len(data[data > xmax])

    return N, mean, meanErr, stdDev, stdDevErr, underflows, overflows

def bin(data, bin_width = 1.0): 

    # Bin the data
    bin_edges = np.arange(min(data), max(data) + bin_width, bin_width)
    bin_indices = np.digitize(data, bin_edges)
    bin_counts = np.bincount(bin_indices)

    return bin_edges, bin_indices, bin_counts

# Calculates the mode for binned data
def GetMode(data, bin_width = 1.0):

    # Bin
    bin_edges, bin_indices, bin_counts = bin(data, bin_width)
    # Get mode index
    mode_bin_index = np.argmax(bin_counts)
    # Get mode count
    mode_count = bin_counts[mode_bin_index]
    # Get bin width
    # bin_width = bin_edges[mode_bin_index] - bin_edges[mode_bin_index + 1]
    # Calculate the bin center corresponding to the mode
    mode_bin_center = (bin_edges[mode_bin_index] + bin_edges[mode_bin_index + 1]) / 2
    # Mode uncertainty 
    N = len(data)
    mode_bin_center_err = np.sqrt(N / (N - mode_count)) * bin_width

    return mode_bin_center, abs(mode_bin_center_err)

# --------------------
# Fit function
# --------------------

# The Gaussian function
def gaussian(x, norm, mu, sigma):
    return norm * np.exp(-((x - mu) / (2 * sigma)) ** 2)

# --------------------
# TTree wrangling 
# --------------------

import uproot
import pandas as pd

branchNamesExtended = [ 
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
    "Bx",
    "By",
    "Bz",
    "Ex",
    "Ey",
    "Ez",
    "ProperTime",
    "PathLength",
    "PolX",
    "PolY",
    "PoyZ",
    "InitX",
    "InitY",
    "InitZ",
    "InitKE"
]  

# Just up to "Weight"
branchNames = branchNamesExtended[:12]

def TTreeToDataFrame(finName, treeName, branchNames):

    # print("\n---> Reading...")

    print("---> Reading", treeName, "in", finName)

    # # Check the file has keys available
    # try:
    #     with uproot.open(finName) as fin:
    #         # Check if the file contains any keys (objects)
    #         if not bool(fin.keys()):
    #             print("Warning: file", finName, "has no keys!")

    #         else:

    # Open the file            
    fin = uproot.open(finName)
    
    # print("---> Got input file ", finName, ", ", (fin))

    # Get tree
    tree = fin[treeName]

    if len(tree) == 0: 
        
        return

    # print("---> Got tree ", str(tree))

    # Create an empty dictionary to store the selected columns as NumPy arrays
    branchData = {}

    # Iterate over the specified column names
    for branchName in branchNames:
        # Check if the column name exists in the TTree
        if branchName in tree:
            # Load values in array
            branchData[branchName] = tree[branchName].array(library="np")

    # Create the DataFrame directly from the dictionary of column data
    df = pd.DataFrame(branchData)

    # Close the ROOT file
    fin.close()

    # Print the raw DataFrame 
    # print("\n---> Raw DataFrame:\n", df)

    # Return the DataFrame
    return df

def GetTotalMomentum(df):
    df["P"] = np.sqrt( pow(df["Px"],2) + pow(df["Py"],2) + pow(df["Pz"],2) ) 
    return df

def GetRadialPosition(df):
    df["R"] = np.sqrt( pow(df["x"],2) + pow(df["y"],2) )
    return df


# ---------------------------------
# PDGid wrangling
# ---------------------------------

particleDict = {
    2212: 'proton',
    211: 'pi+',
    -211: 'pi-',
    -13: 'mu+',
    13: 'mu-',
    -11: 'e+',
    11: 'e-',
    321: "kaon+",
    -321: "kaon-",
    311: "kaon0",
    130: "kaon0L",
    310: "kaon0S"
    # Add more particle entries as needed
    }


def FilterParticles(df, particle): 

    # Filter particles
    if particle in particleDict.values():
        PDGid = list(particleDict.keys())[list(particleDict.values()).index(particle)]
        return df[df['PDGid'] == PDGid]

    elif particle=="no_proton":
        return df[df['PDGid'] != 2212]

    elif particle=="pi-_and_mu-":
        return df[(df['PDGid'] == -211) | (df['PDGid'] == 13)]

    elif particle=="pi+-":
        return df[(df['PDGid'] == 211) | (df['PDGid'] == -211)]

    elif particle=="mu+-":
        return df[(df['PDGid'] == -13) | (df['PDGid'] == 13)]

    else: 
        return df

def GetLatexParticleName(particle):

    if particle == "proton": return "$p$"
    elif particle == "pi+-": return "$\pi^{\pm}$"
    elif particle == "pi+": return "$\pi^{+}$"
    elif particle == "pi-": return "$\pi^{-}$"
    elif particle == "mu+-": return "$\mu^{\pm}$"
    elif particle == "mu+": return "$\mu^{+}$"
    elif particle == "mu-": return "$\mu^{-}$"
    elif particle == "e+": return "$e^{+}$"
    elif particle == "e-": return "$e^{-}$"
    elif particle == "kaon+": return "$K^{+}$"
    elif particle == "kaon-": return "$K^{-}$"
    elif particle == "kaon0": return "$K^{0}$"
    elif particle == "kaon0L": return "$K^{0}_{L}$"
    elif particle == "kaon0S": return "$K^{0}_{S}$"
    elif particle == "no_proton": return "No protons"
    elif particle == "pi-_and_mu-": return "$\pi^{-}$ & $\mu^{-}$"
    elif particle == "pi+_and_mu+": return "$\pi^{+}$ & $\mu^{+}$"
    # Add more as required
    else: return particle

# get the latex names of the particles in the particle dictionary 
latexParticleDict = {}
for key, value in  particleDict.items():
    latexParticleDict[key] = GetLatexParticleName(value)

# --------------------
# Plotting
# --------------------

import matplotlib.pyplot as plt

def ProfileX(x, y, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0): 
   
    # Create 2D histogram
    hist, xEdge_, yEdge_ = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])

    # bin widths
    xBinWidths = xEdge_[1]-xEdge_[0]

    # Calculate the mean and RMS values of each vertical slice of the 2D distribution
    xSlice_, xSliceErr_, ySlice_, ySliceErr_ = [], [], [], []

    for i in range(len(xEdge_) - 1):

        # Average x-value
        xSlice = x[ (xEdge_[i] < x) & (x <= xEdge_[i+1]) ]

        # Get y-slice within current x-bin
        ySlice = y[ (xEdge_[i] < x) & (x <= xEdge_[i+1]) ]

        # Avoid empty slices
        if len(xSlice) == 0 or len(ySlice) == 0:
            continue

        # Central values are means and errors are standard errors on the mean
        xSlice_.append(np.mean(xSlice))
        xSliceErr_.append(xSlice.std() / len(xSlice))
        ySlice_.append(ySlice.mean()) 
        ySliceErr_.append(ySlice.std() / len(ySlice))

    return np.array(xSlice_), np.array(xSliceErr_), np.array(ySlice_), np.array(ySliceErr_)

import matplotlib.cm as cm
from matplotlib.colors import ListedColormap

# Enable LaTeX rendering
# plt.rcParams["text.usetex"] = True

def Plot1D(data, nBins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", legPos="best", stats=True, peak=False, underOver=False, errors=False, NDPI=300):
    
    # Create figure and axes
    fig, ax = plt.subplots()

    # Plot the histogram with outline
    counts, bin_edges, _ = ax.hist(data, bins=nBins, range=(xmin, xmax), histtype='step', edgecolor='black', linewidth=1.0, fill=False, density=False)

    # Set x-axis limits
    ax.set_xlim(xmin, xmax)

    # Calculate statistics
    N, mean, meanErr, stdDev, stdDevErr, underflows, overflows = GetBasicStats(data, xmin, xmax)
    # peak = np.max(counts)
    # peak_bin_edges = bin_edges[i_peak:i_peak + 2]
    # peak = counts[i_peak]
    # peakErr = (bin_edges[1] - bin_edges[0]) / 2
    # N, mean, meanErr, stdDev, stdDevErr = str(N), Round(mean, 3), Round(mean, 3), Round(meanErr, 1), Round(stdDev, 3), Round(stdDevErr, 1) 

    # Create legend text
    legend_text = f"Entries: {N}\nMean: {Round(mean, 3)}\nStd Dev: {Round(stdDev, 3)}"
    # if errors: legend_text = f"Entries: {N}\nMean: {Round(mean, 3)}$\pm${Round(meanErr, 1)}\nStd Dev: {Round(stdDev, 3)}$\pm${Round(stdDevErr, 1)}"
    if errors: legend_text = f"Entries: {N}\nMean: {Round(mean, 3)}$\pm${Round(meanErr, 1)}\nStd Dev: {Round(stdDev, 3)}$\pm${Round(stdDevErr, 1)}"
    if peak and not errors: legend_text += f"\nPeak: {Round(GetMode(data, nBins / (xmax - xmin))[0], 3)}"
    if peak and errors: legend_text += f"\nPeak: {Round(GetMode(data, nBins / (xmax - xmin))[0], 3)}$\pm${Round(GetMode(data, nBins / (xmax - xmin))[1], 1)}"
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

    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.clf()
    plt.close()

# Under development!
def Plot1DWithGaussFit(data, nBins=100, xmin=-1.0, xmax=1.0, norm=1.0, mu=0.0, sigma=1.0, fitMin=-1.0, fitMax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", legPos="best", stats=True, peak=False, underOver=False, errors=False, NDPI=300):
    
    # Create figure and axes
    fig, ax = plt.subplots()

    # Plot the histogram with outline
    counts, bin_edges, _ = ax.hist(data, bins=nBins, range=(xmin, xmax), histtype='step', edgecolor='black', linewidth=1.0, fill=False, density=False)

    # Set x-axis limits
    ax.set_xlim(xmin, xmax)

    # Fit gaussian

    # Calculate bin centers
    bin_centres = (bin_edges[:-1] + bin_edges[1:]) / 2
    # Fit the Gaussian function to the histogram data
    params, covariance = curve_fit(gaussian, bin_centres[(bin_centres >= fitMin) & (bin_centres <= fitMax)], counts, p0=[norm, mu, sigma])
    # Extract parameters from the fitting
    norm, mu, sigma = params
    # Plot the Gaussian curve
    ax.plot(bin_centres, gaussian(bin_centres, norm, mu, sigma), color="red", label=f"Norm: {norm}\n$\mu$: {mu}\n$sigma {sigma}")

    # Calculate statistics
    N, mean, meanErr, stdDev, stdDevErr, underflows, overflows = GetBasicStats(data, xmin, xmax)

    # Create legend text
    legend_text = f"Entries: {N}\nMean: {Round(mean, 3)}\nStd Dev: {Round(stdDev, 3)}"
    # if errors: legend_text = f"Entries: {N}\nMean: {Round(mean, 3)}$\pm${Round(meanErr, 1)}\nStd Dev: {Round(stdDev, 3)}$\pm${Round(stdDevErr, 1)}"
    if errors: legend_text = f"Entries: {N}\nMean: {Round(mean, 4)}$\pm${Round(meanErr, 1)}\nStd Dev: {Round(stdDev, 4)}$\pm${Round(stdDevErr, 1)}"
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

    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.clf()
    plt.close()

def Plot2D(x, y, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", cb=True, NDPI=300):

    # Create 2D histogram
    hist, x_edges, y_edges = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])

    # Set up the plot
    fig, ax = plt.subplots()

    # Plot the 2D histogram
    im = ax.imshow(hist.T, cmap='inferno', extent=[xmin, xmax, ymin, ymax], aspect='auto', origin='lower', vmax=np.max(hist)) # , norm=cm.LogNorm())

    # Add colourbar
    if cb: plt.colorbar(im)

    plt.title(title, fontsize=16, pad=10)
    plt.xlabel(xlabel, fontsize=14, labelpad=10)
    plt.ylabel(ylabel, fontsize=14, labelpad=10)

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

def PlotGraph(x, xerr, y, yerr, title=None, xlabel=None, ylabel=None, fout="scatter.png", NDPI=300):

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


    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.clf()
    plt.close()

def Plot1DOverlay(hists, nbins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", labels=None, legPos="upper right", NDPI=300, includeBlack=False, logY=False):

    # Create figure and axes
    fig, ax = plt.subplots()

    # Define a colormap
    # cmap = cm.get_cmap('tab10') # !!deprecated!!

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
        counts, bin_edges, _ = ax.hist(hist, bins=nbins, range=(xmin, xmax), histtype='step', edgecolor=colour, linewidth=1.0, fill=False, density=False, color=colour, label=labels[i], log=logY)

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

def Plot1DOverlayNewColours(hists, nbins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", labels=None, legPos="upper right", NDPI=300, includeBlack=False):

    # Create figure and axes
    fig, ax = plt.subplots()

    # Define a colormap
    # cmap = cm.get_cmap('tab10') # !!deprecated!!

    # Define the colourmap colours
    colours = [
        (0., 0., 0.),                                                   # Black
        (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),  # Red
        (0.12156862745098039, 0.4666666666666667, 0.7058823529411765),  # Blue
        (1.0, 0.4980392156862745, 0.054901960784313725),                # Orange
        (0.17254901960784313, 0.6274509803921569, 0.17254901960784313), # Green
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

def Plot1DOverlayWithStats(hists, nbins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", labels=None, legPos="best", errors=True, NDPI=300, includeBlack=False, peak=False):

    # Create figure and axes
    fig, ax = plt.subplots()

    # Define a colormap
    # cmap = cm.get_cmap('tab10') # !!deprecated!!

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
        # Calculate statistics
        N, mean, meanErr, stdDev, stdDevErr, underflows, overflows = GetBasicStats(hist, xmin, xmax)
        # Create legend text
        legend_text = f"Entries: {N}\nMean: {Round(mean, 3)}\nStd Dev: {Round(stdDev, 3)}"
        if errors: legend_text = f"Entries: {N}\nMean: {Round(mean, 4)}$\pm${Round(meanErr, 1)}\nStd Dev: {Round(stdDev, 4)}$\pm${Round(stdDevErr, 1)}"
        if peak and not errors: legend_text += f"\nPeak: {Round(GetMode(hist, nbins / (xmax - xmin))[0], 3)}"
        if peak and errors: legend_text += f"\nPeak: {Round(GetMode(hist, nbins / (xmax - xmin))[0], 3)}$\pm${Round(GetMode(hist, nbins / (xmax - xmin))[1], 1)}"
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

    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.close()

# Input is a dictionary with four lists per key
# Lists are x, xerr, y, err; key is the label
def PlotGraphOverlay(graph_dict, title=None, xlabel=None, ylabel=None, fout="scatter.png", NDPI=300, offsetLegend=False, useCustomCmap=True):

    # Create a scatter plot with error bars using NumPy arrays 

    # Create figure and axes
    fig, ax = plt.subplots()

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
    # cmap = ListedColormap(colours)
    colour_idx = 0

    cmap = ListedColormap(colours) 
    if not useCustomCmap: cmap = cm.get_cmap('tab10') # !!deprecated!!

    print(graph_dict)

    # Iterate through the keys (momentum values) in the dictionary
    for label, graph_list in graph_dict.items():

        for graph in graph_list:

            print(graph)

            print("\n", label, graph)

            x = graph["x"]
            y = graph['y']
            xerr = graph['xerr'] 
            yerr = graph['yerr']

            print(x,y)

            # Plot scatter with error bars
            # if len(xerr)==0: xerr = [0] * len(x) # Sometimes we only use yerr
            # if len(yerr)==0: yerr = [0] * len(y) # Sometimes we only use yerr

            ax.errorbar(x=x, y=y, xerr=xerr, yerr=yerr, fmt='o', color=cmap(colour_idx), markersize=4, ecolor=cmap(colour_idx), capsize=2, elinewidth=1, linestyle='None', label=label)

            colour_idx += 1

    # Add a line at 30 MeV

    # Set title, xlabel, and ylabel
    ax.set_title(title, fontsize=16, pad=10)
    ax.set_xlabel(xlabel, fontsize=14, labelpad=10) 
    ax.set_ylabel(ylabel, fontsize=14, labelpad=10) 

    # Set font size of tick labels on x and y axes
    ax.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
    ax.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size

    if offsetLegend: 
        legend = ax.legend(loc="center left", frameon=False, fontsize=14, bbox_to_anchor=(1, 0.5)) 
    else: 
        legend = ax.legend(loc="best", frameon=False, fontsize=14) 

    # Add a legend on the right side outside the plot
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Adjust the figure size to make space for the legend
    # plt.gcf().set_size_inches(8, 5)  # Adjust the width and height as needed

    # plt.xlim(xmin=-10) # , xmax=110)


    # legend = ax.legend(loc="upper right", frameon=False, fontsize=14, bbox_to_anchor=(0.73, 0.99)) 
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

def Plot2DWith1DProj(x, y, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", NDPI=300):

    # Create 2D histogram
    hist, x_edges, y_edges = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])

    # Set up the plot
    fig = plt.figure(figsize=(8, 10))
    gs = fig.add_gridspec(2, 2, width_ratios=[4, 1], wspace=0.1, hspace=0.1)

    # Plot the 2D histogram
    ax1 = fig.add_subplot(gs[0, 0])
    im = ax1.imshow(hist.T, cmap='inferno', extent=[xmin, xmax, ymin, ymax], aspect='auto', origin='lower')

    # Format main plot axes
    ax1.set_title(title, fontsize=16, pad=10)
    ax1.set_xlabel(xlabel, fontsize=14, labelpad=10) 
    ax1.set_ylabel(ylabel, fontsize=14, labelpad=10) 

    # Set font size of tick labels on x and y axes
    ax1.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
    ax1.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size

    # Scientific notation
    if ax1.get_xlim()[1] > 999:
        ax1.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax1.xaxis.offsetText.set_fontsize(14)
    if ax1.get_ylim()[1] > 999:
        ax1.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax1.yaxis.offsetText.set_fontsize(14)

    # Draw a horizontal white line at y=50 
    # ax1.axhline(y=50, color='white', linestyle='--', linewidth=1)

    # Add colourbar
    ax_cb = fig.add_subplot(gs[0, 1])
    cbar = plt.colorbar(im, cax=ax_cb)
    cbar.ax.set_position(cbar.ax.get_position().shrunk(0.25, 1))
    cbar.ax.set_position(cbar.ax.get_position().translated(0.10, 0))
    cbar.ax.tick_params(labelsize=14)

    # Project the 2D histogram onto the x-axis
    hist_x = np.sum(hist, axis=1)
    bin_centers_x = (x_edges[:-1] + x_edges[1:]) / 2

    # Create a dummy copy of ax1 to be shared with projection axes,
    # this prevents the original being modified
    ax1_dummy = ax1.figure.add_axes(ax1.get_position(), frame_on=False)
    ax1_dummy.set_xticks([])  # Turn off x-axis ticks of ax1_dummy
    ax1_dummy.set_yticks([])  # Turn off y-axis ticks of ax1_dummy
    # Make sure that the ranges are the same between ax1 and ax1_dummy
    ax1_dummy.set_xlim(ax1.get_xlim())
    ax1_dummy.set_ylim(ax1.get_ylim())

    # Plot the 1D histogram along the x-axis
    ax2 = fig.add_subplot(gs[1, 0], sharex=ax1_dummy)

    counts, bin_edges, _ = ax2.hist(x, bins=nBinsX, range=(xmin, xmax), histtype='step', edgecolor='black', linewidth=1.0, fill=False)

    # Set the position of ax2 while maintaining the same width and adjusting the height
    ax2.set_position([ax1.get_position().x0, ax1.get_position().y0 + ax1.get_position().height + 0.01, ax1.get_position().width, ax1.get_position().height / 5])

    # Turn off appropriate tick markers/numbering and spines 
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_visible(True)

    ax2.yaxis.set_ticklabels([])
    # ax2.tick_params(axis='x', which='major', length=ax1.get_tick_params('length'))  # Turn on tick markers
    ax2.tick_params(axis='y', which='major', length=0)  # Hide tick markers

    # Project the 2D histogram onto the y-axis
    hist_y = np.sum(hist, axis=0)
    bin_centers_y = (y_edges[:-1] + y_edges[1:]) / 2

    # Plot the 1D histogram along the y-axis (rotated +90 degrees)
    ax3 = fig.add_subplot(gs[1, 1], sharey=ax1_dummy)
    counts, bin_edges, _ = ax3.hist(y, bins=nBinsY, range=(ymin, ymax), histtype='step', edgecolor='black', linewidth=1.0, fill=False, orientation='horizontal')

    # Set the position of ax3 while maintaining the same height and adjusting the width
    ax3.set_position([ax1.get_position().x0 + ax1.get_position().width + 0.01, ax1.get_position().y0, ax1.get_position().width / 5, ax1.get_position().height])

    # Turn off appropriate tick markers/numbering and spines 
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['left'].set_visible(True)
    ax3.spines['bottom'].set_visible(False)

    ax3.xaxis.set_ticklabels([])
    ax3.tick_params(axis='x', which='major', length=0)  # Hide tick markers
    # ax3.tick_params(axis='y', which='major', length=ax1.get_tick_params('length')) 

    # Save figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.close()

def Plot3D(x, y, z, nBinsX=100, xmin=-1.0, xmax=1.0, nBinsY=100, ymin=-1.0, ymax=1.0, zmax=1.0, title=None, xlabel=None, ylabel=None, zlabel=None, fout="3d_plot.png", contours=False, cb=True, NDPI=300):

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

from matplotlib.ticker import ScalarFormatter

def BarChart(data, label_dict, title=None, xlabel=None, ylabel=None, fout="bar_chart.png", percentage=False, bar_alpha=1.0, bar_color='black', NDPI=300):
    
    # This came from ChatGPT
    # it matches the key of the dict with row in the data array and returns the element as the label
    labels = [label_dict.get(p, 'other') for p in data]

    # Count occurrences of each label
    unique_labels, label_counts = np.unique(labels, return_counts=True)

    # Only works for particles 

    # Sort labels and counts in descending order
    sorted_indices = np.argsort(label_counts)[::-1]
    unique_labels = unique_labels[sorted_indices]
    label_counts = label_counts[sorted_indices]

    if percentage: 
        label_counts = (label_counts / np.sum(label_counts))*100

    # Create figure and axes
    fig, ax = plt.subplots()

    # print(unique_labels)

    # Plot the bar chart
    indices = np.arange(len(unique_labels))

    # print(indices)
    # for i, index in enumerate(indices):
    #     indices[i] = GetLatexParticleName(index)

    # TODO: handle this better
    n_bars = len(indices)
    bar_width = 3.0 / n_bars
    if(n_bars == 3.0): 
        bar_width = 2.0 / n_bars
    elif(n_bars == 2.0):
        bar_width = 1.0 / n_bars


    ax.bar(indices, label_counts, align='center', alpha=bar_alpha, color=bar_color, width=bar_width, fill=False, hatch='/', linewidth=1, edgecolor='black')

    # Set x-axis labels
    ax.set_xticks(indices)
    ax.set_xticklabels(unique_labels, rotation=0) # 45)

    # Set labels for the chart
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
    if ax.get_ylim()[1] > 999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax.yaxis.offsetText.set_fontsize(14)

    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.clf()
    plt.close()

def Plot1DRatio(hists, nbins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", labels=None, legPos="best", stats=False, errors=False, NDPI=300, peak=False, invertRatio=False, limitRatio=False, ratioMin=0, ratioMax=1):
    
    if len(hists) > 2: 
        print("!!! ERROR: Plot1DRatio must take two histograms as input !!!")
        return

    # Create figure and axes
    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, figsize=(8, 6))

    # Define a colormap
    colours = [
        (0.12156862745098039, 0.4666666666666667, 0.7058823529411765),  # Blue
        (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),  # Red
    ]

    # Create the colormap
    cmap = ListedColormap(colours)

    counts_ = []

    # Iterate over the histograms and plot each one in the top frame
    for i, hist in enumerate(hists):

        colour = cmap(i)

        # Calculate statistics for the current histogram
        N, mean, meanErr, stdDev, stdDevErr, underflows, overflows = GetBasicStats(hist, xmin, xmax)

        # Create legend text
        legend_text = f"Entries: {N}\nMean: {Round(mean, 3)}\nStd Dev: {Round(stdDev, 3)}"
        if errors:
            legend_text = f"Entries: {N}\nMean: {Round(mean, 4)}$\pm${Round(meanErr, 1)}\nStd Dev: {Round(stdDev, 3)}$\pm${Round(stdDevErr, 1)}"
        if peak and not errors:
            legend_text += f"\nPeak: {Round(GetMode(hist, nbins / (xmax - xmin))[0], 3)}"
        if peak and errors:
            legend_text += f"\nPeak: {Round(GetMode(hist, nbins / (xmax - xmin))[0], 3)}$\pm${Round(GetMode(hist, nbins / (xmax - xmin))[1], 1)}"

        if stats:
            label = r"$\bf{"+labels[i]+"}$"+"\n"+legend_text
        else:
            label = labels[i]

        # Plot the current histogram in the top frame
        counts, bin_edges, _ = ax1.hist(hist, bins=nbins, range=(xmin, xmax), histtype='step', edgecolor=colour, linewidth=1.0, fill=False, density=False, color=colour, label=label) 

        # Plot the current histogram in the top frame with error bars
        # hist_err = np.sqrt(hist)
        # bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        # ax1.bar(bin_centers, hist, width=0.1, align='center', alpha=0.7, label=label)
        # ax1.errorbar(bin_centers, hist, yerr=hist_err, fmt='none', color=colour, capsize=2)


        counts_.append(counts)

    # Calculate the ratio of the histograms with a check for division by zero
    ratio = np.divide(counts_[0], counts_[1], out=np.full_like(counts_[0], np.nan), where=(counts_[1] != 0))

    # Calculate the statistical uncertainty for the ratio
    ratio_err = np.divide(np.sqrt(counts_[0]), counts_[1], out=np.full_like(counts_[0], np.nan), where=(counts_[1] != 0))

    # Create a second y-axis for the ratio
    # ax2 = ax1.twinx() # This overlays them
    # Create a separate figure and axis for the ratio plot
    # fig2, ax2 = plt.subplots(figsize=(8, 2))  # Adjust the height as needed

    # Add line at 1.0 
    ax2.axhline(y=1.0, color='gray', linestyle='--', linewidth=1)


    if invertRatio: ratio = np.divide(1, ratio)

    # Plot the ratio in the lower frame with error bars
    ax2.errorbar(bin_edges[:-1], ratio, yerr=ratio_err, color='black', fmt='o', markersize=4, linewidth=1)

    # # Plot the ratio in the lower frame
    # ax2.plot(bin_edges[:-1], ratio, color='black', marker='o', markersize=4, linewidth=0)

    # Format 

    # Set x-axis limits for the top frame
    ax1.set_xlim(xmin, xmax)


    # Remove markers for main x-axis
    ax1.set_xticks([])

    ax2.set_xlabel(xlabel, fontsize=14, labelpad=10)
    ax2.set_ylabel("Ratio", fontsize=14, labelpad=10)
    ax2.tick_params(axis='x', labelsize=14)
    ax2.tick_params(axis='y', labelsize=14)

    # Create a second y-axis for the ratio
    ax2.yaxis.tick_left()
    ax2.xaxis.tick_bottom()
    ax2.xaxis.set_tick_params(width=0.5)
    ax2.yaxis.set_tick_params(width=0.5)

    # Set x-axis limits for the ratio plot to match the top frame
    if limitRatio:
        ax2.set_ylim(ratioMin, ratioMax)

    ax2.set_xlim(xmin, xmax)

    # Set titles and labels for both frames
    ax1.set_title(title, fontsize=16, pad=10)
    # ax1.set_xlabel("", fontsize=0, labelpad=10)
    ax1.set_ylabel(ylabel, fontsize=14, labelpad=10)

    # Set font size of tick labels on x and y axes for both frames
    # ax1.tick_params(axis='x', labelsize=14)
    ax1.tick_params(axis='y', labelsize=14)

    # Scientific notation for top frame
    if ax2.get_xlim()[1] > 9999:
        ax2.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax2.xaxis.offsetText.set_fontsize(14)
    if ax1.get_ylim()[1] > 9999:
        ax1.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax1.yaxis.offsetText.set_fontsize(14)

    # Add legend to the top frame
    ax1.legend(loc=legPos, frameon=False, fontsize=14)

    # Adjust the spacing between subplots
    plt.tight_layout()

    # Adjust the spacing between subplots to remove space between them
    plt.subplots_adjust(hspace=0.0)

    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.close()

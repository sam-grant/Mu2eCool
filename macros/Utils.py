# Common custom functions for plotting, reading data, and other things
# Sam Grant (June 2023)

# ---------------------------------
# Calculations and value formatting
# ---------------------------------

import math
import numpy as np
from scipy import stats

def Round(value, sf):

    if value == 0.0:
        return "0"

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

# --------------------
# TTree wrangling 
# --------------------

import uproot
import pandas as pd

def TTreeToDataFrame(finName, treeName, branchNames):

    # print("\n---> Reading...")

    # Open the ROOT file
    fin = uproot.open(finName)
    
    # print("---> Got input file ", finName, ", ", (fin))

    # Get tree
    tree = fin[treeName]

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

    # print("---> Reading done, closing input file...")

    # Close the ROOT file
    fin.close()

    # Print the raw DataFrame 
    # print("\n---> Raw DataFrame:\n", df)

    # Return the DataFrame
    return df

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
    ySliceMean_, ySliceRMS_ = [], []
    for i in range(len(xEdge_) - 1):
        # Get y-slice within current x-bin
        ySlice = y[ (xEdge_[i] < x) & (x <= xEdge_[i+1]) ]
        # Append the means and rms in each slice
        ySliceMean_.append(ySlice.mean()) 
        ySliceRMS_.append(ySlice.std())

    # Convert lists to numpy arrays
    ySliceMean_ = np.array(ySliceMean_)
    ySliceRMS_ = np.array(ySliceRMS_)

    return ySliceMean_, ySliceRMS_

import matplotlib.cm as cm
from matplotlib.colors import ListedColormap

# Enable LaTeX rendering
# plt.rcParams["text.usetex"] = True

def Plot1D(data, nBins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", legPos="best", underOver=False, stats=True, errors=False, NDPI=300):
    
    # Create figure and axes
    fig, ax = plt.subplots()

    # Plot the histogram with outline
    counts, bin_edges, _ = ax.hist(data, bins=nBins, range=(xmin, xmax), histtype='step', edgecolor='black', linewidth=1.0, fill=False, density=False)

    # Set x-axis limits
    ax.set_xlim(xmin, xmax)

    # Calculate statistics
    N, mean, meanErr, stdDev, stdDevErr, underflows, overflows = GetBasicStats(data, xmin, xmax)
    # N, mean, meanErr, stdDev, stdDevErr = str(N), Round(mean, 3), Round(mean, 3), Round(meanErr, 1), Round(stdDev, 3), Round(stdDevErr, 1) 

    # Create legend text
    legend_text = f"Entries: {N}\nMean: {Round(mean, 3)}\nStd Dev: {Round(stdDev, 3)}"
    # if errors: legend_text = f"Entries: {N}\nMean: {Round(mean, 3)}$\pm${Round(meanErr, 1)}\nStd Dev: {Round(stdDev, 3)}$\pm${Round(stdDevErr, 1)}"
    if errors: legend_text = f"Entries: {N}\nMean: {Round(mean, 4)}$\pm${Round(meanErr, 1)}\nStd Dev: {Round(stdDev, 4)}$\pm${Round(stdDevErr, 1)}"
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
    ax.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='o', color='black', markersize=4, ecolor='black', capsize=2, elinewidth=1, linestyle='None')

    # Set title, xlabel, and ylabel
    ax.set_title(title, fontsize=16, pad=10)
    ax.set_xlabel(xlabel, fontsize=14, labelpad=10) 
    ax.set_ylabel(ylabel, fontsize=14, labelpad=10) 

    # Set font size of tick labels on x and y axes
    ax.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
    ax.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size

     # Scientific notation
    if ax.get_xlim()[1] > 999:
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax.xaxis.offsetText.set_fontsize(14)
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

def Plot1DOverlay(hists, nbins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", labels=None, legPos="upper right", NDPI=300):

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
        counts, bin_edges, _ = ax.hist(hist, bins=nbins, range=(xmin, xmax), histtype='step', edgecolor=cmap(i), linewidth=1.0, fill=False, density=False, color=cmap(i), label=labels[i])

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
    
    labels = [label_dict.get(p, 'other') for p in data]

    # Count occurrences of each label
    unique_labels, label_counts = np.unique(labels, return_counts=True)

    # Sort labels and counts in descending order
    sorted_indices = np.argsort(label_counts)[::-1]
    unique_labels = unique_labels[sorted_indices]
    label_counts = label_counts[sorted_indices]

    if percentage: 
        label_counts = (label_counts / np.sum(label_counts))*100

    # Create figure and axes
    fig, ax = plt.subplots()

    # Plot the bar chart
    indices = np.arange(len(unique_labels))
    
    n_bars = len(indices)
    bar_width = 3.0 / n_bars

    ax.bar(indices, label_counts, align='center', alpha=bar_alpha, color=bar_color, width=bar_width, fill=False, hatch='/', linewidth=1, edgecolor='black')

    # Set x-axis labels
    ax.set_xticks(indices)
    ax.set_xticklabels(unique_labels, rotation=45)

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
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.ticker import ScalarFormatter

import Utils as ut

# def Plot1DRatio(hists, nbins=100, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="hist.png", labels=None, legPos="best", stats=False, errors=False, NDPI=300, peak=False):
#     if len(hists) != 2:
#         print("!!! ERROR: Plot1DRatio must take two histograms as input !!!")
#         return

#     # Create figure and axes
#     fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, figsize=(8, 6))

#     # Define a colormap
#     colours = [
#         (0.12156862745098039, 0.4666666666666667, 0.7058823529411765),  # Blue
#         (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),  # Red
#     ]

#     # Create the colormap
#     cmap = ListedColormap(colours)

#     counts_ = []

#     # Iterate over the histograms and plot each one in the top frame
#     for i, hist in enumerate(hists):

#         colour = cmap(i)

#         if stats:
#             label = r"$\bf{"+labels[i]+"}$"+"\n"+legend_text
#         else:
#             label = labels[i]

#         # Plot the current histogram in the top frame with error bars
#         counts, bin_edges, _ = ax1.hist(hist, bins=nbins, range=(xmin, xmax), histtype='step', edgecolor=colour, linewidth=1.0, fill=False, density=False, color=colour, label=label, alpha=0.5) 

#         counts_.append(counts)

#     # Set x-axis limits for the top frame
#     ax1.set_xlim(xmin, xmax)

#     # Calculate the ratio of the histograms with a check for division by zero
#     ratio = np.divide(counts_[0], counts_[1], out=np.full_like(counts_[0], np.nan), where=(counts_[1] != 0))

#     # Calculate the statistical uncertainty for the ratio
#     ratio_err = np.divide(np.sqrt(counts_[0]), counts_[1], out=np.full_like(counts_[0], np.nan), where=(counts_[1] != 0))

#     # Plot the ratio in the lower frame with error bars
#     ax2.errorbar(bin_edges[:-1], ratio, yerr=ratio_err, color='black', fmt='o', markersize=4, linewidth=0)

#     # Add line at 1.0 
#     ax2.axhline(y=1.0, color='gray', linestyle='--', linewidth=1)

#     # Set x-axis limits for the ratio plot to match the top frame
#     ax2.set_xlim(xmin, xmax)

#     # Format 
#     ax2.set_xlabel(xlabel, fontsize=14, labelpad=10)
#     ax2.set_ylabel("Ratio", fontsize=14, labelpad=10)
#     ax2.tick_params(axis='x', labelsize=14)
#     ax2.tick_params(axis='y', labelsize=14)

#     # Set titles and labels for both frames
#     ax1.set_title(title, fontsize=16, pad=10)
#     ax1.set_xlabel(xlabel, fontsize=14, labelpad=10)
#     ax1.set_ylabel(ylabel, fontsize=14, labelpad=10)

#     # Set font size of tick labels on x and y axes for both frames
#     ax1.tick_params(axis='x', labelsize=14)
#     ax1.tick_params(axis='y', labelsize=14)

#     # Scientific notation for top frame
#     if ax1.get_xlim()[1] > 9999:
#         ax1.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
#         ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
#         ax1.xaxis.offsetText.set_fontsize(14)
#     if ax1.get_ylim()[1] > 9999:
#         ax1.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
#         ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#         ax1.yaxis.offsetText.set_fontsize(14)

#     # Add legend to the top frame
#     ax1.legend(loc=legPos, frameon=False, fontsize=12)

#     # Adjust the spacing between subplots
#     plt.tight_layout()

#     # Save the figure
#     plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
#     print("---> Written", fout)

#     # Clear memory
#     plt.close()

# GetBasicStats() = ut.GetBasicStats()
# Round() = ut.Round()

# This actually overlays the two axes, it's quite neat


# Generate random data for the two histograms
np.random.seed(0)  # Set seed for reproducibility
data1 = np.random.normal(0, 1, 10000)  # Normal distribution with mean=0 and std=1
data2 = np.random.normal(0, 1, 10000)  # Normal distribution with mean=1 and std=1

ut.Plot1DRatio([data1, data2],  nbins=100, xmin=-5.0, xmax=5.0, title="My ratio plot", xlabel="x", ylabel="y", labels=["Data1", "Data2"], fout="../img/TestRatio.png", stats=True, errors=False) 

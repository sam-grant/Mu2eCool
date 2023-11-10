import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import Utils as ut

g4blVer="v3.06"

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

    # print(graph_dict)

    # Iterate through the keys (momentum values) in the dictionary
    for label, graph in graph_dict.items():

        # for graph in graph_list:

        print(graph)

        # print("\n", label, graph)

        x = graph["x"]
        y = graph['y']
        # Fill xerr and yerr with zeros
        xerr = [0] * len(x)
        yerr = [0] * len(y)

        print(x,y)

        # Plot scatter with error bars
        # if len(xerr)==0: xerr = [0] * len(x) # Sometimes we only use yerr
        # if len(yerr)==0: yerr = [0] * len(y) # Sometimes we only use yerr

        ax.errorbar(x=x, y=y, xerr=xerr, yerr=yerr, fmt='o', color=cmap(colour_idx), markersize=4, ecolor=cmap(colour_idx), capsize=2, elinewidth=1, linestyle='None', label=ut.GetLatexParticleName(label))

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


Z = [1850, 1950, 2050, 2150, 2250, 2350, 2450, 2550, 2650, 2750, 2850, 2950, 3050, 3150, 3250, 3350, 3450, 3550, 3650, 3750, 3850, 3950, 4050, 4150, 4250]

# With pbar window
# pi = [0.014743973, 0.129612961, 0.358573217, 0.357172385, 0.361387632, 0.365084579, 0.368402346, 0.362887782, 0.364275377, 0.364442474, 0.369315462, 0.357851871, 0.360196025, 0.357517483, 0.357783968, 0.336265885, 0.323822619, 0.308583846, 0.295471988, 0.276904474, 0.215868477, 0.148216256, 0.116242038, 0.095400341, 0.098315885]
# mu = [0.005096204, 0.032466351, -0.076797917, -0.057106693, -0.041860143, -0.034435709, -0.03274358, -0.028156698, -0.026418459, -0.019501451, -0.01407646, -0.008519433, -0.00352751, -0.002477606, -0.000512295, 0.002556027, 0.005417021, 0.009824221, 0.010260629, 0.011577424, -0.018915625, -0.032043031, -0.024794938, -0.022552152, -0.01934245]

# Without pbar window
pi = [0.016129032, 0.137091319, 0.370500881, 0.381772715, 0.384288102, 0.371279032, 0.380977873, 0.36970278, 0.375259444, 0.372802137, 0.361485687, 0.344438878, 0.343415418, 0.348983682, 0.349220898, 0.342959117, 0.350689655, 0.3330917, 0.33512476, 0.336987414, 0.333764554, 0.180537772, 0.152411283, 0.129110251, 0.121775026]
mu = [0.010388531, 0.030562568, -0.085725872, -0.074391144, -0.064410032, -0.049828955, -0.043472959, -0.038798353, -0.036165264, -0.028990158, -0.021221532, -0.017310587, -0.016405413, -0.014431521, -0.010387201, -0.004449691, -0.007201280, -0.006239909, -0.005064378, -0.005149635, -0.003241626, -0.030859014, -0.027045621, -0.025844245, -0.025828355]

# Multiply each element of pi and mu by 100
pi_times_100 = [x * 100 for x in pi]
mu_times_100 = [x * 100 for x in mu]

graphs = {} 
graphs["pi-"] = { "x":Z, "xerr":[], "y":pi_times_100, "yerr":[] }
graphs["mu-"] = { "x":Z, "xerr":[], "y":mu_times_100, "yerr":[] }

PlotGraphOverlay(graphs, xlabel="z [mm]", ylabel="Percent gain / 100 mm", fout="../img/"+g4blVer+"/Mu2eZScan/gr_NvsZ_PercentGain_Absorber3.1_noPbarWindow.png")


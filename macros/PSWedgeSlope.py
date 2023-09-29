
# Make a plot with the fit function, from 100 MeV onwards 
# We can then translate momentum to thickness in terms of cooling 

# External libraries
# import uproot
import numpy as np
# import h5py
import matplotlib.pyplot as plt
# from scipy.optimize import curve_fit

# Internal libraries
import Utils as ut

# From fit in PSDispersionFits	
# m =  0.9672093309695315 +/- 0.0038052607030987203
# c =  0.942937553736711 +/- 0.3595682153746669

def LinearFunction(x, m, c):
    return m*x + c

def Plot1DFunction(x, y, xmin=-1.0, xmax=1.0, title=None, xlabel=None, ylabel=None, fout="func.png", label=f"$y=mx+c$\n$m=0.967$ mm/MeV\n$c=0.9$ mm", legPos="best", NDPI=300):
    
    # Create figure and axes
    fig, ax = plt.subplots()

    ax.plot(x, y, color='red', linestyle='-', label=label) 

    # Set x-axis limits
    ax.set_xlim(xmin, xmax)

    ax.set_title(title, fontsize=16, pad=10)
    ax.set_xlabel(xlabel, fontsize=14, labelpad=10) 
    ax.set_ylabel(ylabel, fontsize=14, labelpad=10) 

    # Set font size of tick labels on x and y axes
    ax.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
    ax.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size

    ax.legend(loc=legPos, frameon=False, fontsize=14)

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

def Run():

	x = np.linspace(100, 150, 1000)
	m = 0.967
	c = 0.9

	f = LinearFunction(x, m, c)

	Plot1DFunction(x, f, xmin=100, xmax=150, title="", xlabel="Momentum [MeV]", ylabel="Radial position [mm]", fout="../img/v3.06/PSWedgeSlope/func.png")

	# Make a plot with the fit function, from 100 MeV onwards 
	# We can then translate momentum to thickness in terms of cooling 

	return

def main():

	Run() 

	return

if __name__ == "__main__":
    main()
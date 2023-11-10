# Samuel Grant 2023

# External libraries
import uproot
import numpy as np
import h5py
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats
import pandas as pd

# Internal libraries
import Utils as ut

# Globals
g4blVer="v3.06"

def LinearFunction(x, m, c):
    return m*x + c

def PlotSomeNonsense(x, y, offset, xlabel, ylabel, fout):


    # Create figure and axes
    fig, ax = plt.subplots()

    ax.axhline(100, color="grey", linestyle="--", linewidth=1.0, zorder=1)
    ax.axvline(150, color="grey", linestyle="--", linewidth=1.0, zorder=1)
    ax.axvline(90, color="grey", linestyle="--", linewidth=1.0, zorder=1)

    # Set title, xlabel, and ylabel
    ax.set_xlabel(xlabel, fontsize=14, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=14, labelpad=10)

    # Set font size of tick labels on x and y axes
    ax.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
    ax.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size

    # Scientific notation
    if ax.get_xlim()[1] > 9999:
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 9999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax.yaxis.offsetText.set_fontsize(14)

    ax.plot(x, y, color='red', linestyle='-', label=f"$y=mx+c$", zorder=1) #  \n$\chi^{2}/ndf=$"+ut.Round(chiSqrNDF,3)+"\n$m=$"+ut.Round(m_f,3)+"$\pm$"+ut.Round(merr,1)+"\n$c=$"+ut.Round(c_f,3)+"$\pm$"+ut.Round(cerr,1), zorder=1)
    ax.plot(x, y-offset, color='red', linestyle='--', label=r"$c\pm\langle\sigma_{y}\rangle/2=c\pm$"+ut.Round(offset,3), zorder=2)
    ax.plot(x, y+offset, color='red', linestyle='--', zorder=2)
    
    ax.legend(loc="upper left", frameon=False, fontsize=14)

    # ax.set_ylim(85, np.max(fit_y) + 30)
    # ax.set_ylim(np.min(fit_y) - 5, np.max(fit_y) + 5)
    
    # Save the figure
    plt.savefig("SomeNonsense.png", dpi=300, bbox_inches="tight")

    print("---> Written", fout)

    return

def PlotGraphWithLineFit(x, xerr, y, yerr, m_i=1, c_i=0, fitMin=0, fitMax=1, title=None, xlabel=None, ylabel=None, fout="scatter.png", NDPI=300, y_rms = []):

    # Create a scatter plot with error bars using NumPy arrays

    # Create figure and axes
    fig, ax = plt.subplots()

    # Plot scatter with error bars
    if len(xerr) == 0:
        xerr = [0] * len(x)  # Sometimes we only use yerr
    if len(yerr) == 0:
        yerr = [0] * len(y)  # Sometimes we only use yerr

    if len(x) != len(y):
        print("Warning: x has length", len(x), ", while y has length", len(y))

    ax.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='o', color='black', markersize=4, ecolor='black', capsize=2, elinewidth=1, linestyle='None', zorder=2)
    ax.axhline(100, color="grey", linestyle="--", linewidth=1.0, zorder=1)
    ax.axvline(150, color="grey", linestyle="--", linewidth=1.0, zorder=1)

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
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 9999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax.yaxis.offsetText.set_fontsize(14)

    ax.set_xlim(90, 185)

    # Fit

    # Set fit range
    x_f = x[(x >= fitMin) & (x <= fitMax)]
    y_f = y[(x >= fitMin) & (x <= fitMax)]
    xerr_f = xerr[(x >= fitMin) & (x <= fitMax)]
    yerr_f = yerr[(x >= fitMin) & (x <= fitMax)]

    # Calculate fit parameters
    params, cov = curve_fit(LinearFunction, x_f, y_f, sigma=yerr_f, absolute_sigma=True, p0=[m_i, c_i])

    # Extract the parameters and their errors
    m_f, c_f = params
    merr, cerr = np.sqrt(np.diag(cov))

    # Calculate the chi-square value
    fit = LinearFunction(x_f, m_f, c_f)
    res = y_f - fit

    chiSqr = np.sum(res ** 2 / yerr_f ** 2)
    dof = len(x_f) - len(params)
    chiSqrNDF = chiSqr / dof

    # Plot the fitted line (with a higher zorder)
    fit_x = np.linspace(float(fitMin), float(fitMax), 100)
    fit_y = LinearFunction(fit_x, m_f, c_f)

    ax.plot(fit_x, fit_y, color='red', linestyle='-', label=f"$y=mx+c$\n$\chi^{2}/ndf=$"+ut.Round(chiSqrNDF,3)+"\n$m=$"+ut.Round(m_f,3)+"$\pm$"+ut.Round(merr,1)+"\n$c=$"+ut.Round(c_f,3)+"$\pm$"+ut.Round(cerr,1), zorder=3)
    # ax.plot(fit_x, fit_y-np.mean(y_rms)/2, color='red', linestyle='--', label=r"$c\pm\langle\sigma_{y}\rangle/2=c\pm$"+ut.Round(np.mean(y_rms)/2,3), zorder=4)
    # ax.plot(fit_x, fit_y+np.mean(y_rms)/2, color='red', linestyle='--', zorder=4)
    ax.legend(loc="upper left", frameon=False, fontsize=14)

    # ax.set_ylim(85, np.max(fit_y) + 30)
    ax.set_ylim(np.min(fit_y) - 5, np.max(fit_y) + 5)

    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    print("m =", m_f, "+/-", merr)
    print("c =", c_f, "+/-", cerr)

    PlotSomeNonsense(np.linspace(90, 200, 100), LinearFunction(fit_x, m_f, c_f), np.mean(y_rms)/2, xlabel, ylabel, fout)

    # Clear memory
    plt.clf()
    plt.close()

    return

# def PlotGraphWithLineFit(x, xerr, y, yerr, m_i=1, c_i=0, fitMin=0, fitMax=1, title=None, xlabel=None, ylabel=None, fout="scatter.png", NDPI=300):

#    # Create a scatter plot with error bars using NumPy arrays 

#     # Create figure and axes
#     fig, ax = plt.subplots()

#     # Plot scatter with error bars
#     if len(xerr)==0: xerr = [0] * len(x) # Sometimes we only use yerr
#     if len(yerr)==0: yerr = [0] * len(y) # Sometimes we only use yerr

#     if len(x) != len(y): print("Warning: x has length", len(x),", while y has length", len(y))

#     ax.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='o', color='black', markersize=4, ecolor='black', capsize=2, elinewidth=1, linestyle='None')

#     # Set title, xlabel, and ylabel
#     ax.set_title(title, fontsize=16, pad=10)
#     ax.set_xlabel(xlabel, fontsize=14, labelpad=10) 
#     ax.set_ylabel(ylabel, fontsize=14, labelpad=10) 

#     # Set font size of tick labels on x and y axes
#     ax.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
#     ax.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size

#      # Scientific notation
#     if ax.get_xlim()[1] > 9999:
#         ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
#         ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
#         ax.xaxis.offsetText.set_fontsize(14)
#     if ax.get_ylim()[1] > 9999:
#         ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
#         ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#         ax.yaxis.offsetText.set_fontsize(14)

#     ax.set_xlim(100, 200)

#     # Fit

#     # Set fit range
#     x_f = x[(x >= fitMin) & (x <= fitMax)]
#     y_f = y[(x >= fitMin) & (x <= fitMax)]
#     xerr_f = [(x >= fitMin) & (x <= fitMax)]
#     yerr_f = yerr[(x >= fitMin) & (x <= fitMax)]

#     # Calculate fit parameters
#     params, cov = curve_fit(LinearFunction, x_f, y_f, sigma=yerr_f, absolute_sigma=True, p0=[m_i, c_i])

#     # Extract the parameters and their errors
#     m_f, c_f = params
#     merr, cerr = np.sqrt(np.diag(cov))

# 	# def chi2_ndf(x, y, y_err, func, pars):
# 	#     '''
# 	#     Calcualte chi2
# 	#     '''    
# 	#     ndf = len(x) - len(pars) # total N - fitting pars 
# 	#     chi2_i=residuals(x, y, func, pars)**2/y_err**2 # (res**2)/(error**2)
# 	#     chi2=chi2_i.sum() # np sum 
# 	#     return chi2/ndf, chi2, ndf 

#     # Calculate the chi-square value
#     fit = LinearFunction(x_f, m_f, c_f)
#     res = y_f - fit

#     # chiSqr = np.sum( pow(res, 2)  / pow(fit, 2) )  
#     chiSqr = np.sum( res**2 / yerr_f**2) 
#     dof = len(x_f) - len(params) 
#     chiSqrNDF = chiSqr / dof

#     # Plot the fitted line
#     fit_x = np.linspace(float(fitMin), float(fitMax), 100)
#     fit_y = LinearFunction(fit_x, m_f, c_f)

#     ax.plot(fit_x, fit_y, color='red', linestyle='-', label=f"$y=mx+c$\n$\chi^{2}/ndf=$"+ut.Round(chiSqrNDF,3)+"\n$m=$"+ut.Round(m_f,3)+"$\pm$"+ut.Round(merr,1)+"\n$c=$"+ut.Round(c_f,3)+"$\pm$"+ut.Round(cerr,3)) # 'Fit (y={m_f:.2f}x+{c_f:.2f})') # 
#     # ax.plot(fit_x, fit_y, color='red', linestyle='-', label=f"$y=mx+c$\nm: "+ut.Round(m_f,5)+"$\pm$"+ut.Round(merr,1)+"\nc: "+ut.Round(c_f,4)+"$\pm$"+ut.Round(cerr,1)) # 'Fit (y={m_f:.2f}x+{c_f:.2f})') # 
#     ax.legend(loc="best", frameon=False, fontsize=14)

#     ax.set_ylim(np.min(fit_y)-10, np.max(fit_y)+10)

#     # Save the figure
#     plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
#     print("---> Written", fout)

#     print("m = ", m_f, "+/-", merr)
#     print("c = ", c_f, "+/-", cerr)

#     # Clear memory
#     plt.clf()
#     plt.close()

#     return 

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def PlotGraphWithRMS(x, xerr, y, yerr, yrms, title=None, xlabel=None, ylabel=None, fout="scatter.png", NDPI=300):
    # Create a scatter plot with error bars using NumPy arrays 

    # Create figure and axes
    fig, ax = plt.subplots()

    # Plot scatter with error bars
    if len(xerr) == 0:
        xerr = [0] * len(x)  # Sometimes we only use yerr
    if len(yerr) == 0:
        yerr = [0] * len(y)  # Sometimes we only use yerr

    if len(x) != len(y):
        print("Warning: x has length", len(x), ", while y has length", len(y))

    ax.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='o', color='black', markersize=4, ecolor='black', capsize=2, elinewidth=1, linestyle='None', label="Mean")
    ax.axhline(100, color="grey", linestyle="--", linewidth=1.0)
    ax.axvline(150, color="grey", linestyle="--", linewidth=1.0)
    ax.plot(x, y + yrms/2, color='red', linestyle='-', linewidth=1) # , label="RMS")
    ax.plot(x, y - yrms/2, color='red', linestyle='-', linewidth=1, label="RMS")

    df = pd.DataFrame({'p': x, 'y - yrms/2': y - yrms/2})
    # print(pd.DataFrame({'p': x, 'y - yrms/2': y - yrms/2}))
    df.to_csv("../txt/v3.06/PSDispersionFits.csv", index=False) 
    print("\n---> Written csv to", "../txt/v3.06/PSDispersionFits.csv")

    ax.legend(loc="best", frameon=False, fontsize=14)

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
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 9999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax.yaxis.offsetText.set_fontsize(14)

    ax.set_xlim(90, 200)
    ax.set_ylim(75, 150)



    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.clf()
    plt.close()


# Fit radius vs momentum distributions in the PS
def Run(Z, particle):

    h5File="../h5/v3.06/BeamProfile/dispersion_reversed_150MeVcut_"+Z+"_"+particle+"_Mu2E_1e7events_NoAbsorber_fromZ1850_parallel_finePSZScan.h5"

    # Open the HDF5 file for reading
    with h5py.File(h5File, "r") as hf:
        # Access the datasets by their names
        x_ = hf["x_"][:]
        xerr_ = hf["xerr_"][:]
        y_ = hf["y_"][:]
        yerr_ = hf["yerr_"][:]
        yrms_ = hf["yrms_"][:]

    # PlotGraphWithRMS(x_, xerr_, y_, yerr_, yrms_, r"$\pi^{-}$, $Z=1915$ mm", "Radial position [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/PSDispersionFits/px_mom_vs_rad_wrms_150MeVcut_"+particle+".png")
    # PlotGraphWithRMS(x_, xerr_, y_, yerr_, yrms_, r"$\pi^{-}$, $Z=1915$ mm, $<150$ MeV", "Radial position [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/PSDispersionFits/px_mom_vs_rad_wrms_150MeVcut_"+particle+".png")
    PlotGraphWithLineFit(x_, xerr_, y_, yerr_, y_rms=yrms_, m_i=0.5, c_i=0, fitMin=90, fitMax=185, title=r"$\pi^{-}$, $Z=1915$ mm, $<150$ MeV", ylabel="Momentum [MeV]", xlabel="Radial position [mm]", fout="../img/"+g4blVer+"/PSDispersionFits/px_mom_vs_rad_wrms_150MeVcut_fit_"+particle+".png")


    return

    # Sanity check
    ut.PlotGraph(x_, xerr_, y_, yerr_, "", "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/PSDispersionFits/px_rad_vs_mom_"+particle+".png")

    # Graph with RMS
    PlotGraphWithRMS(x_, xerr_, y_, yerr_, yrms_, "", "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/PSDispersionFits/px_rad_vs_mom_wrms_"+particle+".png")

    PlotGraphWithRMS(x_, xerr_, y_, yerr_, yrms_, "", "Momentum [MeV]", "Radial position [mm]", "../img/"+g4blVer+"/PSDispersionFits/px_rad_vs_mom_wrms_100-150MeV_"+particle+".png")

    if particle=="pi-":
        # PlotGraphWithLineFit(x_, xerr_, y_, yerr_, m_i=1.0, c_i=0, fitMin=50, fitMax=130, title=r"$\pi^{-}$", xlabel="Momentum [MeV]", ylabel="Radial position [mm]", fout="../img/"+g4blVer+"/PSDispersionFits/px_rad_vs_mom_fit_"+particle+".png")
        PlotGraphWithLineFit(x_, xerr_, y_, yerr_, m_i=1.0, c_i=0, fitMin=100, fitMax=140, title=r"$\pi^{-}$, $Z=1915$ mm", xlabel="Momentum [MeV]", ylabel="Radial position [mm]", fout="../img/"+g4blVer+"/PSDispersionFits/px_rad_vs_mom_fit_"+particle+".png")
    elif particle=="mu-":
        PlotGraphWithLineFit(x_, xerr_, y_, yerr_, m_i=0.5, c_i=20, fitMin=50, fitMax=100, title=r"$\mu^{-}$", xlabel="Momentum [MeV]", ylabel="Radial position [mm]", fout="../img/"+g4blVer+"/PSDispersionFits/px_rad_vs_mom_fit_"+particle+".png")

    # Make a plot with the fit function, from 100 MeV onwards 
    # We can then translate momentum to thickness in terms of cooling 

    return

def main():

	Run("Z1915", "pi-") # "../h5/v3.06/BeamProfile/dispersion_Z1915_pi-_Mu2E_1e7events_NoAbsorber_fromZ1850_parallel_finePSZScan.h5")
	# Run("Z1915", "mu-") # "../h5/v3.06/BeamProfile/dispersion_Z1915_pi-_Mu2E_1e7events_NoAbsorber_fromZ1850_parallel_finePSZScan.h5")

	return

if __name__ == "__main__":
    main()
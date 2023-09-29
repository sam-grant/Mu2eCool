# Work out the gradient required for a TS3 wedge
# Slope of <y> vs <mom>

import uproot
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

# Internal libraries
import Utils as ut

from scipy.optimize import curve_fit

# Globals
g4blVer="v3.06"

def LinearFunction(x, m, c):
    return m*x + c

def PlotGraphWithLine(x, xerr, y, yerr, title=None, xlabel=None, ylabel=None, fout="scatter.png", NDPI=300):

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


    ax.axvline(x=50.0, color="black", linestyle="--", linewidth=1)

    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.clf()
    plt.close()

def PlotGraphWithLineFit(x, xerr, y, yerr, m_i, c_i, fitMin, fitMax, title=None, xlabel=None, ylabel=None, fout="scatter.png", NDPI=300):

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

    # Fit

    # Set fit range
    x_f = x[(x >= fitMin) & (x <= fitMax)]
    y_f = y[(x >= fitMin) & (x <= fitMax)]
    xerr_f = [(x >= fitMin) & (x <= fitMax)]
    yerr_f = yerr[(x >= fitMin) & (x <= fitMax)]

    # Calculate fit parameters
    params, cov = curve_fit(LinearFunction, x_f, y_f, sigma=yerr_f, absolute_sigma=True, p0=[m_i, c_i])

    # Extract the parameters and their errors
    m_f, c_f = params
    merr, cerr = np.sqrt(np.diag(cov))

# def chi2_ndf(x, y, y_err, func, pars):
#     '''
#     Calcualte chi2
#     '''    
#     ndf = len(x) - len(pars) # total N - fitting pars 
#     chi2_i=residuals(x, y, func, pars)**2/y_err**2 # (res**2)/(error**2)
#     chi2=chi2_i.sum() # np sum 
#     return chi2/ndf, chi2, ndf 

    # Calculate the chi-square value
    fit = LinearFunction(x_f, m_f, c_f)
    res = y_f - fit
    # chiSqr = np.sum( pow(res, 2)  / pow(fit, 2) )  
    chiSqr = np.sum( res**2 / yerr_f**2) 
    dof = len(x_f) - len(params) 
    chiSqrNDF = chiSqr / dof

    # Plot the fitted line
    fit_x = np.linspace(float(fitMin), float(fitMax), 100)
    fit_y = LinearFunction(fit_x, m_f, c_f)

    # ax.plot(fit_x, fit_y, color='red', linestyle='-', label=f"$y=mx+c$\n$\chi^{2}/ndf$: "+ut.Round(chiSqrNDF,3)+"\nm: "+ut.Round(m_f,3)+"$\pm$"+ut.Round(merr,1)+"\nc: "+ut.Round(c_f,3)+"$\pm$"+ut.Round(cerr,3)) # 'Fit (y={m_f:.2f}x+{c_f:.2f})') # 
    ax.plot(fit_x, fit_y, color='red', linestyle='-', label=f"$y=mx+c$\nm: "+ut.Round(m_f,5)+"$\pm$"+ut.Round(merr,1)+"\nc: "+ut.Round(c_f,4)+"$\pm$"+ut.Round(cerr,1)) # 'Fit (y={m_f:.2f}x+{c_f:.2f})') # 
    ax.legend(loc="best", frameon=False, fontsize=14)

    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.clf()
    plt.close()

# ---- End of plotting functions ----  
def RunTSWedgeSlope(config, ntupleName, particle):

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"
    df = ut.TTreeToDataFrame(finName, ntupleName, ut.branchNames)  

    # Titles and names
    ntupleName = ntupleName.split("/")[1] 
    title = ut.GetLatexParticleName(particle) # 
    if ntupleName[0] == "Z": title += ", Z = "+ntupleName[1:]+" mm"
    else: title += ", "+ntupleName

    # Filter particles
    df = ut.FilterParticles(df, particle)

    # Need to translate position, based on where we are along the beamline
    df_trans = df 
    if ntupleName[:7] == "Coll_03":
        # x is now z, shifted by z position of collimator 5
        # param Coll_03_up_z=$MECO_G4_zTrans
        # param MECO_G4_zTrans=(5.00+2.929)*1000
        df_trans["x"] = df["z"] - (5.00+2.929)*1000 # 082
        df = df_trans
    elif ntupleName[:7] == "Coll_05" or ntupleName == "prestop" or ntupleName == "poststop":
        # x is still x, but shifted by x position of collimator 5
        # param MECO_G4_xTrans=-(2.929+1.950/2.0)*1000
        # param Coll_05_x=-3904+$MECO_G4_xTrans
        df_trans["x"] = df["x"] + 3904 + (2.929+1.950/2.0)*1000
        df = df_trans 

    # Momentum 
    df["P"] = np.sqrt( pow(df["Px"],2) + pow(df["Py"],2) + pow(df["Pz"],2) ) 

    ut.Plot1D(df["P"], 170, 0, 170, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/TSWedgeSlope/h1_mom_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)
    ut.Plot2D(df["P"], df["y"], 170, 0, 170, 500, -250, 250, title, "Momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/TSWedgeSlope/h2_YvsMom_"+ntupleName+"_"+particle+"_"+config+".png") 

    x_, xerr_, y_, yerr_ = ut.ProfileX(df["P"], df["y"], 170, 0, 170, 500, -250, 250)
    PlotGraphWithLine(x_, xerr_, y_, yerr_, title, r"$\langle$momentum$\rangle$ [MeV] / mm", r"$\langle$y$\rangle$ [mm] / MeV", "../img/"+g4blVer+"/TSWedgeSlope/px_YvsMom_wline_"+ntupleName+"_"+particle+"_"+config+".png")

    m_i = 1.10
    c_i = 65
    fitMin = 50 
    fitMax = 110

    # High momentum 
    x_, xerr_, y_, yerr_ = ut.ProfileX(df[ (df["P"] > 50) & (df["P"] <= fitMax) ]["P"], df[ (df["P"] > 50) & (df["P"] <= fitMax) ]["y"], 68, 0, 170, 200, -250, 250)
    PlotGraphWithLineFit(x_, xerr_, y_, yerr_, m_i, c_i, fitMin, fitMax, title, r"$\langle$momentum$\rangle$ [MeV] / 2.5 mm", r"$\langle$y$\rangle$ [mm] / 2.5 MeV", "../img/"+g4blVer+"/TSWedgeSlope/px_YvsMom_above50MeV_wlineFit_"+ntupleName+"_"+particle+"_"+config+".png")

    # Check with Diktys 
    x_, xerr_, y_, yerr_ = ut.ProfileX(df[(df["P"] >= 35) & (df["P"] <= 60)]["P"], df[(df["P"] >= 35) & (df["P"] <= 60)]["y"], 68, 0, 170, 200, -250, 250)
    PlotGraphWithLineFit(x_, xerr_, y_, yerr_, m_i, c_i, 35, 60, title, r"$\langle$momentum$\rangle$ [MeV] / 2.5 mm", r"$\langle$y$\rangle$ [mm] / 2.5 MeV", "../img/"+g4blVer+"/TSWedgeSlope_wlineFit_DiktysCheck_"+ntupleName+"_"+particle+"_"+config+".png")


    return

def main():

    # RunTSWedgeSlope("Mu2E_1e7events_fromZ1850_parallel_noColl03", "VirtualDetector/Coll_03_DetIn", "no_proton")
    # RunTSWedgeSlope("Mu2E_1e7events_fromZ1850_parallel_noColl03", "VirtualDetector/Coll_03_DetIn", "mu-")
    # RunTSWedgeSlope("Mu2E_1e7events_fromZ1850_parallel_noColl03", "VirtualDetector/Coll_03_DetIn", "mu-")
    # RunTSWedgeSlope("Mu2E_1e7events_fromZ1850_parallel_noColl03", "VirtualDetector/Coll_03_DetIn", "pi-")

    RunTSWedgeSlope("Mu2E_1e7events_fromZ1850_parallel_noColl03", "VirtualDetector/Coll_03_DetMid", "mu-")
    # RunTSWedgeSlope("Mu2E_1e7events_fromZ1850_parallel", "VirtualDetector/Coll_03_DetOut", "mu-")

if __name__ == "__main__":
    main()
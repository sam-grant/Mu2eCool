# Make some basic momentum and beam profile plots before and after the absorber

# Make plots from the zntuple

import uproot
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

# Internal libraries
import Utils as ut

def Run(config, branchNames, g4blVer, particle):

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

    df_BeAbsorber_DetIn = ut.TTreeToDataFrame(finName, "/VirtualDetector/BeAbsorber_DetIn", branchNames)  
    df_BeAbsorber_DetOut = ut.TTreeToDataFrame(finName, "/VirtualDetector/BeAbsorber_DetOut", branchNames)  

    particle_dict = {
        13: 'mu-',
        -13: 'mu+',
        211: 'pi+',
        -211: 'pi-',
        2212: 'proton',
        # Add more particle entries as needed
    }

    absorberName = config.split('_')[2]
	
	# Particle populations
    ut.BarChart(df_BeAbsorber_DetIn['PDGid'], particle_dict, "Entering "+absorberName, "", "Percentage / PDGid", fout="../img/v3.06/bar_ParticleFraction_BeAbsorber_DetIn_"+config+".pdf", percentage=True)
    ut.BarChart(df_BeAbsorber_DetOut['PDGid'], particle_dict, "Exiting "+absorberName, "", "Percentage / PDGid", fout="../img/v3.06/bar_ParticleFraction_BeAbsorber_DetOut_"+config+".pdf", percentage=True)

    # Filter particles
    PDGid = 0

    if particle in particle_dict.values():
        PDGid = list(particle_dict.keys())[list(particle_dict.values()).index(particle)]
        df_BeAbsorber_DetIn = df_BeAbsorber_DetIn[df_BeAbsorber_DetIn['PDGid'] == PDGid]
        df_BeAbsorber_DetOut = df_BeAbsorber_DetOut[df_BeAbsorber_DetOut['PDGid'] == PDGid]

    # Momentum and radial distribution 
    mom_BeAbsorber_DetIn = np.sqrt( pow(df_BeAbsorber_DetIn["Px"],2) + pow(df_BeAbsorber_DetIn["Py"],2) + pow(df_BeAbsorber_DetIn["Pz"],2) ) 
    rad_BeAbsorber_DetIn = np.sqrt( pow(df_BeAbsorber_DetIn['x'],2) + pow(df_BeAbsorber_DetIn['y'],2))

    mom_BeAbsorber_DetOut = np.sqrt( pow(df_BeAbsorber_DetOut["Px"],2) + pow(df_BeAbsorber_DetOut["Py"],2) + pow(df_BeAbsorber_DetOut["Pz"],2) ) 
    rad_BeAbsorber_DetOut = np.sqrt( pow(df_BeAbsorber_DetOut['x'],2) + pow(df_BeAbsorber_DetOut['y'],2))

    # Momentum in/out
    ut.Plot1D(mom_BeAbsorber_DetIn, 500, 0, 500, r"$\mu^{-}$ entering "+absorberName , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/h1_mom_BeAbsorber_DetIn_"+particle+"_"+config+".pdf", "upper right") 
    ut.Plot1D(mom_BeAbsorber_DetOut, 500, 0, 500, r"$\mu^{-}$ exiting "+absorberName , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/h1_mom_BeAbsorber_DetOut_"+particle+"_"+config+".pdf", "upper right") 

    # Beam profile in/out
    ut.Plot2D(df_BeAbsorber_DetIn['x'], df_BeAbsorber_DetIn['y'], 400, -200, 200, 400, -200, 200, r"$\mu^{-}$ entering "+absorberName, "x [mm]", "y [mm]", "../img/v3.06/h2_XY_BeAbsorber_DetIn_"+particle+"_"+config+".pdf")
    ut.Plot2D(df_BeAbsorber_DetOut['x'], df_BeAbsorber_DetOut['y'], 400, -200, 200, 400, -200, 200, r"$\mu^{-}$ exiting "+absorberName, "x [mm]", "y [mm]", "../img/v3.06/h2_XY_BeAbsorber_DetOut_"+particle+"_"+config+".pdf")
    ut.Plot2DWith1DProj(df_BeAbsorber_DetIn['x'], df_BeAbsorber_DetIn['y'], 400, -200, 200, 400, -200, 200, r"$\mu^{-}$ entering "+absorberName, "x [mm]", "y [mm]", "../img/v3.06/h2_XY_wproj_BeAbsorber_DetIn_"+particle+"_"+config+".pdf")
    ut.Plot2DWith1DProj(df_BeAbsorber_DetOut['x'], df_BeAbsorber_DetOut['y'], 400, -200, 200, 400, -200, 200, r"$\mu^{-}$ exiting "+absorberName, "x [mm]", "y [mm]", "../img/v3.06/h2_XY_wproj_BeAbsorber_DetOut_"+particle+"_"+config+".pdf")
    ut.Plot2D(df_BeAbsorber_DetIn['Px'], df_BeAbsorber_DetIn['Py'], 400, -200, 200, 400, -200, 200, r"$\mu^{-}$ entering "+absorberName, "Px [mm]", "Py [mm]", "../img/v3.06/h2_MomXY_BeAbsorber_DetIn_"+particle+"_"+config+".pdf")
    ut.Plot2D(df_BeAbsorber_DetOut['Px'], df_BeAbsorber_DetOut['Py'], 400, -200, 200, 400, -200, 200, r"$\mu^{-}$ exiting "+absorberName, "Px [mm]", "Py [mm]", "../img/v3.06/h2_MomXY_BeAbsorber_DetOut_"+particle+"_"+config+".pdf")

    # Radius verus momentum 
    ut.Plot2D(mom_BeAbsorber_DetIn, rad_BeAbsorber_DetIn, 250, 0, 250, 200, 0, 200, r"$\mu^{-}$ entering "+absorberName, "Momentum [MeV]", "Radius [mm]", "../img/v3.06/h2_RadiusVsMom_BeAbsorber_DetIn_"+particle+"_"+config+".pdf")
    ut.Plot2D(mom_BeAbsorber_DetOut, rad_BeAbsorber_DetOut, 250, 0, 250, 200, 0, 200, r"$\mu^{-}$ exiting "+absorberName, "Momentum [MeV]", "Radius [mm]", "../img/v3.06/h2_RadiusVsMom_BeAbsorber_DetOut_"+particle+"_"+config+".pdf")

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
        "Weight"
    ]  

    g4blVer="v3.06"
    config="Mu2E_1e7events_Absorber0_fromZ2265_parallel" 

    # Run(config, branchNames, g4blVer, "all") 
    # Run(config, branchNames, g4blVer, "proton") 
    # Run(config, branchNames, g4blVer, "pi+") 
    # Run(config, branchNames, g4blVer, "pi-") 
    # Run(config, branchNames, g4blVer, "mu+") 
    Run(config, branchNames, g4blVer, "mu-") 



if __name__ == "__main__":
    main()



# External libraries
import uproot
import pandas as pd
import numpy as np
import h5py

# Internal libraries
import Utils as ut

def Run():

    # TTree branches
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

    g4blVersion="v3.06"
    nEvents="10e4"
    config = "Mu2E_"
    particleFlag = "pi-"

    finName = "../plots/"+g4blVersion+"/g4beamline_"+config+nEvents+"events.root"

    # Setup output file
    foutName = "../plots/"+g4blVersion+"/g4beamlinePlots_"+config+nEvents+"events.h5" 
    fout = h5py.File(foutName, "w")

    # Access the collimator TTrees
    df_Coll_01_DetIn = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_01_DetIn", branchNames)
    df_Coll_01_DetOut = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_01_DetOut", branchNames)
    
    # Useful printout
    print("Number of pi- into Coll_01 =", df_Coll_01_DetIn[df_Coll_01_DetIn['PDGid'] == -211].shape[0])
    print("Number of pi- out of Coll_01 =", df_Coll_01_DetOut[df_Coll_01_DetOut['PDGid'] == -211].shape[0])

    # Filter pi-
    if particleFlag=="pi-": 
        df_Coll_01_DetIn = df_Coll_01_DetIn[df_Coll_01_DetIn['PDGid'] == -211]
        df_Coll_01_DetOut = df_Coll_01_DetOut[df_Coll_01_DetOut['PDGid'] == -211]

    # Get variables
    t_Coll_01_DetIn = df_Coll_01_DetIn["t"]
    x_Coll_01_DetIn = df_Coll_01_DetIn["x"]
    y_Coll_01_DetIn = df_Coll_01_DetIn["y"]

    mom_Coll_01_DetIn = np.sqrt( pow(df_Coll_01_DetIn["Px"],2) + pow(df_Coll_01_DetIn["Py"],2) + pow(df_Coll_01_DetIn["Pz"],2) )
    mom_Coll_01_DetOut = np.sqrt( pow(df_Coll_01_DetOut["Px"],2) + pow(df_Coll_01_DetOut["Py"],2) + pow(df_Coll_01_DetOut["Pz"],2) )

    # Run plots
    ut.Plot1D(mom_Coll_01_DetIn, 500, 0, 500, r""+g4blVersion+", $\pi^{-}$ into TS collimator 1" , "Momentum [MeV]", "Events / MeV", "../img/"+g4blVersion+"/h1_mom_Coll_01_DetIn_"+config+particleFlag+"_"+nEvents+"events.pdf", "upper right") 
    ut.Plot1D(mom_Coll_01_DetOut, 500, 0, 500, r""+g4blVersion+", $\pi^{-}$ out of TS collimator 1" , "Momentum [MeV]", "Events / MeV", "../img/"+g4blVersion+"/h1_mom_Coll_01_DetOut_"+config+particleFlag+"_"+nEvents+"events.pdf", "upper right") 

    # Write the histograms to the HDF5 file
    fout.create_dataset("mom_Coll_01_DetIn", data=mom_Coll_01_DetIn)
    fout.create_dataset("mom_Coll_01_DetOut", data=mom_Coll_01_DetOut)

    # Run with Be target 
    df_BeTarget_DetOut = None 

    if config == "Mu2E": 

        # Close the HDF5 file
        fout.close()

    elif config == "Mu2E_withBeTarget_": # Repeat for Be target 

        df_BeTarget_DetOut = ut.TTreeToDataFrame(finName, "VirtualDetector/BeTarget_DetOut", branchNames)

        print("Number of pi- at BeTarget_DetOut =", df_BeTarget_DetOut[df_BeTarget_DetOut['PDGid'] == -211].shape[0])

        # Filter pi-
        if particleFlag=="pi-": 
            df_BeTarget_DetOut = df_BeTarget_DetOut[df_BeTarget_DetOut['PDGid'] == -211]

        mom_BeTarget_DetOut= np.sqrt( pow(df_BeTarget_DetOut["Px"],2) + pow(df_BeTarget_DetOut["Py"],2) + pow(df_BeTarget_DetOut["Pz"],2) )

        # Run plots
        ut.Plot1D(mom_BeTarget_DetOut, 500, 0, 500, r""+g4blVersion+", $\pi^{-}$ out of Be target" , "Momentum [MeV]", "Events / MeV", "../img/"+g4blVersion+"/h1_mom_BeTarget_DetOut_"+config+particleFlag+"_"+nEvents+"events.pdf", "upper right") 

        fout.create_dataset("mom_BeTarget_DetOut", data=mom_BeTarget_DetOut)

        fout.close()

    print("---> Written", foutName)

    return 


def main():

    Run()

if __name__ == "__main__":
    main()
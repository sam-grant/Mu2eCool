# External libraries
import pandas as pd
import numpy as np
import h5py

# Internal libraries
import Utils as ut

def Run():   

    g4blVersion="v3.06"
    nEvents="10e4"

    print("\n--->Running plots")

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

    # Input file name
    finName = "../plots/"+g4blVersion+"/g4beamline_MuonBerylliumTarget_"+nEvents+"events.root" 

    # Access the TTree
    dfForward = ut.TTreeToDataFrame(finName, "VirtualDetector/DetForward", branchNames)
    dfBackward = ut.TTreeToDataFrame(finName, "VirtualDetector/DetBackward", branchNames)

    # Put this before filtering the whole DataFrame, so you can count other particles if you like
    nMuMinusForward = dfForward[dfForward['PDGid'] == 13].shape[0]
    print("Number of mu- at forward detector =", nMuMinusForward)

    nMuMinusBackward = dfBackward[dfBackward['PDGid'] == 13].shape[0]
    print("Number of mu- at backward detector =", nMuMinusBackward)

    timeForward = dfForward["t"]
    timeBackward = dfBackward["t"]   

    xForward = dfForward["x"]
    xBackward = dfBackward["x"]  

    yForward = dfForward["y"]
    yBackward = dfBackward["y"]  

    xMomForward = dfForward["Px"]
    xMomBackward = dfBackward["Px"]

    yMomForward = dfForward["Py"]
    yMomBackward = dfBackward["Py"]

    momForward = np.sqrt( pow(dfForward["Px"],2) + pow(dfForward["Py"],2) + pow(dfForward["Pz"],2) )
    momBackward = np.sqrt( pow(dfBackward["Px"],2) + pow(dfBackward["Py"],2) + pow(dfBackward["Pz"],2) )

    print("Max mu- momentum entering the absorber = ",momForward.max())
    print("Max mu- momentum exiting the absorber = ",momBackward.max())

    # Momentum 

    ut.Plot1D(momForward, 200, 100, 200, r""+g4blVersion+", $\pi^{-}$ into Be target", "Momentum [MeV]", "Events / MeV", "../img/"+g4blVersion+"/h1_mom_detForward_MuonBerylliumTarget_"+nEvents+"events.pdf")
    ut.Plot1D(momBackward, 200, 100, 200, r""+g4blVersion+", $\pi^{-}$ out of Be target", "Momentum [MeV]", "Events / MeV", "../img/"+g4blVersion+"/h1_mom_detBackward_MuonBerylliumTarget_"+nEvents+"events.pdf")

    ut.Plot1D(xMomForward, 120, -60, 60, r""+g4blVersion+", $\pi^{-}$ into Be target", "x-momentum [MeV]", "Events / MeV", "../img/"+g4blVersion+"/h1_px_detForward_MuonBerylliumTarget_"+nEvents+"events.pdf")
    ut.Plot1D(xMomBackward, 120, -60, 60, r""+g4blVersion+", $\pi^{-}$ out of Be target", "x-momentum [MeV]", "Events / MeV", "../img/"+g4blVersion+"/h1_px_detBackward_MuonBerylliumTarget_"+nEvents+"events.pdf") 

    ut.Plot1D(yMomForward, 120, -60, 60, r""+g4blVersion+", $\pi^{-}$ into Be target", "y-momentum [MeV]", "Events / MeV", "../img/"+g4blVersion+"/h1_py_detForward_MuonBerylliumTarget_"+nEvents+"events.pdf")
    ut.Plot1D(yMomBackward, 120, -60, 60, r""+g4blVersion+", $\pi^{-}$ out of Be target", "y-momentum [MeV]", "Events / MeV", "../img/"+g4blVersion+"/h1_py_detBackward_MuonBerylliumTarget_"+nEvents+"events.pdf") 

    ut.Plot2DWith1DProj(xMomForward, yMomForward, 120, -60, 60, 120, -60, 60, r""+g4blVersion+", $\pi^{-}$ into Be target", "x-momentum [MeV]", "y-momentum [MeV]", "../img/"+g4blVersion+"/h2_pxy_wproj_detForward_MuonBerylliumTarget_"+nEvents+"events.pdf")
    ut.Plot2DWith1DProj(xMomBackward, yMomBackward, 120, -60, 60, 120, -60, 60, r""+g4blVersion+", $\pi^{-}$ out of Be target", "x-momentum [MeV]", "y-momentum [MeV]", "../img/"+g4blVersion+"/h2_pxy_wproj_detBackward_MuonBerylliumTarget_"+nEvents+"events.pdf")

    # # Beam profile
    # ut.Plot1D(xForward, 220, -1100, 1100, r""+g4blVersion+", $\pi^{-}$ into Be target", "x [mm]", "Events / 10 mm", "../img/"+g4blVersion+"/h1_x_detForward_BerylliumTarget_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")
    # ut.Plot1D(xBackward, 220, -1100, 1100, r""+g4blVersion+", $\pi^{-}$ out of Be target", "x [mm]", "Events / 10 mm", "../img/"+g4blVersion+"/h1_x_detBackward_BerylliumTarget_"+particleFlag+"_"+nEvents+"events_"+str(ene)+"MeV"+stepSize+".pdf")

    # ut.Plot1D(yForward, 220, -1100, 1100,  r""+g4blVersion+", $\pi^{-}$ into Be target", "y [mm]" , "Events / 10 mm", "../img/"+g4blVersion+"/h1_y_detForward_BerylliumTarget_"+particleFlag+"_"+nEvents+"events_"+str(ene)+"MeV"+stepSize+".pdf")
    # ut.Plot1D(yBackward, 220, -1100, 1100,  r""+g4blVersion+", $\pi^{-}$ out of Be target", "y [mm]", "Events / 10 mm", "../img/"+g4blVersion+"/h1_y_detBackward_BerylliumTarget_"+particleFlag+"_"+nEvents+"events_"+str(ene)+"MeV"+stepSize+".pdf")

    # ut.Plot2D(xForward, yForward, 110, -550, 550, 110, -550, 550, r""+g4blVersion+", $\pi^{-}$ into Be target", "x [mm]", "y [mm]", "../img/"+g4blVersion+"/h2_xy_detForward_BerylliumTarget_"+particleFlag+"events_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")
    # ut.Plot2D(xBackward, yBackward, 110, -550, 550, 110, -550, 550, r""+g4blVersion+", $\pi^{-}$ out of Be target", "x [mm]", "y [mm]", "../img/"+g4blVersion+"/h2_xy_detBackward_BerylliumTarget_"+particleFlag+"events_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")

    # ut.Plot2DWith1DProj(xForward, yForward, 110, -550, 550, 110, -550, 550, r""+g4blVersion+", $\pi^{-}$ into Be target", "x [mm]", "y [mm]", "../img/"+g4blVersion+"/h2_xy_xProj_detForward_BerylliumTarget_"+particleFlag+"_"+nEvents+"events_"+str(ene)+"MeV"+stepSize+".pdf")
    # ut.Plot2DWith1DProj(xBackward, yBackward, 110, -550, 550, 110, -550, 550, r""+g4blVersion+", $\pi^{-}$ out of Be target", "x [mm]", "y [mm]", "../img/"+g4blVersion+"/h2_xy_xProj_detBackward_BerylliumTarget_"+particleFlag+"_"+nEvents+"events_"+str(ene)+"MeV"+stepSize+".pdf")


    # Write everything to hdf5 file
    foutName = "../plots/"+g4blVersion+"/g4beamlinePlots_MuonBerylliumTarget_"+nEvents+"events.h5" 

    fout = h5py.File(foutName, "w")

    # Write the DataFrames to the HDF5 file
    fout.create_dataset("momForward", data=momForward)
    fout.create_dataset("momBackward", data=momBackward)
    fout.create_dataset("xMomForward", data=xMomForward)
    fout.create_dataset("xMomBackward", data=xMomBackward)
    fout.create_dataset("yMomForward", data=yMomForward)
    fout.create_dataset("yMomBackward", data=yMomBackward)
    # fout.create_dataset("xForward", data=xForward)
    # fout.create_dataset("xBackward", data=xBackward)
    # fout.create_dataset("yForward", data=yForward)
    # fout.create_dataset("yBackward", data=yBackward)

    # Close the HDF5 file
    fout.close()

    print("---> Written", foutName)

    return 

def main():

    Run()

if __name__ == "__main__":
    main()
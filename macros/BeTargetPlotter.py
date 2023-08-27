# External libraries
import pandas as pd
import numpy as np
import h5py

# Internal libraries
import Utils as ut

def Run(ene):   

    g4blVersion="v3.08"
    nEvents="10e4"

    # stepSize="_maxStep0.1625" 
    # stepSize="_maxStep0.16" 
    # stepSize="_maxStep0.162" 
    # stepSize="_maxStep0.164" 
    # stepSize="_maxStep0.166" 
    # stepSize="_maxStep0.163" 
    stepSize="_maxStep50e-3_ShieldingM" # Lazy!

    print("\n--->Running at "+str(ene)+"MeV")

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
    finName = "../plots/"+g4blVersion+"/g4beamline_BerylliumTarget_pi-_"+str(ene)+"MeV_"+nEvents+"events"+stepSize+".root" 

    # Access the TTree
    dfForward = ut.TTreeToDataFrame(finName, "VirtualDetector/DetForward", branchNames)
    dfBackward = ut.TTreeToDataFrame(finName, "VirtualDetector/DetBackward", branchNames)

    # Put this before filtering the whole DataFrame, so you can count other particles if you like
    nPiMinusForward = dfForward[dfForward['PDGid'] == -211].shape[0]
    print("Number of pi- at forward detector =", nPiMinusForward)

    nPiMinusBackward = dfBackward[dfBackward['PDGid'] == -211].shape[0]
    print("Number of pi- at backward detector =", nPiMinusBackward)

    # TODO: make this more sophisticated, with if statements and PDGids and so on
    particleFlag = "pi-"

    # Filter 
    if particleFlag=="pi-": 
        dfForward = dfForward[dfForward['PDGid'] == -211]
        dfBackward= dfBackward[dfBackward['PDGid'] == -211]

    timeForward = dfForward["t"]
    timeBackward = dfBackward["t"]   

    xForward = dfForward["x"]
    xBackward = dfBackward["x"]  

    yForward = dfForward["y"]
    yBackward = dfBackward["y"]  

    momForward = np.sqrt( pow(dfForward["Px"],2) + pow(dfForward["Py"],2) + pow(dfForward["Pz"],2) )
    momBackward = np.sqrt( pow(dfBackward["Px"],2) + pow(dfBackward["Py"],2) + pow(dfBackward["Pz"],2) )

    ut.Plot1D(momForward, 500, 0, 500, r""+g4blVersion+", $\pi^{-}$ into Be target", "Momentum [MeV]", "Events / MeV", "../img/"+g4blVersion+"/h1_mom_detForward_BerylliumTarget_"+particleFlag+"_"+nEvents+"events_"+str(ene)+"MeV"+stepSize+".pdf")
    ut.Plot1D(momBackward, 500, 0, 500, r""+g4blVersion+", $\pi^{-}$ out of Be target", "Momentum [MeV]", "Events / MeV", "../img/"+g4blVersion+"/h1_mom_detBackward_BerylliumTarget_"+particleFlag+"_"+nEvents+"events_"+str(ene)+"MeV"+stepSize+".pdf", "best")
    # Zoom in on 50 MeV peak
    ut.Plot1D(momBackward, 1000, 30, 70, r""+g4blVersion+", $\pi^{-}$ out of Be target", "Momentum [MeV]", "Events", "../img/"+g4blVersion+"/h1_mom_detBackward_BerylliumTarget_"+particleFlag+"_"+nEvents+"events_"+str(ene)+"MeV"+stepSize+"_zoom.pdf")

    ut.Plot1D(xForward, 220, -1100, 1100, r""+g4blVersion+", $\pi^{-}$ into Be target", "x[mm]", "Events / 10 mm", "../img/"+g4blVersion+"/h1_x_detForward_BerylliumTarget_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")
    ut.Plot1D(xBackward, 220, -1100, 1100, r""+g4blVersion+", $\pi^{-}$ out of Be target", "x [mm]", "Events / 10 mm", "../img/"+g4blVersion+"/h1_x_detBackward_BerylliumTarget_"+particleFlag+"_"+nEvents+"events_"+str(ene)+"MeV"+stepSize+".pdf")

    ut.Plot1D(yForward, 220, -1100, 1100,  r""+g4blVersion+", $\pi^{-}$ into Be target", "y [mm]" , "Events / 10 mm", "../img/"+g4blVersion+"/h1_y_detForward_BerylliumTarget_"+particleFlag+"_"+nEvents+"events_"+str(ene)+"MeV"+stepSize+".pdf")
    ut.Plot1D(yBackward, 220, -1100, 1100,  r""+g4blVersion+", $\pi^{-}$ out of Be target", "y [mm]", "Events / 10 mm", "../img/"+g4blVersion+"/h1_y_detBackward_BerylliumTarget_"+particleFlag+"_"+nEvents+"events_"+str(ene)+"MeV"+stepSize+".pdf")

    ut.Plot2D(xForward, yForward, 110, -550, 550, 110, -550, 550, r""+g4blVersion+", $\pi^{-}$ into Be target", "x [mm]", "y [mm]", "../img/"+g4blVersion+"/h2_xy_detForward_BerylliumTarget_"+particleFlag+"events_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")
    ut.Plot2D(xBackward, yBackward, 110, -550, 550, 110, -550, 550, r""+g4blVersion+", $\pi^{-}$ out of Be target", "x [mm]", "y [mm]", "../img/"+g4blVersion+"/h2_xy_detBackward_BerylliumTarget_"+particleFlag+"events_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".pdf")

    ut.Plot2DWith1DProj(xForward, yForward, 110, -550, 550, 110, -550, 550, r""+g4blVersion+", $\pi^{-}$ into Be target", "x [mm]", "y [mm]", "../img/"+g4blVersion+"/h2_xy_xProj_detForward_BerylliumTarget_"+particleFlag+"_"+nEvents+"events_"+str(ene)+"MeV"+stepSize+".pdf")
    ut.Plot2DWith1DProj(xBackward, yBackward, 110, -550, 550, 110, -550, 550, r""+g4blVersion+", $\pi^{-}$ out of Be target", "x [mm]", "y [mm]", "../img/"+g4blVersion+"/h2_xy_xProj_detBackward_BerylliumTarget_"+particleFlag+"_"+nEvents+"events_"+str(ene)+"MeV"+stepSize+".pdf")

    # Write everything to hdf5 file
    foutName = "../plots/"+g4blVersion+"/g4beamlinePlots_BerylliumTarget_"+particleFlag+"_"+nEvents+"_"+str(ene)+"MeV"+stepSize+".h5"

    fout = h5py.File(foutName, "w")

    # Write the histograms to the HDF5 file
    fout.create_dataset("momForward", data=momForward)
    fout.create_dataset("momBackward", data=momBackward)
    fout.create_dataset("xForward", data=xForward)
    fout.create_dataset("xBackward", data=xBackward)
    fout.create_dataset("yForward", data=yForward)
    fout.create_dataset("yBackward", data=yBackward)

    # Close the HDF5 file
    fout.close()

    print("---> Written", foutName)

    return 

def main():

    Run(500)

    # for ene in range(100,1100,100):
    #     run(ene) 

if __name__ == "__main__":
    main()
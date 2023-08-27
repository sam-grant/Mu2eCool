# Run quick sanity check on g4bl sim 
# Print out the number of particles through VDs
# Make a momentum plot

# External libraries
import pandas as pd
import numpy as np
import h5py

# Internal libraries
import Utils as ut

def Run(branchNames, g4blVer, config, treeName, particle):

    # Setup input
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"
    print("---> Reading ",finName)
    # Access the TTree
    df = ut.TTreeToDataFrame(finName, treeName, branchNames)

    # Filter particles 
    particleFlag = "all"

    # Filter particles
    PDGid = 0
    if particle == "mu-": PDGid = 13
    elif particle == "pi-": PDGid = -211

    if PDGid != 0: 
        df_Coll_01_DetIn = df_Coll_01_DetIn[df_Coll_01_DetIn['PDGid'] == PDGid]
        df_Coll_01_DetOut = df_Coll_01_DetOut[df_Coll_01_DetOut['PDGid'] == PDGid]
        df_Coll_05_DetOut = df_Coll_05_DetOut[df_Coll_05_DetOut['PDGid'] == PDGid]
        df_Coll_05_DetOut = df_Coll_05_DetOut[df_Coll_05_DetOut['PDGid'] == PDGid]
        df_Coll_05_DetOut = df_Coll_05_DetOut[df_Coll_05_DetOut['PDGid'] == PDGid]
        df_prestop = df_prestop[df_prestop['PDGid'] == PDGid]
        df_poststop = df_poststop[df_poststop['PDGid'] == PDGid]
        df_LostInTarget = df_LostInTarget[df_LostInTarget['PDGid'] == PDGid]

    print("---> Total number of particles passing through "+treeName+" is", df.shape[0])
    # print("---> Number of pi- passing through "+treeName+" is", df[df['PDGid'] == -211].shape[0])
    # print("---> Number of mu- passing through "+treeName+" is", df[df['PDGid'] == 13].shape[0])

    mom = np.sqrt( pow(df["Px"],2) + pow(df["Py"],2) + pow(df["Pz"],2) )

    num_lines_to_print = 50
    line_count = 0
    while line_count < num_lines_to_print and line_count < mom.shape[0]:
        print(mom[line_count])
        line_count += 1

    ut.Plot1D(mom, 100, 1000, 10000, "", "Momentum [MeV]", "Events / 10 MeV", "../img/sanity/h1_mom_VD.png")

    # Write the df to csv
    foutName = "../txt/"+g4blVer+"/g4beamline_"+config+".csv"
    df.to_csv(foutName, index=False) # , header=None), sep='\t')
    print("---> Written to", foutName)

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
    config="ZNtupleDebug_5events" 
    treeName="VirtualDetector/VD"
    particle="all"

    Run(branchNames, g4blVer, config, treeName, particle) 
    Run(branchNames, g4blVer, config+"_fromBeamFile", treeName, particle) 

if __name__ == "__main__":
    main()
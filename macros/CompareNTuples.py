# Debug G4beamline outputs
# Discrepancies between files generated from source and those generated from zntuple
# Produce csv files for small samples and then compare them

# External libraries
import pandas as pd
import numpy as np

# Internal libraries
import Utils as ut

def Run(branchNames, config1, config2, treeName, g4blVer, particle):

    print(config1, config2)

    # Setup input2
    finName1 = "../ntuples/"+g4blVer+"/g4beamline_"+config1+".root"
    finName2 = "../ntuples/"+g4blVer+"/g4beamline_"+config2+".root"

    print("---> Opening ",finName1,finName2)

    # Access the TTree
    df1 = ut.TTreeToDataFrame(finName1, treeName, branchNames)
    df2 = ut.TTreeToDataFrame(finName2, treeName, branchNames)


    # Sort by EventID (only needed when you parallelise)
    df1 = df1.sort_values(by="EventID", ascending=True)
    df2 = df2.sort_values(by="EventID", ascending=True)

    print("---> Number of tracks in "+finName1+" = ",df1.shape[0])
    print("---> Number of tracks in "+finName2+" = ",df2.shape[0])

    # Find unique tracks
    df2['TrackID'] = df2['TrackID'] + 1000

    df1['UniqueID'] = 1e7*df1['EventID'] + 1e3*df1['TrackID'] + df1['ParentID']
    df2['UniqueID'] = 1e7*df2['EventID'] + 1e3*(df2['TrackID']) + df2['ParentID']

    print(df1) 
    print(df2)

    # Get unique IDS
    commonTracks1 = df1[df1['UniqueID'].isin(df2['UniqueID'])]
    commonTracks2 = df2[df2['UniqueID'].isin(df1['UniqueID'])]
    # uniqueTracks1 = df2[~df2['UniqueID'].isin(df1['UniqueID'])]
    # uniqueTracks2 = df1[~df1['UniqueID'].isin(df2['UniqueID'])]

    # Create df_stopped by selecting commmon events between df_prestop and df_LostInTarget

    print(commonTracks1.shape[0], commonTracks2.shape[0])
    
    return

    # Write the df to csv
    foutName = "../txt/"+g4blVer+"/g4beamline_"+treeName+"_"+config+".csv"
    df.to_csv(foutName, index=False) 
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
    treeName="NTuple/Z2265" # "VirtualDetector/Coll_01_DetOut" # "VirtualDetector/Coll_01_DetIn" #  # 
    particle="all"

    # Run(branchNames, "Mu2E_1e3events_rseedNone_fromSource", "Mu2E_1e3events_rseedNone_fromZ2265_series", treeName, g4blVer, particle) 
    # Run(branchNames, "Mu2E_5e6events", "Mu2E_5e6events.2", treeName, g4blVer, particle) 
    Run(branchNames, "Mu2E_1e7events", "Mu2E_1e7events_fromZ2265_parallel", treeName, g4blVer, particle) 

if __name__ == "__main__":
    main()
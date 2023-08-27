# Debug G4beamline outputs
# Discrepancies between files generated from source and those generated from zntuple
# Produce csv files for small samples and then compare them

# External libraries
import pandas as pd
import numpy as np

# Internal libraries
import Utils as ut

def Run(branchNames, g4blVer, config, treeName, particle):

    # Setup input
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"
    print("---> Reading ",finName)

    # Access the TTree
    df = ut.TTreeToDataFrame(finName, treeName, branchNames)

    # Sort by EventID (only needed when you parallelise)
    df = df.sort_values(by="EventID", ascending=True)

    # Filter particles 
    particleFlag = "all"

    # Filter particles
    PDGid = 0
    if particle == "mu-": PDGid = 13
    elif particle == "pi-": PDGid = -211

    if PDGid != 0: 
        df = df[df['PDGid'] == PDGid]

    print("\n---> Total number of particles passing through "+treeName+" is", df.shape[0])
    print("---> protons:", df[df['PDGid'] == 2212].shape[0])
    print("---> pi-:", df[df['PDGid'] == -211].shape[0])
    print("---> pi+:", df[df['PDGid'] == 211].shape[0])
    print("---> mu-:", df[df['PDGid'] == 13].shape[0])
    print("---> mu+:", df[df['PDGid'] == -13].shape[0])

    # Check for duplicate IDs
    df['UniqueID'] = 1e6*df['EventID'] + 1e3*df['TrackID'] + df['ParentID']

    # uniqueTracks = df2[~df2['UniqueID'].isin(df1['UniqueID'])]

    duplicates = df[df.duplicated(subset=['EventID', 'TrackID', 'ParentID'], keep=False)]

    while not duplicates.empty:
        print("\n---> "+str(duplicates.shape[0])+" duplicate rows found!")
        print("---> Duplicates:\n", duplicates, "\n")  
        print("---> Cleaning up duplicates...")
        # Keep all but the last
        df = df.drop_duplicates(subset=['EventID', 'TrackID', 'ParentID'], keep='last')
        duplicates = df[df.duplicated(subset=['EventID', 'TrackID', 'ParentID'], keep=False)]
        print("\nDuplicates:\n",duplicates,"\n") 

    # print(df[(df['EventID'] == 939) & (df['TrackID'] == 1017) & (df['ParentID'] == 1016)])

    mom = np.sqrt( pow(df["Px"],2) + pow(df["Py"],2) + pow(df["Pz"],2) )

    # num_lines_to_print = 50
    # line_count = 0
    # while line_count < num_lines_to_print and line_count < mom.shape[0]:
    #     print(mom[line_count])
    #     line_count += 1

    treeName = treeName.split("/")[-1]

    # ut.Plot1D(mom, 300, 0, 300, config, "Momentum [MeV]", "Counts / MeV", "../img/sanity/h1_Momentum_"+treeName+"_"+config+".pdf")
    # ut.Plot1D(df["EventID"], int(abs(df.shape[0]/10000)), 0, np.max(df["EventID"]), config, "Event ID", "Counts / 1e4 IDs", "../img/sanity/h1_EventID_"+treeName+"_"+config+".pdf", "best")

    # Write the df to csv
    # foutName = "../txt/"+g4blVer+"/g4beamline_"+treeName+"_"+config+".csv"
    # df.to_csv(foutName, index=False) 
    # print("---> Written to", foutName)

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

    # Run(branchNames, g4blVer, "Mu2E_100events_rdmSeedEventNum_noExotics_fromSource", treeName, particle) 
    # Run(branchNames, g4blVer, "Mu2E_100events_rdmSeedEventNum_noExotics_fromZ2265_series", treeName, particle) 
    # Run(branchNames, g4blVer, "Mu2E_100events_rdmSeedEventNum_noExotics_fromZ2265_TEST_series", treeName, particle) 
    # Run(branchNames, g4blVer, "Mu2E_100events_rdmSeedEventNum_noExotics_fromZ2265_parallel", treeName, particle) 
    # Run(branchNames, g4blVer, "Mu2E_100events_rdmSeedEventNum_noExotics_fromZ2265_parallel_oneFile", treeName, particle) 

    # Run(branchNames, g4blVer, "Mu2E_1e6events_rseedTime", treeName, particle) 
    # Run(branchNames, g4blVer, "Mu2E_1e6events_rseedTime_fromZ2265_series", treeName, particle) 

    # Run(branchNames, g4blVer, "Mu2E_1e6events", treeName, particle) 
    # Run(branchNames, g4blVer, "Mu2E_1e6events_fromZ2265_series", treeName, particle) 

    # Run(branchNames, g4blVer, "Mu2E_1e3events_rseedNone_fromSource", treeName, particle) 
    # Run(branchNames, g4blVer, "Mu2E_1e3events_rseedNone_fromZ2265_series", treeName, particle) 

    # Run(branchNames, g4blVer, "Mu2E_5e6events", treeName, particle) 
    # Run(branchNames, g4blVer, "Mu2E_5e6events_fromZ2265_parallel", treeName, particle)
    # Run(branchNames, g4blVer, "Mu2E_5e6events_fromZ2265_wDupes_parallel", treeName, particle)
    # ../ntuples/v3.06/g4beamline_Mu2E_5e6events_fromZ2265_wDupes_parallel.root\

    # Run(branchNames, g4blVer, "Mu2E_5e6events", treeName, particle)
    # Run(branchNames, g4blVer, "Mu2E_5e6events.2", treeName, particle)
    Run(branchNames, g4blVer, "Mu2E_1e7events", treeName, particle)
    Run(branchNames, g4blVer, "Mu2E_1e7events_fromZ2265_parallel", treeName, particle)

if __name__ == "__main__":
    main()
# Plot the momentum coming out the toy PS model

# External libraries
import pandas as pd
import numpy as np
import h5py

# Internal libraries
import Utils as ut

def Run():

    # Only grab the ones we need
    branchNames = [ 
        "EventID",
        "TrackID",
        "ParentID",
        "Px", 
        "Py",
        "Pz",
        "PDGid"
    ]  

    g4blVersion = "v3.06"
    # config = "ToyPs_1e4events_notFromBeamFile" 
    config = "ToyPs_1e4events" 

    finNameFBF = "../plots/"+g4blVersion+"/g4beamline_"+config+"_fromBeamFile.root"
    finNameNFBF = "../plots/"+g4blVersion+"/g4beamline_"+config+"_notFromBeamFile.root"

    # Access the TTree

    vdFBF = ut.TTreeToDataFrame(finNameFBF, "VirtualDetector/VD", branchNames)
    vdNFBF = ut.TTreeToDataFrame(finNameNFBF, "VirtualDetector/VD", branchNames)

    # print('FBF', vdFBF)
    # print('NFBF', vdNFBF)

    # return

    # TODO: make this more sophisticated, with if statements and PDGids and so on
    particleFlag = "all"

    # Filter pi minus
    if particleFlag == "pi-":
        vdFBF = vdFBF[vdFBF['PDGid'] == -211]
        vdNFBF = vdNFBF[vdNFBF['PDGid'] == -211]
    elif particleFlag == "mu-":
        vdFBF = vdFBF[vdFBF['PDGid'] == 13]
        vdNFBF = vdNFBF[vdNFBF['PDGid'] == 13]

    # Check for unique events

    # Add unique ID column to both DataFrames
    # vdNFBF['UniqueID'] = vdNFBF['EventID']*vdNFBF['TrackID']*vdNFBF['ParentID']*vdNFBF['PDGid']
    # vdFBF['UniqueID'] = vdFBF['EventID']*vdFBF['TrackID']*vdFBF['ParentID']*vdNFBF['PDGid']
    # # print('FBF', vdFBF)
    # # print('NFBF', vdNFBF)

    # vdNFBFUnique = vdNFBF[vdNFBF['UniqueID'].isin(vdFBF['UniqueID'])]

    # vdNFBFCommon = vdNFBF[vdNFBF['UniqueID'].isin(vdFBF['UniqueID'])]
    # vdFBFCommon = vdFBF[vdFBF['UniqueID'].isin(vdNFBF['UniqueID'])]

    # print('vdNFBFCommon\n', vdNFBFCommon)
    # print('vdFBFCommon\n', vdFBFCommon)
    
    # return
    # vdFBF['UniqueID'] = vdFBF['EventID'] * vdFBF['TrackID'] #  1e3 * vdFBF['ParentID'] 

    # print(vdNFBF['UniqueID'])

    # # Get common IDS
    # unique_ids = vdNFBF[~vdNFBF['UniqueID'].isin(vdFBF['UniqueID'])]

    # print(len(unique_ids))

    # return

    momFBF = np.sqrt( pow(vdFBF["Px"],2) + pow(vdFBF["Py"],2) + pow(vdFBF["Pz"],2) )
    momNFBF = np.sqrt( pow(vdNFBF["Px"],2) + pow(vdNFBF["Py"],2) + pow(vdNFBF["Pz"],2) )

    # Add momentum magnitude as a column to dfs
    vdFBF['P'] = momFBF
    vdNFBF['P'] = momNFBF

    vdNFBFCommon = vdNFBF[~vdNFBF['P'].isin(vdFBF['P'])]
    vdFBFCommon = vdFBF[~vdFBF['P'].isin(vdNFBF['P'])]

    print("vdNFBFCommon\n",vdNFBFCommon)
    print("vdFBFCommon\n",vdFBFCommon)
    # momNFBFUnique = np.sqrt( pow(vdNFBFUnique["Px"],2) + pow(vdNFBFUnique["Py"],2) + pow(vdNFBFUnique["Pz"],2) ) 
    # momNFBFCommon = np.sqrt( pow(vdNFBFCommon["Px"],2) + pow(vdNFBFCommon["Py"],2) + pow(vdNFBFCommon["Pz"],2) ) 
    # momFBFCommon = np.sqrt( pow(vdFBFCommon["Px"],2) + pow(vdFBFCommon["Py"],2) + pow(vdFBFCommon["Pz"],2) ) 

    # print(momUnique)

    # ut.Plot1D(mom, 105, -50, 1000, "Not using beam file", "Momentum [MeV]", "Events / 10 MeV", "../img/v3.06/h1_mom_"+config+".pdf", "best", True)
    ut.Plot1D(momFBF, 105, -50, 1000, "From beam file", "Momentum [MeV]", "Events / 10 MeV", "../img/v3.06/h1_mom_"+config+"_fromBeamFile.pdf", "best", True)
    ut.Plot1D(momNFBF, 105, -50, 1000, "Not from beam file", "Momentum [MeV]", "Events / 10 MeV", "../img/v3.06/h1_mom_"+config+"_notFromBeamFile.pdf", "best", True)


    # ut.Plot1D(momNFBFUnique, 105, -50, 1000, "Unique NFBF", "Momentum [MeV]", "Events / 10 MeV", "../img/v3.06/h1_mom_"+config+"_uniqueNFBF.pdf", "best", True)
    # ut.Plot1D(momNFBFCommon, 105, -50, 1000, "Common NFBF", "Momentum [MeV]", "Events / 10 MeV", "../img/v3.06/h1_mom_"+config+"_commonNFBF.pdf", "best", True)
    # ut.Plot1D(momFBFCommon, 105, -50, 1000, "Common FBF", "Momentum [MeV]", "Events / 10 MeV", "../img/v3.06/h1_mom_"+config+"_commonFBF.pdf", "best", True)
    
    return 


def main():

    Run()

if __name__ == "__main__":
    main()
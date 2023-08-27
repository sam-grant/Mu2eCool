# Make beam profile plots at a zntuple or VD
# Interested in the relationship between momentum and traverse space, for absorber study

import uproot
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

# Internal libraries
import Utils as ut

# Globals
g4blVer="v3.06"

particleDict = {
    2212: 'proton',
    211: 'pi+',
    -211: 'pi-',
    -13: 'mu+',
    13: 'mu-'
    # Add more particle entries as needed
    }

def Run(config, branchNames, ntupleName):

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

    df = ut.TTreeToDataFrame(finName, ntupleName, branchNames)  

    ntupleName = ntupleName.split("/")[1] 

    # df['UniqueID'] = 1e6*df['EventID'] + 1e3*df['TrackID'] 

    # Calculate the number of dropped duplicates

    # Keep one of the duplicates while dropping the rest
    df_duplicates = df[df.duplicated(subset=["EventID", "TrackID"], keep=False)] # , keep='first') == False]
    # mask_first_occurrences = df.duplicated(subset=["EventID", "TrackID"], keep="first")
    # df_duplicates = df_duplicates[~mask_first_occurrences]
    # print(df_duplicates)

    # Calculate the number of duplicates removed
    nDupes = len(df_duplicates)

    print("---> Number of duplicates in", ntupleName, "is", nDupes, "out of", len(df))

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
        "Weight",
        "InitX",
        "InitY",
        "InitZ"
    ] 

    ntupleName="NTuple/Z1800" # 965"
    Run("Mu2E_1e7events", branchNames, ntupleName) 


if __name__ == "__main__":
    main()



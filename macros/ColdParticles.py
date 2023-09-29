# Write cooled off muons and pions to an ntuple

# External libraries
import pandas as pd
import numpy as np
from scipy import stats
import uproot

# Internal libraries
import Utils as ut

# Globals
g4blVer="v3.06"

def RunFilter(df):
    # Drop any duplicates
    df = df.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"], keep="first") 
    # Filter upstream particles
    # df = df[df["Pz"]>0]
    return df

def GetLostAndNewParticles(df_in, df_out):

    # Get particles that are unique to df_in and df_out, using an outer join
    df_unique = df_in.merge(df_out, on=["EventID", "TrackID", "ParentID", "PDGid"], suffixes=("_in", "_out"), how="outer")

    # Select null rows in "out"
    df_lost = df_unique[df_unique["x_out"].isnull()] 
    # Drop any duplicates
    df_lost = df_lost.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])
    # Drop the "out" columns
    df_lost = df_lost[[col for col in df_lost.columns if not col.endswith("_out")]] # [df_in_cold_pions.columns]
    # Strip the suffixes
    for col in df_lost.columns:
        if col.endswith("_in"):
            df_lost.rename(columns={col: col[:-len("_in")]}, inplace=True)
    # Reorder the columns 
    df_lost = df_lost[['x', 'y', 'z', 'Px', 'Py', 'Pz', 't', 'PDGid', 'EventID', 'TrackID', 'ParentID', 'Weight', "P", "R"]]

    # Select null rows in "in"
    df_new = df_unique[df_unique["x_in"].isnull()] 
    # Drop any duplicates
    df_new = df_new.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])
    # Drop the "in" columns
    df_new = df_new[[col for col in df_new.columns if not col.endswith("_in")]]
    # Strip the suffixes
    for col in df_new.columns:
        if col.endswith("_out"):
            df_new.rename(columns={col: col[:-len("_out")]}, inplace=True)
    # Reorder the columns 
    df_new = df_new[['x', 'y', 'z', 'Px', 'Py', 'Pz', 't', 'PDGid', 'EventID', 'TrackID', 'ParentID', 'Weight', "P", "R"]]

    return df_lost, df_new


def WriteDataFrameToTTree(df, treeName, foutName):

    import ROOT as r 

    foutName = "../ntuples/"+g4blVer+"/g4beamline_"+foutName+".root"

    fout = r.TFile(foutName, "RECREATE")
    tree = r.TTree("NTuple", treeName)

    # Define TBranch arrays with appropriate data types (without "array_" prefix)
    x = np.zeros(1, dtype=np.float64)
    y = np.zeros(1, dtype=np.float64)
    z = np.zeros(1, dtype=np.float64)
    R = np.zeros(1, dtype=np.float64)
    Px = np.zeros(1, dtype=np.float64)
    Py = np.zeros(1, dtype=np.float64)
    Pz = np.zeros(1, dtype=np.float64)
    P = np.zeros(1, dtype=np.float64)
    t = np.zeros(1, dtype=np.float64)
    PDGid = np.zeros(1, dtype=np.int32)
    EventID = np.zeros(1, dtype=np.int32)
    TrackID = np.zeros(1, dtype=np.int32)
    ParentID = np.zeros(1, dtype=np.int32)
    Weight = np.zeros(1, dtype=np.int32)

    # Create TBranches for each column (without "array_" prefix)
    tree.Branch('x', x, 'x/D')
    tree.Branch('y', y, 'y/D')
    tree.Branch('z', z, 'z/D')
    tree.Branch('R', R, 'R/D')
    tree.Branch('Px', Px, 'Px/D')
    tree.Branch('Py', Py, 'Py/D')
    tree.Branch('Pz', Pz, 'Pz/D')
    tree.Branch('P', P, 'P/D')
    tree.Branch('t', t, 't/D')
    tree.Branch('PDGid', PDGid, 'PDGid/I')
    tree.Branch('EventID', EventID, 'EventID/I')
    tree.Branch('TrackID', TrackID, 'TrackID/I')
    tree.Branch('ParentID', ParentID, 'ParentID/I')
    tree.Branch('Weight', Weight, 'Weight/I')

    # Fill the TBranches with data from the DataFrame
    for index, row in df.iterrows():
        x[0] = row['x']
        y[0] = row['y']
        z[0] = row['z']
        R[0] = row['R']
        Px[0] = row['Px']
        Py[0] = row['Py']
        Pz[0] = row['Pz']
        P[0] = row['P']
        t[0] = row['t']
        PDGid[0] = row['PDGid']
        EventID[0] = row['EventID']
        TrackID[0] = row['TrackID']
        ParentID[0] = row['ParentID']
        Weight[0] = row['Weight']
        tree.Fill()
        # Write the ROOT file to disk
        # fout.Write()
        # fout.Close()
        
    fout.Write()
    fout.Close()

    print("---> Written DataFrame to TTree:",fout)

    return 

def RunColdParticles(config, foutName):

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

    absorberName = config.split("_")[2] 
 
    # Read in TTree
    df_in = ut.TTreeToDataFrame(finName, "VirtualDetector/BeAbsorber_DetIn", ut.branchNames)
    df_out = ut.TTreeToDataFrame(finName, "VirtualDetector/BeAbsorber_DetOut", ut.branchNames)
    df_prestop = ut.TTreeToDataFrame(finName, "VirtualDetector/prestop", ut.branchNames)

    # Filter
    df_in = RunFilter(df_in)
    df_out = RunFilter(df_out)
    df_prestop = RunFilter(df_prestop)

    # Add momentum column
    df_in["P"] = np.sqrt( pow(df_in["Px"], 2) + pow(df_in["Py"], 2) + pow(df_in["Pz"], 2) ) 
    df_out["P"] = np.sqrt( pow(df_out["Px"], 2) + pow(df_out["Py"], 2) + pow(df_out["Pz"], 2) ) 
    # Add radius column
    df_in["R"] = np.sqrt( pow(df_in["x"], 2) + pow(df_in["y"], 2) ) 
    df_out["R"] = np.sqrt( pow(df_out["x"], 2) + pow(df_out["y"], 2) ) 

    # pions and muons
    df_in_pions = ut.FilterParticles(df_in, "pi-")
    df_in_muons = ut.FilterParticles(df_in, "mu-")
    df_out_pions = ut.FilterParticles(df_out, "pi-")
    df_out_muons = ut.FilterParticles(df_out, "mu-")
    # df_prestop_pions = ut.FilterParticles(df_prestop_pions, "pi-") 
    # df_prestop_muons = ut.FilterParticles(df_prestop_muons, "mu-") 

    # Sanity plots, compare with AbsorberCooling.py
    ut.Plot1D(df_in_pions["P"], 750, 0, 750, "pions in", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdParticles/h1_Mom_In_pi-_"+config+".png") # , stats=True) 
    ut.Plot1D(df_in_muons["P"], 275, 0, 275, "muons in", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdParticles/h1_Mom_In_mu-_"+config+".png") # , stats=True) 
    ut.Plot1D(df_out_pions["P"], 750, 0, 750, "pions in", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdParticles/h1_Mom_Out_pi-_"+config+".png") # , stats=True) 
    ut.Plot1D(df_out_muons["P"], 275, 0, 275, "muons out", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdParticles/h1_Mom_Out_mu-_"+config+".png") # , stats=True) 

    # Cold particles, pions below 100 MeV and muons below 50 MeV
    df_in_cold_pions = df_in_pions[df_in_pions["P"] < 100]
    df_out_cold_pions = df_out_pions[df_out_pions["P"] < 100]
    df_in_cold_muons = df_in_muons[df_in_muons["P"] < 50]
    df_out_cold_muons = df_out_muons[df_out_muons["P"] < 50]

    # More sanity plots, compare with AbsorberCooling.py
    ut.Plot1D(df_in_cold_pions["P"], 100, 0, 100, "cold pions in", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdParticles/h1_mom_in_cold_pi-_"+config+".png") # , stats=True) 
    ut.Plot1D(df_in_cold_muons["P"], 50, 0, 50, "cold muons in", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdParticles/h1_mom_in_cold_mu-_"+config+".png") # , stats=True) 
    ut.Plot1D(df_out_cold_pions["P"], 100, 0, 100,"cold pions out", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdParticles/h1_mom_out_cold_pi-_"+config+".png") # , stats=True) 
    ut.Plot1D(df_out_cold_muons["P"], 50, 0, 50, "cold muons out", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdParticles/h1_mom_out_cold_mu-_"+config+".png") # , stats=True) 

    # Get lost and new particles
    df_lost_cold_pions, df_new_cold_pions = GetLostAndNewParticles(df_in_cold_pions, df_out_cold_pions)
    df_lost_cold_muons, df_new_cold_muons = GetLostAndNewParticles(df_in_cold_muons, df_out_cold_muons)

    # print(df_lost_cold_muons)
    # print(df_new_cold_pions)
    # print(df_lost_cold_muons)
    # print(df_new_cold_muons)

    # return

    # Check results make sense, they usually don't
    print("\n---> Actual number of additional cold pions (from histograms):", df_out_cold_pions.shape[0] - df_in_cold_pions.shape[0])
    print("---> Actual number of additional cold muons (from histograms):", df_out_cold_muons.shape[0] - df_in_cold_muons.shape[0])
    print("---> Additional cold pions (using pandas):", df_new_cold_pions.shape[0]-df_lost_cold_pions.shape[0])
    print("---> Additional cold muons (using pandas):", df_new_cold_muons.shape[0]-df_lost_cold_muons.shape[0])
    print("---> This must be zero:", (df_out_cold_pions.shape[0]-df_in_cold_pions.shape[0]) - (df_new_cold_pions.shape[0]-df_lost_cold_pions.shape[0]))
    print("---> This must be zero:", (df_out_cold_muons.shape[0] - df_in_cold_muons.shape[0]) - (df_new_cold_muons.shape[0]-df_lost_cold_muons.shape[0]))

    print("\n---> Lost cold pions:", df_lost_cold_pions.shape[0])
    print("---> Lost cold muons:", df_lost_cold_muons.shape[0])
    print("---> New cold pions:", df_new_cold_pions.shape[0])
    print("---> New cold pions:", df_new_cold_muons.shape[0])

    # DataFrame for cold particles, pions below 100 MeV and muons below 50 MeV
    df_coldParticles = pd.concat( [df_new_cold_pions, df_new_cold_muons] )

    # Sanity plot, compare with P branch in the ntuple
    ut.Plot1D(df_coldParticles["P"], 120, 0, 120, "cold particles", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/ColdParticles/h1_mom_cold_particles_"+config+".png") # , stats=True) 
    
    # Presentation plot, compare lost and new
    ut.Plot1DOverlay([df_lost_cold_pions["P"], df_new_cold_pions["P"]], 100, 0, 100, r"$\pi^{-}$", "Momentum [MeV]", "Counts / MeV", labels=["Lost", "New"], fout="../img/"+g4blVer+"/ColdParticles/h1_mom_cold_pions_overlay_"+config+".png", legPos="best", legFontSize=14)  
    ut.Plot1DOverlay([df_lost_cold_muons["P"], df_new_cold_muons["P"]], 50, 0, 50, r"$\mu^{-}$", "Momentum [MeV]", "Counts / MeV", labels=["Lost", "New"], fout="../img/"+g4blVer+"/ColdParticles/h1_mom_cold_muons_overlay_"+config+".png", legPos="best", legFontSize=14)
    ut.Plot1DOverlay([df_lost_cold_pions["R"], df_new_cold_pions["R"]], 200, 0, 200, r"$\pi^{-}$", "Radial position [mm]", "Counts / mm", labels=["Lost", "New"], fout="../img/"+g4blVer+"/ColdParticles/h1_rad_cold_pions_overlay_"+config+".png", legPos="best", legFontSize=14)  
    ut.Plot1DOverlay([df_lost_cold_muons["R"], df_new_cold_muons["R"]], 40, 0, 200, r"$\mu^{-}$", "Radial position [mm]", "Counts / 5 mm", labels=["Lost", "New"], fout="../img/"+g4blVer+"/ColdParticles/h1_rad_cold_muons_overlay_"+config+".png", legPos="best", legFontSize=14) 

    ut.Plot1DRatio([df_lost_cold_pions["P"], df_new_cold_pions["P"]], 100, 0, 100, r"$\pi^{-}$", "Momentum [MeV]", "Counts / MeV", labels=["Lost", "New"], fout="../img/"+g4blVer+"/ColdParticles/h1_ratio_mom_cold_pions_overlay_"+config+".png", legPos="best", invertRatio=True)
    ut.Plot1DRatio([df_lost_cold_muons["P"], df_new_cold_muons["P"]], 50, 0, 50, r"$\mu^{-}$", "Momentum [MeV]", "Counts / MeV", labels=["Lost", "New"], fout="../img/"+g4blVer+"/ColdParticles/h1_ratio_mom_cold_muons_overlay_"+config+".png", legPos="best", invertRatio=True)
    ut.Plot1DRatio([df_lost_cold_pions["R"], df_new_cold_pions["R"]], 200, 0, 200, r"$\pi^{-}$", "Radial position [mm]", "Counts / mm", labels=["Lost", "New"], fout="../img/"+g4blVer+"/ColdParticles/h1_ratio_rad_cold_pions_overlay_"+config+".png", legPos="best", invertRatio=True) 
    ut.Plot1DRatio([df_lost_cold_muons["R"], df_new_cold_muons["R"]], 40, 0, 200, r"$\mu^{-}$", "Radial position [mm]", "Counts / 5 mm", labels=["Lost", "New"], fout="../img/"+g4blVer+"/ColdParticles/h1_ratio_rad_cold_muons_overlay_"+config+".png", legPos="best", invertRatio=True)


    # ut.Plot2D(df_lost_cold_pions["P"], df_lost_cold_pions["R"], )
    # print("---> Total new cold particles:", df_coldParticles.shape[0])

    print("--->prestop / cold particles:", df_prestop.shape[0] / df_prestop)

    # Convert the DataFrame to a TTree
    treeName = "ColdParticles"  

    WriteDataFrameToTTree(df_coldParticles, treeName, foutName) 

    return

def main():

    # RunColdParticles("Mu2E_1e7events_Absorber3_l40mm_r100mm_fromZ1850_parallel", "Mu2E_Absorber3_l40mm_r100mm_fromZ1850_parallel_ColdParticles")
    # RunColdParticles("Mu2E_1e7events_AbsorberB_l30mm_r100mm_fromZ1850_parallel", "Mu2E_1e7events_AbsorberB_l30mm_r100mm_fromZ1850_parallel")
    
    RunColdParticles("Mu2E_1e7events_AbsorberD_l25mm_r110mm_fromZ1850_parallel", "Mu2E_1e7events_AbsorberD_l25mm_r110mm_fromZ1850_parallel_ColdParticles")
    # RunColdParticles("Mu2E_1e7events_AbsorberD_l25mm_r110mm_fromZ1850_parallel_noColl_noPbar", "Mu2E_1e7events_AbsorberD_l25mm_r110mm_fromZ1850_parallel_noColl_noPbar_ColdParticles")

if __name__ == "__main__":
    main()
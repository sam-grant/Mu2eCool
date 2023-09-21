# Write cooled off muons and pions to an ntuple

# External libraries
import pandas as pd
import numpy as np
from scipy import stats

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
    df_lost.columns = df_lost.columns.str.rstrip('_in')

    # Select null rows in "in"
    df_new = df_unique[df_unique["x_in"].isnull()] 
    # Drop any duplicates
    df_new = df_new.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"])
    # Drop the "in" columns
    df_new = df_new[[col for col in df_new.columns if not col.endswith("_in")]]
    # Strip the suffixes
    df_new.columns = df_new.columns.str.rstrip('_out')

    return df_lost, df_new


def RunWriteColdParticles(config, dim=""):

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

    absorberName = config.split("_")[2] 
 
    # Read in TTree
    df_in = ut.TTreeToDataFrame(finName, "VirtualDetector/BeAbsorber_DetIn", ut.branchNames)
    df_out = ut.TTreeToDataFrame(finName, "VirtualDetector/BeAbsorber_DetOut", ut.branchNames)

    # Filter
    df_in = RunFilter(df_in)
    df_out = RunFilter(df_out)

    # Add momentum column
    df_in["P"] = np.sqrt( pow(df_in["Px"], 2) + pow(df_in["Py"], 2) + pow(df_in["Pz"], 2) ) 
    df_out["P"] = np.sqrt( pow(df_out["Px"], 2) + pow(df_out["Py"], 2) + pow(df_out["Pz"], 2) ) 

    # pions and muons
    df_in_pions = ut.FilterParticles(df_in, "pi-")
    df_in_muons = ut.FilterParticles(df_in, "mu-")
    df_out_pions = ut.FilterParticles(df_out, "pi-")
    df_out_muons = ut.FilterParticles(df_out, "mu-")

    # Sanity plots, compare with AbsorberCooling.py
    ut.Plot1D(df_in_pions["P"], 750, 0, 750, "pions in", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/WriteColdParticles/h1_Mom_In_pi-_"+config+".png") # , stats=True) 
    ut.Plot1D(df_in_muons["P"], 275, 0, 275, "muons in", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/WriteColdParticles/h1_Mom_In_mu-_"+config+".png") # , stats=True) 
    ut.Plot1D(df_out_pions["P"], 750, 0, 750, "pions in", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/WriteColdParticles/h1_Mom_Out_pi-_"+config+".png") # , stats=True) 
    ut.Plot1D(df_out_muons["P"], 275, 0, 275, "muons out", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/WriteColdParticles/h1_Mom_Out_mu-_"+config+".png") # , stats=True) 

    # Cold particles, pions below 100 MeV and muons below 50 MeV
    df_in_cold_pions = df_in_pions[df_in_pions["P"] < 100]
    df_out_cold_pions = df_out_pions[df_out_pions["P"] < 100]
    df_in_cold_muons = df_in_muons[df_in_muons["P"] < 50]
    df_out_cold_muons = df_out_muons[df_out_muons["P"] < 50]

    # More sanity plots, compare with AbsorberCooling.py
    ut.Plot1D(df_in_cold_pions["P"], 100, 0, 100, "cold pions in", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/WriteColdParticles/h1_Mom_In_cold_pi-_"+config+".png") # , stats=True) 
    ut.Plot1D(df_in_cold_muons["P"], 50, 0, 50, "cold muons in", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/WriteColdParticles/h1_Mom_In_cold_mu-_"+config+".png") # , stats=True) 
    ut.Plot1D(df_out_cold_pions["P"], 100, 0, 100,"cold pions out", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/WriteColdParticles/h1_Mom_Out_cold_pi-_"+config+".png") # , stats=True) 
    ut.Plot1D(df_out_cold_muons["P"], 50, 0, 50, "cold muons out", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/WriteColdParticles/h1_Mom_Out_cold_mu-_"+config+".png") # , stats=True) 

    # Get lost and new particles
    df_lost_cold_pions, df_new_cold_pions = GetLostAndNewParticles(df_in_cold_pions, df_out_cold_pions)
    df_lost_cold_muons, df_new_cold_muons = GetLostAndNewParticles(df_in_cold_muons, df_out_cold_muons)

    # Check results make sense
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

    # Write out cold particles

    # DataFrame for cold particles, pions below 100 MeV and muons below 50 MeV
    df_coldParticles = pd.concat( [df_new_cold_pions, df_new_cold_muons] )

    print("---> Total new cold particles:", df_coldParticles.shape[0])

    return






    # # Drop any duplicates 
    # df_BeAbsorber_DetOut = df_BeAbsorber_DetOut.drop_duplicates(["EventID", "TrackID", "ParentID", "PDGid"], keep="first")

    # ut.Plot1D()

    # i_xmax = 0 
    # # xmax_ = [1250, 1250, 750, 750, 275, 275] 
    # xmax_ = [750, 275] 

    # # DataFrame for cold particles
    # df_coldParticles = pd.DataFrame()

    # particles = ["pi-", "mu-"]

    # for particle in particles: 

    #     print("\n--->",particle)

    #     title = ut.GetLatexParticleName(particle)+", "+absorberName+", "+dim

    #     in_ = ut.FilterParticles(df_BeAbsorber_DetIn, particle)
    #     out_ = ut.FilterParticles(df_BeAbsorber_DetOut, particle)

    #     # Sanity check, compare with AbsorberCooling.py
    #     ut.Plot1DOverlayWithStats([in_["P"], out_["P"]], int(xmax_[i_xmax]), 0, xmax_[i_xmax], title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/WriteColdParticles/h1_Mom_InOut_"+particle+"_"+config+".png", ["Entering", "Exiting"], peak=True)

    #     # Iterate xmax
    #     i_xmax += 1

    #     # Select cold particles 
    #     if particle=="pi-":
    #         df_coldParticles = out_[out_["P"] < 100]
    #     elif particle=="mu-":
    #         df_coldParticles = pd.concat[df_coldParticles, out_[out_["P"] < 50]]





    # return

def main():

    RunWriteColdParticles("Mu2E_1e7events_Absorber3_l40mm_r100mm_fromZ1850_parallel", "$L_{max}$ = 40 mm, $R_{i}$ = 100 mm")

if __name__ == "__main__":
    main()
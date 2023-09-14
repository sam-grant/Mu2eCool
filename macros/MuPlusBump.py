# Check out a bump in the mu+ momentum (it's from kaons)

# External libraries
import uproot
import pandas as pd
import numpy as np
import h5py

# Internal libraries
import Utils as ut

# Suppress warnings about overwriting a dataframe
pd.options.mode.chained_assignment = None  # default='warn'

# Globals

g4blVer="v3.06"

def RunMuPlusBump(config, ntupleName, particle, maxMom = 500):

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"
    df = ut.TTreeToDataFrame(finName, ntupleName, ut.branchNamesExtended)  

    # Titles and names
    ntupleName = ntupleName.split("/")[1] 
    title = ut.GetLatexParticleName(particle) # 
    if ntupleName[0] == "Z": title += ", Z = "+ntupleName[1:]+" mm"
    else: title += ", "+ntupleName

    # Define some useful parameters

    # Momentum 
    df["P"] = np.sqrt( pow(df["Px"],2) + pow(df["Py"],2) + pow(df["Pz"],2) ) 
    # Radius 
    df["R"] = np.sqrt( pow(df["x"],2) + pow(df["y"],2)) 
    # Tranvserse momentum 
    df["PT"] = np.sqrt( pow(df["Px"],2) + pow(df["Py"],2) ) 

    df_mu_plus = ut.FilterParticles(df, "mu+")

    # Some mu+ plots 
    ut.Plot1D(df_mu_plus["P"], 500, 0, maxMom, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/MuPlusBump/h1_mom_"+ntupleName+"_"+particle+"_"+config+".png", errors=True)
    ut.Plot1D(df_mu_plus[(df_mu_plus["P"]>15)&(df_mu_plus["P"]<31)]["P"], 500, 0, maxMom, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/MuPlusBump/h1_mom_loBump_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)
    ut.Plot1D(df_mu_plus[(df_mu_plus["P"]>150)&(df_mu_plus["P"]<250)]["P"], 500, 0, maxMom, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/MuPlusBump/h1_mom_hiBump_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)
    ut.Plot1D(df_mu_plus["R"], 500, 0, 500, title, "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/MuPlusBump/h1_rad_"+ntupleName+"_"+particle+"_"+config+".png", errors=True)
    ut.Plot2D(df_mu_plus["P"], df_mu_plus["R"], 250, 0, 250, 210, 0, 210, title, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/MuPlusBump/h2_RvsMom_"+ntupleName+"_"+particle+"_"+config+".png")
    ut.Plot2D(df_mu_plus["x"], df_mu_plus["y"], 400, -200, 200, 400, -200, 200, title, "x [mm]", "y [mm]", "../img/"+g4blVer+"/MuPlusBump/h2_XvsY_"+ntupleName+"_"+particle+"_"+config+".png") 
    ut.Plot2D(df_mu_plus["InitX"], df_mu_plus["InitY"], 400, -200, 200, 400, -200, 200, title, "Initial x [mm]", "Initial y [mm]", "../img/"+g4blVer+"/MuPlusBump/h2_InitXvsY_"+ntupleName+"_"+particle+"_"+config+".png")         

    # Merge the original DataFrame with itself based on EventID and ParentID
    # This is really clever, it won't capture them all though since most of the parents don't enter the plane.
    df_children_and_parents = df.merge(df, left_on=["EventID", "ParentID"], right_on=["EventID", "TrackID"], suffixes=("_child", "_parent"))

    # Get the parents of mu+
    df_mu_plus_parents = df_children_and_parents[df_children_and_parents["PDGid_child"] == -13] 

    # print(df_mu_plus_parents[(df_mu_plus_parents["P_child"] >= 200) & (df_mu_plus_parents["P_child"] <= 250)]["PDGid_parent"])
    # PDGids of parents which are not pi+ or K+
    # print(df_mu_plus_parents[(df_mu_plus_parents["P_child"] >= 200) & (df_mu_plus_parents["P_child"] <= 250) & (df_mu_plus_parents["PDGid_parent"] != 211) & (df_mu_plus_parents["PDGid_parent"] != 321)]["PDGid_parent"])

    # # get the latex names of the particles in the particle dictionary 
    # latexParticleDict = {}
    # for key, value in  ut.particleDict.items():
    #     latexParticleDict[key] = ut.GetLatexParticleName(value)


    # Plot the PDGids of the parents
    ut.BarChart(df_mu_plus_parents["PDGid_parent"], ut.latexParticleDict, r"$\mu^{+}$ parents", "", "Counts / particle", fout="../img/"+g4blVer+"/MuPlusBump/bar_ParentIDCounts_"+ntupleName+"_"+config+".png", percentage=False)
    ut.BarChart(df_mu_plus_parents[(df_mu_plus_parents["P_child"] > 15) & (df_mu_plus_parents["P_child"] < 31)]["PDGid_parent"], ut.latexParticleDict, r"$\mu^{+}$ parents, 15 < p [MeV] < 31", "", "Counts / particle", fout="../img/"+g4blVer+"/MuPlusBump/bar_ParentIDCounts_loBump_"+ntupleName+"_"+config+".png", percentage=False)
    ut.BarChart(df_mu_plus_parents[(df_mu_plus_parents["P_child"] > 150) & (df_mu_plus_parents["P_child"] < 250)]["PDGid_parent"], ut.latexParticleDict, r"$\mu^{+}$ parents, 150 < p [MeV] < 250", "", "Counts / particle", fout="../img/"+g4blVer+"/MuPlusBump/bar_ParentIDCounts_hiBump_"+ntupleName+"_"+config+".png", percentage=False)
    # ut.BarChart(df_mu_plus_parents[(df_mu_plus_parents["P_child"] >= 200) & (df_mu_plus_parents["P_child"] <= 250)]["PDGid_parent"], ut.latexParticleDict, r"$\mu^{+}$ parents, 200 < p [MeV] < 250", "", "Counts / particle", fout="../img/"+g4blVer+"/MuPlusBump/bar_ParentIDCounts_200-250MeV_"+ntupleName+"_"+config+".png", percentage=False)

    # What do muons which come from K+ look like 
    title2 = r"$\mu^{+}$ from $K^{+}$, Z = 1850 mm"
    ut.Plot1D(df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==321]["P_child"], int(maxMom/10), 0, maxMom, title2, "Momentum [MeV]", "Counts / 10 MeV", "../img/"+g4blVer+"/MuPlusBump/h1_mom_mu+FromK+_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)
    ut.Plot1D(df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==321]["P_parent"], int(maxMom/10), 0, maxMom, title2, "Momentum [MeV]", "Counts / 10 MeV", "../img/"+g4blVer+"/MuPlusBump/h1_mom_parentK+_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)
    ut.Plot1D(df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==321]["R_child"], 50, 0, 500, title2, "Radial position [mm]", "Counts / 10 mm", "../img/"+g4blVer+"/MuPlusBump/h1_rad_mu+FromK+_"+ntupleName+"_"+particle+"_"+config+".png", errors=True)
    ut.Plot2D(df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==321]["P_child"], df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==321]["R_child"], 25, 0, 250, 21, 0, 210, title2, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/MuPlusBump/h2_RvsMom_mu+FromK+_"+ntupleName+"_"+particle+"_"+config+".png")

    title2 = r"$\mu^{+}$ from $K^{0}_{L}$, Z = 1850 mm"
    ut.Plot1D(df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==130]["P_child"], int(maxMom/10), 0, maxMom, title2, "Momentum [MeV]", "Counts / 10 MeV", "../img/"+g4blVer+"/MuPlusBump/h1_mom_mu+FromK0L_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)
    ut.Plot1D(df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==130]["P_parent"], int(maxMom/10), 0, maxMom, title2, "Momentum [MeV]", "Counts / 10 MeV", "../img/"+g4blVer+"/MuPlusBump/h1_mom_parentK0L_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)
    ut.Plot1D(df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==130]["R_child"], 50, 0, 500, title2, "Radial position [mm]", "Counts / 10 mm", "../img/"+g4blVer+"/MuPlusBump/h1_rad_mu+FromK0L_"+ntupleName+"_"+particle+"_"+config+".png", errors=True)
    ut.Plot2D(df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==130]["P_child"], df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==130]["R_child"], 25, 0, 250, 21, 0, 210, title2, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/MuPlusBump/h2_RvsMom_mu+FromK0L_"+ntupleName+"_"+particle+"_"+config+".png")

    title2 = r"$\mu^{+}$ from $\pi^{+}$, Z = 1850 mm"
    ut.Plot1D(df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==211]["P_child"], int(maxMom/10), 0, maxMom, title2, "Momentum [MeV]", "Counts / 10 MeV", "../img/"+g4blVer+"/MuPlusBump/h1_mom_mu+FromPi+_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)
    ut.Plot1D(df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==211]["P_parent"], int(maxMom/10), 0, maxMom, title2, "Momentum [MeV]", "Counts / 10 MeV", "../img/"+g4blVer+"/MuPlusBump/h1_mom_parentPi+_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)
    ut.Plot1D(df_mu_plus_parents[(df_mu_plus_parents["PDGid_parent"]==211) & (df_mu_plus_parents["P_child"] > 15) & (df_mu_plus_parents["P_child"] < 31)]["P_parent"], int(maxMom/10), 0, maxMom, r"$\pi^{+}$ parents, 15 < $p_{\mu^{+}}$ [MeV] < 31", "Momentum [MeV]", "Counts / 10 MeV", "../img/"+g4blVer+"/MuPlusBump/h1_mom_parentPi+_loBump_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)
    ut.Plot1D(df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==211]["R_child"], 50, 0, 500, title2, "Radial position [mm]", "Counts / 10 mm", "../img/"+g4blVer+"/MuPlusBump/h1_rad_mu+FromPi+_"+ntupleName+"_"+particle+"_"+config+".png", errors=True)
    ut.Plot2D(df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==211]["P_child"], df_mu_plus_parents[df_mu_plus_parents["PDGid_parent"]==211]["R_child"], 25, 0, 250, 21, 0, 210, title2, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/MuPlusBump/h2_RvsMom_mu+FromPi+_"+ntupleName+"_"+particle+"_"+config+".png")

    # ut.Plot2D(df_mu_plus["x"], df_mu_plus["y"], 400, -200, 200, 400, -200, 200, title, "x [mm]", "y [mm]", "../img/"+g4blVer+"/MuPlusBump/h2_XvsY_"+ntupleName+"_"+particle+"_"+config+".png") 
    # ut.Plot2D(df_mu_plus["InitX"], df_mu_plus["InitY"], 400, -200, 200, 400, -200, 200, title, "Initial x [mm]", "Initial y [mm]", "../img/"+g4blVer+"/MuPlusBump/h2_InitXvsY_"+ntupleName+"_"+particle+"_"+config+".png")         

    # Filter mu+ particles
    # df_mu_plus = ut.FilterParticles(df, particle)

    # print(df_mu_plus)
    # print(df[df["EventID"]==21])
    # print(df[df["EventID"]==77])
    # print(df[df["EventID"]==82])

    # Merge the original DataFrame with itself based on EventID and ParentID
    # merged_df_mu_plus = df.merge(df, left_on=["EventID", "ParentID"], right_on=["EventID", "TrackID"], suffixes=("_child", "_parent"))

    # df_mu_plus_parents = merged_df_mu_plus[merged_df_mu_plus["PDGid_child"] == -13] 


    return

    # Momentum 
    df_mu_plus["P"] = np.sqrt( pow(df_mu_plus["Px"],2) + pow(df_mu_plus["Py"],2) + pow(df_mu_plus["Pz"],2) ) 
    # Radius 
    df_mu_plus["R"] = np.sqrt( pow(df_mu_plus["x"],2) + pow(df_mu_plus["y"],2)) 
    # Tranvserse momentum 
    df_mu_plus["PT"] = np.sqrt( pow(df_mu_plus["Px"],2) + pow(df_mu_plus["Py"],2) ) 

    ut.Plot1D(df_mu_plus["P"], 500, 0, maxMom, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/MuPlusBump/h1_mom_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)
    ut.Plot1D(df_mu_plus["R"], 500, 0, 500, title, "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/MuPlusBump/h1_rad_"+ntupleName+"_"+particle+"_"+config+".png", errors=True)
    ut.Plot2D(df_mu_plus["P"], df_mu_plus["R"], 250, 0, 250, 210, 0, 210, title, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/MuPlusBump/h2_RvsMom_"+ntupleName+"_"+particle+"_"+config+".png")
    ut.Plot2D(df_mu_plus["x"], df_mu_plus["y"], 400, -200, 200, 400, -200, 200, title, "x [mm]", "y [mm]", "../img/"+g4blVer+"/MuPlusBump/h2_XvsY_"+ntupleName+"_"+particle+"_"+config+".png") 
    ut.Plot2D(df_mu_plus["InitX"], df_mu_plus["InitY"], 400, -200, 200, 400, -200, 200, title, "Initial x [mm]", "Initial y [mm]", "../img/"+g4blVer+"/MuPlusBump/h2_InitXvsY_"+ntupleName+"_"+particle+"_"+config+".png")         

    # Select 200-250 MeV
    df_mu_plus_bump = df_mu_plus[(df_mu_plus["P"] >= 200) & (df_mu_plus["P"] <= 250)]

    ut.Plot1D(df_mu_plus_bump["P"], 500, 0, maxMom, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/MuPlusBump/h1_mom_200-250MeV_"+ntupleName+"_"+particle+"_"+config+".png", errors=True, peak=True)
    ut.Plot1D(df_mu_plus_bump["R"], 500, 0, 500, title, "Radial position [mm]", "Counts / mm", "../img/"+g4blVer+"/MuPlusBump/h1_rad_200-250MeV_"+ntupleName+"_"+particle+"_"+config+".png", errors=True)
    ut.Plot2D(df_mu_plus_bump["P"], df_mu_plus_bump["R"], 250, 0, 250, 210, 0, 210, title, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/MuPlusBump/h2_RvsMom_200-250MeV_"+ntupleName+"_"+particle+"_"+config+".png")
    ut.Plot2D(df_mu_plus_bump["x"], df_mu_plus_bump["y"], 400, -200, 200, 400, -200, 200, title, "x [mm]", "y [mm]", "../img/"+g4blVer+"/MuPlusBump/h2_XvsY_200-250MeV_"+ntupleName+"_"+particle+"_"+config+".png") 
    ut.Plot2D(df_mu_plus_bump["InitX"], df_mu_plus_bump["InitY"], 400, -200, 200, 400, -200, 200, title, "Initial x [mm]", "Initial y [mm]", "../img/"+g4blVer+"/MuPlusBump/h2_InitXvsY_200-250MeV_"+ntupleName+"_"+particle+"_"+config+".png")         

    # ut.BarChart(df["PDGid"], ut.particleDict, title, "", "Counts / particle", fout="../img/"+g4blVer+"/MuPlusBump/bar_ParentIDCounts_"+ntupleName+"_"+config+".png", percentage=False)

    return


def main():

    RunMuPlusBump("Mu2E_1e7events_NoAbsorber", "NTuple/Z1850", "mu+", 300)

if __name__ == "__main__":
    main()
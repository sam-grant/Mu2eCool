# For comparing two beamlines
# Takes two input files
# Overlays the momentum distributions at each VD a particular particle species. 

# External libraries
import uproot
import pandas as pd
import numpy as np

# Internal libraries
import Utils as ut

# Suppress warnings about overwriting a dataframe
pd.options.mode.chained_assignment = None  # default='warn'

# Globals
g4blVer="v3.06"

def ParticleMomentumOverlay(df, ntupleName, title, config, xmax):

    df["P"] = np.sqrt( np.power(df["Px"], 2) + np.power(df["Py"], 2) + np.power(df["Pz"], 2) )

    df_proton = ut.FilterParticles(df, "proton") 
    df_pi_plus = ut.FilterParticles(df, "pi+") 
    df_pi_minus = ut.FilterParticles(df, "pi-") 
    df_mu_plus = ut.FilterParticles(df, "mu+") 
    df_mu_minus = ut.FilterParticles(df, "mu-")  

    ut.Plot1DOverlay([df["P"], df_proton["P"], df_pi_plus["P"], df_pi_minus["P"], df_mu_plus["P"], df_mu_minus["P"]], nbins=int(xmax), xmin=0, xmax=xmax, title = title, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = ["All", "$p$", "$\pi^{+}$", "$\pi^{-}$", "$\mu^{+}$", "$\mu^{-}$"], fout = "../img/"+g4blVer+"/BeamFlux/h1_ParticleMomentumOverlay_"+ntupleName+"_"+config+".png", includeBlack=True)

    # print("Mean momentum [MeV]:")
    # print("---> all:", np.mean(df["P"]))
    # print("---> proton:", np.mean(df_proton["P"])) 
    # print("---> pion:", np.mean(df_pion["P"]))
    # print("---> muon:", np.mean(df_muon["P"]))

    # print("RMS momentum [MeV]:")
    # print("---> all:", np.std(df["P"]))
    # print("---> proton:", np.std(df_proton["P"])) 
    # print("---> pion:", np.std(df_pion["P"]))
    # print("---> muon:", np.std(df_muon["P"]))

    # print("Peak momentum [MeV]:")
    # print("---> all:", df["P"].value_counts().idxmax())
    # print("---> proton:", df_proton["P"].value_counts().idxmax())
    # print("---> pion:", df_pion["P"].value_counts().idxmax())
    # print("---> muon:", df_muon["P"].value_counts().idxmax())

    return

def RunCompareBeams(config_, label_, name, absorber=False):

    # Setup input 
    finName_ = []
    for config in config_:
        finName_.append("../ntuples/"+g4blVer+"/g4beamline_"+config+".root") 

    # Set up container for dataframes
    # We're dealing with multiple files at once, so it's a bit awkard

    df_Z_ = [] 
    df_BeAbsorber_DetIn_ = []
    df_BeAbsorber_DetOut_ = []
    df_Coll_01_DetIn_ = [] 
    df_Coll_01_DetOut_ = [] 
    df_Coll_03_DetIn_ = [] 
    df_Coll_03_DetOut_ = [] 
    df_Coll_05_DetIn_ = [] 
    df_Coll_05_DetOut_ = [] 
    df_prestop_ = [] 
    df_poststop_ = [] 

    dfDict = {
        "NTuple/Z1850":  df_Z_,
        "VirtualDetector/BeAbsorber_DetIn": df_BeAbsorber_DetIn_,
        "VirtualDetector/BeAbsorber_DetOut": df_BeAbsorber_DetOut_,
        "VirtualDetector/Coll_01_DetIn": df_Coll_01_DetIn_,
        "VirtualDetector/Coll_01_DetOut": df_Coll_01_DetOut_,
        "VirtualDetector/Coll_03_DetIn": df_Coll_03_DetIn_,
        "VirtualDetector/Coll_03_DetOut": df_Coll_03_DetOut_,
        "VirtualDetector/Coll_05_DetIn": df_Coll_05_DetIn_,
        "VirtualDetector/Coll_05_DetOut": df_Coll_05_DetOut_,
        "VirtualDetector/prestop": df_prestop_, 
        "VirtualDetector/poststop": df_poststop_
        }

    # Fill the DataFrames
    for finName in finName_:

        for key, df_ in dfDict.items():

            # Read in TTrees, avoiding absorber VDs if they're not being used
            if not absorber and (key == "VirtualDetector/BeAbsorber_DetIn" or key == "VirtualDetector/BeAbsorber_DetOut"):
                continue

            df = ut.TTreeToDataFrame(finName, key, ut.branchNames) 

            # Add total momentum column
            df["P"] = np.sqrt( pow(df["Px"], 2) + pow(df["Py"], 2) + pow(df["Pz"], 2) )
            # Add more columns here as needed

            # Append
            df_.append(df)


    # ------ Overlay the momentum distributions at each VD for particular particle species ------

    particle_ = ["mu-"] # ["All", "proton", "pi+", "pi-", "mu+", "mu-"]

    i_xmax = 0 
    xmax_ = [1350, 725, 725, 725, 725, 150, 150, 150, 150, 150, 150] 

    for key, df_ in dfDict.items():

        if not absorber and (key == "VirtualDetector/BeAbsorber_DetIn" or key == "VirtualDetector/BeAbsorber_DetOut"):
            i_xmax += 1
            continue

        for particle in particle_:

             # Momentum overlay for two files for a particular particle species
            title = key.split("/")[1] 

            # Could extend this to 3+ entries easily enough
            ut.Plot1DOverlayWithStats([ut.FilterParticles(df_[0], particle)["P"], ut.FilterParticles(df_[1], particle)["P"]], nbins=int(xmax_[i_xmax]), xmin=0, xmax=xmax_[i_xmax], title = ut.GetLatexParticleName(particle)+", "+title, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = label_, fout = "../img/"+g4blVer+"/CompareBeams/h1_ParticleMomentumOverlay_"+particle+"_"+title+"_"+name+".png", peak=True)
            ut.Plot1DOverlayWithStats([ut.FilterParticles(df_[0], particle)["P"], ut.FilterParticles(df_[1], particle)["P"]], nbins=50, xmin=0, xmax=50, title = ut.GetLatexParticleName(particle)+", "+title, xlabel = "Momentum [MeV]", ylabel = "Counts / MeV", labels = label_, fout = "../img/"+g4blVer+"/CompareBeams/h1_ParticleMomentumOverlay_xmax50MeV_"+particle+"_"+title+"_"+name+".png", peak=False)

            # TODO: add ratio plot here

        i_xmax += 1

    return

def main():

    # RunMuonFlux("Mu2E_1e7events_fromZ1850_parallel")

    # Compare beamline with/without collimator
    # RunBeamCooling(["Mu2E_1e7events_fromZ1850_parallel", "Mu2E_1e7events_fromZ1850_parallel_noColl03"], ["With Coll_03", "Without Coll_03"], "Mu2E_1e7events_fromZ1850_parallel_WithVsWoutColl03")

    # Compare Absorbers to control
    # RunCompareBeams(["Mu2E_1e7events_fromZ1850_parallel_noColl03", "Mu2E_1e7events_Absorber1_l55mm_r85mm_fromZ1850_parallel_noColl03"], [r"No\ absorber", r"Absorber\ 1"], "Mu2E_1e7events_fromZ1850_parallel_NoAbsorberVsAbsorber1_noColl03", absorber=True)
    # RunCompareBeams(["Mu2E_1e7events_fromZ1850_parallel_noColl03", "Mu2E_1e7events_Absorber3_l55mm_r85mm_fromZ1850_parallel_noColl03"], [r"No\ absorber", r"Absorber\ 3"], "Mu2E_1e7events_fromZ1850_parallel_NoAbsorberVsAbsorber3_noColl03", absorber=True)
    RunCompareBeams(["Mu2E_1e7events_fromZ1850_parallel_noColl03", "Mu2E_1e7events_Absorber3.1_l90mm_r85mm_fromZ1850_parallel_noColl03"], [r"No\ absorber", r"Absorber\ 3.1"], "Mu2E_1e7events_fromZ1850_parallel_NoAbsorberVsAbsorber3.1_noColl03", absorber=True)

    # RunMuonFlux("Mu2E_1e7events_Absorber0_100mm_fromZ1850_parallel")
    # RunMuonFlux("Mu2E_1e7events_Absorber1_100mm_fromZ1850_parallel") 
    # RunMuonFlux("Mu2E_1e7events_Absorber2_100mm_fromZ1850_parallel")
    # RunMuonFlux("Mu2E_1e7events_Absorber3_100mm_fromZ1850_parallel")

    # RunMuonFlux("Mu2E_1e7events_Absorber0_100mm_fromZ1850_parallel_noColl03")
    # RunMuonFlux("Mu2E_1e7events_Absorber1_100mm_fromZ1850_parallel_noColl03")
    # RunMuonFlux("Mu2E_1e7events_Absorber2_100mm_fromZ1850_parallel_noColl03")
    # RunMuonFlux("Mu2E_1e7events_Absorber3_100mm_fromZ1850_parallel_noColl03")

    # RunMuonFlux("Mu2E_1e7events_Absorber0_20mm_fromZ1850_parallel_noColl03") 
    # RunMuonFlux("Mu2E_1e7events_Absorber1_20mm_fromZ1850_parallel_noColl03") 
    # RunMuonFlux("Mu2E_1e7events_Absorber2_20mm_fromZ1850_parallel_noColl03") 
    # RunMuonFlux("Mu2E_1e7events_Absorber3_20mm_fromZ1850_parallel_noColl03") 

    # RunMuonFlux("Mu2E_1e7events_Absorber0_30mm_fromZ1850_parallel_noColl03") 
    # RunMuonFlux("Mu2E_1e7events_Absorber1_30mm_fromZ1850_parallel_noColl03") 
    # RunMuonFlux("Mu2E_1e7events_Absorber2_30mm_fromZ1850_parallel_noColl03") 
    # RunMuonFlux("Mu2E_1e7events_Absorber3_30mm_fromZ1850_parallel_noColl03") 

if __name__ == "__main__":
    main()
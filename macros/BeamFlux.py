# Summarise the overall flux of particles passing through each virtual detector in the experiment

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

# Analyse muon flux through Mu2e, including the stopped muon yield
def RunMuonFlux(config):

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"
 
    # Read in TTrees
    # TODO: store this all in a dictionary
    df_Z = ut.TTreeToDataFrame(finName, "NTuple/Z1850", ut.branchNames)
    df_Coll_01_DetIn = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_01_DetIn", ut.branchNames)
    df_Coll_01_DetOut = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_01_DetOut", ut.branchNames)
    df_Coll_03_DetIn = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_03_DetIn", ut.branchNames)
    df_Coll_03_DetOut = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_03_DetOut", ut.branchNames)
    df_Coll_05_DetIn = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_05_DetIn", ut.branchNames)
    df_Coll_05_DetOut = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_05_DetOut", ut.branchNames)
    df_prestop = ut.TTreeToDataFrame(finName, "VirtualDetector/prestop", ut.branchNames)
    df_poststop = ut.TTreeToDataFrame(finName, "VirtualDetector/poststop", ut.branchNames)
    df_LostInTarget = ut.TTreeToDataFrame(finName, "NTuple/LostInTarget_Ntuple", ut.branchNames)

    # ------ All flux ------

    # All particles at Z
    everythingAtZ = df_Z.shape[0]

    # Particle populations entering the TS, sometimes useful
    # ut.BarChart(df_Z['PDGid'], particle_dict, "Particles at Z1850", "", "Percentage / PDGid", fout="../img/"+g4blVer+"/BeamFlux/bar_ParticleFraction_Z1800_"+config+".pdf", percentage=False)
    # ut.BarChart(df_Coll_01_DetOut['PDGid'], particle_dict, "Particles exiting TS", "", "Percentage / PDGid", fout="../img/"+g4blVer+"/BeamFlux/bar_ParticleFraction_Coll_01_DetOut_"+config+".pdf", percentage=False)
    # ut.BarChart(df_Coll_01_DetOut['PDGid'], particle_dict, title="Out of TS collimator 1", xlabel="", ylabel="Percentage / PDGid", fout='../img/v3.06/bar_ParticleFraction_df_Coll_01_DetOut.pdf', percentage=True)
    # ut.BarChart(df_Coll_03_DetIn['PDGid'], particle_dict, title="Into TS collimator 3", xlabel="", ylabel="Percentage / PDGid", fout='../img/v3.06/bar_ParticleFraction_Coll_03_DetIn.pdf', percentage=True)
    # ut.BarChart(df_Coll_03_DetOut['PDGid'], particle_dict, title="Out of TS collimator 3", xlabel="", ylabel="Percentage / PDGid", fout='../img/v3.06/bar_ParticleFraction_Coll_03_DetOut.pdf', percentage=True)
    # ut.BarChart(df_Coll_05_DetIn['PDGid'], particle_dict, title="Into TS collimator 5", xlabel="", ylabel="Percentage / PDGid", fout='../img/v3.06/bar_ParticleFraction_Coll_05_DetIn.pdf', percentage=True)
    # ut.BarChart(df_Coll_05_DetOut['PDGid'], particle_dict, title="Out of TS collimator 5", xlabel="", ylabel="Percentage / PDGid", fout='../img/v3.06/bar_ParticleFraction_Coll_05_DetOut.pdf', percentage=True)
    # ut.BarChart(df_prestop['PDGid'], particle_dict, title="Into stopping target", xlabel="", ylabel="Percentage / PDGid", fout='../img/v3.06/bar_ParticleFraction_prestop.pdf', percentage=True)

    # Momentum overlay for particle species in each zntuple/VD, before filtering
    print("\n---> ParticleMomentumOverlays:")
    ParticleMomentumOverlay(df_Z, "Z1850", "At Z = 1850 mm", config, 1350)
    ParticleMomentumOverlay(df_Coll_01_DetIn, "Coll_01_DetIn", "Entering TS collimator 1", config, 725)
    ParticleMomentumOverlay(df_Coll_01_DetOut, "Coll_01_DetOut", "Exiting TS collimator 1", config, 725)
    ParticleMomentumOverlay(df_Coll_03_DetIn, "Coll_03_DetIn", "Entering TS collimator 3", config, 150)
    ParticleMomentumOverlay(df_Coll_03_DetOut, "Coll_03_DetOut", "Exiting TS collimator 3", config, 150)
    ParticleMomentumOverlay(df_Coll_05_DetIn, "Coll_05_DetIn", "Exiting TS collimator 5", config, 150)
    ParticleMomentumOverlay(df_Coll_05_DetOut, "Coll_05_DetOut", "Exiting TS collimator 5", config, 150)
    ParticleMomentumOverlay(df_prestop, "df_prestop", "Entering ST", config, 150)
    ParticleMomentumOverlay(df_poststop, "df_poststop", "Exiting ST", config, 150)

    # Store pi- entering the TS, for a plot...
    df_Coll_01_DetOut_piminus = ut.FilterParticles(df_Coll_01_DetOut, "pi-")

    # ------ Muon flux ------
    print("\n---> Muon flux:")
    # Filter muons
    particle = "mu-"
    df_Z = ut.FilterParticles(df_Z, particle) 
    df_Coll_01_DetIn = ut.FilterParticles(df_Coll_01_DetIn, particle)
    df_Coll_01_DetOut = ut.FilterParticles(df_Coll_01_DetOut, particle)
    df_Coll_03_DetIn = ut.FilterParticles(df_Coll_03_DetIn, particle)
    df_Coll_03_DetOut = ut.FilterParticles(df_Coll_03_DetOut, particle) 
    df_Coll_05_DetIn = ut.FilterParticles(df_Coll_05_DetIn, particle) 
    df_Coll_05_DetOut = ut.FilterParticles(df_Coll_05_DetOut, particle) 
    df_prestop = ut.FilterParticles(df_prestop, particle) 
    df_poststop = ut.FilterParticles(df_poststop, particle) 
    df_LostInTarget = ut.FilterParticles(df_LostInTarget, particle) 

    # Stopped muons: muons which are present in prestop and LostInTarget
    # Add the "UniqueID" column sto df_prestop and df_LostInTarget, get the common tracks
    df_prestop['UniqueID'] = 1e6*df_prestop['EventID'] + 1e3*df_prestop['TrackID'] + df_prestop['ParentID'] 
    df_LostInTarget['UniqueID'] = 1e6*df_LostInTarget['EventID'] + 1e3*df_LostInTarget['TrackID'] + df_LostInTarget['ParentID']
    df_stoppedMuons = df_prestop[df_prestop['UniqueID'].isin(df_LostInTarget['UniqueID'])] 

    # Momentum 
    df_Z["P"] = np.sqrt( pow(df_Z["Px"],2) + pow(df_Z["Py"],2) + pow(df_Z["Pz"],2) )
    # df_Coll_01_DetIn["P"] = np.sqrt( pow(df_Coll_01_DetIn["Px"],2) + pow(df_Coll_01_DetIn["Py"],2) + pow(df_Coll_01_DetIn["Pz"],2) )
    df_Coll_01_DetOut["P"] = np.sqrt( pow(df_Coll_01_DetOut["Px"],2) + pow(df_Coll_01_DetOut["Py"],2) + pow(df_Coll_01_DetOut["Pz"],2) )
    df_Coll_01_DetOut_piminus["P"] = np.sqrt( pow(df_Coll_01_DetOut_piminus["Px"],2) + pow(df_Coll_01_DetOut_piminus["Py"],2) + pow(df_Coll_01_DetOut_piminus["Pz"],2) )
    # df_Coll_05_DetOut["P"] = np.sqrt( pow(df_Coll_05_DetOut["Px"],2) + pow(df_Coll_05_DetOut["Py"],2) + pow(df_Coll_05_DetOut["Pz"],2) )
    df_prestop["P"] = np.sqrt( pow(df_prestop["Px"],2) + pow(df_prestop["Py"],2) + pow(df_prestop["Pz"],2) )

    # print(df_stoppedMuons)
    df_stoppedMuons["P"] = np.sqrt( pow(df_stoppedMuons["Px"],2) + pow(df_stoppedMuons["Py"],2) + pow(df_stoppedMuons["Pz"],2) ) 
    # print(df_stoppedMuons)

    # Write out the number of partices at each point along the beamline
    fluxDict = {
        "Particle & location": [
                    "All at Z", particle+" at Z", 
                    particle+" at Coll_01", particle+" at Coll_01", 
                    particle+" at Coll_03", particle+" at Coll_03", 
                    particle+" at Coll_05", particle+" at Coll_05", 
                    particle+" at ST", particle+" at ST", 
                    particle+" at ST", particle+" at ST", 
                    particle+" at ST", particle+" at ST",
                    "---", particle+" at ST",
                    particle+" at ST", particle+" at ST",
                    particle+" at ST", particle+" at ST",
                ],
            "Info": [
                    "At", "At",
                    "Entering", "Exiting", 
                    "Entering", "Exiting", 
                    "Entering", "Exiting", 
                    "Entering", "Entering (<50 MeV)", 
                    "Exiting", "Lost", 
                    "Stopped", "Stopped (<50 MeV)",
                    "---", "Entering <50 MeV / Entering",
                    "Stopped / POT", "Stopped / All at Z",
                    "Stopped / Entering", "Stopped / Entering (>50 Mev)"
                ],
            "Count": [
                    everythingAtZ, df_Z.shape[0],
                    df_Coll_01_DetIn.shape[0], df_Coll_01_DetOut.shape[0],
                    df_Coll_03_DetIn.shape[0], df_Coll_03_DetOut.shape[0],
                    df_Coll_05_DetIn.shape[0], df_Coll_05_DetOut.shape[0],
                    df_prestop.shape[0],  df_prestop[df_prestop["P"] < 50].shape[0],
                    df_poststop.shape[0], df_LostInTarget.shape[0], 
                    df_stoppedMuons.shape[0], df_stoppedMuons[df_stoppedMuons["P"] < 50].shape[0],
                    "---", df_prestop[df_prestop["P"] < 50].shape[0] / df_prestop.shape[0],
                    df_stoppedMuons.shape[0] / 1e7, df_stoppedMuons.shape[0] / everythingAtZ, 
                    df_stoppedMuons.shape[0] / df_prestop.shape[0], df_stoppedMuons.shape[0] / df_prestop[df_prestop["P"] < 50].shape[0]
                ]
    }

    df_flux = pd.DataFrame(fluxDict)
    print("---> Flux summary:\n", df_flux)

    # Write the df to csv
    csvName = "../txt/"+g4blVer+"/g4beamline_"+particle+"_flux_"+config+".csv" 
    df_flux.to_csv(csvName, index=False) 
    print("\n---> Written csv to", csvName)

    # Momentum plots
    ut.Plot1D(df_Z["P"], 750, 0, 750, "", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_Z2265_"+particle+"_"+config+".png", "upper right", errors=True) 
    ut.Plot1D(df_Coll_01_DetOut["P"], 750, 0, 750, r"$\mu^{-}$ entering TS collimator 1" , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_Coll_01_DetOut_"+particle+"_"+config+".png", "upper right", errors=True) 
    # ut.Plot1D(mom_Coll_05_DetOut, 500, 0, 500, r""+g4blVer+", $\mu^{-}$ out of TS collimator 5" , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_Coll_05_DetOut_"+config+particle+"_"+nEvents+"events.pdf", "upper right") 
    ut.Plot1D(df_prestop["P"], 150, 0, 150, r"$\mu^{-}$ entering stopping target" , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_prestop_"+particle+"_"+config+".png", "upper right", errors=True) 
    ut.Plot1D(df_stoppedMuons["P"], 100, 0, 100, r"Stopped $\mu^{-}$" , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_stoppedMuons_"+particle+"_"+config+".png", "upper right", errors=True) 
    # ut.Plot1DOverlay([mom_Coll_01_DetIn, mom_Coll_05_DetOut, mom_prestop, mom_stoppedMuons], 300, 0, 300, config, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_TS_ST_verboseOverlay_"+config+".pdf", ["$\mu^{-}$ before TS", "$\mu^{-}$ after TS", "$\mu^{-}$ reaching ST", "Stopped $\mu^{-}$"], "best", 100)
    ut.Plot1DOverlay([df_Z["P"], df_Coll_01_DetOut["P"], df_prestop["P"], df_stoppedMuons["P"]], 250, 0, 250, "", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_TS_ST_overlay_wZ1850_"+particle+"_"+config+".png", ["$\mu^{-}$ exiting PT", "$\mu^{-}$ entering TS", "$\mu^{-}$ reaching ST", "Stopped $\mu^{-}$"], "best")
    ut.Plot1DOverlay([df_Coll_01_DetOut["P"], df_prestop["P"], df_stoppedMuons["P"]], 250, 0, 250, "", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_TS_ST_overlay_"+particle+"_"+config+".png", ["$\mu^{-}$ entering TS", "$\mu^{-}$ reaching ST", "Stopped $\mu^{-}$"], "best")
    ut.Plot1DOverlay([df_Coll_01_DetOut_piminus["P"], df_Coll_01_DetOut["P"], df_prestop["P"], df_stoppedMuons["P"]], 250, 0, 250, "", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_TS_ST_overlay_wpi-_"+particle+"_"+config+".png", ["$\pi^{-}$ entering TS", "$\mu^{-}$ entering TS", "$\mu^{-}$ reaching ST", "Stopped $\mu^{-}$"], "best")

    df_prestop["P"] = np.sqrt( pow(df_prestop["Px"],2) + pow(df_prestop["Py"],2) + pow(df_prestop["Pz"],2) )

    return

def main():

    # RunMuonFlux("Mu2E_1e7events_fromZ1850_parallel")
    RunMuonFlux("Mu2E_1e7events_fromZ1850_parallel_noColl03")

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
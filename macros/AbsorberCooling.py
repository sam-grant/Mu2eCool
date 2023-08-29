# Analyse cooling effect of the absorber 

# External libraries
import pandas as pd
import numpy as np

# Internal libraries
import Utils as ut


# Globals

g4blVer="v3.06"

# Analyse muon flux through Mu2e, including the stopped muon yield
def RunAbsorberCooling(config):

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

    absorberName = config.split("_")[2] 
    thickness = config.split("_")[3] 
 
    # Read in TTrees
    df_BeAbsorber_DetIn = ut.TTreeToDataFrame(finName, "VirtualDetector/BeAbsorber_DetIn", ut.branchNames)
    df_BeAbsorber_DetOut = ut.TTreeToDataFrame(finName, "VirtualDetector/BeAbsorber_DetOut", ut.branchNames)

    # Add momentum column
    df_BeAbsorber_DetIn["P"] = np.sqrt( pow(df_BeAbsorber_DetIn["Px"], 2) + pow(df_BeAbsorber_DetIn["Py"], 2) + pow(df_BeAbsorber_DetIn["Pz"], 2) ) 
    df_BeAbsorber_DetOut["P"] = np.sqrt( pow(df_BeAbsorber_DetOut["Px"], 2) + pow(df_BeAbsorber_DetOut["Py"], 2) + pow(df_BeAbsorber_DetOut["Pz"], 2) ) 

    # ------ Stats ------
    # meanMom_BeAbsorber_DetIn, meanMomErr_BeAbsorber_DetIn = np.mean(df_BeAbsorber_DetIn["P"]), np.std(df_BeAbsorber_DetOut["P"])/len(df_BeAbsorber_DetOut["P"])
    # meanMom_BeAbsorber_DetOut, meanMomErr_BeAbsorber_DetOut = np.mean(df_BeAbsorber_DetOut["P"]), np.std(df_BeAbsorber_DetOut["P"])/len(df_BeAbsorber_DetOut["P"])

    # 
    coolingDict = {
        "Entering": [],
        "Exiting": [],
        "Delta": []
    }

    # Loop through particles
    particle_ = ["All", "proton", "pi+", "pi-", "mu+", "mu-"]

    i_xmax = 0 
    xmax_ = [1250, 1250, 750, 750, 275, 275] 

    for particle in particle_: 

        title = ut.GetLatexParticleName(particle)+", "+absorberName+", "+thickness

        in_ = ut.FilterParticles(df_BeAbsorber_DetIn, particle)["P"]
        out_ = ut.FilterParticles(df_BeAbsorber_DetOut, particle)["P"]

        ut.Plot1DOverlayWithStats([in_, out_], int(xmax_[i_xmax]), 0, xmax_[i_xmax], title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/AbsorberCooling/h1_Mom_InOut_"+particle+"_"+config+".png", ["Entering", "Exiting"])

        i_xmax += 1

    return

def main():

    RunAbsorberCooling("Mu2E_1e7events_Absorber0_100mm_fromZ1850_parallel")

    # RunMuonFlux("Mu2E_1e7events_fromZ1850_parallel")
    # RunMuonFlux("Mu2E_1e7events_fromZ1850_parallel_noColl03")

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
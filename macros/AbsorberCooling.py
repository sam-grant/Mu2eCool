# Analyse cooling effect of the absorber 

# External libraries
import pandas as pd
import numpy as np
from scipy import stats

# Internal libraries
import Utils as ut

# Globals
g4blVer="v3.06"

def bin(data, bin_width=1.0): 

    # Bin the data
    bin_edges = np.arange(min(data), max(data) + bin_width, bin_width)
    bin_indices = np.digitize(data, bin_edges)
    bin_counts = np.bincount(bin_indices)

    return bin_edges, bin_indices, bin_counts

def GetMode(data):

    # Bin
    bin_edges, bin_indices, bin_counts = bin(data)
    # Get mode index
    mode_bin_index = np.argmax(bin_counts)
    # Get mode count
    mode_count = bin_counts[mode_bin_index]
    # Get bin width
    bin_width = bin_edges[mode_bin_index] - bin_edges[mode_bin_index + 1]
    # Calculate the bin center corresponding to the mode
    mode_bin_center = (bin_edges[mode_bin_index] + bin_edges[mode_bin_index + 1]) / 2
    # Mode uncertainty 
    N = len(data)
    mode_bin_center_err = np.sqrt(N / (N - mode_count)) * bin_width

    return mode_bin_center, abs(mode_bin_center_err)

def RunAbsorberCooling(config, dim=""):

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

    absorberName = config.split("_")[2] 
    # absorberName = absorberName[:1]+" "+absorberName[2:]
    # thickness = config.split("_")[3] 
    # thickness = thickness[:2]+" "+thickness[2:]
 
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
    df_cooling = {
        "Particle": ["All", "proton", "pi+", "pi-", "mu+", "mu-"],
        "Entering (mean)": [],
        "Entering (mean err)": [],
        "Exiting (mean)": [],
        "Exiting (mean err)": [],
        "Delta (mean)": [],
        "Delta (mean err)": [],
        "Entering (mode)": [],
        "Entering (mode err)": [],
        "Exiting (mode)": [],
        "Exiting (mode err)": [],
        "Delta (mode)": [],
        "Delta (mode err)": []
    }

    # Loop through particles
    # particle_ = ["All", "proton", "pi+", "pi-", "mu+", "mu-"]

    i_xmax = 0 
    xmax_ = [1250, 1250, 750, 750, 275, 275] 

    for particle in df_cooling["Particle"]: 

        title = ut.GetLatexParticleName(particle)+", "+absorberName+", "+dim

        in_ = ut.FilterParticles(df_BeAbsorber_DetIn, particle)["P"]
        out_ = ut.FilterParticles(df_BeAbsorber_DetOut, particle)["P"]

        ut.Plot1DOverlayWithStats([in_, out_], int(xmax_[i_xmax]), 0, xmax_[i_xmax], title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/AbsorberCooling/h1_Mom_InOut_"+particle+"_"+config+".png", ["Entering", "Exiting"], peak=True)
        ut.Plot1DOverlayWithStats([in_, out_], 50, 0, 50, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/AbsorberCooling/h1_Mom_InOut_xmax50MeV_"+particle+"_"+config+".png", ["Entering", "Exiting"], peak=False, legPos="upper left")
        # ut.Plot1DOverlayWithStats([in_, out_], int(xmax_[i_xmax]), 120, 140, title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/AbsorberCooling/h1_Mom_InOut_"+particle+"_"+config+".png", ["Entering", "Exiting"])

        meanIn = np.mean(in_)
        meanOut = np.mean(out_)
        deltaMean = np.mean(in_) - meanOut
        rmsIn = np.std(in_)
        rmsOut = np.std(out_)
        meanErrIn = rmsIn / np.sqrt(len(in_))
        meanErrOut = rmsOut / np.sqrt(len(out_))
        deltaMeanErr = np.sqrt( pow(meanErrIn, 2) + pow(meanErrOut, 2))

        modeIn, modeInErr = GetMode(in_)
        modeOut, modeOutErr = GetMode(out_)
        deltaMode = modeIn - modeOut
        deltaModeErr = np.sqrt( pow(modeInErr, 2) + pow(modeOutErr, 2))

        # Bin the data
        # bin_edges, bin_indices, bin_counts = bin(meanIn)
        # mode_bin_index = np.argmax(bin_counts)
        # # Calculate the bin center corresponding to the mode
        # mode_bin_center = (bin_edges[mode_bin_index] + bin_edges[mode_bin_index + 1]) / 2

        # Fill results dict
        df_cooling["Entering (mean)"].append(meanIn)
        df_cooling["Entering (mean err)"].append(meanErrIn)
        df_cooling["Exiting (mean)"].append(meanOut)
        df_cooling["Exiting (mean err)"].append(meanErrOut)
        df_cooling["Delta (mean)"].append(deltaMean)
        df_cooling["Delta (mean err)"].append(deltaMeanErr) 

        df_cooling["Entering (mode)"].append(modeIn)
        df_cooling["Entering (mode err)"].append(modeInErr)
        df_cooling["Exiting (mode)"].append(modeOut)
        df_cooling["Exiting (mode err)"].append(modeOutErr)
        df_cooling["Delta (mode)"].append(deltaMode)
        df_cooling["Delta (mode err)"].append(deltaModeErr) 
        # coolingDict["Entering"].append()

        i_xmax += 1

    df_cooling = pd.DataFrame(df_cooling)

    print("---> Cooling results:\n", df_cooling)

    return

def main():

    # Need to examine what's happening below 50 MeV! Just count the bins there 

    # RunAbsorberCooling("Mu2E_1e7events_Absorber0_55mm_fromZ1850_parallel_noColl03", "L = 55 mm")
    # RunAbsorberCooling("Mu2E_1e7events_Absorber0_55mm_fromZ1850_parallel_noColl03")
    # RunAbsorberCooling("Mu2E_1e7events_Absorber1_l55mm_r85mm_fromZ1850_parallel_noColl03", "L = 55 mm, $R_{i}$ = 85 mm")
    # RunAbsorberCooling("Mu2E_1e7events_Absorber1_l55mm_r100mm_fromZ1850_parallel", "L = 55 mm, $R_{i}$ = 100 mm")
    # RunAbsorberCooling("Mu2E_1e7events_Absorber1_l55mm_r100mm_fromZ1850_parallel")
    # RunAbsorberCooling("Mu2E_1e7events_Absorber1_l55mm_r85mm_fromZ1850_parallel_noColl03", "L = 55 mm, $R_{i}$ = 85 mm")
    # RunAbsorberCooling("Mu2E_1e7events_Absorber2_55mm_fromZ1850_parallel_noColl03", "L = 55 mm")
    # RunAbsorberCooling("Mu2E_1e7events_Absorber3_l55mm_r85mm_fromZ1850_parallel", "L = 55 mm, $R_{i}$ = 85 mm")
    # RunAbsorberCooling("Mu2E_1e7events_Absorber4_l90-25mm_r85mm_fromZ1850_parallel_noColl03", "L = 90-25 mm, $R_{i}$ = 85 mm")
    RunAbsorberCooling("Mu2E_1e7events_Absorber3.1_l90mm_r85mm_fromZ1850_parallel_noColl03", "L = 90 mm, $R_{i}$ = 85 mm")
    # RunAbsorberCooling("Mu2E_1e7events_Absorber3_l55mm_r100mm_fromZ1850_parallel", "L = 55 mm, $R_{i}$ = 100 mm")
    # RunAbsorberCooling("Mu2E_1e7events_Absorber3_l55mm_r100mm_fromZ1850_parallel")

    # RunAbsorberCooling("Mu2E_1e7events_Absorber0_100mm_fromZ1850_parallel")


if __name__ == "__main__":
    main()
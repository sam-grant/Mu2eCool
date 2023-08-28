# Summarise the overall flux of particles passing through the experiment, including momentum distributions 

# External libraries
import uproot
import pandas as pd
import numpy as np
import h5py

# Internal libraries
import Utils as ut

g4blVer="v3.06"

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from matplotlib.colors import ListedColormap

def PlotGraphOverlay(df_NewParticles, particle_dict, title=None, xlabel=None, ylabel=None, fout="scatter.png", NDPI=300):

   # Create a scatter plot with error bars using NumPy arrays 

    # Create figure and axes
    fig, ax = plt.subplots()

    # TODO: generalise this 
    # Iterate through unique particle IDs
    for particle_id in df_NewParticles['PDGid'].unique():
        print( df_NewParticles['PDGid'].unique())
        particle_name = particle_dict.get(particle_id, str(particle_id))
        particle_data = df_NewParticles[df_NewParticles['PDGid'] == particle_id]
        ax.plot(particle_data['z'], range(len(particle_data)), label=particle_name)

    # Set title, xlabel, and ylabel
    ax.set_title(title, fontsize=16, pad=10)
    ax.set_xlabel(xlabel, fontsize=14, labelpad=10) 
    ax.set_ylabel(ylabel, fontsize=14, labelpad=10) 

    # Set font size of tick labels on x and y axes
    ax.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
    ax.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size

     # Scientific notation
    if ax.get_xlim()[1] > 999:
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
        ax.xaxis.offsetText.set_fontsize(14)
    if ax.get_ylim()[1] > 999:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax.yaxis.offsetText.set_fontsize(14)

    # Create the colormap
    colours = [
        (0.12156862745098039, 0.4666666666666667, 0.7058823529411765),  # Blue
        (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),  # Red
        (0.17254901960784313, 0.6274509803921569, 0.17254901960784313), # Green
        (1.0, 0.4980392156862745, 0.054901960784313725),                # Orange
        (0.5803921568627451, 0.403921568627451, 0.7411764705882353),    # Purple
        (0.09019607843137255, 0.7450980392156863, 0.8117647058823529),   # Cyan
        (0.8901960784313725, 0.4666666666666667, 0.7607843137254902),   # Pink
        (0.5490196078431373, 0.33725490196078434, 0.29411764705882354), # Brown
        (0.4980392156862745, 0.4980392156862745, 0.4980392156862745),   # Gray 
        (0.7372549019607844, 0.7411764705882353, 0.13333333333333333)  # Yellow
    ]
    cmap = ListedColormap(colours)

    # Create a legend with corresponding names from label_dict
    ax.legend(loc='best')

    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.clf()
    plt.close()

def Plot1DOverlayCustom(df, label_dict, title=None, xlabel=None, ylabel=None, fout="hist_overlay.png", NDPI=300):
    # Create figure and axes
    fig, ax = plt.subplots()

    # Create the colormap
    colours = [
        (0.12156862745098039, 0.4666666666666667, 0.7058823529411765),  # Blue
        (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),  # Red
        (0.17254901960784313, 0.6274509803921569, 0.17254901960784313), # Green
        (1.0, 0.4980392156862745, 0.054901960784313725),                # Orange
        (0.5803921568627451, 0.403921568627451, 0.7411764705882353),    # Purple
        (0.09019607843137255, 0.7450980392156863, 0.8117647058823529),   # Cyan
        (0.8901960784313725, 0.4666666666666667, 0.7607843137254902),   # Pink
        (0.5490196078431373, 0.33725490196078434, 0.29411764705882354), # Brown
        (0.4980392156862745, 0.4980392156862745, 0.4980392156862745),   # Gray 
        (0.7372549019607844, 0.7411764705882353, 0.13333333333333333)  # Yellow
    ]
    cmap = ListedColormap(colours)

    # # Iterate through unique particle IDs
    # for particle_id in df['PDGid'].unique():
    #     particle_name = label_dict.get(particle_id, str(particle_id))
    #     particle_data = df[df['PDGid'] == particle_id]['z']
    #     ax.hist(particle_data, bins=30, alpha=0.5, label=particle_name, color=cmap(particle_id % len(cmap)))

    # Iterate through unique particle IDs
    for i, particle_id in enumerate(df['PDGid'].unique()):
        particle_name = label_dict.get(particle_id, str(particle_id))
        particle_data = df[df['PDGid'] == particle_id]['z']
        # color_idx = i % len(cmap)  # Calculate the valid index for the colormap
        ax.hist(particle_data, bins=30, alpha=0.5, label=particle_name, color=cmap(i))


    # Set title, xlabel, and ylabel
    ax.set_title(title, fontsize=16, pad=10)
    ax.set_xlabel(xlabel, fontsize=14, labelpad=10) 
    ax.set_ylabel(ylabel, fontsize=14, labelpad=10) 

    # Set font size of tick labels on x and y axes
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)

    # Create a legend with corresponding names from label_dict
    ax.legend(loc='best')

    # Save the figure
    plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
    print("---> Written", fout)

    # Clear memory
    plt.clf()
    plt.close()

def Run(config, branchNames, particle): 

    # Setup input 
    finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"
 
    # Read in TTrees
    # df_NewParticles = ut.TTreeToDataFrame(finName, "NTuple/NewParticles", branchNames) # ntuples/v3.06/g4beamline_Mu2E_1e7events_wnewparticlentuple_fromZ2265_parallel.root
    df_Z = ut.TTreeToDataFrame(finName, "NTuple/Z1850", branchNames)
    df_Coll_01_DetIn = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_01_DetIn", branchNames)
    df_Coll_01_DetOut = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_01_DetOut", branchNames)
    df_Coll_03_DetIn = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_03_DetIn", branchNames)
    df_Coll_03_DetOut = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_03_DetOut", branchNames)
    df_Coll_05_DetIn = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_05_DetIn", branchNames)
    df_Coll_05_DetOut = ut.TTreeToDataFrame(finName, "VirtualDetector/Coll_05_DetOut", branchNames)
    df_prestop = ut.TTreeToDataFrame(finName, "VirtualDetector/prestop", branchNames)
    df_poststop = ut.TTreeToDataFrame(finName, "VirtualDetector/poststop", branchNames)
    df_LostInTarget = ut.TTreeToDataFrame(finName, "NTuple/LostInTarget_Ntuple", branchNames)

    # Filter upstream particles
    # df_Z = df_Z[df_Z['Pz'] > 0]
    
    # df_Coll_01_DetIn = df_Coll_01_DetIn[df_Coll_01_DetIn['Pz'] > 0]
    # df_Coll_01_DetOut = df_Coll_01_DetOut[df_Coll_01_DetOut['Pz'] > 0]
    # df_Coll_03_DetIn = df_Coll_03_DetIn[df_Coll_03_DetIn['Pz'] > 0]
    # df_Coll_03_DetOut = df_Coll_03_DetOut[df_Coll_03_DetOut['Pz'] > 0]
    # df_Coll_05_DetIn = df_Coll_05_DetIn[df_Coll_05_DetIn['Pz'] > 0]
    # df_Coll_05_DetOut = df_Coll_05_DetOut[df_Coll_05_DetOut['Pz'] > 0]
    # df_prestop = df_prestop[df_prestop['Pz'] > 0]
    # df_poststop = df_poststop[df_poststop['Pz'] > 0]
    # df_LostInTarget = df_LostInTarget[df_LostInTarget['Pz'] > 0]

    everythingAtZ = df_Z.shape[0]

    # Look at the fraction of partices as the move through the experiment

    particle_dict = {
        13: 'mu-',
        -13: 'mu+',
        211: 'pi+',
        -211: 'pi-', # ,
        2212: 'proton',
        # Add more particle entries as needed
    }

    # 
    # Plot new particles as a function of z

    # newParticleHist_ = []
    # newParticleLabel_ =  []

    # # Iterate through unique particle IDs
    # for i, particleID in enumerate(df_NewParticles['PDGid'].unique()):
    #     if particleID==2212: continue
    #     particleName = particle_dict.get(particleID, str(particleID))
    #     particleData = df_NewParticles[df_NewParticles['PDGid'] == particleID]['z']
    #     newParticleHist_.append(particleData)
    #     newParticleLabel_.append(particleName)

    # zmin = 2265 # np.min(df_NewParticles["z"])
    # zmax = 8500 # 3884.550049 # (start of TS) 8500 # np.max(df_NewParticles["z"])

    # ut.Plot1DOverlay(newParticleHist_, int(zmax-zmin), zmin, zmax, "", "z [mm]", "Counts", "../img/"+g4blVer+"/BeamFlux/h1_nParticleVsZ_Z2265_to_TS_"+config+".pdf", newParticleLabel_) 

    # return

    # Particle populations entering the TS
    ut.BarChart(df_Z['PDGid'], particle_dict, "Particles at Z1850", "", "Percentage / PDGid", fout="../img/"+g4blVer+"/BeamFlux/bar_ParticleFraction_Z1800_"+config+".pdf", percentage=False)
    ut.BarChart(df_Coll_01_DetOut['PDGid'], particle_dict, "Particles exiting TS", "", "Percentage / PDGid", fout="../img/"+g4blVer+"/BeamFlux/bar_ParticleFraction_Coll_01_DetOut_"+config+".pdf", percentage=False)

    # ut.BarChart(df_Coll_01_DetOut['PDGid'], particle_dict, title="Out of TS collimator 1", xlabel="", ylabel="Percentage / PDGid", fout='../img/v3.06/bar_ParticleFraction_df_Coll_01_DetOut.pdf', percentage=True)
    # ut.BarChart(df_Coll_03_DetIn['PDGid'], particle_dict, title="Into TS collimator 3", xlabel="", ylabel="Percentage / PDGid", fout='../img/v3.06/bar_ParticleFraction_Coll_03_DetIn.pdf', percentage=True)
    # ut.BarChart(df_Coll_03_DetOut['PDGid'], particle_dict, title="Out of TS collimator 3", xlabel="", ylabel="Percentage / PDGid", fout='../img/v3.06/bar_ParticleFraction_Coll_03_DetOut.pdf', percentage=True)
    # ut.BarChart(df_Coll_05_DetIn['PDGid'], particle_dict, title="Into TS collimator 5", xlabel="", ylabel="Percentage / PDGid", fout='../img/v3.06/bar_ParticleFraction_Coll_05_DetIn.pdf', percentage=True)
    # ut.BarChart(df_Coll_05_DetOut['PDGid'], particle_dict, title="Out of TS collimator 5", xlabel="", ylabel="Percentage / PDGid", fout='../img/v3.06/bar_ParticleFraction_Coll_05_DetOut.pdf', percentage=True)
    # ut.BarChart(df_prestop['PDGid'], particle_dict, title="Into stopping target", xlabel="", ylabel="Percentage / PDGid", fout='../img/v3.06/bar_ParticleFraction_prestop.pdf', percentage=True)

    # Filter particles
    PDGid = 0
    if particle == "mu-": PDGid = 13
    elif particle == "pi-": PDGid = -211

    if PDGid != 0: 
        df_Z = df_Z[df_Z['PDGid'] == PDGid]
        df_Coll_01_DetIn = df_Coll_01_DetIn[df_Coll_01_DetIn['PDGid'] == PDGid]
        df_Coll_01_DetOut = df_Coll_01_DetOut[df_Coll_01_DetOut['PDGid'] == PDGid]
        df_Coll_03_DetIn = df_Coll_03_DetIn[df_Coll_03_DetIn['PDGid'] == PDGid]
        df_Coll_03_DetOut = df_Coll_03_DetOut[df_Coll_03_DetOut['PDGid'] == PDGid]
        df_Coll_05_DetIn = df_Coll_05_DetIn[df_Coll_05_DetIn['PDGid'] == PDGid]
        df_Coll_05_DetOut = df_Coll_05_DetOut[df_Coll_05_DetOut['PDGid'] == PDGid]
        df_prestop = df_prestop[df_prestop['PDGid'] == PDGid]
        df_poststop = df_poststop[df_poststop['PDGid'] == PDGid]
        df_LostInTarget = df_LostInTarget[df_LostInTarget['PDGid'] == PDGid]

    # Stopped muons: muons which are present in prestop and LostInTarget
    # Add the "UniqueID" column sto df_prestop and df_LostInTarget, get the common tracks
    df_prestop['UniqueID'] = 1e6*df_prestop['EventID'] + 1e3*df_prestop['TrackID'] + df_prestop['ParentID'] 
    df_LostInTarget['UniqueID'] = 1e6*df_LostInTarget['EventID'] + 1e3*df_LostInTarget['TrackID'] + df_LostInTarget['ParentID']
    df_stoppedMuons = df_prestop[df_prestop['UniqueID'].isin(df_LostInTarget['UniqueID'])] 

    # Write out the number of partices at each point along the beamline
    particleSummary = {
        'Location': ['Everything at Z', 'Z', 'Coll_01', 'Coll_01', 'Coll_03', 'Coll_03', 'Coll_05', 'Coll_05', 'ST', 'ST', 'ST', 'ST'],
        'Type': ['At', 'At', 'Entering', 'Exiting', 'Entering', 'Exiting', 'Entering', 'Exiting', 'Entering', 'Exiting', 'Lost', 'Stopped'],
        'Count': [everythingAtZ, df_Z.shape[0],
                  df_Coll_01_DetIn.shape[0], df_Coll_01_DetOut.shape[0],
                  df_Coll_03_DetIn.shape[0], df_Coll_03_DetOut.shape[0],
                  df_Coll_05_DetIn.shape[0], df_Coll_05_DetOut.shape[0],
                  df_prestop.shape[0], df_poststop.shape[0], df_LostInTarget.shape[0],
                  df_stoppedMuons.shape[0]]
    }

    df_particleSummary = pd.DataFrame(particleSummary)

    print(df_particleSummary)

    print("\n---> Stopped muons = ",ut.Round((df_stoppedMuons.shape[0]/df_Z.shape[0])*100,3),"%")

    # Write the df to csv
    csvName = "../txt/"+g4blVer+"/g4beamline_"+particle+"_counts_"+config+".csv" 
    df_particleSummary.to_csv(csvName, index=False) 
    print("\n---> Written csv to", csvName)

    # Momentum plots 

    mom_Z2265 = np.sqrt( pow(df_Z["Px"],2) + pow(df_Z["Py"],2) + pow(df_Z["Pz"],2) )
    # mom_Coll_01_DetIn = np.sqrt( pow(df_Coll_01_DetIn["Px"],2) + pow(df_Coll_01_DetIn["Py"],2) + pow(df_Coll_01_DetIn["Pz"],2) )
    mom_Coll_01_DetOut = np.sqrt( pow(df_Coll_01_DetOut["Px"],2) + pow(df_Coll_01_DetOut["Py"],2) + pow(df_Coll_01_DetOut["Pz"],2) )
    # mom_Coll_05_DetOut = np.sqrt( pow(df_Coll_05_DetOut["Px"],2) + pow(df_Coll_05_DetOut["Py"],2) + pow(df_Coll_05_DetOut["Pz"],2) )
    mom_prestop = np.sqrt( pow(df_prestop["Px"],2) + pow(df_prestop["Py"],2) + pow(df_prestop["Pz"],2) )
    mom_stoppedMuons = np.sqrt( pow(df_stoppedMuons["Px"],2) + pow(df_stoppedMuons["Py"],2) + pow(df_stoppedMuons["Pz"],2) ) 

    # Run plots config+":\n"+r"$\mu^{-}$ at " 
    ut.Plot1D(mom_Z2265, 750, 0, 750, "", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_Z2265_"+particle+"_"+config+".png", "upper right", errors=True) 
    ut.Plot1D(mom_Coll_01_DetOut, 750, 0, 750, r"$\mu^{-}$ entering TS collimator 1" , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_Coll_01_DetOut_"+particle+"_"+config+".png", "upper right", errors=True) 
    # ut.Plot1D(mom_Coll_05_DetOut, 500, 0, 500, r""+g4blVer+", $\mu^{-}$ out of TS collimator 5" , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_Coll_05_DetOut_"+config+particle+"_"+nEvents+"events.pdf", "upper right") 
    ut.Plot1D(mom_prestop, 150, 0, 150, r"$\mu^{-}$ entering stopping target" , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_prestop_"+particle+"_"+config+".png", "upper right", errors=True) 
    ut.Plot1D(mom_stoppedMuons, 100, 0, 100, r"Stopped $\mu^{-}$" , "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_stoppedMuons_"+particle+"_"+config+".png", "upper right", errors=True) 
    # ut.Plot1DOverlay([mom_Coll_01_DetIn, mom_Coll_05_DetOut, mom_prestop, mom_stoppedMuons], 300, 0, 300, config, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_TS_ST_overlay_"+config+".pdf", ["$\mu^{-}$ before TS", "$\mu^{-}$ after TS", "$\mu^{-}$ reaching ST", "Stopped $\mu^{-}$"], "best", 100)
    ut.Plot1DOverlay([mom_Coll_01_DetOut, mom_prestop, mom_stoppedMuons], 250, 0, 250, "", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/BeamFlux/h1_mom_TS_ST_overlay_"+particle+"_"+config+".png", ["$\mu^{-}$ entering TS", "$\mu^{-}$ reaching ST", "Stopped $\mu^{-}$"], "best")

    df_prestop["P"] = np.sqrt( pow(df_prestop["Px"],2) + pow(df_prestop["Py"],2) + pow(df_prestop["Pz"],2) )


    # print("Number of muons at prestop below 50 MeV", len(mom_prestop))
    print("Number of muons at prestop below 50 MeV", df_prestop["P"][df_prestop["P"] < 50].shape[0])

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
    particle = "mu-" # mu-" # all"

    # Run("Mu2E_1e7events", branchNames, particle) 
    # Run("Mu2E_1e7events_fromZ1800_parallel", branchNames, particle) 
    # Run("Mu2E_1e7events_fromZ1800_series", branchNames, particle) 
    # Run("Mu2E_1e7events_Absorber0_fromZ1800_parallel", branchNames, particle) 
    # Run("Mu2E_1e7events_Absorber1_fromZ1800_parallel", branchNames, particle) 
    # Run("Mu2E_1e7events_fromZ2265_parallel", branchNames, particle) 
    # Run("Mu2E_1e7events_wnewparticlentuple_fromZ2265_parallel", branchNames, particle) 
    # Run("Mu2E_1e7events_Absorber0_fromZ2265_parallel", branchNames, particle) 
    # Run("Mu2E_1e7events_Absorber1_fromZ2265_parallel", branchNames, particle)  
    # Run("Mu2E_1e7events_Absorber2_fromZ2265_parallel", branchNames, particle) 

    # Run("Mu2E_1e7events_Z1850", branchNames, particle)
    # Run("Mu2E_1e7events_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_fromZ1850_parallel_noColl03", branchNames, particle)

    # Run("Mu2E_1e7events_Absorber0_100mm_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber1_100mm_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber2_100mm_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber3_100mm_fromZ1850_parallel", branchNames, particle)

    # Run("Mu2E_1e7events_Absorber0_100mm_fromZ1850_parallel_noColl03", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber1_100mm_fromZ1850_parallel_noColl03", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber2_100mm_fromZ1850_parallel_noColl03", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber3_100mm_fromZ1850_parallel_noColl03", branchNames, particle)

    # Run("Mu2E_1e7events_Absorber0_20mm_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber1_20mm_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber2_20mm_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber3_20mm_fromZ1850_parallel", branchNames, particle)

    # Run("Mu2E_1e7events_Absorber0_20mm_fromZ1850_parallel_noColl03", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber1_20mm_fromZ1850_parallel_noColl03", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber2_20mm_fromZ1850_parallel_noColl03", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber3_20mm_fromZ1850_parallel_noColl03", branchNames, particle)

    # Run("Mu2E_1e7events_Absorber0_30mm_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber1_30mm_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber2_30mm_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber3_30mm_fromZ1850_parallel", branchNames, particle)

    # Run("Mu2E_1e7events_Absorber0_30mm_fromZ1850_parallel_noColl03", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber1_30mm_fromZ1850_parallel_noColl03", branchNames, particle)
    Run("Mu2E_1e7events_Absorber2_30mm_fromZ1850_parallel_noColl03", branchNames, particle)
    Run("Mu2E_1e7events_Absorber3_30mm_fromZ1850_parallel_noColl03", branchNames, particle)

    # Run("Mu2E_1e7events_Absorber0_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber1_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber2_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber3_fromZ1850_parallel", branchNames, particle)

    # Run("Mu2E_1e7events_Absorber0_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber1_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber2_fromZ1850_parallel", branchNames, particle)
    # Run("Mu2E_1e7events_Absorber3_fromZ1850_parallel", branchNames, particle)


if __name__ == "__main__":
    main()
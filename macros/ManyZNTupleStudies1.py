# Investigate the two populations of particles seen in radius vs momentum in the PS
# Rely on a set of 11 ZNTuples spaced around the PT, at 1265:2265:100 mm 
# Code draws on BeamProfile.py 


import uproot
import pandas as pd
import csv
import matplotlib.pyplot as plt
import numpy as np

# Internal libraries
import Utils as ut

from matplotlib.patches import Rectangle

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

def FilterParticles(df, particle): 

	# Filter particles
	if particle in particleDict.values():
		PDGid = list(particleDict.keys())[list(particleDict.values()).index(particle)]
		df = df[df['PDGid'] == PDGid]

	if particle=="no_proton":

		df = df[df['PDGid'] != 2212]

	if particle=="pi-_and_mu-":

		df = df[(df['PDGid'] == -211) | (df['PDGid'] == 13)]

	if particle=="pi+-":

		df = df[(df['PDGid'] == -211) | (df['PDGid'] == 211)]

	if particle=="mu+-":

		df = df[(df['PDGid'] == 13) | (df['PDGid'] == -13)]


	return df

from matplotlib.ticker import ScalarFormatter
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap
import math

def PlotGraphOverlay(allData, title=None, xlabel=None, ylabel=None, fout="scatter.png", NDPI=300):

	# Create figure and axes
	fig, ax = plt.subplots()

	# Create a dictionary to store data for each particle type
	data_series = {particleName: [] for particleName in particleDict.values()}

	# Extract individual dictonaries from data and populate graphs
	for i, a in allData.items():
	    for label, count in a.items():
	        data_series[label].append((i, count))

    # Define the colourmap colours
	colours = [
		# (0., 0., 0.),                                                   # Black
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

	# Create the colormap
	cmap = ListedColormap(colours)

	# Create scatter plots for each particle type
	for i, (label, data) in enumerate(data_series.items()):

		if data: # Check that the list is not empty 

			# Get the axes
			z, N = zip(*data)

			# Update the labels
			if label == "proton": label = "$p$"
			elif label == "pi+": label = "$\pi^{+}$"
			elif label == "pi-": label = "$\pi^{-}$"
			elif label == "mu+": label = "$\mu^{+}$"
			elif label == "mu-": label = "$\mu^{-}$"

			# Plot
			ax.scatter(z, N, label=label, marker='o', color=cmap(i), s=4) # , linestyle="-")
			ax.plot(z, N, label=None, color=cmap(i), linestyle='-')  # Connect points with lines

	# Add a legend
	legend = ax.legend(loc="upper right", frameon=False, fontsize=14, bbox_to_anchor=(0.73, 0.99)) 
	# legend.set_bbox_to_anchor(legend.get_bbox_to_anchor().shrunk(0.8, 1))  # Adjust the width by changing the first argument

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
		# Move the exponent label off the top of the plot
		ax.yaxis.get_offset_text().set_position((-0.125, 100))
		# Rotate it vertically
		# ax.yaxis.get_offset_text().set_rotation('vertical')

	# Mark critical geometry 
	ax.axvline(x=1764.5, color='gray', linestyle='--', linewidth=1) # PT
	ax.axvline(x=3885, color='gray', linestyle='--', linewidth=1) # TS1

	plt.annotate("PT",
	             xy=(1764.5, plt.ylim()[1]),  # Position of the label
	             xytext=(10, 10),  # Offset of the label from the point
	             textcoords='offset points',  # Specify offset in points
	             va='bottom',  # Vertical alignment of the label
	             ha='right',  # Horizontal alignment of the label
	             color='gray',  # Color of the label text
	             fontsize=14,  # Font size of the label text
	             rotation='vertical')  # Rotate the label
	plt.annotate("TS1",
	             xy=(3885, plt.ylim()[1]),  
	             xytext=(10, 10),  
	             textcoords='offset points',  
	             va='bottom',  
	             ha='right', 
	             color='gray', 
	             fontsize=14,  # Font size of the label text
	             rotation='vertical')  # Rotate the label


	# Save the figure
	plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
	print("---> Written", fout)

	# Clear memory
	plt.clf()
	plt.close()

def RunZScan(config, branchNames, particle, outDir):

	# Setup input 
	finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

	# Nested dictionary for particle populations over all Z
	particleNZ = {}
	z_ = []
	theta_ = []
	thetaRMS_ = []
	Pz_ = []
	PzRMS_ = []

	alpha_ = []
	beta_ = []

	# Loop through zntuples
	for i_z in range(265, 3466, 100):

		# Store Z for graphs
		z_.append(i_z)

		# Get ntuple name
		ntupleName = "Z"+str(i_z)
		print("---> Reading", ntupleName)

		# Load TTree into DataFrame
		df = ut.TTreeToDataFrame(finName, "NTuple/"+ntupleName, branchNames) 

		# Filter upstream particles 
		# df = df[df['Pz'] > 0]

		# Dictionary for particles at this Z
		particleN = {}

	    # Loop through particleDict
		for PDGid, particleName in particleDict.items():
			# Count the occurrences of pdg_id in the DataFrame and add the count to particleN dictionary
			# if particleName=="proton": continue
			particleN[particleName] = df[df['PDGid'] == PDGid].shape[0]

		particleNZ[i_z] = particleN

		# Filter PDGids
		df = FilterParticles(df, particle)

		# Plot particle populations for each
		# ut.BarChart(df['PDGid'], particleDict, "At "+ntupleName, "", "Percentage / PDGid", fout="../img/"+g4blVer+"/RadiusVsMomentumStudy/bar_ParticleFraction_"+ntupleName+"_upstream.png", percentage=False)

		# Tranvserse momentum 
		df['PT'] = np.sqrt( pow(df["Px"],2) + pow(df["Py"],2) ) 
		# Total momentum
		df['P'] = np.sqrt( pow(df["Px"],2) + pow(df["Py"],2) + pow(df["Pz"],2) ) 
		# Radius of curvature
		df['R'] = np.sqrt( pow(df['x'],2) + pow(df['y'],2))
		# Polar (pitch) angle
		df['Theta'] = np.arctan(df['PT']/df['Pz'])
		# Azimuthal angle
		df['Phi'] = np.arctan(df['Py']/df['Px']) # np.arcsin(df['Px']/df['PT']) 

		# Vertical angle 
		df['Alpha'] = np.arcsin(df['Py']/df['P'])
		# Horizontal angle
		df['Beta'] = np.arcsin(df['Px']/df['Py'])

		# Store average momentum
		Pz_.append(np.mean(df['Pz']))
		PzRMS_.append(np.std(df['Pz']))

		# Store average pitch
		theta_.append(np.mean(df['Theta']))
		thetaRMS_.append(np.std(df['Theta']))

		# Horizontal and vertical angles
		alpha_.append(np.mean(df['Alpha']))
		beta_.append(np.mean(df['Beta']))

		title="$Z="+ntupleName.split("Z")[1]+"$ mm"


		# Make dispersion plots
		ut.Plot2D(df['P'], df['x'], 500, 0, 500, 250, -250, 250, title, "Momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_XvsMom_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
		ut.Plot2D(df['P'], df['y'], 500, 0, 500, 500, -250, 250, title, "Momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_YvsMom_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)

		ut.Plot2D(df['PT'], df['x'], 500, 0, 500, 250, -250, 250, title, "Tranverse momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_XvsMomT_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
		ut.Plot2D(df['PT'], df['y'], 500, 0, 500, 500, -250, 250, title, "Tranverse momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_YvsMomT_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)

		ut.Plot2D(df['Pz'], df['x'], 1000, -500, 500, 250, -250, 250, title, "Longitundinal momentum [MeV]", "x [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_XvsMomZ_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
		ut.Plot2D(df['Pz'], df['y'], 1000, -500, 500, 500, -250, 250, title, "Longitundinal momentum [MeV]", "y [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_YvsMomZ_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)


		# ut.Plot1D(df['Theta'], int(np.pi)*1000, -np.pi/2, np.pi/2, title, r"$\theta$ [rad]", "Counts / mrad", fout="../img/"+g4blVer+"/"+outDir+"/h1_Theta_"+ntupleName+"_"+particle+"_"+config+".png", legPos="best", stats=False, errors=False)
		# ut.Plot1D(df['Phi'], int(np.pi)*1000, -np.pi/2, np.pi/2, title, r"$\phi$ [rad]", "Counts / mrad", fout="../img/"+g4blVer+"/"+outDir+"/h1_Phi_"+ntupleName+"_"+particle+"_"+config+".png", legPos="best", stats=False, errors=False)

		# # Plot XY at each z
		ut.Plot1D(df['x'], 400, -200, 200, title, "x [mm]", "Counts / mm", "../img/"+g4blVer+"/"+outDir+"/h1_X_"+ntupleName+"_"+particle+"_"+config+".png", stats=False) # , cb=False)
		ut.Plot1D(df['y'], 400, -200, 200, title, "y [mm]", "Counts / mm", "../img/"+g4blVer+"/"+outDir+"/h1_Y_"+ntupleName+"_"+particle+"_"+config+".png", stats=False) # , cb=False)
		ut.Plot2D(df['x'], df['y'], 400, -200, 200, 400, -200, 200, title, "x [mm]", "y [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_XY_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)


		# # Plot radius vs. momentum at each z
		ut.Plot2D(df['P'], df['R'], 500, 0, 500, 200, 0, 200, title, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RVsMom_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
		ut.Plot2D(df['PT'], df['R'], 500, 0, 500, 200, 0, 200, title, "Tranvserse momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RVsMomT_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
		ut.Plot2D(df['Pz'], df['R'], 1000, -500, 500, 200, 0, 200, title, "Longitundinal momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RVsMomZ_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
		# # ut.Plot2D(df['P'], df['R'], 750, 0, 750, 200, 0, 200, title, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsMom_"+ntupleName+"_"+particle+"_"+config+"_long.png", cb=False)
		# # Plot radius vs. longtidunal momentum at each z
		# ut.Plot2D(df['Pz'], df['R'], 1000, -500, 500, 200, 0, 200, title, "$P_{z}$ [MeV]", "Radius [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsPz_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
		# # ut.Plot2D(df['Pz'], df['R'], 750, 0, 750, 200, 0, 200, particle+" at "+ntupleName, "Pz [MeV]", "Radius [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsPz_"+ntupleName+"_"+particle+"_"+config+"_long.png", cb=False)
		# # Plot radius vs. transverse momentum at each z
		# ut.Plot2D(df['PT'], df['R'], 500, 0, 500, 200, 0, 200, title, "$P_{T}$ [MeV]", "Radius [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsPT_"+ntupleName+"_"+particle+"_"+config+".png")
		
		# Mom vs polar angle
		# ut.Plot2D(df['Pz'], df['Theta'], 1000, -500, 500, int(np.pi)*1000, -np.pi/2, np.pi/2, title, "$P_{z}$ [MeV]", r"$\theta$ [rad]", "../img/"+g4blVer+"/"+outDir+"/h2_ThetaVsPz_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
		# ut.Plot2D(df['PT'], df['Theta'], 500, 0, 500, int(np.pi)*1000, -np.pi/2, np.pi/2, title, "$P_{T}$ [MeV]", r"$\theta$ [rad]", "../img/"+g4blVer+"/"+outDir+"/h2_ThetaVsPT_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
		# ut.Plot2D(df['P'], df['Theta'], 500, 0, 500, int(np.pi)*1000, -np.pi/2, np.pi/2, title, "Momentum [MeV]", r"$\theta$ [rad]", "../img/"+g4blVer+"/"+outDir+"/h2_ThetaVsMom_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)

		# Rad vs polar angle
		# ut.Plot2D(df['R'], df['Theta'], 200, 0, 200, int(np.pi)*1000, -np.pi/2, np.pi/2, title, "Radius [mm]", r"$\theta$ [rad]", "../img/"+g4blVer+"/"+outDir+"/h2_ThetaVsRad_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)

		# ut.Plot2D(df['PT'], df['R'], 750, 0, 750, 200, 0, 200, particle+" at "+ntupleName, "Pz [MeV]", "Radius [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsPT_"+ntupleName+"_"+particle+"_"+config+"_long.png", cb=False)
		# Plot XY weighted with momentum at each z
		ut.Plot3D(df['x'], df['y'], df['P'], 80, -200, 200, 80, -200, 200, 500, title, "x [mm]", "y [mm]", "Momentum [MeV]", "../img/"+g4blVer+"/"+outDir+"/h3_XYMom_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)

	# Plot particle population as a function of z
	PlotGraphOverlay(particleNZ, xlabel="z [mm]", ylabel="N / 100 mm", fout="../img/"+g4blVer+"/"+outDir+"/gr_NvsZ_"+config+".png")

	# ut.PlotGraph(x=z_, y=Pz_, xerr=[], yerr=[], xlabel="z [mm]", ylabel=r"$\langle P_{z} \rangle$ [MeV]", fout="../img/"+g4blVer+"/"+outDir+"/gr_AvgPzVsZ_"+particle+"_"+config+".png")
	# ut.PlotGraph(x=z_[16:], y=theta_[16:], xerr=[], yerr=[], xlabel="z [mm]", ylabel=r"$\langle \theta \rangle$ [rad]", fout="../img/"+g4blVer+"/"+outDir+"/gr_AvgThetaVsZ_"+particle+"_"+config+".png")

	# ut.PlotGraph(x=z_, y=[x * 1000 for x in alpha_], xerr=[], yerr=[], title=particle, xlabel="z [mm]", ylabel=r"$\langle \alpha \rangle$ [mrad]", fout="../img/"+g4blVer+"/"+outDir+"/gr_AvgAlphaVsZ_"+particle+"_"+config+".png")
	# ut.PlotGraph(x=z_, y=[x * 1000 for x in beta_], xerr=[], yerr=[], title=particle, xlabel="z [mm]", ylabel=r"$\langle \beta \rangle$ [mrad]", fout="../img/"+g4blVer+"/"+outDir+"/gr_AvgBetaVsZ_"+particle+"_"+config+".png")

	return


# Cut left and right populations at Z2265
def RunInitParam(config, branchNames, particle, outDir):

	# Setup input 
	finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

	# Get ntuple name
	ntupleName = "Z2265" 
	print("---> Reading", ntupleName)

	# Load TTree into DataFrame
	df = ut.TTreeToDataFrame(finName, "NTuple/"+ntupleName, branchNames) 

	# Filter PDGids
	df = FilterParticles(df, particle)

	# Add some useful things to DataFrame:
	# Tranvserse momentum 
	df['PT'] = np.sqrt( pow(df["Px"],2) + pow(df["Py"],2) ) 
	# Total momentum
	df['P'] = np.sqrt( pow(df["Px"],2) + pow(df["Py"],2) + pow(df["Pz"],2) ) 
	# Radius of curvature
	df['R'] = np.sqrt( pow(df['x'],2) + pow(df['y'],2))
	# Polar (pitch) angle
	df['Theta'] = np.arctan(df['PT']/df['Pz'])
	# Azimuthal angle
	df['Phi'] = np.arctan(df['Py']/df['Px'])
	# Initial radius
	df['InitR'] = np.sqrt( pow(df['InitX'],2) + pow(df['InitY'],2))



	# Cut at P_z >< 100 MeV and plot R vs P 
	ut.Plot2D(df['P'], df['R'], 250, 0, 250, 200, 0, 200, particle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsMom_"+ntupleName+"_"+particle+"_"+config+".png")
	ut.Plot2D(df['P'][df['Pz'] > 100], df['R'][df['Pz'] > 100], 250, 0, 250, 200, 0, 200, particle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsMom_gt100MeVPz_"+ntupleName+"_"+particle+"_"+config+".png")
	ut.Plot2D(df['P'][df['Pz'] < 100], df['R'][df['Pz'] < 100], 250, 0, 250, 200, 0, 200, particle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsMom_t100MeVPz_"+ntupleName+"_"+particle+"_"+config+".png")

	# Cut dataframe in two according to rad=2*mom-150 at Z2265
	# # Define the function y = mx + c
	m = 2 # gradient
	b = 75 # x-intercept
	c = -b*m # y-intercept
	# x = (rad - c) / m
	df_left = df[df['P'] < (df['R'] - c)/m]
	df_right = df[df['P'] > (df['R'] - c)/m]

	# Plot R vs p for each
	# Can add a line later if you like, we already have that plot from BeamProfile.py though. 
	ut.Plot2D(df_left['P'], df_left['R'], 250, 0, 250, 200, 0, 200, "Left, "+particle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsMom_cutLeft_"+ntupleName+"_"+particle+"_"+config+".png")
	ut.Plot2D(df_right['P'], df_right['R'], 250, 0, 250, 200, 0, 200, "Right, "+particle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsMom_cutRight_"+ntupleName+"_"+particle+"_"+config+".png")

	# Plot Pz for each
	ut.Plot1D(df_left['Pz'], 750, -250, 500, "Left, "+particle, "$P_{z}$ [MeV]", "Counts / MeV", "../img/"+g4blVer+"/"+outDir+"/h1_Pz_cutLeft_"+ntupleName+"_"+particle+"_"+config+".png") 
	ut.Plot1D(df_right['Pz'], 750, -250, 500, "Right, "+particle, "$P_{z}$ [MeV]", "Counts / MeV", "../img/"+g4blVer+"/"+outDir+"/h1_Pz_cutRight_"+ntupleName+"_"+particle+"_"+config+".png")

	# Plot PT for each
	ut.Plot1D(df_left['PT'], 250, 0, 250, "Left, "+particle, "$P_{T}$ [MeV]", "Counts / MeV", "../img/"+g4blVer+"/"+outDir+"/h1_PT_cutLeft_"+ntupleName+"_"+particle+"_"+config+".png") # , "upper left")
	ut.Plot1D(df_right['PT'], 250, 0, 250,  "Right, "+particle, "$P_{T}$ [MeV]", "Counts / MeV", "../img/"+g4blVer+"/"+outDir+"/h1_PT_cutRight_"+ntupleName+"_"+particle+"_"+config+".png") # , "upper left")

	# Plot InitZ for each
	ut.Plot1D(df_left['InitZ'], 175, 1000, 2750, "Left, "+particle, "Initial z [mm]", "Counts / 10 mm", "../img/"+g4blVer+"/"+outDir+"/h1_InitZ_cutLeft_"+ntupleName+"_"+particle+"_"+config+".png")
	ut.Plot1D(df_right['InitZ'], 175, 1000, 2750, "Right, "+particle, "Initial z [mm]", "Counts / 10 mm", "../img/"+g4blVer+"/"+outDir+"/h1_InitZ_cutRight_"+ntupleName+"_"+particle+"_"+config+".png")

	# Plot InitR for each
	ut.Plot1D(df_left['InitR'], 200, 0, 200, "Left, "+particle, "Initial R [mm]", "Counts / mm", "../img/"+g4blVer+"/"+outDir+"/h1_InitR_cutLeft_"+ntupleName+"_"+particle+"_"+config+".png")
	ut.Plot1D(df_right['InitR'], 200, 0, 200, "Right, "+particle, "Initial R [mm]", "Counts / mm", "../img/"+g4blVer+"/"+outDir+"/h1_InitR_cutRight_"+ntupleName+"_"+particle+"_"+config+".png")

	# Plot pitch for each
	ut.Plot1D(df_left['Theta'], int(np.pi)*100, 0, np.pi/2, "Left, "+particle, r"$\theta$ [rad]", "Counts / 10 mrad", "../img/"+g4blVer+"/"+outDir+"/h1_Theta_cutLeft_"+ntupleName+"_"+particle+"_"+config+".png") # , "upper left")
	ut.Plot1D(df_right['Theta'], int(np.pi)*100, 0, np.pi/2,  "Right, "+particle, r"$\theta$ [rad]", "Counts / 10 mrad", "../img/"+g4blVer+"/"+outDir+"/h1_Theta_cutRight_"+ntupleName+"_"+particle+"_"+config+".png") # , "upper left")

	# Cut at 100 MeV and plot pitch for each
	ut.Plot1D(df_left['Theta'][df_left['Pz'] > 100], int(np.pi)*100, 0, np.pi/2, "Left, $P_{z}>100$ MeV, "+particle, r"$\theta$ [rad]", "Counts / 10 mrad", "../img/"+g4blVer+"/"+outDir+"/h1_Theta_cutLeft_gt100MeVPz_"+ntupleName+"_"+particle+"_"+config+".png") # , "upper left")
	ut.Plot1D(df_right['Theta'][df_right['Pz'] > 100], int(np.pi)*100, 0, np.pi/2,  "Right, $P_{z}>100$ MeV, "+particle, r"$\theta$ [rad]", "Counts / 10 mrad", "../img/"+g4blVer+"/"+outDir+"/h1_Theta_cutRight_gt100MeVPz_"+ntupleName+"_"+particle+"_"+config+".png") # , "upper left")

	# Mid monemtum low radius population 
	# Cut between 75-150 MeV and below 30 mm 
	filtered_data = df[(df['P'] > 75) & (df['P'] < 150) & (df['R'] < 30)]
	ut.Plot1D(filtered_data['Theta'], int(np.pi)*100, 0, np.pi/2, "$75>P_{z}>125$ MeV, $R<30$ mm, "+particle, r"$\theta$ [rad]", "Counts / 10 mrad", "../img/"+g4blVer+"/"+outDir+"/h1_Theta_midModLowRad_"+ntupleName+"_"+particle+"_"+config+".png") # , "upper left")
	ut.Plot2D(filtered_data['P'], filtered_data['R'], 250, 0, 250, 200, 0, 200, particle, "Momentum [MeV]", "Radius [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsMom_cutRight_midModLowRad_"+ntupleName+"_"+particle+"_"+config+".png")


	return

import math


# Calculate Theta while handling cases outside -1 to 1
def adjust_angle(angle, cos_value, Bx, By):
    # Calculate the angle using arccos
    arccos_angle = np.arccos(cos_value)
    
    # Determine the quadrant based on the signs of Bx and By
    if Bx >= 0 and By >= 0:  # Quadrant I
        return arccos_angle
    elif Bx < 0 and By >= 0:  # Quadrant II
        return np.pi - arccos_angle
    elif Bx < 0 and By < 0:   # Quadrant III
        return np.pi + arccos_angle
    else:                      # Quadrant IV
        return 2 * np.pi - arccos_angle

def RunAnaRadius(config, branchNames, particle, outDir):

	# Setup input 
	finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

	# Loop through zntuples
	for i_z in range(265, 3466, 100):

		# Get ntuple name
		ntupleName = "Z"+str(i_z)
		print("---> Reading", ntupleName)

		# Load TTree into DataFrame
		df = ut.TTreeToDataFrame(finName, "NTuple/"+ntupleName, branchNames) 

		# Filter PDGids
		df = FilterParticles(df, particle)

		# Scan momentum bins and plot R 
		# R = p/qBsin(theta) * gamma. 
		# p is lab frame momentum, if it's relativistic then there's a factor of gamma. 
		# q = e = +-1
		# E_k=E-E_0=(gamma-1)*m_0*c^2 --> gamma - 1 = E_k / m_0 * c^2 --> gamma = E_k/m_0*c^2 + 1 --> gamma = E_k/m_0 + 1 (NL)
		# E_k = E - E_0 = sqrt(p^2 + m_0^2) - m_0

		# Constants
		m_0 = 139.570 # pi+- rest mass in MeV/c^2
		e = 1.602e-19 # C
		df["Sign"] = df["PDGid"].apply(lambda x: math.copysign(1, x))
		df["Charge"] = df["Sign"] * e
		c = 299792458 # m/s

		# Radius of curvature (simulated)
		df['R'] = np.sqrt( pow(df['x'],2) + pow(df['y'],2))
		# Total momentum
		df["PT"] = np.sqrt( pow(df["Px"],2) + pow(df["Py"],2) ) 
		# Total momentum
		df["P"] = np.sqrt( pow(df["Px"],2) + pow(df["Py"],2) + pow(df["Pz"],2) ) 
		
		# df["P"] = df["P"]
		# Total field
		df["B"] = np.sqrt( pow(df["Bx"],2) + pow(df["By"],2) + pow(df["Bz"],2) ) 
		# Kinetic energy 
		df["Ek"] = np.sqrt(pow(df["P"], 2) + pow(m_0, 2)) - m_0
		# Gamma
		df["gamma"] = df["Ek"]/m_0 + 1 
		# Theta
		# df["BdotP"] = np.dot(df["B"], df["P"])
		df["BdotP"] = df["Bx"] * df["Px"] + df["By"] * df["Py"] + df["Bz"] * df["Pz"]
		# Calculate magnitudes of P and B vectors
		df["Pmag"] = np.linalg.norm(df[["Px", "Py", "Pz"]], axis=1)
		df["Bmag"] = np.linalg.norm(df[["Bx", "By", "Bz"]], axis=1)
		df["cosTheta"] = df["BdotP"] / (df["Pmag"] * df["Bmag"])
		# print("hello")
		# df["Theta"] = np.arccos(df["cosTheta"] ) 
		df["Theta"] = np.vectorize(adjust_angle)(df["cosTheta"], df["cosTheta"], df["Bx"], df["By"])
		# print("bye")
		# Calculate R in mm (need to convert MeV to kgm/s as well)
		
		df["Rana"] =  ( df["P"] * df["gamma"] ) / ( df["Charge"] * df["B"] * np.sin(df["Theta"]) ) * (1e6 * e / c) * 1e3 
		df["Rana"] = df["Rana"].abs()

		# print(df["Theta"])
		# Now histogram 
		title="$Z="+ntupleName.split("Z")[1]+"$ mm"

		ut.Plot2D(df['P'], df['R'], 250, 0, 250, 200, 0, 200, title, "Momentum [MeV]", "Radius (simulated) [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsMom_Sim_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
		ut.Plot2D(df['P'], df['Rana'], 250, 0, 250, 200, 0, 200, title, "Momentum [MeV]", "Radius (calculated) [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsMom_Ana_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)

		ut.Plot2D(df['PT'], df['R'], 250, 0, 250, 200, 0, 200, title, "$P_{T}$ [MeV]", "Radius (simulated) [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsPT_Sim_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
		ut.Plot2D(df['PT'], df['Rana'], 250, 0, 250, 200, 0, 200, title, "$P_{T}$ [MeV]", "Radius (calculated) [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsPT_Ana_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)

		ut.Plot2D(df['Pz'], df['R'], 500, -250, 250, 200, 0, 200, title, "$P_{z}$ [MeV]", "Radius (simulated) [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsPz_Sim_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)
		ut.Plot2D(df['Pz'], df['Rana'], 500, -250, 250, 200, 0, 200, title, "$P_{z}$ [MeV]", "Radius (calculated) [mm]", "../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsPz_Ana_"+ntupleName+"_"+particle+"_"+config+".png", cb=False)

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
		"Bx",
		"By",
		"Bz",
		"InitX",
		"InitY",
		"InitZ"
		# extend as needed
		]  

	particle = "mu+-" # "mu+-" # "pi+-" # mu+-" # pi+-" # mu+-" # all" # "pi+-" # "mu+-" # "no_proton"

	config="Mu2E_1e6events_ManyZNTuple1"
	outDir="DispersionAndBeamSpot" # AnaRadius" # "RadiusVsMomentumStudy"  # "AnaRadius" # "RadiusVsMomentumStudy" 

	# RunZScan(config, branchNames, particle, outDir) 

	# RunInitParam(config, branchNames, particle, outDir) 

	# RunAnaRadius(config, branchNames, particle, outDir)


if __name__ == "__main__":
	main()

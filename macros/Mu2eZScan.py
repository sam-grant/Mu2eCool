# Investigate the two populations of particles seen in radius vs momentum in the PS
# Rely on a set of 11 ZNTuples spaced around the PT, at 1265:2265:100 mm 
# Code draws on BeamProfile.py 

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Internal libraries
import Utils as ut

# from matplotlib.patches import Rectangle

# Globals
g4blVer="v3.06"

from matplotlib.ticker import ScalarFormatter
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap
# import math

def PlotGraphOverlay(allData, title=None, xlabel=None, ylabel=None, fout="scatter.png", NDPI=300, includeBlack=False):

	# Create figure and axes
	fig, ax = plt.subplots()

	# Create a dictionary to store data for each particle type
	data_series = {particleName: [] for particleName in ut.particleDict.values()}

	# Extract individual dictonaries from data and populate graphs
	for i, a in allData.items():
	    for label, count in a.items():
	        data_series[label].append((i, count))

    # Define the colourmap colours
	colours = [
		(0., 0., 0.),                                                   # Black
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
			latexLabel = ut.GetLatexParticleName(label)

			# if label[0]=="e": 
			# 	latexLabel += " >10 MeV"
			# 	print(latexLabel)


			colour = cmap(i+1)
			if includeBlack: colour = cmap(i)


			non_zero_indices = [i for i, n in enumerate(N) if n > 0]

			if non_zero_indices:  # Check that there are non-zero indices

			    z_non_zero = [z[i] for i in non_zero_indices]
			    N_non_zero = [N[i] for i in non_zero_indices]

			    # Plot non-zero points
			    ax.scatter(z_non_zero, N_non_zero, label=latexLabel, marker='o', color=colour, s=4)
			    ax.plot(z_non_zero, N_non_zero, label=None, color=colour, linestyle='-')

			# i_max = 0

			# for n in N:
			# 	if n > 0: i_max += 1
			# 	else: continue

			# # while n in N < 0:

			# # Non-zero points
			# # z = z[N]

			# z = z[:i_max]
			# N = N[:i_max]

			# # Plot
			# # non_zero_indices = N != 0
			# ax.scatter(z, N, label=label, marker='o', color=colour, s=4) # , linestyle="-")
			# # non_zero_indices = N != 0
			# ax.plot(z, N, label=None, color=colour, linestyle='-')  # Connect points with lines
			# # ax.scatter(z[non_zero_indices], N[non_zero_indices], label=label, marker='o', color=colour, s=4) # , linestyle="-")
			# # ax.plot(z[non_zero_indices], N[non_zero_indices], label=None, color=colour, linestyle='-')  # Connect points with lines


	# Add a legend
	# legend = ax.legend(loc="upper left", frameon=False, fontsize=14, bbox_to_anchor=(0.73, 0.99)) 
	# legend = ax.legend(frameon=False, fontsize=14, bbox_to_anchor=(0.73, 0.99)) 
	# legend.set_bbox_to_anchor(legend.get_bbox_to_anchor().shrunk(0.8, 1))  # Adjust the width by changing the first argument
	# Place the legend outside of the plot on the right side
	# legend = ax.legend(loc="upper left", frameon=False, fontsize=14, bbox_to_anchor=(0.0, 1)) # 1.02, 1))
	# plt.subplots_adjust(left=0.2)  # Adjust the right margin to make space for the legend
	# # Place the legend outside of the plot on the right side and center it horizontally
	legend = ax.legend(loc="center left", frameon=False, fontsize=14, bbox_to_anchor=(1, 0.5))
	plt.subplots_adjust(right=0.8)  # Adjust the right margin to make space for the legend


	ax.set_xlim( (1764.5-500)*1e-3, (13800+500)*1e-3)

	# Set title, xlabel, and ylabel
	ax.set_title(title, fontsize=16, pad=10)
	ax.set_xlabel(xlabel, fontsize=14, labelpad=10) 
	ax.set_ylabel(ylabel, fontsize=14, labelpad=10) 

	# Set font size of tick labels on x and y axes
	ax.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
	ax.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size

	# Scientific notation
	if ax.get_xlim()[1] > 9999:
		ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
		ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
		ax.xaxis.offsetText.set_fontsize(14)
	if ax.get_ylim()[1] > 9999:
		ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
		ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
		ax.yaxis.offsetText.set_fontsize(14)
		# Move the exponent label off the top of the plot
		ax.yaxis.get_offset_text().set_position((-0.125, 100))
		# Rotate it vertically
		# ax.yaxis.get_offset_text().set_rotation('vertical')

	# Mark critical geometry 
	ax.axvline(x=1764.5*1e-3, color='gray', linestyle='--', linewidth=1) # PT
	ax.axvline(x=3885*1e-3, color='gray', linestyle='--', linewidth=1) # TS1
	ax.axvline(x=7929*1e-3, color='gray', linestyle='--', linewidth=1) # TS3
	ax.axvline(x=11359*1e-3, color='gray', linestyle='--', linewidth=1) # TS5
	ax.axvline(x=13800*1e-3, color='gray', linestyle='--', linewidth=1) # ST
	# ax.axvline(x=17964, color='gray', linestyle='--', linewidth=1) # Tracker
	# ax.axvline(x=20394, color='gray', linestyle='--', linewidth=1) # Calo

	plt.annotate("PT",
	             xy=(1764.5*1e-3, plt.ylim()[1]),  # Position of the label
	             xytext=(10, 10),  # Offset of the label from the point
	             textcoords='offset points',  # Specify offset in points
	             va='bottom',  # Vertical alignment of the label
	             ha='right',  # Horizontal alignment of the label
	             color='gray',  # Color of the label text
	             fontsize=14,  # Font size of the label text
	             rotation='vertical')  # Rotate the label
	plt.annotate("TS1",
	             xy=(3885*1e-3, plt.ylim()[1]),  
	             xytext=(10, 10),  
	             textcoords='offset points',  
	             va='bottom',  
	             ha='right', 
	             color='gray', 
	             fontsize=14,  # Font size of the label text
	             rotation='vertical')  # Rotate the label
	plt.annotate("TS3",
	             xy=(7929*1e-3, plt.ylim()[1]),  
	             xytext=(10, 10),  
	             textcoords='offset points',  
	             va='bottom',  
	             ha='right', 
	             color='gray', 
	             fontsize=14,  # Font size of the label text
	             rotation='vertical')  # Rotate the label
	plt.annotate("TS5",
	             xy=(11359*1e-3, plt.ylim()[1]),  
	             xytext=(10, 10),  
	             textcoords='offset points',  
	             va='bottom',  
	             ha='right', 
	             color='gray', 
	             fontsize=14,  # Font size of the label text
	             rotation='vertical')  # Rotate the label
	plt.annotate("ST",
	             xy=(13800*1e-3, plt.ylim()[1]),  
	             xytext=(10, 10),  
	             textcoords='offset points',  
	             va='bottom',  
	             ha='right', 
	             color='gray', 
	             fontsize=14,  # Font size of the label text
	             rotation='vertical')  # Rotate the label
	# ----- Add tracker and calo if needed ----- 
	# plt.annotate("Tracker",
	#              xy=(17964, plt.ylim()[1]),  
	#              xytext=(10, 10),  
	#              textcoords='offset points',  
	#              va='bottom',  
	#              ha='right', 
	#              color='gray', 
	#              fontsize=14,  # Font size of the label text
	#              rotation='vertical')  # Rotate the label
	# plt.annotate("Calo",
	#              xy=(20394, plt.ylim()[1]),  
	#              xytext=(10, 10),  
	#              textcoords='offset points',  
	#              va='bottom',  
	#              ha='right', 
	#              color='gray', 
	#              fontsize=14,  # Font size of the label text
	#              rotation='vertical')  # Rotate the label



	# Save the figure
	plt.savefig(fout, dpi=NDPI, bbox_inches="tight")
	print("---> Written", fout)

	# Clear memory
	plt.clf()
	plt.close()


def PlotGraphOverlayPS(allData, title=None, xlabel=None, ylabel=None, fout="scatter.png", NDPI=300):

	# Create figure and axes
	fig, ax = plt.subplots()

	print(data_series)

	# Create a dictionary to store data for each particle type
	data_series = {particleName: [] for particleName in ut.particleDict.values()}

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

			label = ut.GetLatexParticleName(label)

			# Plot
			ax.scatter(z, N, label=label, marker='o', color=cmap(i), s=4) # , linestyle="-")
			ax.plot(z, N, label=None, color=cmap(i), linestyle='-')  # Connect points with lines

	# Add a legend
	legend = ax.legend(loc="best", frameon=False, fontsize=14) # , bbox_to_anchor=(0.73, 0.99)) 
	# legend.set_bbox_to_anchor(legend.get_bbox_to_anchor().shrunk(0.8, 1))  # Adjust the width by changing the first argument

	# Set title, xlabel, and ylabel
	ax.set_title(title, fontsize=16, pad=10)
	ax.set_xlabel(xlabel, fontsize=14, labelpad=10) 
	ax.set_ylabel(ylabel, fontsize=14, labelpad=10) 

	# Set font size of tick labels on x and y axes
	ax.tick_params(axis='x', labelsize=14)  # Set x-axis tick label font size
	ax.tick_params(axis='y', labelsize=14)  # Set y-axis tick label font size

	# ax.set_ylim(0.0, 2.5e4)

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

def RunMu2eZScan(config, proton=True): # , branchNames, particle): 

	# Setup input 
	finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

	# Nested dictionary for particle populations over all Z
	particleNZ = {}

	# Loop through zntuples
	for i_z in range(1765+500, 13266, 500):
	# for i_z in range(1850, 13350, 500):

		# Get ntuple name
		ntupleName = "Z"+str(i_z)
		print("---> Reading", ntupleName)

		# Load TTree into DataFrame
		df = ut.TTreeToDataFrame(finName, "NTuple/"+ntupleName, ut.branchNames) 

		# Filter upstream particles 
		# df = df[df['Pz'] > 0]

		# Filter PDGids
		# df = ut.FilterParticles(df, particle)

		# Dictionary for particles at this Z
		particleN = {}

	    # Loop through particleDict
		for PDGid, particleName in ut.particleDict.items():
			# Count the occurrences of pdg_id in the DataFrame and add the count to particleN dictionary
			if not proton and particleName=="proton": continue
			if particleName[:4] == "kaon": continue
			# if particleName[0] == "e":
			# 	df = df[np.sqrt(pow(df["Px"], 2) + pow(df["Py"], 2) + pow(df["Px"], 2)) > 10]
				# particleName += " >10 MeV"

			# print(particleName)

			N = df[df['PDGid'] == PDGid].shape[0]

			
			particleN[particleName] = df[df['PDGid'] == PDGid].shape[0]

		particleNZ[i_z*1e-3] = particleN

	# Plot particle population as a function of z
	PlotGraphOverlay(particleNZ, xlabel="z-position [m]", ylabel="Counts / 500 mm", fout="../img/"+g4blVer+"/Mu2eZScan/gr_NvsZ_"+config+".png")

	return

def RunMu2eZScanPS(config, proton=True): # , branchNames, particle): 

	# Setup input 
	finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

	title = config.split("_")[2]

	# Nested dictionary for particle populations over all Z
	particleNZ = {}

	# Loop through zntuples
	# for i_z in range(2265, 13766, 500):
	for i_z in range(1850, 4350, 100):

		# Get ntuple name
		ntupleName = "Z"+str(i_z)
		print("---> Reading", ntupleName)

		# Load TTree into DataFrame
		df = ut.TTreeToDataFrame(finName, "NTuple/"+ntupleName, ut.branchNames) 

		# df = df[df["P"] < 50]

		# Filter PDGids
		# df = ut.FilterParticles(df, particle)

		# Dictionary for particles at this Z
		particleN = {}

	    # Loop through particleDict
		for PDGid, particleName in ut.particleDict.items():

			# Count the occurrences of pdg_id in the DataFrame and add the count to particleN dictionary
			if not proton and particleName=="proton": continue

			# if particleName[:4] == "kaon": 
			# 	continue
				# particleName = "K(PDGid == 321 || PDGid

			particleN[particleName] = df[df['PDGid'] == PDGid].shape[0]

			# Include some beam profile plots 
			# Something is wrong here, I don't think it's filtering correctly
			# I thought I fixed this... 

			# if particleName == "pi-":

		particleNZ[i_z] = particleN

		# Look at cold pions
		df = ut.FilterParticles(df, "pi-")

		# Momentum and radius 
		df["P"] = np.sqrt( pow(df["Px"], 2) + pow(df["Py"], 2) + pow(df["Pz"], 2) )
		df["R"] = np.sqrt( pow(df["x"], 2) + pow(df["y"], 2) ) 

		ut.GetLatexParticleName("pi-")+", "+"Z = "+str(i_z)+" mm"+", "+title

		ut.Plot1D(df["P"], 300, 0, 300, ut.GetLatexParticleName("pi-")+", "+"Z = "+str(i_z)+" mm"+", "+title, "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/Mu2eZScan/h1_Mom_"+ntupleName+"_"+particleName+"_"+config+".png")
		ut.Plot1D(df[df["P"] < 50]["P"], 300, 0, 300, ut.GetLatexParticleName("pi-")+", "+"Z = "+str(i_z)+" mm"+", "+title+", <50 MeV", "Momentum [MeV]", "Counts / MeV", "../img/"+g4blVer+"/Mu2eZScan/h1_Mom_below50MeV_"+ntupleName+"_"+particleName+"_"+config+".png")
		ut.Plot1D(df["R"], 250, 0, 250, ut.GetLatexParticleName("pi-")+", "+"Z = "+str(i_z)+" mm"+", "+title, "Radius [mm]", "Counts / mm", "../img/"+g4blVer+"/Mu2eZScan/h1_R_"+ntupleName+"_"+particleName+"_"+config+".png") 
		ut.Plot1D(df[df["P"] < 50]["R"], 250, 0, 250, ut.GetLatexParticleName("pi-")+", "+"Z = "+str(i_z)+" mm"+", "+title+", <50 MeV", "Radius [mm]", "Counts / mm", "../img/"+g4blVer+"/Mu2eZScan/h1_R_below50MeV_"+ntupleName+"_"+particleName+"_"+config+".png")  
		

	# Plot particle population as a function of z
	PlotGraphOverlayPS(particleNZ, title=title, xlabel="z [mm]", ylabel="N / 100 mm", fout="../img/"+g4blVer+"/Mu2eZScan/gr_NvsZ_below50MeV_"+config+"_PS.png") 

	df_particleNZ = pd.DataFrame(particleNZ)
	print("---> Particle N(z) summary:\n", df_particleNZ)

	# Write the df to csv
	csvName = "../txt/"+g4blVer+"/g4beamline_NvsZ_below50MeV_"+config+"_PS.csv" 
	df_particleNZ.to_csv(csvName, index=True) 
	print("\n---> Written csv to", csvName)


	return

def main():

# 	Run("Mu2E_1e7events_ManyZNTuple2_fromZ2265_parallel") 
 	# Run("Mu2E_1e7events_Absorber3.1_l90mm_r85mm_ManyZNTuple3_fromZ1850_parallel_noColl03", proton=False) 
 	# RunMu2eZScanPS("Mu2E_1e7events_Absorber3.1_l90mm_r85mm_ManyZNTuple3_fromZ1850_parallel_noColl03", proton=False) 
	#" Mu2E_1e7events_Absorber3.1_ManyZNTuple3_fromZ1850_parallel_noColl03
 	# RunMu2eZScanPS("Mu2E_1e7events_NoAbsorber_ManyZNTuple3_fromZ1850_parallel_noColl03", proton=False) 
 	# RunMu2eZScanPS("Mu2E_1e7events_Absorber3.1_ManyZNTuple3_fromZ1850_parallel_noColl_noPbar", proton=False) 
 	# RunMu2eZScan("Mu2E_1e7events_Absorber3.1_ManyZNTuple3_fromZ1850_parallel_noColl03", proton=False) 
 	# RunMu2eZScan("Mu2E_1e7events_Absorber3_ManyZNTuple3_fromZ1850_parallel_noColl03", proton=False) 
 	RunMu2eZScan("Mu2E_1e7events_NoAbsorber_fromZ1850_parallel_Mu2eZScan") # , proton=False) 
 	# ../ntuples/v3.06/g4beamline_Mu2E_1e7events_NoAbsorber_fromZ1850_parallel_Mu2eZScan.root
 	# RunMu2eZScanPS("Mu2E_1e7events_Absorber3.1_ManyZNTuple3_fromZ1850_parallel_noColl_noPbar", proton=False) 

if __name__ == "__main__":
	main()

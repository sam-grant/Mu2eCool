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
	legend = ax.legend(loc="upper left", frameon=False, fontsize=14, bbox_to_anchor=(0.73, 0.99)) 
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
	ax.axvline(x=7929, color='gray', linestyle='--', linewidth=1) # TS3
	ax.axvline(x=11359, color='gray', linestyle='--', linewidth=1) # TS5
	ax.axvline(x=13800, color='gray', linestyle='--', linewidth=1) # ST
	# ax.axvline(x=17964, color='gray', linestyle='--', linewidth=1) # Tracker
	# ax.axvline(x=20394, color='gray', linestyle='--', linewidth=1) # Calo

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
	plt.annotate("TS3",
	             xy=(7929, plt.ylim()[1]),  
	             xytext=(10, 10),  
	             textcoords='offset points',  
	             va='bottom',  
	             ha='right', 
	             color='gray', 
	             fontsize=14,  # Font size of the label text
	             rotation='vertical')  # Rotate the label
	plt.annotate("TS5",
	             xy=(11359, plt.ylim()[1]),  
	             xytext=(10, 10),  
	             textcoords='offset points',  
	             va='bottom',  
	             ha='right', 
	             color='gray', 
	             fontsize=14,  # Font size of the label text
	             rotation='vertical')  # Rotate the label
	plt.annotate("ST",
	             xy=(13800, plt.ylim()[1]),  
	             xytext=(10, 10),  
	             textcoords='offset points',  
	             va='bottom',  
	             ha='right', 
	             color='gray', 
	             fontsize=14,  # Font size of the label text
	             rotation='vertical')  # Rotate the label
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

def Run(config, branchNames, particle, outDir): 

	# Setup input 
	finName = "../ntuples/"+g4blVer+"/g4beamline_"+config+".root"

	# Nested dictionary for particle populations over all Z
	particleNZ = {}

	# Loop through zntuples
	for i_z in range(2265, 13766, 500):

		# Get ntuple name
		ntupleName = "Z"+str(i_z)
		print("---> Reading", ntupleName)

		# Load TTree into DataFrame
		df = ut.TTreeToDataFrame(finName, "NTuple/"+ntupleName, branchNames) 

		# Filter upstream particles 
		# df = df[df['Pz'] > 0]

		# Filter PDGids
		df = FilterParticles(df, particle)

		# Dictionary for particles at this Z
		particleN = {}

	    # Loop through particleDict
		for PDGid, particleName in particleDict.items():
			# Count the occurrences of pdg_id in the DataFrame and add the count to particleN dictionary
			# if particleName=="proton": continue
			particleN[particleName] = df[df['PDGid'] == PDGid].shape[0]

		particleNZ[i_z] = particleN

	# Plot particle population as a function of z
	PlotGraphOverlay(particleNZ, xlabel="z [mm]", ylabel="N / 500 mm", fout="../img/"+g4blVer+"/"+outDir+"/gr_NvsZ_"+config+".png")

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
		# extend as needed
		]  

	particle = "all" # no_proton"

	config="Mu2E_1e7events_ManyZNTuple2_fromZ2265_parallel"
	outDir="BeamFlux"

	Run(config, branchNames, particle, outDir)


if __name__ == "__main__":
	main()

import numpy as np
import matplotlib.pyplot as plt

import Utils as ut

# Some random data

N = 10000
x = np.random.rand(N)*2*np.pi # flat distribution between 0 and 2pi
y = np.sin(x) + np.random.normal(0, 0.1, N) +  np.random.normal(0, 0.3, N)*x/5 # sin wave + some spread which increases with x 

# Create 2D histogram
hist, x_edges, y_edges = np.histogram2d(x, y, bins=[100, 100], range=[[np.min(x), np.max(x)], [np.min(y), np.max(y)]])

# Set up the first plot
fig1, ax1 = plt.subplots()

# Plot and write the 2D histogram
im = ax1.imshow(hist.T, cmap='inferno', extent=[np.min(x), np.max(x), np.min(y), np.max(y)], aspect='auto', origin='lower')
fout = "../img/test/h2.png"
plt.savefig(fout)
print("---> Written", fout)


#####

# bin width
xBinWidths = x_edges[1]-x_edges[0]

# Calculate the mean and RMS values of each vertical slice of the 2D distribution
ySliceMean_, ySliceRMS_ = [], []
for i, x_edge in enumerate(x_edges[:-1]):
	# Get y-slice within current x-bin
	ySlice = y[ (x_edges[i] < x) & (x <= x_edges[i+1]) ]
	# Append the means and rms in each slice
	ySliceMean_.append(ySlice.mean()) 
	ySliceRMS_.append(ySlice.std())

# Convert lists to numpy arrays
ySliceMean_ = np.array(ySliceMean_)
ySliceRMS_ = np.array(ySliceRMS_)


# Set up the second plot
fig2, ax2 = plt.subplots()

# Plot scatter with error bars
ax2.errorbar(range(len(ySliceMean_)), ySliceMean_, yerr=ySliceRMS_, fmt='o', color='black', markersize=4, ecolor='black', capsize=2, elinewidth=1, linestyle='None')

fout = "../img/test/h1_profile.png"
plt.savefig(fout)
print("---> Written", fout)


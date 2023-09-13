import math 
import numpy as np

def GetHelix(df):

	# Transverse radius of curvature in the B field

	# R = p/qBsin(theta) * gamma
	# E_k_T = E_T - E_0 = sqrt(p_T^2 + m_0^2) - m_0
	# E_k=E-E_0=(gamma-1)*m_0*c^2 --> gamma - 1 = E_k / m_0 * c^2 --> gamma = E_k/m_0*c^2 + 1 
	# --> gamma = E_k/m_0 + 1 

	# sin(Theta) = 1 for 2D, since 
	# cos(Theta) = BdotP / (Pmag * Bmag) = 0
	# BdotP = Bx * Px + By * Py + Bz * Pz = 0*Px + 0*Py + Bz*0 = 0

	# —> R = p_T/qB_z * gamma

	# Constants
	m_0 = 139.570 # pi+- rest mass in MeV/c^2
	e = 1.602e-19 # C
	c = 299792458 # m/s

	# Sign of charge 
	df["Sign"] = df["PDGid"].apply(lambda x: math.copysign(1, x))

	# Tranverse momentum, kinetic energy, and gamma
	df["PT"] = np.sqrt( pow(df["Px"], 2) + pow(df["Py"], 2) ) 
	df["EkT"] = np.sqrt(pow(df["PT"], 2) + pow(m_0, 2)) - m_0
	df["gammaT"] = df["EkT"]/m_0 + 1 

	df["LorentzRadius"] = df["gammaT"] *  (df["PT"] / (df["Sign"] * e * df["Bz"]) ) * (1e6 * e / c) * 1e3 # MeV/c -> J and m -> mm

	# Calculate the helical center 
	# We a looking into the helix, it spirals towards us
	# This bit came from ChatGPT, I need to think about it more but it seems to work when testing against the GUI...
	# In particular, I don't understand the signs. 
	# You adjust the x, y coordinates based on the radius of curvature, scaled according to the contribution of Px, Py to the total transverse momentum.
	df["HelixX"] = df["x"] + df["LorentzRadius"] * df["Px"] / df["PT"] # adjust x 
	df["HelixY"] = df["y"] - df["LorentzRadius"] * df["Py"] / df["PT"] # adjust y 
	df["HelixZ"] = df["z"]  # Assuming the magnetic field is along the z-axis

	df["HelixR"] = np.sqrt( pow(df["HelixX"], 2) + pow(df["HelixY"], 2) )

	return df

# Can test against the g4bl GUI with a source file like this. 
#BLTrackFile: Source file
#x            y            z            Px         Py         Pz         t            PDGid   EventID    TrackID    ParentID  Weight 
#mm           mm           mm           MeV/c      MeV/c      MeV/c      ns           ID      ID         ID         ID        ID     
#0        	  0            1850.000     50.000     50.000     50.000    0.50        -211    1          1           1          1      

import pandas as pd

# Create a dictionary with the data
data = {
    "x": [0.00],
    "y": [0.00],
    "z": [1850.000],
    "Bz": [4.273137], # This is Bz at Z=1850 mmm
    "Px": [50.000],
    "Py": [50.000],
    "PDGid": [-211]
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

df = GetHelix(df)

print(df)







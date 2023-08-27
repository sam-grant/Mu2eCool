import h5py
import Utils as ut

def main():

	hists = []
	labels = []

	particleFlag = "pi-" # "pi-" "all"

	for energy in range(100, 1100, 100):

	    file_name = "../plots/v3.08/g4beamlinePlots_"+str(particleFlag)+"_"+str(energy)+"MeV_10e4events.h5"

	    labels.append(str(energy)+" MeV")
	    
	    with h5py.File(file_name, "r") as file:

	        if 'momBackward' in file:
	            histogram_data = file['momBackward'][:]
	            hists.append(histogram_data)
	        else:
	            print(f"No 'momBackward' histogram found in file: {file_name}")

	ut.Plot1DOverlay(hists, 1100, -100, 1100, r"v3.08, $\pi^{-}$ out of Be target", "Momentum [MeV]", "Events / MeV", "../img/v3.08/h1_mom_detBackward_"+str(particleFlag)+"_100MeV-1000MeV_overlay.png", labels)


# def main():

# 	hists_ = []
# 	labels_ = [r"$50\times10^{-3}", r"$50\times10^{-2}", r"$50\times10^{-1}", r"50"]
# 	maxStep_ = ["50e-3", "50e-2", "50e-1", "50"]

# 	for maxStep in maxStep_:

# 	    file_name = "../plots/v3.08/g4beamline_BerylliumTarget_"+maxStep+".root" 

# 	    with h5py.File(file_name, "r") as file:

# 	        if 'momBackward' in file:
# 	            hist = file['momBackward'][:]
# 	            hists_.append(hist)
# 	        else:
# 	            print(f"No 'momBackward' histogram found in file: {file_name}")

# 	ut.Plot1DOverlay(hists, 1150, -50, 1100, r"v3.08, backward detector, $\pi^{-}$ only", "Momentum [MeV]", "Events / MeV", "../img/v3.08/h1_mom_detBackward_"+str(particleFlag)+"_100MeV-1000MeV_overlay.png", labels)


if __name__ == "__main__":
    main()
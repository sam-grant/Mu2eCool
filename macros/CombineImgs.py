# Samuel Grant 2023

from PIL import Image

particle = "pi-"
thickness = "25mm"
innerRadius = "110mm"
absorber = "AbsorberD"

# img1Name = "../img/v3.06/AbsorberCooling/h1_Mom_InOut_pi-_Mu2E_1e7events_"+absorber+"_l"+thickness+"_r"+innerRadius+"_fromZ1850_parallel.png"
# img2Name = "../img/v3.06/AbsorberCooling/h1_Mom_InOut_xmax100MeV_pi-_Mu2E_1e7events_"+absorber+"_l"+thickness+"_r"+innerRadius+"_fromZ1850_parallel.png"
# img3Name = "../img/v3.06/AbsorberCooling/h1_Mom_InOut_mu-_Mu2E_1e7events_"+absorber+"_l"+thickness+"_r"+innerRadius+"_fromZ1850_parallel.png"
# img4Name = "../img/v3.06/AbsorberCooling/h1_Mom_InOut_xmax50MeV_mu-_Mu2E_1e7events_"+absorber+"_l"+thickness+"_r"+innerRadius+"_fromZ1850_parallel.png"

img1Name = "../img/v3.06/ColdParticles/h1_mom_cold_pions_overlay_Mu2E_1e7events_AbsorberD_l25mm_r110mm_fromZ1850_parallel.png"
img2Name = "../img/v3.06/ColdParticles/h1_mom_cold_muons_overlay_Mu2E_1e7events_AbsorberD_l25mm_r110mm_fromZ1850_parallel.png"
img3Name = "../img/v3.06/ColdParticles/h1_rad_cold_pions_overlay_Mu2E_1e7events_AbsorberD_l25mm_r110mm_fromZ1850_parallel.png"
img4Name = "../img/v3.06/ColdParticles/h1_rad_cold_muons_overlay_Mu2E_1e7events_AbsorberD_l25mm_r110mm_fromZ1850_parallel.png"

imgName_ = [img1Name, img2Name, img3Name, img4Name]
img_ = [] 

for imgName in imgName_:
	img_.append(Image.open(imgName))

# Get the dimensions of the GIFs
width, height = img_[0].size

# print(width, height)
width = int(width * 1.025)
height = int(height * 1.025)

# Create a new image with a larger width to fit all GIFs side by side
combined_width = width * 2
combined_height = height * 2
combined_img = Image.new('RGBA', (combined_width, combined_height))

# Paste the images into the grid
for i, img in enumerate(img_):
	x = (i % 2) * width
	y = (i // 2) * height
	combined_img.paste(img, (x, y))

# Save the combined GIF
# fout="../img/v3.06/AbsorberCooling/combo_h1_Mom_InOut_"+particle+"_Mu2E_1e7events_"+absorber+"_l"+thickness+"_r"+innerRadius+"_fromZ1850_parallel.png" 
fout="../img/v3.06/ColdParticles/combo_h1_cold_particles_Mu2E_1e7events_"+absorber+"_l"+thickness+"_r"+innerRadius+"_fromZ1850_parallel.png" 

combined_img.save(fout, format='PNG')
print("---> Written", fout)

# 	# img0 = Image.open("../img/"+g4blVer+"/"+outDir+"/h3_XYMom_Z"+str(i_z)+"_"+particle+"_"+config+".png")
# 	img1 = Image.open("../img/"+g4blVer+"/"+inDir+"/"+img1Name+".png")
# 	img2 = Image.open("../img/"+g4blVer+"/"+inDir+"/"+img2Name+".png")

# 	img1Name = "h2_rad_vs_mom_Z"+str(i_z)+"_pi-_Mu2E_1e7events_NoAbsorber_fromZ1850_parallel_finePSZScan" # "h2_XY_Z"+str(i_z)+"_"+particle+"_Mu2E_1e7events_NoAbsorber_ManyZNTuple3_fromZ1850_parallel_noColl03"
# 	img2Name = "h2_rad_vs_mom_Z"+str(i_z)+"_mu-_Mu2E_1e7events_NoAbsorber_fromZ1850_parallel_finePSZScan"


# 	# img1Name = "h2_XvsMom_Z"+str(i_z)+"_"+particle+"_"+config
# 	# img2Name = "h2_YvsMom_Z"+str(i_z)+"_"+particle+"_"+config
# 	# img3Name = "h2_RVsMom_Z"+str(i_z)+"_"+particle+"_"+config

# 	# img1Name = "h2_XY_Z"+str(i_z)+"_pi+-_"+config
# 	# img2Name = "h2_XY_Z"+str(i_z)+"_mu+-_"+config

# 	# Open the GIFs
# 	# img0 = Image.open("../img/"+g4blVer+"/"+outDir+"/h3_XYMom_Z"+str(i_z)+"_"+particle+"_"+config+".png")
# 	img1 = Image.open("../img/"+g4blVer+"/"+inDir+"/"+img1Name+".png")
# 	img2 = Image.open("../img/"+g4blVer+"/"+inDir+"/"+img2Name+".png")
		
# 	# Get the dimensions of the GIFs
# 	width, height = img1.size

# 	# Create a new image with a larger width to fit all GIFs side by side
# 	combined_width = width * 2
# 	combined_height = height # * 2
# 	combined_img = Image.new('RGBA', (combined_width, combined_height))

# 	# Paste the GIFs side by side
# 	combined_img.paste(img1, (0, 0))
# 	combined_img.paste(img2, (width, 0))
# 	# combined_img.paste(img3, (2 * width, 0))

# 	# images = [img0, img1] # , img2, img3]

# 	# # Paste the images into the grid
# 	# for i, img in enumerate(images):
# 	# 	x = (i % 2) * width
# 	# 	y = (i // 2) * height
# 	# 	combined_img.paste(img, (x, y))

# 	# Save the combined GIF
# 	fout="../img/"+g4blVer+"/"+inDir+"/CombinedImgs/combo_rad_vs_mom_Z"+str(i_z)+"_Mu2E_1e7events_NoAbsorber_fromZ1850_parallel_finePSZScan.png" 
# 	combined_img.save(fout, format='PNG')
# 	print("---> Written", fout)


# g4blVer="v3.06"
# inDir="PSZScan" # PSZScan" # "DispersionAndBeamSpot" # AnaRadius" # RadiusVsMomentumStudy"
# config="Mu2E_1e7events_NoAbsorber_fromZ1850_parallel_finePSZScan"
# particle="pi-" # "pi+-" # pi+-" # mu+-" # no_proton"

# for i_z in range(1865, 3666, 50):

# 	img1Name = "h2_rad_vs_mom_Z"+str(i_z)+"_pi-_Mu2E_1e7events_NoAbsorber_fromZ1850_parallel_finePSZScan" # "h2_XY_Z"+str(i_z)+"_"+particle+"_Mu2E_1e7events_NoAbsorber_ManyZNTuple3_fromZ1850_parallel_noColl03"
# 	img2Name = "h2_rad_vs_mom_Z"+str(i_z)+"_mu-_Mu2E_1e7events_NoAbsorber_fromZ1850_parallel_finePSZScan"


# 	# img1Name = "h2_XvsMom_Z"+str(i_z)+"_"+particle+"_"+config
# 	# img2Name = "h2_YvsMom_Z"+str(i_z)+"_"+particle+"_"+config
# 	# img3Name = "h2_RVsMom_Z"+str(i_z)+"_"+particle+"_"+config

# 	# img1Name = "h2_XY_Z"+str(i_z)+"_pi+-_"+config
# 	# img2Name = "h2_XY_Z"+str(i_z)+"_mu+-_"+config

# 	# Open the GIFs
# 	# img0 = Image.open("../img/"+g4blVer+"/"+outDir+"/h3_XYMom_Z"+str(i_z)+"_"+particle+"_"+config+".png")
# 	img1 = Image.open("../img/"+g4blVer+"/"+inDir+"/"+img1Name+".png")
# 	img2 = Image.open("../img/"+g4blVer+"/"+inDir+"/"+img2Name+".png")
		
# 	# Get the dimensions of the GIFs
# 	width, height = img1.size

# 	# Create a new image with a larger width to fit all GIFs side by side
# 	combined_width = width * 2
# 	combined_height = height # * 2
# 	combined_img = Image.new('RGBA', (combined_width, combined_height))

# 	# Paste the GIFs side by side
# 	combined_img.paste(img1, (0, 0))
# 	combined_img.paste(img2, (width, 0))
# 	# combined_img.paste(img3, (2 * width, 0))

# 	# images = [img0, img1] # , img2, img3]

# 	# # Paste the images into the grid
# 	# for i, img in enumerate(images):
# 	# 	x = (i % 2) * width
# 	# 	y = (i // 2) * height
# 	# 	combined_img.paste(img, (x, y))

# 	# Save the combined GIF
# 	fout="../img/"+g4blVer+"/"+inDir+"/CombinedImgs/combo_rad_vs_mom_Z"+str(i_z)+"_Mu2E_1e7events_NoAbsorber_fromZ1850_parallel_finePSZScan.png" 
# 	combined_img.save(fout, format='PNG')
# 	print("---> Written", fout)


# for i_z in range(265, 3466, 100):

# 	img1Name = "h2_XvsMomZ_Z"+str(i_z)+"_"+particle+"_"+config
# 	img2Name = "h2_YvsMomZ_Z"+str(i_z)+"_"+particle+"_"+config
# 	img3Name = "h2_RVsMomZ_Z"+str(i_z)+"_"+particle+"_"+config

# 	# img1Name = "h2_XvsMom_Z"+str(i_z)+"_"+particle+"_"+config
# 	# img2Name = "h2_YvsMom_Z"+str(i_z)+"_"+particle+"_"+config
# 	# img3Name = "h2_RVsMom_Z"+str(i_z)+"_"+particle+"_"+config

# 	# img1Name = "h2_XY_Z"+str(i_z)+"_pi+-_"+config
# 	# img2Name = "h2_XY_Z"+str(i_z)+"_mu+-_"+config

# 	# Open the GIFs
# 	# img0 = Image.open("../img/"+g4blVer+"/"+outDir+"/h3_XYMom_Z"+str(i_z)+"_"+particle+"_"+config+".png")
# 	img1 = Image.open("../img/"+g4blVer+"/"+inDir+"/"+img1Name+".png")
# 	img2 = Image.open("../img/"+g4blVer+"/"+inDir+"/"+img2Name+".png")
# 	img3 = Image.open("../img/"+g4blVer+"/"+inDir+"/"+img3Name+".png")
	
# 	# Get the dimensions of the GIFs
# 	width, height = img1.size

# 	# Create a new image with a larger width to fit all GIFs side by side
# 	combined_width = width * 3
# 	combined_height = height # * 2
# 	combined_img = Image.new('RGBA', (combined_width, combined_height))

# 	# Paste the GIFs side by side
# 	combined_img.paste(img1, (0, 0))
# 	combined_img.paste(img2, (width, 0))
# 	combined_img.paste(img3, (2 * width, 0))

# 	# images = [img0, img1] # , img2, img3]

# 	# # Paste the images into the grid
# 	# for i, img in enumerate(images):
# 	# 	x = (i % 2) * width
# 	# 	y = (i // 2) * height
# 	# 	combined_img.paste(img, (x, y))

# 	# Save the combined GIF
# 	fout="../img/"+g4blVer+"/"+inDir+"/CombinedImgs/combo_XYRvsMomZ_Z"+str(i_z)+"_"+particle+"_"+config+".png"
# 	combined_img.save(fout, format='PNG')
# 	print("---> Written", fout)


	# break

# for i_z in range(265, 3466, 100):

# 	# Open the GIFs
# 	# img0 = Image.open("../img/"+g4blVer+"/"+outDir+"/h3_XYMom_Z"+str(i_z)+"_"+particle+"_"+config+".png")
# 	img1 = Image.open("../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsMom_Ana_Z"+str(i_z)+"_"+particle+"_"+config+".png")
# 	img2 = Image.open("../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsPT_Ana_Z"+str(i_z)+"_"+particle+"_"+config+".png")
# 	img3 = Image.open("../img/"+g4blVer+"/"+outDir+"/h2_RadiusVsPz_Ana_Z"+str(i_z)+"_"+particle+"_"+config+".png") 

# 	# Get the dimensions of the GIFs
# 	width, height = img1.size

# 	# Create a new image with a larger width to fit all GIFs side by side
# 	combined_width = width * 3
# 	combined_height = height # * 2
# 	combined_img = Image.new('RGBA', (combined_width, combined_height))

# 	# Paste the GIFs side by side
# 	combined_img.paste(img1, (0, 0))
# 	combined_img.paste(img2, (width, 0))
# 	combined_img.paste(img3, (2 * width, 0))

# 	# images = [img0, img1] # , img2, img3]

# 	# # Paste the images into the grid
# 	# for i, img in enumerate(images):
# 	# 	x = (i % 2) * width
# 	# 	y = (i // 2) * height
# 	# 	combined_img.paste(img, (x, y))

# 	# Save the combined GIF
# 	fout="../img/"+g4blVer+"/"+outDir+"/h2_combined_RadiusVsMom_Ana_Z"+str(i_z)+"_"+particle+"_"+config+".png"
# 	combined_img.save(fout, format='PNG')
# 	print("---> Written", fout)
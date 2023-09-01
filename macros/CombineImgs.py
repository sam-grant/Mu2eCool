from PIL import Image
g4blVer="v3.06"
inDir="Mu2eZScan" # PSZScan" # "DispersionAndBeamSpot" # AnaRadius" # RadiusVsMomentumStudy"
config="ManyZNTuple3_fromZ1850_parallel_noColl03"
particle="pi-" # "pi+-" # pi+-" # mu+-" # no_proton"

for i_z in range(1850, 4350, 100):

	img1Name = "h2_XY_Z"+str(i_z)+"_"+particle+"_Mu2E_1e7events_NoAbsorber_ManyZNTuple3_fromZ1850_parallel_noColl03"
	img2Name = "h2_XY_Z"+str(i_z)+"_"+particle+"_Mu2E_1e7events_Absorber3.1_ManyZNTuple3_fromZ1850_parallel_noColl03"


	# img1Name = "h2_XvsMom_Z"+str(i_z)+"_"+particle+"_"+config
	# img2Name = "h2_YvsMom_Z"+str(i_z)+"_"+particle+"_"+config
	# img3Name = "h2_RVsMom_Z"+str(i_z)+"_"+particle+"_"+config

	# img1Name = "h2_XY_Z"+str(i_z)+"_pi+-_"+config
	# img2Name = "h2_XY_Z"+str(i_z)+"_mu+-_"+config

	# Open the GIFs
	# img0 = Image.open("../img/"+g4blVer+"/"+outDir+"/h3_XYMom_Z"+str(i_z)+"_"+particle+"_"+config+".png")
	img1 = Image.open("../img/"+g4blVer+"/"+inDir+"/"+img1Name+".png")
	img2 = Image.open("../img/"+g4blVer+"/"+inDir+"/"+img2Name+".png")
		
	# Get the dimensions of the GIFs
	width, height = img1.size

	# Create a new image with a larger width to fit all GIFs side by side
	combined_width = width * 2
	combined_height = height # * 2
	combined_img = Image.new('RGBA', (combined_width, combined_height))

	# Paste the GIFs side by side
	combined_img.paste(img1, (0, 0))
	combined_img.paste(img2, (width, 0))
	# combined_img.paste(img3, (2 * width, 0))

	# images = [img0, img1] # , img2, img3]

	# # Paste the images into the grid
	# for i, img in enumerate(images):
	# 	x = (i % 2) * width
	# 	y = (i // 2) * height
	# 	combined_img.paste(img, (x, y))

	# Save the combined GIF
	fout="../img/"+g4blVer+"/"+inDir+"/CombinedImgs/combo_XY_Z"+str(i_z)+"_"+particle+"_NoAbsorberVsAbsorber3.1_ManyZNTuple3_fromZ1850_parallel_noColl03.png" 
	combined_img.save(fout, format='PNG')
	print("---> Written", fout)


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
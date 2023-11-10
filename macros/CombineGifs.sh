# Samuel Grant 2023

nGifs=3
gif1="../gif/h2_RadiusVsMom_Z265_Z3465_no_proton_Mu2E_1e6events_ManyZNTuple1.gif"
gif2="../gif/h2_RadiusVsPT_Z265_Z3465_no_proton_Mu2E_1e6events_ManyZNTuple1.gif"
gif3="../gif/h2_RadiusVsPz_Z265_Z3465_no_proton_Mu2E_1e6events_ManyZNTuple1.gif"
gifOut="../gif/h2_RadiusVsMomAll_Z265_Z3465_no_proton_Mu2E_1e6events_ManyZNTuple1.gif"

ffmpeg -i $gif1 -vf "scale=-1:1432" $gif1


ffmpeg -i $gif1 -i $gif2 -i $gif3 -filter_complex "hstack=inputs=${nGifs}" $gifOut
# ffmpeg -i $gif1 -i $gif2 -i $gif3 -filter_complex "[0:v]scale=1795:1433[v0];[1:v]scale=1795:1433[v1];[2:v]scale=1795:1433[v2];[v0][v1][v2]hstack=inputs=${nGifs}" $gifOut
# ffmpeg -i $gif1 -i $gif2 -i $gif3 -filter_complex "hstack=inputs=${nGifs},scale=1795:1433" $gifOut

# ffmpeg -i $gif1 -i $gif2 -i $gif3 -filter_complex "[0:v]scale=1795:1433:flags=lanczos,format=rgba,pix_fmt=rgba[v0];[1:v]scale=1795:1433:flags=lanczos,format=rgba,pix_fmt=rgba[v1];[2:v]scale=1795:1433:flags=lanczos,format=rgba,pix_fmt=rgba[v2];[v0][v1][v2]hstack=inputs=${nGifs}" -pix_fmt rgba $gifOut



# ffmpeg -i $gif1 -q:v 1 gif1.png
# ffmpeg -i $gif2 -q:v 1 gif2.png
# ffmpeg -i $gif3 -q:v 1 gif3.png

# ffmpeg -i gif1.png -i gif2.png -i gif3.png -filter_complex "[0:v]scale=1795:1433:flags=lanczos[v0];[1:v]scale=1795:1433:flags=lanczos[v1];[2:v]scale=1795:1433:flags=lanczos[v2];[v0][v1][v2]hstack=inputs=${nGifs}" -pix_fmt rgba stacked.png
# ffmpeg -i stacked.png -pix_fmt rgba $gifOut

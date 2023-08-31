# convert -delay 50 -loop 0 `ls ../img/v3.06/RadiusVsMomentumStudy/h2_RadiusVsMomAll_Z*_no_proton_Mu2E_1e6events_ManyZNTuple1.png | sort -V` ../gif/h2_RadiusVsMomAll_Z265_Z3465_no_proton_Mu2E_1e6events_ManyZNTuple1.gif
# convert -delay 50 -loop 0 `ls ../img/v3.06/RadiusVsMomentumStudy/h2_ThetaVsPz_Z*_no_proton_Mu2E_1e6events_ManyZNTuple1.png | sort -V` ../gif/h2_ThetaVsPz_Z265_Z3465_no_proton_Mu2E_1e6events_ManyZNTuple1.gif
# convert -delay 50 -loop 0 `ls ../img/v3.06/RadiusVsMomentumStudy/h2_ThetaVsPT_Z*_no_proton_Mu2E_1e6events_ManyZNTuple1.png | sort -V` ../gif/h2_ThetaVsPT_Z265_Z3465_no_proton_Mu2E_1e6events_ManyZNTuple1.gif
# convert -delay 50 -loop 0 `ls ../img/v3.06/RadiusVsMomentumStudy/h2_ThetaVsMom_Z*_no_proton_Mu2E_1e6events_ManyZNTuple1.png | sort -V` ../gif/h2_ThetaVsMom_Z265_Z3465_no_proton_Mu2E_1e6events_ManyZNTuple1.gif
# convert -delay 50 -loop 0 `ls ../img/v3.06/RadiusVsMomentumStudy/h2_ThetaVsRad_Z*_no_proton_Mu2E_1e6events_ManyZNTuple1.png | sort -V` ../gif/h2_ThetaVsRad_Z265_Z3465_no_proton_Mu2E_1e6events_ManyZNTuple1.gif
# convert -delay 50 -loop 0 `ls ../img/v3.06/RadiusVsMomentumStudy/h3_XYMom_Z*_mu+-_Mu2E_1e6events_ManyZNTuple1.png | sort -V` ../gif/h3_XYMomAll_Z265_Z3465_mu+-_Mu2E_1e6events_ManyZNTuple1.gif
# convert -delay 50 -loop 0 `ls ../img/v3.06/RadiusVsMomentumStudy/h3_XYMom_Z*_pi+-_Mu2E_1e6events_ManyZNTuple1.png | sort -V` ../gif/h3_XYMomAll_Z265_Z3465_pi+-_Mu2E_1e6events_ManyZNTuple1.gif
#convert -delay 50 -loop 0 `ls ../img/v3.06/AnaRadius/h2_combined_RadiusVsMom_Ana_Z*_pi+-_Mu2E_1e6events_ManyZNTuple1.png | sort -V` ../gif/h2_combined_RadiusVsMom_Ana_Z265_Z3465_pi+-_Mu2E_1e6events_ManyZNTuple1.gif 
#

ver="v3.06"
dir="PSZScan/CombinedImgs"
name="combo_XYRvsMomZ" # combo_XYRvsMomZ" # combo_XY"
particle="pi+-" # "pi+-" # "mu+-"
config="${name}_${particle}_Mu2E_1e6events_ManyZNTuple1"

convert -delay 50 -loop 0 `ls ../img/${ver}/${dir}/${name}_Z*_${particle}_Mu2E_1e6events_ManyZNTuple1.png | sort -V` ../gif/${name}_${particle}_Z265_Z3465_Mu2E_1e6events_ManyZNTuple1.gif 

echo "../gif/${name}_${particle}_Z265_Z3465_Mu2E_1e6events_ManyZNTuple1.gif"
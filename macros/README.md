* __AbsorberCooling.py__: Analyse the momentum change before/after the absorber material within Mu2e geometry.

* __BeamFlux.py__: Analyse the flux of muons through each virtual detector through experiment, creates a .csv file recording the muon flux (included stopped muons).

* __BeamProfile.py__: Analyse transverse beam profiles at a particular virtual detector.

* __ColdParticleBeamLoss.py__: Analyse beamloss NTuple generated by running the output of ColdParticles.py. 

* __ColdParticles.py__: Identify newly cooled particles exiting the absorber and write them to a ROOT NTuple. Analyse file generated by This file contains code related to cold particles.

* __CombineGifs.sh__: Bash script for combining pngs into a gif.

* __CombineImgs.py__: For combining images into a single panel.

* __CompareBeams.py__: Compare the relative flux between two different absorber configurations, usually just with/without an absorber.

* __CoolingScan.py__: Analyse a scan using G4beamline over pion/muon beams of varying momentum passing through material of varying thickness. 

* __MakeSource.py__: Generate a text source file input for G4beamline, based on krlynch's script.

* __Mu2eZScan.py__: Analyse a zntuple scan through entire Mu2e beamline. 

* __MuPlusBump.py__: Analyse the mu+ momentum bump in the production solenoid (it's from kaons).

* __PSDispersionFits.py__: Dispersion relation fits within the production solenoid.

* __PSZScan.py__: Analyse a zntuple scan through the production solenoid. 

* __StoppedMuons.py__: Track stopped muons and their parents backwards down the beamline. 

* __TSWedgeSlow.py__: Attempted dispersion fits in the transport solenoid.

* __Utils.py__: Common utility function, including TTree handling and plotting.
#!/usr/bin/env python3
# source  /grid/fermiapp/products/mu2e/setupmu2e-art.sh
# setup root v5_34_05 -qmu2e:e2:prof
# Run as: python3 MakeSource.py Source.root 0/1
# 0 - PS Only. Neutrons only
# 1 - Beam source. All particles, excluding neutrons, soft gammas and electrons
# External libraries
import ROOT
from ROOT import TFile, TTree, TH2F, TCanvas
from math import sqrt, fabs
import sys
import numpy as np
import re

ROOT.gROOT.Reset()

def Run():

    # inputs
    finName = "../ntuples/v3.06/g4beamline_Mu2E_Absorber3_l40mm_r100mm_fromZ1850_parallel_ColdParticles.root" 
    NTuple = "NTuple" 
    foutName = "../beamFiles/v3.06/g4beamline_Mu2E_Absorber3_l40mm_r100mm_fromZ1850_parallel_ColdParticles_bm.txt" 

    fin = TFile(finName)
    tree = fin.Get(NTuple) 

    print(fin)
    print(tree)
    print(foutName)

    fout = open(f"{foutName}", "w")
    print(fout)

    fout.write("#BLTrackFile: Source file\n")
    # fout.write("#{:<12} {:<12} {:<12} {:<10} {:<10} {:<10} {:<12} {:<7} {:<10} {:<10} {:<9} {:<7}\n".format("x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "TrackID"))
    fout.write("#{:<12} {:<12} {:<12} {:<10} {:<10} {:<10} {:<12} {:<7} {:<10} {:<10} {:<9} {:<7}\n".format("x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"))
    fout.write("#{:<12} {:<12} {:<12} {:<10} {:<10} {:<10} {:<12} {:<7} {:<10} {:<10} {:<9} {:<7}\n".format("mm", "mm", "mm", "MeV/c", "MeV/c", "MeV/c", "ns", "ID", "ID", "ID", "ID", "ID"))

    nEvents = tree.GetEntries()

    print("Number of input events:", nEvents)

    counter = 0

    for i in range(nEvents):

        tree.GetEntry(i)

        x = tree.x
        y = tree.y
        z = tree.z
        Px = tree.Px
        Py = tree.Py
        Pz = tree.Pz
        t = tree.t
        PDGid = tree.PDGid
        EventID = tree.EventID
        TrackID = tree.TrackID
        ParentID = tree.ParentID
        Weight = tree.Weight

        # Write event
        fout.write("{:<13.3f} {:<12.3f} {:<12.3f} {:<10.3f} {:<10.3f} {:<10.3f} {:<12.3f} {:<7} {:<10} {:<10} {:<7} {:<7}\n".format(x, y, z, Px, Py, Pz, t, PDGid, EventID, TrackID, ParentID, Weight))

        counter+=1

    fout.close()
    fin.Close()
    
    print("Counter:", counter)
    print("Written", foutName)

def Run2():

    # inputs
    finName = "../ntuples/v3.06/g4beamline_Mu2E_Absorber3_l40mm_r100mm_fromZ1850_parallel_ColdParticles.root" 
    NTuple = "NTuple" 
    foutName = "../beamFiles/v3.06/g4beamline_Mu2E_Absorber3_l40mm_r100mm_fromZ1850_parallel_ColdParticles_bm.txt" 

    fin = TFile(finName)
    tree = fin.Get(NTuple) 

    print(fin)
    print(tree)
    print(foutName)

    fout = open(f"{foutName}", "w")
    print(fout)

    fout.write("#BLTrackFile: Source file\n")
    # fout.write("#{:<12} {:<12} {:<12} {:<10} {:<10} {:<10} {:<12} {:<7} {:<10} {:<10} {:<9} {:<7}\n".format("x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "TrackID"))
    fout.write("#{:<12} {:<12} {:<12} {:<10} {:<10} {:<10} {:<12} {:<7} {:<10} {:<10} {:<9} {:<7}\n".format("x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"))
    fout.write("#{:<12} {:<12} {:<12} {:<10} {:<10} {:<10} {:<12} {:<7} {:<10} {:<10} {:<9} {:<7}\n".format("mm", "mm", "mm", "MeV/c", "MeV/c", "MeV/c", "ns", "ID", "ID", "ID", "ID", "ID"))

    nEvents = tree.GetEntries()

    print("Number of input events:", nEvents)

    counter = 0

    lastEventID = -9999999
    lastTrackID = -9999999


    for i in range(nEvents):

        tree.GetEntry(i)

        x = tree.x
        y = tree.y
        z = tree.z
        Px = tree.Px
        Py = tree.Py
        Pz = tree.Pz
        t = tree.t
        PDGid = tree.PDGid
        EventID = tree.EventID
        TrackID = tree.TrackID
        ParentID = tree.ParentID
        Weight = tree.Weight

        # Set ParentID to one, g4bl treats all source particles as primaries 
        ParentID = 1
        # Force all tracks to be primaries, otherwise g4bl will complain
        while TrackID > 1000: # Keep doing this until it behaves
            TrackID = TrackID - 1000

        # Handle duplicate events 
        # No need for anything fancy, EventIDs proceed in-order so just keep iterating the TrackID
        if lastEventID == EventID and lastTrackID == TrackID:
            # Iterate TrackID 
            TrackID += 1 # Could also just skip
            nDuplicates += 1
            continue

        # # Filter upstream particles 
        # if Pz < 0: 
        #     # Update lastIDs and continue
        #     lastEventID = EventID
        #     lastTrackID = TrackID
        #     continue

        # Remove exotic particles. g4bl can't handle them as the source
        if PDGid > 1000000:
            continue

        # Write event
        fout.write("{:<13.3f} {:<12.3f} {:<12.3f} {:<10.3f} {:<10.3f} {:<10.3f} {:<12.3f} {:<7} {:<10} {:<10} {:<7} {:<7}\n".format(x, y, z, Px, Py, Pz, t, PDGid, EventID, TrackID, ParentID, Weight))

        counter+=1

        # Update lastIDs
        lastEventID = EventID
        lastTrackID = TrackID

    fout.close()
    fin.Close()
    
    print("Counter:", counter)
    print("Written", foutName)

if __name__ == "__main__":

   Run2()

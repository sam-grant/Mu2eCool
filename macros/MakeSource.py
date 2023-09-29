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

    if len(sys.argv) != 4:
        print("Usage: python MakeSource.py <finName> <ZNtuple> <nFout> (e.g. python MakeSource.py g4beamline.root Z500 10)\nExiting...")
        sys.exit(0)

    finName = sys.argv[1]
    ZNtuple = sys.argv[2] # Z3712
    nFout = int(sys.argv[3])

    # Extract the file name without extension and concatenate with "_ps.txt"
    foutName = finName.split("/")[-1][:-5] # + "_ps.txt"

    # Assuming the directory structure is "../ntuples/v3.06/g4beamline_Mu2E_1e5events.root"
    # Replace "ntuples" with "beamFiles" in the path
    foutName = finName.replace("/ntuples/", "/beamFiles/").replace("_Z1850", "").replace(".root", "") + "_" +ZNtuple+ "_withSoftElectrons_bm"

    # Handle file splitting
    match = re.search(r'_(\d+)e(\d+)events', finName)
    totEvents=0 

    if match:
        totEvents = match.group(1)+"e"+match.group(2)
        # exponent = match.group(2)
        print(f"Total events: {totEvents}")
    else:
        print("Total events not found...")

    # Create a list of output files, if we're splitting them
    fout_ = []

    if nFout > 1: 
        fout_ = [open(f"{foutName}_{i}.txt", "w") for i in range(nFout)]
    else:
        fout_ = [open(f"{foutName}.txt", "w")]

    eventsPerFile = float(totEvents) / nFout

    print(eventsPerFile)

    # Get inputs
    fin = TFile(finName)
    tree = fin.Get("/NTuple/"+ZNtuple)

    # histo = TH2F("histo", "histo", int(1000), float(-10000), float(10000), int(10000), float(-10000), float(10000))

    print("The input source file:", finName)
    print("The output source file(s):")

    for fout in fout_:

        print(fout.name)

        fout.write("#BLTrackFile: Source file\n")
        # fout.write("#{:<12} {:<12} {:<12} {:<10} {:<10} {:<10} {:<12} {:<7} {:<10} {:<10} {:<9} {:<7}\n".format("x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "TrackID"))
        fout.write("#{:<12} {:<12} {:<12} {:<10} {:<10} {:<10} {:<12} {:<7} {:<10} {:<10} {:<9} {:<7}\n".format("x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"))
        fout.write("#{:<12} {:<12} {:<12} {:<10} {:<10} {:<10} {:<12} {:<7} {:<10} {:<10} {:<9} {:<7}\n".format("mm", "mm", "mm", "MeV/c", "MeV/c", "MeV/c", "ns", "ID", "ID", "ID", "ID", "ID"))

    lastEventID = -9999999
    lastTrackID = -9999999

    nEvents = tree.GetEntries()

    targetPerc = 0
    nDuplicates = 0

    for i, trk in enumerate(tree):

        # Store these variables used more than once in the loop
        EventID = int(trk.EventID)
        TrackID = int(trk.TrackID)
        Px = trk.Px
        Py = trk.Py
        Pz = trk.Pz
        PDGid = int(trk.PDGid)

        # Set ParentID to one, g4bl treats all source particles as primaries 
        ParentID = 1
        # Force all tracks to be primaries, otherwise g4bl will complain
        while TrackID > 1000: # Keep doing this until it behaves
            TrackID = TrackID - 1000

        # if TrackID > 1000:
        #     TrackID = TrackID - 1000
        #     if TrackID > 1000:

        # Handle duplicate events 
        # No need for anything fancy, EventIDs proceed in-order so just keep iterating the TrackID
        if lastEventID == EventID and lastTrackID == TrackID:
            # Iterate TrackID 
            TrackID += 1 # Could also just skip
            nDuplicates += 1
            continue

        # Filter upstream particles 
        if Pz < 0: 
            # Update lastIDs and continue
            lastEventID = EventID
            lastTrackID = TrackID
            continue

        # Remove exotic particles. g4bl can't handle them as the source
        if PDGid > 1000000:
            continue

        # Drop soft e+- in beam source
        # if fabs(PDGid) == 11 and np.sqrt( pow(Px,2) + pow(Py,2) + pow(Pz,2) )<10.0: 
        #     continue

        # Add more filters here as needed

        # Determine the output file index, based on the event ID
        fout_i = (EventID - 1) // int(eventsPerFile)
        fout = fout_[fout_i]

        # Write event
        fout.write("{:<13.3f} {:<12.3f} {:<12.3f} {:<10.3f} {:<10.3f} {:<10.3f} {:<12.3f} {:<7} {:<10} {:<10} {:<7} {:<7}\n".format(trk.x, trk.y, trk.z, Px, Py, Pz, trk.t, PDGid, EventID, TrackID, ParentID, int(trk.Weight)))

        # Print status
        perc = 100 * (i + 1) / nEvents  # Use 'idx' for loop index
        if perc >= targetPerc:
            print("\nProcessed", int(perc), "%")
            print("Snapshot: EventID = ",EventID,"; OutputID = ",fout_i,"; Number of duplicates = ",nDuplicates)
            targetPerc += 10

        # Update lastIDs
        lastEventID = EventID
        lastTrackID = TrackID

    fin.Close()

    for fout in fout_:
        fout.close()

    print("\n", nDuplicates, "duplicates out of", nEvents)

if __name__ == "__main__":
   Run()
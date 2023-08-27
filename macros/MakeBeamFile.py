# Make a beam source file from zntuple
# See 
import uproot
import pandas as pd
import csv
import sys

def TTreeToDataFrame(finName, treeName, branchNames):

    print("\n---> Reading...")

    # Open the ROOT file
    fin = uproot.open(finName)
    
    print("---> Got input file ", finName, ", ", (fin))

    # Get tree
    tree = fin[treeName]

    print("---> Got tree ", str(tree))

    # Create an empty dictionary to store the selected columns as NumPy arrays
    branchData = {}

    # Iterate over the specified column names
    for branchName in branchNames:
        # Check if the column name exists in the TTree
        if branchName in tree:
            # Load values in array
            branchData[branchName] = tree[branchName].array(library="np")

    # Create the DataFrame directly from the dictionary of column data
    df = pd.DataFrame(branchData)

    print("---> Reading done, closing input file...")

    # Close the ROOT file
    fin.close()

    # Print the raw DataFrame
    print("\n---> Raw DataFrame:\n", df)

    # Return the DataFrame
    return df

def Filter(df):

	# Keep filtering stuff here

	return df

def Run(finName, treeName, branchNames, foutName):

	# The file format is ASCII:
	# Lines beginning with # are comments
	# First line is a structured comment (if not present the input
	# routine issues a warning):
	# #BLTrackFile ... user comment...
	# Second line is a comment giving the column names:
	# #x y z Px Py Pz t PDGid EvNum TrkId Parent weight
	# Third line is a comment giving the units:
	# #cm cm cm MeV/c MeV/c MeV/c ns - - - - -
	# OR:
	# #mm mm mm MeV/c MeV/c MeV/c ns - - - - -

	df = TTreeToDataFrame(finName, treeName, branchNames)

	# Truncate IDs to ints
	df['PDGid'] = df['PDGid'].astype(int)
	df['EventID'] = df['EventID'].astype(int)
	df['TrackID'] = df['TrackID'].astype(int)
	df['ParentID'] = df['ParentID'].astype(int)

	df = Filter(df)
	
	# Drop the weights, they are not an available variable
	df = df.drop(columns=['Weight'])

	# print(df[df['Pz'] < 0])

	# Formatting according to Section 9.1 of the G4beamline manual
	header = [

         ["#BLTrackFile: Source file"]
        ,["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]
        ,["mm", "mm", "mm", "MeV/c", "MeV/c", "MeV/c", "ns", "ID", "ID", "ID", "ID", "ID"]

        ]


	# Write to the file without quotes and using the custom header
	with open(foutName, 'w') as fout:
	    fout.write(header[0] + '\n')
	    fout.write(header[1] + '\n')
	    fout.write(header[2] + '\n')
	    df.to_csv(fout, sep='\t', index=False, header=False)

	# # Write to the file with the custom header and without quotes
	# with open(foutName, 'w') as fout:
	#     fout.write(header + '\n')

	#     # Iterate through header rows 
	#     for row in header:
	#         # row_str = " ".join(str(val) for val in row.values)
	#         fout.write(row + '\n')

	#     # Iterate through DataFrame rows and write each row to the file
	#     for index, row in df.iterrows():
	#         row_str = " ".join(str(val) for val in row.values)
	#         fout.write(row_str + '\n')

	print("---> Done. Written to", foutName)

	return

def main():

    if len(sys.argv) != 4:
        print("Usage: python MakeBeamFile.py <finName> <ZNtuple> <nFout> (e.g. python MakeSource.py g4beamline.root Z500 10)\nExiting...")
        sys.exit(0)

    finName = sys.argv[1]
    ZNTuple = "NTuple/"+sys.argv[2] 
    nFout = int(sys.argv[3])

    branchNames = [ 
        "x", 
        "y", 
        "z", 
        "Px", 
        "Py",
        "Pz",
        "t",
        "PDGid",
        "EventID",
        "TrackID",
        "ParentID",
        "Weight"
    ]  

    Run(finName, ZNTuple, branchNames, "../txt/v3.06/test.csv") # , nFout)


if __name__ == "__main__":
    main()



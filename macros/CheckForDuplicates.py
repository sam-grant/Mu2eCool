import pandas as pd

# Read the text file into a DataFrame
file_path = '../beamFiles/v3.06/g4beamline_Mu2E_1e7events_Z1800_bm_0.txt' # ../beamFiles/v3.06/g4beamline_Mu2E_1e6events_Z2265_bm.txt'

# Define column names
column_names = ['x', 'y', 'z', 'Px', 'Py', 'Pz', 't', 'PDGid', 'EventID', 'TrackID', 'ParentID', 'Weight']

df = pd.read_csv(file_path, delim_whitespace=True, comment='#', skiprows=2, names=column_names)

print(df)

df['UniqueID'] = 1e6*df['EventID'] + 1e3*df['TrackID'] + df['ParentID']
# df['UniqueID'] = df['EventID'] * df['TrackID'] * df['ParentID']

# print(df)

# Check for duplicate rows
duplicates = df[df['UniqueID'].duplicated()]

if duplicates.empty:
    print("\n---> No duplicate rows found.")
else:
    print(str(duplicates.shape[0])+"duplicate rows found.")
    print(duplicates)  

# print(df[df['UniqueID']==39001001.0])
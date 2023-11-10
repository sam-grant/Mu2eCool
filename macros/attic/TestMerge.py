import pandas as pd

# Example data frame 1
prestop = {'EventID': [1, 2, 3, 4, 4],
         'TrackID': [101, 102, 103, 104, 105],
         'ParentID': [201, 202, 203, 204, 205],
         'PDGid': [11, 13, 13, 13, -211]}
df_prestop = pd.DataFrame(prestop)

# Example data frame 2
lost = {'EventID': [2, 4, 6],
         'TrackID': [102, 104, 106],
         'ParentID': [202, 204, 206],
         'PDGid': [11, 13, 13]}

df_lost = pd.DataFrame(lost)

# Example data frame 2
plane = {'EventID': [2, 4, 6],
         'TrackID': [102, 104, 106],
         'ParentID': [202, 204, 206],
         'PDGid': [11, -211, 13]}

df_plane = pd.DataFrame(lost)

# Display the data frames
print("\nPrestop:")
print(df_prestop)

print("Lost:")
print(df_lost)

df_stops = df_prestop.merge(df_lost, on=["EventID", "TrackID", "ParentID", "PDGid"], suffixes=("", "_lost"), how="inner")


print(df_stops)
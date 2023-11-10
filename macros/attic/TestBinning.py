import numpy as np

def bin(data, bin_width = 1.0): 

    # Bin the data
    bin_edges = np.arange(min(data), max(data) + bin_width, bin_width)
    bin_indices = np.digitize(data, bin_edges)
    bin_counts = np.bincount(bin_indices)

    return bin_edges, bin_indices, bin_counts

data = np.array([1.2, 2.3, 2.3, 3.5, 4.1, 2.3, 5.0, 4.1, 3.5, 2.3])
print(bin(data, 0.1))
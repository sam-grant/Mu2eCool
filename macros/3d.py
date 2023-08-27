import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def Plot3D(x, y, z, nBinsX, xmin, xmax, nBinsY, ymin, ymax, title, xlabel, ylabel, zlabel, fout):

    hist_xy, x_edges_xy, y_edges_xy = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]], weights=z)

    # Calculate the histogram bin counts
    hist_counts, _, _ = np.histogram2d(x, y, bins=[nBinsX, nBinsY], range=[[xmin, xmax], [ymin, ymax]])

    # Avoid division by zero and invalid values
    non_zero_counts = hist_counts > 0
    hist_xy[non_zero_counts] /= hist_counts[non_zero_counts]

    fig, ax = plt.subplots()

    # Plot the 2D histogram without logarithmic color scale
    im = ax.imshow(hist_xy.T, cmap='inferno', extent=[xmin, xmax, ymin, ymax], aspect='auto', origin='lower')

    # Add colorbar with specified number of levels
    num_levels = 10  # Adjust this number as needed
    cbar = plt.colorbar(im, ticks=np.linspace(hist_xy.min(), hist_xy.max(), num=num_levels))

    # Manually set contour levels spanning the entire range of z values
    # contour_levels = np.linspace(z.min(), z.max(),  num=num_levels)

    # Add contour lines to visualize bin boundaries
    # ax.contour(hist_xy.T, levels=contour_levels, extent=[xmin, xmax, ymin, ymax], colors='black', linewidths=0.7)

    plt.title(title, fontsize=16, pad=10)
    plt.xlabel(xlabel, fontsize=14, labelpad=10)
    plt.ylabel(ylabel, fontsize=14, labelpad=10)

    # # Format colorbar tick labels if needed
    # if cbar.get_clim()[1] > 999:
    #     cbar.ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    #     cbar.ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    #     cbar.ax.yaxis.offsetText.set_fontsize(14)

    plt.savefig(fout, dpi=300, bbox_inches="tight")
    print("---> Written", fout)

    plt.close()

# Example usage
x = np.random.uniform(-1, 1, 1000)
y = np.random.uniform(-1, 1, 1000)
z = np.sqrt(pow(x,2) + pow(y,2)) # np.random.normal(0, 5, 1000)  # Example z values

print(z)
Plot3D(x, y, z, 10, -1, 1, 10, -1, 1, "Example 3D plot", "X Label", "Y Label", "Z Label", "../img/example_3D_plot.png")

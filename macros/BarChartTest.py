import matplotlib.pyplot as plt
import numpy as np

data = [-13, 13, -13, 221, 221, -221, 2212, 320]

particle_dict = {
    13: 'mu-',
    -13: 'mu-',
    221: 'pi+',
    -221: 'pi-',
    2212: 'proton',
    # Add more particle entries as needed
}

# Convert numerical values to labels using the particle_dict
labels = [particle_dict.get(p, 'other') for p in data]

# Count occurrences of each label
unique_labels, label_counts = np.unique(labels, return_counts=True)

# Sort labels and counts in descending order
sorted_indices = np.argsort(label_counts)[::-1]
unique_labels = unique_labels[sorted_indices]
label_counts = label_counts[sorted_indices]

# Create figure and axes
fig, ax = plt.subplots()

# Plot the bar chart
ax.bar(unique_labels, label_counts)

# Set x-axis labels
ax.set_xticks(range(len(unique_labels)))
ax.set_xticklabels(unique_labels, rotation=45)

# Set labels for the chart
ax.set_xlabel('Particle Type')
ax.set_ylabel('Counts')
ax.set_title('Particle Counts')

# Show the plot
plt.tight_layout()
plt.savefig('tmp.png')

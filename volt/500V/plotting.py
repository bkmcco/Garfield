import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
df = pd.read_csv("electron_positions.csv")  # Replace with your filename

# Circle radius in cm (70 µm diameter)
radius_cm = 70 / 2 / 1e4  # = 0.0035 cm

# Set up the plot
plt.figure(figsize=(8, 8))
colors = plt.cm.tab10.colors

for i, row in df.iterrows():
    xavg, yavg = row['xavg'], row['yavg']
    xmin, xmax = row['xmin'], row['xmax']
    ymin, ymax = row['ymin'], row['ymax']
    ne = int(row['ne'])  
    color = colors[i % len(colors)]

    # Plot horizontal (X) min-max line
    plt.plot([xmin, xmax], [yavg, yavg], color=color, marker='o')

    # Plot vertical (Y) min-max line
    plt.plot([xavg, xavg], [ymin, ymax], color=color, linestyle='--')

    # Draw 70 µm circle around the average
    circle = plt.Circle((xavg, yavg), radius_cm, color=color, fill=False, linestyle='--')
    plt.gca().add_patch(circle)

    # Annotate with "ne = (value)"
    plt.text(xavg + 0.001, yavg + 0.001, f'ne = {ne}', fontsize=8, color=color)

# Aesthetic tweaks
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)

plt.xlabel('X Position (cm)')
plt.ylabel('Y Position (cm)')

# Set plot limits
plt.xlim(-0.05, 0.05)
plt.ylim(-0.05, 0.05)

# Set ticks at 0.02 intervals from -0.1 to 0.1
ticks = np.arange(-0.03 ,0.03, 0.01)
plt.xticks(ticks)
plt.yticks(ticks)
plt.tight_layout()

# Save as PNG
plt.savefig("circleplot.png", dpi=300)
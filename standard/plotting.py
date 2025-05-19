import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Path to your CSV file
csv_file = "charge_density/trajectory_points.csv"

# Lists to hold coordinates
x_vals = []
y_vals = []
z_vals = []

# Read the CSV file
with open(csv_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        x_vals.append(float(row["x"]))
        y_vals.append(float(row["y"]))
        z_vals.append(float(row["z"]))

# Create the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_vals, y_vals, z_vals, color='blue', marker='o', label='Electrons')

# Axis labels and title
ax.set_xlabel("x [cm]")
ax.set_ylabel("y [cm]")
ax.set_zlabel("z [cm]")
ax.set_title("Electron Position : Bottom GEM 3 (2 atm)")

# Define GEM layer z-positions (adjust these to your geometry)
gem_layer_positions = {
    "GEM 1": -0.1,
    "GEM 2": 0,
    "GEM 3": 0.2
}

# Create planes for each GEM layer
x_range = np.linspace(min(x_vals)-0.05, max(x_vals)+0.05, 10)
y_range = np.linspace(min(y_vals)-0.05, max(y_vals)+0.05, 10)
X, Y = np.meshgrid(x_range, y_range)

for name, z_pos in gem_layer_positions.items():
    Z = np.full_like(X, z_pos)
    ax.plot_surface(X, Y, Z, alpha=0.2, label=name, color='gray')
    #ax.text2D(0.02, 0.95 - 0.05 * list(gem_layer_positions.keys()).index(name),
              #f'{name} at z={z_pos:.2f} cm', transform=ax.transAxes)

plt.tight_layout()
plt.savefig("3dplot")
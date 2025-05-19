import csv
import matplotlib.pyplot as plt

# === Path to your CSV file ===
csv_file = "charge_density/trajectory_points.csv"

# === Read x and z coordinates from the CSV ===
x_vals = []
z_vals = []

with open(csv_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        x_vals.append(float(row["x"]))
        z_vals.append(float(row["z"]))

# === Define GEM layer Z-positions ===
gem_layer_positions = {
    "GEM 1": -0.1,
    "GEM 2": 0,
    "GEM 3": 0.2
}

# === Create the X-Z plot ===
plt.figure(figsize=(8, 6))

# Plot electron positions
plt.scatter(x_vals, z_vals, color='blue', s=10, label='Electrons')

# Plot GEM layers
for name, z_pos in gem_layer_positions.items():
    plt.axhline(z_pos, color='gray', linestyle='--', alpha=0.7)
    plt.text(min(x_vals), z_pos + 0.002, name, verticalalignment='bottom', color='black')

# Labels and title
plt.xlabel("x [cm]")
plt.ylabel("z [cm]")
plt.title("x-z : GEM 3 (2 atm)")
plt.grid(True)
plt.tight_layout()

# Optional: flip Z axis (common in drift chambers)
plt.gca().invert_yaxis()

plt.savefig("xz_projection")
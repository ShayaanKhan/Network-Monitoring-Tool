import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file into a pandas DataFrame
csv_file_path = "logs/captured_packets.csv"  # Adjust the path to your CSV file
df = pd.read_csv(csv_file_path)

# Extract source and destination IP addresses from the DataFrame
source_ips = df["Source IP"]
destination_ips = df["Destination IP"]

# Create a cross-tabulation (crosstab) of IP address occurrences
cross_tab = pd.crosstab(source_ips, destination_ips)

# Convert the cross-tabulation to a numpy array for heatmap
heatmap_data = cross_tab.to_numpy()

# Create the heatmap
plt.figure(figsize=(10, 8))
plt.imshow(heatmap_data, cmap="viridis", interpolation="nearest")
plt.colorbar(label="Packet Count")
plt.title("Network Traffic Heatmap")
plt.xlabel("Destination IP Addresses")
plt.ylabel("Source IP Addresses")

# Set tick labels to match the IP addresses
plt.xticks(
    np.arange(len(destination_ips.unique())),
    destination_ips.unique(),
    rotation="vertical",
)
plt.yticks(np.arange(len(source_ips.unique())), source_ips.unique())

# Display the heatmap
plt.tight_layout()
plt.show()

import pandas as pd
from pyvis.network import Network
import os

# Read the CSV file into a pandas DataFrame
csv_file_path = "logs/captured_packets.csv"  # Adjust the path to your CSV file
df = pd.read_csv(csv_file_path)

# Create an interactive network using pyvis
net = Network(notebook=True)
net.barnes_hut(gravity=-5000, central_gravity=0.3, spring_length=250)

# Add nodes and edges from the DataFrame
source_ips = df["Source IP"]
destination_ips = df["Destination IP"]
edges = zip(source_ips, destination_ips)
for src, dest in edges:
    net.add_node(src, label=src, font_size=500)  # Increase fontsize for source nodes
    net.add_node(dest, label=dest, font_size=500)  # Increase fontsize for destination nodes
    net.add_edge(src, dest)

# Define the path to save the HTML file within the "logs" folder
html_file_path = os.path.join("logs", "interactive_graph_with_labels.html")

# Save and show the interactive graph
net.save_graph(html_file_path)

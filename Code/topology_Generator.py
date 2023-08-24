from pyvis.network import Network
import csv

def generate_topology_from_csv(csv_file_path, output_html):
    # Create a Network object
    network = Network(notebook=True)

    # Read data from the CSV file and create nodes and edges
    with open(csv_file_path, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            src_ip = row["Source IP"]
            dst_ip = row["Destination IP"]
            network.add_node(src_ip)
            network.add_node(dst_ip)
            network.add_edge(src_ip, dst_ip)

    # Display the network topology visualization
    network.show(output_html)

if __name__ == "__main__":
    csv_file_path = "logs/captured_packets.csv"
    output_html = "logs/network_topology.html"
    generate_topology_from_csv(csv_file_path, output_html)

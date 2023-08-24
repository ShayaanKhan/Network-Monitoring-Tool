from Code.packet_Capture import *

# from Code.heatmap_Generator import *
# from Code.network_Attack import *
from Code.system_Check import *
from Code.topology_Generator import *
from Code.traffic_Analysis import *


# Global declarations #

# ----------From Packet Capture---------- #

logs_folder = "logs"
if not os.path.exists(logs_folder):
    os.makedirs(logs_folder)

# ---------------------------------------- #


# ----------From Topology Generator---------- #

csv_file_path = "logs/captured_packets.csv"
output_html = "logs/network_topology.html"

# ---------------------------------------- #


# ----------From Traffic analysis---------- #
data = load_packet_data(csv_file_path)
time_interval = 1  # Interval in seconds
subnet = "192.168.0."

# ---------------------------------------- #


# Function calls #

# ----------System Check---------- #

online_check()

# ---------------------------------------- #


# ----------Packet Capture---------- #

try:
    print("Packet capturing has started")
    sniff(filter="", prn=packet_handler)
except KeyboardInterrupt:
    pass
print("Packet capturing stopped.")

# ---------------------------------------- #


# ----------Topology generator---------- #

generate_topology_from_csv(csv_file_path, output_html)

# ---------------------------------------- #


# ----------Traffic Analysis---------- #

traffic_volume, sender_bytes, receiver_bytes = analyze_traffic(
    data, time_interval, subnet
)
visualize_traffic_trend(traffic_volume, data)
visualize_top_senders_receivers(sender_bytes, receiver_bytes)

# ---------------------------------------- #

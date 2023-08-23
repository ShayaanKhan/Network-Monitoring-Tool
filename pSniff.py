from scapy.all import sniff, IP, TCP, UDP, Ether
import csv
import os
from datetime import datetime

def get_protocol_name(proto_num):
    # Define a dictionary to map protocol numbers to protocol names
    protocol_names = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
        # Add more protocol mappings as needed
    }
    return protocol_names.get(proto_num, "Unknown")

def packet_handler(packet):
    protocol_name = "Unknown"
    if IP in packet:
        protocol_num = packet[IP].proto
        protocol_name = get_protocol_name(protocol_num)

        # Extract attributes based on the protocol
        if protocol_name == "TCP":
            protocol_info = packet[TCP]
            source_port = protocol_info.sport
            destination_port = protocol_info.dport
            flags = protocol_info.flags
        elif protocol_name == "UDP":
            protocol_info = packet[UDP]
            source_port = protocol_info.sport
            destination_port = protocol_info.dport
            flags = ""
        else:
            source_port = ""
            destination_port = ""
            flags = ""

        # Extract Ethernet details
        if Ether in packet:
            src_mac = packet[Ether].src
            dst_mac = packet[Ether].dst
        else:
            src_mac = ""
            dst_mac = ""

        # Extract other attributes
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        # Append packet attributes to the CSV file
        csv_file_path = os.path.join("logs", "captured_packets.csv")
        with open(csv_file_path, mode="a", newline="") as csv_file:
            fieldnames = [
                "Time", "Source MAC", "Destination MAC",
                "Source IP", "Destination IP", "Protocol",
                "Source Port", "Destination Port", "Flags"
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if os.path.getsize(csv_file_path) == 0:
                writer.writeheader()

            packet_info = {
                "Time": time,
                "Source MAC": src_mac,
                "Destination MAC": dst_mac,
                "Source IP": src_ip,
                "Destination IP": dst_ip,
                "Protocol": protocol_name,
                "Source Port": source_port,
                "Destination Port": destination_port,
                "Flags": flags
            }
            writer.writerow(packet_info)

# Create a directory if it doesn't exist
logs_folder = "logs"
if not os.path.exists(logs_folder):
    os.makedirs(logs_folder)


# MAIN IS THIS #

# Start packet capturing
print("Real-time packet capturing started. Press Ctrl+C to stop...")
try:
    sniff(filter="", prn=packet_handler)
except KeyboardInterrupt:
    pass

print("Packet capturing stopped.")

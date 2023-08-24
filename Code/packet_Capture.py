from scapy.all import sniff, IP, TCP, UDP, Ether
import csv
import os
import socket
import time


def get_protocol_name(proto_num):
    protocol_names = {
        1: "ICMP",
        6: "TCP",
        17: "UDP",
    }
    return protocol_names.get(proto_num, "Unknown")


def packet_handler(packet):
    local_ip = socket.gethostbyname(socket.gethostname())
    if IP in packet and (packet[IP].src == local_ip or packet[IP].dst == local_ip):
        return

    protocol_name = "Unknown"
    if IP in packet:
        protocol_num = packet[IP].proto
        protocol_name = get_protocol_name(protocol_num)

        packet_size = len(packet)

        headers = packet.copy()
        del headers.payload

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

        if Ether in packet:
            src_mac = packet[Ether].src
            dst_mac = packet[Ether].dst
        else:
            src_mac = ""
            dst_mac = ""

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        csv_file_path = os.path.join("logs", f"captured_packets.csv")
        with open(csv_file_path, mode="a", newline="") as csv_file:
            fieldnames = [
                "Time",
                "Source MAC",
                "Destination MAC",
                "Source IP",
                "Destination IP",
                "Protocol",
                "Source Port",
                "Destination Port",
                "Flags",
                "Packet Size",
                "Headers",
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            if os.path.getsize(csv_file_path) == 0:
                writer.writeheader()

            packet_info = {
                "Time": timestamp,
                "Source MAC": src_mac,
                "Destination MAC": dst_mac,
                "Source IP": src_ip,
                "Destination IP": dst_ip,
                "Protocol": protocol_name,
                "Source Port": source_port,
                "Destination Port": destination_port,
                "Flags": flags,
                "Packet Size": packet_size,
                "Headers": headers.summary(),
            }
            writer.writerow(packet_info)

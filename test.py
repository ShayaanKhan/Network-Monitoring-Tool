import csv
from scapy.all import sniff, Ether, IP, TCP, UDP
import time

def initialize_csv():
    with open('pack_cap.csv', 'w', newline='', encoding='utf-8') as csvfile:
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
            "Headers"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def packet_handler(packet):
    if IP in packet:
        source_mac = packet[Ether].src
        dest_mac = packet[Ether].dst
        source_ip = packet[IP].src
        dest_ip = packet[IP].dst
        protocol = packet[IP].proto
        
        source_port = None
        dest_port = None
        flags = None
        
        if TCP in packet:
            source_port = packet[TCP].sport
            dest_port = packet[TCP].dport
            flags = packet[TCP].flags
        elif UDP in packet:
            source_port = packet[UDP].sport
            dest_port = packet[UDP].dport
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(packet.time))
        
        with open('pack_cap.csv', 'a', newline='', encoding='utf-8') as csvfile:
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
                "Headers"
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writerow({
                "Time": timestamp,
                "Source MAC": source_mac,
                "Destination MAC": dest_mac,
                "Source IP": source_ip,
                "Destination IP": dest_ip,
                "Protocol": protocol,
                "Source Port": source_port,
                "Destination Port": dest_port,
                "Flags": flags,
                "Packet Size": len(packet),
                "Headers": packet.summary()
            })

# Initialize the CSV file with header
initialize_csv()

# Sniff packets on the network
sniff(prn=packet_handler, filter="ip")

# You can stop the packet capturing after a certain time or condition
# sniff(prn=packet_handler, filter="ip", timeout=60)

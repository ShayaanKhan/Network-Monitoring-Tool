from scapy.all import ARP, Ether, srp
import csv
import os
from datetime import datetime


def online_check():
    subnet = "192.168.0.1/24"
    # Create an ARP request packet
    arp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=subnet)

    # Send and receive ARP responses
    result = srp(arp_request, timeout=2, verbose=False)[0]

    # Prepare data for sorting
    online_hosts = []
    offline_hosts = []

    # Sort the responses into online and offline hosts
    for sent, received in result:
        ip = received[ARP].psrc
        mac = received[ARP].hwsrc

        if received[ARP].op == 2:  # ARP Reply
            online_hosts.append((ip, mac))
        else:
            offline_hosts.append((ip, mac))

    # Create a directory if it doesn't exist
    logs_folder = "logs"
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Construct the filename
    filename = f"{logs_folder}/log_{len(online_hosts)}_{timestamp}.csv"

    # Write the results to the CSV file
    with open(filename, mode="w", newline="") as csv_file:
        fieldnames = ["Status", "IP Address", "MAC Address"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for ip, mac in online_hosts:
            writer.writerow({"Status": "Online", "IP Address": ip, "MAC Address": mac})

        for ip, mac in offline_hosts:
            writer.writerow({"Status": "Offline", "IP Address": ip, "MAC Address": mac})

    # return f"Results saved to {filename}"


# Example usage
# result_message = online_check()
# print(result_message)

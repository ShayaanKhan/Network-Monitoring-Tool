import threading
import csv
import socket
from scapy.all import sniff, IP
from datetime import datetime

class NetworkMonitor:
    def __init__(self):
        self.capturing = False
        self.packet_data = []
        self.interface = 'Wi-Fi'  # Replace with your WiFi adapter's interface
        self.capture_thread = None

    def packet_handler(self, packet):
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            src_name = self.resolve_dns(src_ip)
            dst_name = self.resolve_dns(dst_ip)
            self.packet_data.append((src_ip, src_name, dst_ip, dst_name))
            self.display_packet(src_ip, src_name, dst_ip, dst_name)

    def display_packet(self, src_ip, src_name, dst_ip, dst_name):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Source: {src_ip} ({src_name}) -> Destination: {dst_ip} ({dst_name})")

    def resolve_dns(self, ip):
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except (socket.herror, socket.gaierror):
            return "Unknown"

    def start_capture(self):
        if not self.capturing:
            self.capturing = True
            self.packet_data = []
            self.capture_thread = threading.Thread(target=self.sniff_packets)
            self.capture_thread.start()
            print("Network monitoring started.")

    def stop_capture(self):
        if self.capturing:
            self.capturing = False
            self.capture_thread.join()
            self.save_packet_data()
            print("Network monitoring stopped.")

    def sniff_packets(self):
        sniff(iface=self.interface, prn=self.packet_handler, stop_filter=self.should_stop_capture)

    def should_stop_capture(self, _):
        return not self.capturing

    def save_packet_data(self):
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d_%H-%M-%S")
        csv_filename = f"logs/packet_log_{formatted_date}.csv"

        with open(csv_filename, "w", newline="") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Source IP", "Source Name", "Destination IP", "Destination Name"])
            for src_ip, src_name, dst_ip, dst_name in self.packet_data:
                csv_writer.writerow([src_ip, src_name, dst_ip, dst_name])

if __name__ == "__main__":
    network_monitor = NetworkMonitor()

    try:
        while True:
            user_input = input("Enter 'start' to start monitoring, 'stop' to stop, or 'exit' to quit: ").strip().lower()
            if user_input == 'start':
                network_monitor.start_capture()
            elif user_input == 'stop':
                network_monitor.stop_capture()
            elif user_input == 'exit':
                break
    except KeyboardInterrupt:
        print("\nStopping network monitoring...")
        network_monitor.stop_capture()
        print("Network monitoring stopped.")

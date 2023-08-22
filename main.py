import sys
import threading
import time
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QTableWidget, QTableWidgetItem
from scapy.all import sniff, IP
from datetime import datetime

class NetworkMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Monitor")
        self.setGeometry(100, 100, 1000, 600)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 10, 780, 580)

        self.start_button = QPushButton("Start Capture", self)
        self.start_button.setGeometry(800, 10, 180, 40)
        self.start_button.clicked.connect(self.start_capture)

        self.stop_button = QPushButton("Stop Capture", self)
        self.stop_button.setGeometry(800, 60, 180, 40)
        self.stop_button.clicked.connect(self.stop_capture)
        self.stop_button.setEnabled(False)

        self.packet_table = QTableWidget(self)
        self.packet_table.setGeometry(10, 60, 780, 580)
        self.packet_table.setColumnCount(2)
        self.packet_table.setHorizontalHeaderLabels(["Source IP", "Destination IP"])

        self.capture_thread = None
        self.capturing = False
        self.packet_data = []

    def packet_handler(self, packet):
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            self.packet_data.append((src_ip, dst_ip))
            self.update_table(src_ip, dst_ip)

    def update_table(self, src_ip, dst_ip):
        row_position = self.packet_table.rowCount()
        self.packet_table.insertRow(row_position)
        self.packet_table.setItem(row_position, 0, QTableWidgetItem(src_ip))
        self.packet_table.setItem(row_position, 1, QTableWidgetItem(dst_ip))

    def start_capture(self):
        self.capturing = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.packet_data = []
        self.packet_table.setRowCount(0)
        self.capture_thread = threading.Thread(target=self.sniff_packets)
        self.capture_thread.start()

    def stop_capture(self):
        self.capturing = False
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.capture_thread.join()
        self.save_packet_data()

    def sniff_packets(self):
        # Replace 'wlan0' with the appropriate interface name for your WiFi adapter
        interface = 'Wi-Fi'
        sniff(iface=interface, prn=self.packet_handler, stop_filter=self.should_stop_capture)

    def should_stop_capture(self, _):
        return not self.capturing

    def save_packet_data(self):
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"logs/packet_log_{formatted_date}.txt"

        with open(log_filename, "w") as file:
            for src_ip, dst_ip in self.packet_data:
                file.write(f"Source IP: {src_ip} --> Destination IP: {dst_ip}\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetworkMonitor()
    window.show()
    sys.exit(app.exec_())

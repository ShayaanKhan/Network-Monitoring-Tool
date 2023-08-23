import sys
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from scapy.all import sniff, IP

class NetworkMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Monitor")
        self.setGeometry(100, 100, 800, 600)
        
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 10, 780, 580)
        
        self.start_sniffing()

    def packet_handler(self, packet):
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            packet_info = f"Source IP: {src_ip} --> Destination IP: {dst_ip}\n"
            self.text_edit.append(packet_info)

    def start_sniffing(self):
        # Replace 'wlan0' with the appropriate interface name for your WiFi adapter
        interface = 'Wi-Fi'
        threading.Thread(target=self.sniff_packets, args=(interface,)).start()

    def sniff_packets(self, interface):
        sniff(iface=interface, prn=self.packet_handler, store=0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetworkMonitor()
    window.show()
    sys.exit(app.exec_())

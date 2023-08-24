from Code.packet_Capture import *

# from Code.heatmap_Generator import *
# from Code.network_Attack import *
from Code.system_Check import *
from Code.topology_Generator import *
from Code.traffic_Analysis import *
from Code.file_Select import *


# Global declarations

# ----------From Packet Capture---------- #
logs_folder = "logs"
if not os.path.exists(logs_folder):
    os.makedirs(logs_folder)

# ----------From Topology Generator---------- #
output_html = "logs/network_topology.html"

# ----------From Traffic analysis---------- #
time_interval = 1  # Interval in seconds
subnet = "192.168.0."

# Function calls


def main():
    print("\nNetwork Analyser Tool v0.1\n")

    # ----------System Check---------- #
    # print("\n\nChecking and storing information of all systems online\n\n")

    # online_check()

    # print("\n CSV stored in the logs folder \n\n\n")

    # ----------Packet Capture---------- #
    while True:
        print("Please specify what action wouuld you like to perform. \n")
        print("\t 1. Start a packet capturing session \n")
        print("\t 2. Load a previously generated packet capture")
        print("\t 3. Generate and view topology \n")
        print("\t 4. Generate and display graphs for traffic analysis \n")
        print("\t 5. Exit")
        option = input("Enter your option by typing the option number:")

        if option == '1':
            count = 1
            print("Begining packet capturing")
            try:
                print("\nPacket capturing has started\n")
                # pack_Cap()
                sniff(filter="", prn=packet_handler)
            except KeyboardInterrupt:
                pass
            while True:
                filename = "logs/captured_packets.csv"
                nf = f"logs/captured_packets_{count}.csv"
                if not os.path.exists(nf):
                    os.rename(filename, nf)
                    break
                else:
                    count = count + 1
            print("\nPacket capturing stopped.\n")

        elif option == '2':
            # ----------File selector---------- #
            filename = select_file()
            if filename:
                print("Returned filepath:", filename)
            else:
                print("No file selected.")

        elif option == '3':
            # ----------File selector---------- #
            filename = select_file()
            if filename:
                print("Returned filepath:", filename)
            else:
                print("No file selected.")

            # ----------Topology generator---------- #
            generate_topology_from_csv(filename, output_html)

        elif option == '4':
            # ----------File selector---------- #
            filename = select_file()
            if filename:
                print("Returned filepath:", filename)
            else:
                print("No file selected.")

            # ----------Traffic Analysis---------- #
            data = load_packet_data(filename)
            traffic_volume, sender_bytes, receiver_bytes = analyze_traffic(
                data, time_interval, subnet
            )
            visualize_traffic_trend(traffic_volume, data)
            visualize_top_senders_receivers(sender_bytes, receiver_bytes)

        elif option == '5':
            exit()

        else:
            print("Please enter the correct option")


if __name__ == "__main__":
    main()
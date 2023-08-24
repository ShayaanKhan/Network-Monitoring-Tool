# Network-Monitoring-Tool
Creating a tool that monitors a network

Things done:
1. system_Check.py:        Discovers which systems are online and saves their IP and MAC address.
2. packet_Capture.py:      Sniffs and captures packets and their metadata.
3. topology_Generator.py:  Generates an interactable network map on as an html file.
4. heatmap_Generator.py:   Generates a heatmap for the Senders and Receivers IP for the number of packets transmitted.


Things to be done:
1. traffic_Analysis.py:    Analyzes the traffic for performance.
2. network_Attack.py:      Identify patters of network attacks using ML.
3. Establish baseline trends to detect anomalies.
4. Implement IDS.
5. Update the program to work in real-time.
6. Add a GUI  


Details and modifications pending:
----------------------------------
traffic_Analysis.py

Traffic Volume Analysis:
Calculate traffic volume over time intervals (e.g., hours, days). Visualize the traffic trend to identify peak usage periods.

Protocol Distribution:
Analyze the distribution of protocols used in the network traffic. Identify which protocols dominate the traffic and spot anomalies.

Traffic Patterns by Source/Destination:
Identify the most active source and destination IP addresses. Look for communication patterns between specific hosts.

Latency Analysis:
Calculate the time between packets to identify latency and potential bottlenecks. Analyze round-trip times for ICMP packets.

Traffic Distribution by Port:
Analyze the distribution of traffic by source and destination ports. This can help identify which services are heavily used.

Application Identification (Optional):
If possible, use packet payload analysis to identify the applications or services generating the traffic.

Bandwidth Usage:
Estimate bandwidth usage by aggregating packet sizes. Identify which applications or users consume the most bandwidth.

Visualization.
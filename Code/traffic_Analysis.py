import csv
import plotly.graph_objects as go
from datetime import datetime, timedelta


def load_packet_data(file_path):
    data = []
    with open(file_path, mode="r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)
    return data


def analyze_traffic(data, time_interval, subnet):
    traffic_volume = {}
    sender_bytes = {}
    receiver_bytes = {}

    for row in data:
        timestamp = datetime.strptime(row["Time"], "%Y-%m-%d %H:%M:%S")
        time_bucket = timestamp.replace(microsecond=0)  # Remove milliseconds
        time_bucket = time_bucket - timedelta(
            seconds=time_bucket.second % time_interval
        )
        if time_bucket not in traffic_volume:
            traffic_volume[time_bucket] = 0

        packet_size = int(row["Packet Size"])

        sender = row["Source IP"]
        receiver = row["Destination IP"]

        if subnet in sender:
            if sender not in sender_bytes:
                sender_bytes[sender] = 0
            sender_bytes[sender] += packet_size

        if subnet in receiver:
            if receiver not in receiver_bytes:
                receiver_bytes[receiver] = 0
            receiver_bytes[receiver] += packet_size

        traffic_volume[time_bucket] += packet_size

    return traffic_volume, sender_bytes, receiver_bytes


def visualize_traffic_trend(traffic_volume, packet_data):
    timestamps = list(traffic_volume.keys())
    volumes = list(traffic_volume.values())

    trace = go.Scatter(
        x=timestamps,
        y=volumes,
        mode="markers",
        marker=dict(size=10),
        text=[
            f"Time: {ts}<br>Volume: {vol} Bytes<br>Packets: {get_packets_info(ts, packet_data)}"
            for ts, vol in zip(timestamps, volumes)
        ],
        hoverinfo="text",
    )

    layout = go.Layout(
        title="Traffic Trend Based on Packet Volume (Seconds)",
        xaxis=dict(title="Time"),
        yaxis=dict(title="Traffic Volume (Bytes)"),
        hovermode="closest",
    )

    fig = go.Figure(data=[trace], layout=layout)
    fig.show()


def get_packets_info(timestamp, packet_data):
    packets_info = []
    for packet in packet_data:
        packet_time = datetime.strptime(packet["Time"], "%Y-%m-%d %H:%M:%S")
        if packet_time == timestamp:
            packets_info.append(
                f"Sender: {packet['Source IP']}, Receiver: {packet['Destination IP']}"
            )
    return "<br>".join(packets_info)


def visualize_top_senders_receivers(sender_bytes, receiver_bytes):
    top_senders = sorted(sender_bytes.items(), key=lambda x: x[1], reverse=True)[:10]
    top_receivers = sorted(receiver_bytes.items(), key=lambda x: x[1], reverse=True)[
        :10
    ]

    sender_labels = [
        f"{sender}: {bytes_to_human_readable(bytes)}" for sender, bytes in top_senders
    ]
    receiver_labels = [
        f"{receiver}: {bytes_to_human_readable(bytes)}"
        for receiver, bytes in top_receivers
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=sender_labels,
            y=[bytes for sender, bytes in top_senders],
            name="Top Senders",
            text=sender_labels,
            hoverinfo="text",
        )
    )
    fig.add_trace(
        go.Bar(
            x=receiver_labels,
            y=[bytes for receiver, bytes in top_receivers],
            name="Top Receivers",
            text=receiver_labels,
            hoverinfo="text",
        )
    )

    fig.update_layout(
        title="Top Senders and Receivers within Subnet",
        xaxis_title="Node",
        yaxis_title="Bytes",
        barmode="group",
        bargap=0.15,
        bargroupgap=0.1,
    )

    fig.show()


def bytes_to_human_readable(bytes):
    for unit in ["", "KB", "MB", "GB"]:
        if abs(bytes) < 1024.0:
            return "%3.1f %s" % (bytes, unit)
        bytes /= 1024.0
    return "%.1f %s" % (bytes, "TB")

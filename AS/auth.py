import socket
import os

dns_records = {}
DNS_FILE_NAME = "dns.txt"


def find_record_in_file(name):
    try:
        if os.path.exists(DNS_FILE_NAME):
            with open(DNS_FILE_NAME, "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.split(",")
                    if len(parts) == 4:
                        record_type, hostname, ip_address, ttl = parts
                        if record_type == "A" and name == hostname:
                            return f"TYPE=A\nNAME={name}\nVALUE={ip_address}\nTTL={ttl}"
            return "200"
        else:
            return "404: DNS file not found"
    except Exception as e:
        print(f"Error loading DNS records: {e}")
        return "500: Internal server error"

def register_data(data):
    lines = data.splitlines()
    try:
        print("Received data:", lines)
        record_type = lines[0].split("=")[1]
        hostname = lines[1].split("=")[1]
        ip_address = lines[2].split("=")[1]
        ttl = int(lines[3].split("=")[1])
        if record_type == "A":
            with open(DNS_FILE_NAME, "r") as file:
                records = file.readlines()
            updated_records = []
            exists = False
            for r in records:
                parts = r.strip().split(",")
                if len(parts) == 4 and parts[1] == hostname:
                    updated_records.append(f"A,{hostname},{ip_address},{ttl}\n")
                    exists = True
                else:
                    updated_records.append(r)
            if not exists:
                updated_records.append(f"A,{hostname},{ip_address},{ttl}\n")
            with open(DNS_FILE_NAME, "w") as file:
                file.writelines(updated_records)
            return "201: Record created successfully"
        return "400: Invalid record type"
    except Exception as e:
        print(f"Error processing registration: {e}")
        return "400: Internal server error"


def handle_query(data):
    lines = data.splitlines()
    try:
        record_type = lines[0].split("=")[1]
        hostname = lines[1].split("=")[1]
        if record_type == "A":
            return find_record_in_file(hostname)
        else:
            return "400: Invalid record type"
    except Exception as e:
        return "Hostname not found"


def start_authoritative_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind(("0.0.0.0", 53533))
        print("Authoritative Server is running on port 53533...")

        while True:
            data, address = server_socket.recvfrom(1024)
            data = data.decode()
            lines = data.splitlines()
            if len(lines) > 2:
                print("Registering new data")
                response = register_data(data)
            else:
                print("Handling query")
                response = handle_query(data)

            server_socket.sendto(response.encode(), address)


if __name__ == "__main__":
    start_authoritative_server()

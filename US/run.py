from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)


@app.route("/fibonacci", methods=["GET"])
def parse_request():
    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")

    if not hostname or not fs_port or not number or not as_ip or not as_port:
        return jsonify({"error: doesn't have required"}), 400

    fib_ip = query_auth(hostname, as_ip, as_port)
    print(f"printing from user server, fib ip: {fib_ip}, fib port {fs_port}")
    if not fib_ip:
        return jsonify({"error": "Could not resolve hostname"}), 500
    try:
        fib_url = f"http://{fib_ip}:{fs_port}/fibonacci?number={number}"
        print(f"will request fib url: {fib_url}")
        response = requests.get(fib_url)
        print("requested fib url")
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 400


def query_auth(hn, as_ip, as_port):
    dns_query = f"""TYPE=A
    NAME={hn}"""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.sendto(dns_query.encode(), (as_ip, int(as_port)))
        response, _ = udp_socket.recvfrom(1024)
        print(f"Response query is: {response}")
        response_lines = response.decode().splitlines()
        for line in response_lines:
            line = line.strip()
            print(line)
            if line.startswith("VALUE="):
                return line.split("=")[1]
    return None


app.run(host="0.0.0.0", port=8080, debug=True)

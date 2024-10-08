from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)


@app.route("/register", methods=["PUT"])
def register():
    data = request.json
    if not data or not all(k in data for k in ("hostname", "ip", "as_ip", "as_port")):
        return jsonify({"error: doesn't have required"}), 400

    hostname = data["hostname"]
    ip_address = data["ip"]
    as_ip = data["as_ip"]
    as_port = data["as_port"]

    registration = f"""TYPE=A
    NAME={hostname}
    VALUE={ip_address}
    TTL=10"""

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            udp_socket.sendto(registration.encode(), (as_ip, int(as_port)))
            print("Send data to AS")
            return jsonify({"message": f"Registration successful for {hostname} with ip_address {ip_address}"}), 201
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

def calculate(num):
    print(num)
    if num <= 0:
        return 0
    elif num == 1:
        return 1
    else:
        x, y = 0, 1
        for _ in range(2, num + 1):
            temp = x
            x = y
            y = temp + y
        return y

@app.route("/fibonacci", methods=["GET"])
def fibonacci():
    print("received request")
    number = request.args.get("number")
    if not number or not number.isdigit():
        return jsonify({"error": "Invalid or missing 'number' parameter"}), 400

    fib = calculate(int(number))
    return jsonify({"Fibonacci number": fib}), 200

app.run(host="0.0.0.0", port=9090, debug=True)
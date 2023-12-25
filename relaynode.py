import utils
from flask import Flask, request
import socket
import requests

# Setting up the node keys
relay_node_key = b'mfXrVpzghdWnwvBYmjEcAMgd14JD4ZElH0AIQBxo-yk='

app = Flask(__name__)

@app.route('/node/<node_type>', methods=['POST'])
def node(node_type):
    data = request.data
    decreptList = []
    if node_type == 'relay':
        utils.move_package_and_remove_encrepion(relay_node_key,data)

    return "Data received and processed", 200

@app.route('/relay_node', methods=['POST'])
def relay_node():
    encrypted_data = request.data
    re_encrypted_content = utils.decrypt_message(relay_node_key, encrypted_data)
    encrypted = utils.encrypt_message(relay_node_key, re_encrypted_content)
    # Send back to entry node
    utils.forward_message('http://172.17.0.2:5001/entry_node', encrypted)
    return "Relay node forwarded response", 200

# Function to run a node server on a specific port
def run_node(port, node_type):
    print(f"Starting {node_type} node on port {port}")
    app.run(port=port, host="0.0.0.0", debug=False, use_reloader=False)


# Running the nodes in separate threads to avoid port conflicts
client_ip = socket.gethostbyname(socket.gethostname())
print(client_ip)
run_node(5002,'relay')

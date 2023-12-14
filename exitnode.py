import utils
from flask import Flask, request
import requests
import socket

# Setting up the node keys
entry_node_key = b'mtb9sESXDBeNMZcKHTHdRQlxwLGHH_htTvjMbNnK5Zo='
relay_node_key = b'mfXrVpzghdWnwvBYmjEcAMgd14JD4ZElH0AIQBxo-yk='
exit_node_key = b'pfUafqxk18k2eRTyLlyOlye2P5HkLu_UtfGsHdGZBDg='

app = Flask(__name__)

@app.route('/node/<node_type>', methods=['POST'])
def node(node_type):
    data = request.data
    if node_type == 'exit':
        final_message = utils.decrypt_message(exit_node_key, data)
        print(final_message)
        # Fetch website content
        response = requests.get(final_message)
        encrypted_content = utils.encrypt_message(relay_node_key, response.text)

        next_node_url = 'http://172.17.0.3:5002/relay_node'
        # Send back to relay node
        utils.forward_message(next_node_url, encrypted_content)
        return "Exit node processed request", 200
        exit_node(final_message)

    return "Data received and processed", 200

# Function to run a node server on a specific port
def run_node1(port, node_type):
    print(f"Starting {node_type} node on port {port}")
    app.run(port=port, host="0.0.0.0", debug=False, use_reloader=False)


# Running the nodes in separate threads to avoid port conflicts
client_ip = socket.gethostbyname(socket.gethostname())
print(client_ip)
run_node1(5003, 'exit')  # Exit Node

import utils
from flask import Flask, request
import socket


# Setting up the node keys
entry_node_key = utils.not_user_diffie_helman()
relay_node_key = b'mfXrVpzghdWnwvBYmjEcAMgd14JD4ZElH0AIQBxo-yk='
exit_node_key = b'pfUafqxk18k2eRTyLlyOlye2P5HkLu_UtfGsHdGZBDg='
# entry_node_key = utils.generate_key()
# relay_node_key = utils.generate_key()
# exit_node_key = utils.generate_key()

app = Flask(__name__)


@app.route('/node/<node_type>', methods=['POST'])

def node(node_type):
    data = request.data

    if node_type == 'entry':
        decrypted_message = utils.decrypt_message(entry_node_key, data)
        # Forward to relay node
        next_node_url = 'http://172.17.0.3:5002/node/relay'
        utils.forward_message(next_node_url, decrypted_message)

    return "Data received and processed", 200

@app.route('/entry_node', methods=['POST'])
def entry_node():
    encrypted_data = request.data
    re_encrypted_content = utils.decrypt_message(entry_node_key, encrypted_data)

    # Send back to client
    return re_encrypted_content

# Function to run a node server on a specific port
def run_node(port, node_type):
    print(f"Starting {node_type} node on port {port}")
    app.run(port=port, host="0.0.0.0", debug=False, use_reloader=False)


# Running the nodes in separate threads to avoid port conflicts
client_ip = socket.gethostbyname(socket.gethostname())
print(client_ip)

run_node(5001,'entry')

import utils
from flask import Flask, request
import socket
import requests
entry_node_key = utils.not_user_diffie_helman()


# Setting up the node keys


# entry_node_key = utils.generate_key()
# relay_node_key = utils.generate_key()
# exit_node_key = utils.generate_key()

app = Flask(__name__)


@app.route('/node/<node_type>', methods=['POST'])

def node(node_type):

    data = request.data
    decreptList = []
    if node_type == 'entry':
        isDecrept = True
        utils.move_package_and_remove_encrepion(entry_node_key,data)
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


run_node(5001,'entry')

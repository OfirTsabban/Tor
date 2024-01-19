import utils
from flask import Flask, request
import requests
import socket

exit_node_key = utils.not_user_diffie_helman()

app = Flask(__name__)

@app.route('/node/<node_type>', methods=['POST'])
def node(node_type):
    data = request.data
    decreptList = 0
    if node_type == 'exit':
        utils.move_package_and_remove_encrepion(exit_node_key,data)

        #next_node_url = 'http://172.17.0.3:5002/relay_node'
        # Send back to relay node
        #utils.forward_message(next_node_url, encrypted_content)
        return "Exit node processed request", 200
        #exit_node(final_message)

    return "Data received and processed", 200

# Function to run a node server on a specific port
def run_node1(port, node_type):
    print(f"Starting {node_type} node on port {port}")
    app.run(port=port, host="0.0.0.0", debug=False, use_reloader=False)


# Running the nodes in separate threads to avoid port conflicts
client_ip = socket.gethostbyname(socket.gethostname())
print(client_ip)
run_node1(5003, 'exit')  # Exit Node

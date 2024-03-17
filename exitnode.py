import utils
from flask import Flask, request
import requests
import socket


exit_node_key = utils.connect_with_server("server_url","exit")

app = Flask(__name__)

@app.route('/node/<node_type>', methods=['POST'])
def node(node_type):
    data = request.data
    source_ip = request.headers.get('Source-IP')
    decreptList = 0
    if node_type == 'exit':
        answer = utils.move_package_and_remove_encrepion(exit_node_key,data)
        if answer != "":
            utils.move_package_back_and_add_encrepion(exit_node_key,answer,source_ip)
        else:
            while True:
                answer = utils.get_back_the_answer()
                if answer:
                    utils.move_package_back_and_add_encrepion(exit_node_key, answer, source_ip)

    return "Data received and processed", 200

# Function to run a node server on a specific port
def run_node1(port, node_type):
    print(f"Starting {node_type} node on port {port}")
    app.run(port=port, host="0.0.0.0", debug=False, use_reloader=False)


# Running the nodes in separate threads to avoid port conflicts
client_ip = socket.gethostbyname(socket.gethostname())
print(client_ip)
run_node1(5003, 'exit')  # Exit Node

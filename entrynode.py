import utils
from flask import Flask, request
import socket
import requests

app = Flask(__name__)

entry_node_key = utils.connect_with_server("http://10.0.0.15:5000","entry")
print("key - - - - " , entry_node_key)

sender_info = ""

@app.route('/node/<node_type>', methods=['POST'])
def node(node_type):
    global sender_info
    global entry_node_key
    data = request.data
    sender_info = request.headers.get('Sender-Info')
    sender_info = "http://" + str(sender_info) + "/back_way"
    print("sender_info - - - - - " , sender_info)
    if node_type == 'entry':
        headers = {"Sender-Info": "127.0.0.1:5001"}
        answer = utils.move_package_and_remove_encrepion(entry_node_key,data,headers)
        if answer != "":
            response = requests.get(answer).text
            print(response)
            utils.move_package_back_and_add_encrepion(entry_node_key,response,sender_info)
    return "Data received and processed", 200

@app.route('/back_way', methods=['POST'])
def back_way():
    global sender_info
    global entry_node_key
    print("12345678")
    data = request.data
    utils.move_package_back_and_add_encrepion(entry_node_key, data, sender_info)
    return "1"
# Function to run a node server on a specific port
def run_node(port, node_type):
    print(f"Starting {node_type} node on port {port}")
    app.run(port=port, host="0.0.0.0", debug=False, use_reloader=False)

client_ip = socket.gethostbyname(socket.gethostname())
print(client_ip)
run_node(5001, 'entry')

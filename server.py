import socket
import threading
import diffieHelmanHelper
import utils
import sqlite3
import random
from flask import Flask, request
import json


list_of_order = []

#entry_node_url = "http://172.17.0.2:5001/node/entry"
#relay_node_url = "http://172.17.0.3:5002/node/relay"
#exit_node_url = "http://172.17.0.4:5003/node/exit"

entry_node_url = "http://127.0.0.1:5001/node/entry"
relay_node_url = "http://127.0.0.1:5002/node/relay"
exit_node_url = "http://127.0.0.1:5003/node/exit"

app = Flask(__name__)

def initialize_database():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
#    cur.execute("DROP TABLE IF EXISTS users")  # Drop the existing table if it exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            password TEXT,
            key TEXT,
            url TEXT
        )
    """)
    conn.commit()
    conn.close()

def initializeDockers():
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    entry_key = utils.generate_key()
    relay_key = utils.generate_key()
    exit_key = utils.generate_key()
    print(entry_key)
    print(relay_key)
    print(exit_key)
    cur.execute("INSERT INTO users (name, password, key, url) VALUES (?, ?, ?, ?)", ('entry', 'entry', entry_key, entry_node_url))
    con.commit()
    cur.execute("INSERT INTO users (name, password, key, url) VALUES (?, ?, ?, ?)", ('relay', 'relay', relay_key, relay_node_url))
    con.commit()
    cur.execute("INSERT INTO users (name, password, key, url) VALUES (?, ?, ?, ?)", ('exit', 'exit', exit_key, exit_node_url))
    con.commit()
    con.close()
    return '1'  # Registration successful

def is_database_empty():
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    con.close()
    if len(rows) > 0:
        return 0
    return 1

def start_connection():
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)
    return server_socket

def forward_message(data):
    message_recived = False
    fail = False
    packet = create_packet(data)

    conn = start_connection()
    conn.send(packet.encode())

    while message_recived == False:
        data = conn.recv(1024).decode()
        if not data:
            fail = True
            break
        else:
            message_recived = True
    if fail == True:
        data = "couldn't reach the page\n"
    return data


def get_userkey(username):
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute("SELECT key FROM users WHERE name=?", (username,))
    key = cur.fetchone()[0]
    con.close()
    return key

def get_userurl(username):
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute("SELECT url FROM users WHERE name=?", (username,))
    url = cur.fetchone()[0]
    con.close()
    return url


@app.route('/decrypt_packet', methods=['POST'])
def decrypt_packet():
    global list_of_order
    data = request.data
    decrypted_data = None

    # Attempt to decrypt each message with corresponding key and URL
    for order_index in range(len(list_of_order)):
        list_key_and_url = get_key_and_url(list_of_order[2 - order_index])
        data = utils.decrypt_message(list_key_and_url[0], data)

    print(data)
    # Check if decryption was successful
    return data



@app.route('/create_packet', methods=['POST'])
def create_packet():
    global list_of_order
    data = request.json
    target_website = data['website']
    name = data['name']
    dockers = random_order_usernames_with_url()
    list_of_order = dockers
    print(dockers)
    list_key_and_url = get_key_and_url(dockers[0])
    print(list_key_and_url)
    # [key_1,url_1]
    print(type(list_key_and_url[0]))
    target_website_json = json.dumps(target_website)

    # Encrypt the JSON string
    encrypted_message = utils.encrypt_message(list_key_and_url[0], target_website_json.encode('utf-8'))
    print(encrypted_message)
    #one encreption with the first_url key
    argument_list = [encrypted_message,list_key_and_url[1]]
    list_key_and_url = get_key_and_url(dockers[1])
    #[the encrept message, url]
    encrypted_message = utils.encrypt_message(list_key_and_url[0], argument_list)
    #encrept the list from before
    argument_list = [encrypted_message,list_key_and_url[1]]
    list_key_and_url = get_key_and_url(dockers[2])
    print(argument_list)
    print(list_key_and_url[0])
    encrypted_message = utils.encrypt_message(list_key_and_url[0], argument_list)
    data = {
        'first_url': list_key_and_url[1],
        'encrypted_message': encrypted_message.decode(),
    }
    print(data)
    return data


def get_key_and_url(name):
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute("SELECT key, url FROM users WHERE name=?", (name,))
    row = cur.fetchone()
    con.close()
    if row:
        return [row[0], row[1]]
    else:
        return None  # Return None if the name is not found in the database

def get_usernames_with_url():
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute("SELECT name FROM users WHERE url != ''")
    usernames = [row[0] for row in cur.fetchall()]
    con.close()
    return usernames

def random_order_usernames_with_url():
    usernames = get_usernames_with_url()
    random.shuffle(usernames)
    return usernames

    return packet

def diffie_helman(conn):
    conn.send("1".encode())
    P = diffieHelmanHelper.get_P()
    G = diffieHelmanHelper.get_G(P)
    a = diffieHelmanHelper.get_a(P)
    b = pow(G, a) % P
    data = f"P:{P},G:{G},b:{b}"
    conn.send(data.encode())
    data = conn.recv(1024).decode()
    b2 = int(diffieHelmanHelper.get_result(str(data)))
    key = pow(b2, a) % P
    print(key)
    return key

def get_user_info(conn):
    message = "ENTER name: "
    conn.send(message.encode())
    name = conn.recv(1024).decode()
    if not name:
        name = ""
    message = "ENTER password: "
    conn.send(message.encode())
    password = conn.recv(1024).decode()
    if not password:
        password = ""
    return (name, password)

def register_user(username, password, key):
    con = sqlite3.connect("users.db")
    cur = con.cursor()

    # Check if the username already exists
    cur.execute("SELECT * FROM users WHERE name=?", (username,))
    existing_user = cur.fetchone()

    if existing_user:
        con.close()
        return '0'  # User already exists, registration failed
    else:
        cur.execute("INSERT INTO users (name, password, key, url) VALUES (?, ?, ?, ?)", (username, password, key,""))
        con.commit()
        con.close()
        return '1'  # Registration successful

@app.route('/register_user', methods=['POST'])
def register_user_route():
    data = request.json
    username = data['username']
    password = data['password']
    key = data['key']

    response = register_user(username, password, key)
    print(response)
    return response

def login_user(username, password):
    con = sqlite3.connect("users.db")
    cur = con.cursor()

    # Check if the username and password match
    cur.execute("SELECT * FROM users WHERE name=? AND password=?", (username, password))
    matching_user = cur.fetchone()
    con.close()

    if matching_user:
        return '1'  # Login successful
    else:
        return '0'  # Login failed

# Inside the '/login_user' route
@app.route('/login_user', methods=['POST'])
def login_user_route():
    data = request.json
    username = data['username']
    password = data['password']

    print("Received login request:")
    print("Username:", username)
    print("Password:", password)

    response = login_user(username, password)
    return response

# Function to handle Docker node interaction
def handle_docker_node(data):
    # Implement logic to handle Docker node requests
    print("Handling Docker node request:", data)
    return "Docker node request received and processed"

@app.route('/docker_node', methods=['POST'])
def docker_node_route():
    data = request.data
    response = handle_docker_node(data)
    return response

def connect_with_docker(docker_name):
    key = get_userkey(docker_name)  # Replace with your function to get the key
    return key

@app.route('/connect_docker', methods=['POST'])
def connect_docker_route():
    data = request.json
    docker_name = data['docker_name']
    key = connect_with_docker(docker_name)
    print(key)
    return key
    #return {'key': key}

def diffie_helman(conn, docker_name):
    conn.send("1".encode())
    P = diffieHelmanHelper.get_P()
    G = diffieHelmanHelper.get_G(P)
    a = diffieHelmanHelper.get_a(P)
    b = pow(G, a) % P
    data = f"P:{P},G:{G},b:{b}"
    conn.send(data.encode())
    data = conn.recv(1024).decode()
    b2 = int(diffieHelmanHelper.get_result(str(data)))
    key = pow(b2, a) % P

    return key


if __name__ == '__main__':
    initialize_database()
    res = is_database_empty()
    if res == 1:
        initializeDockers()
    # Start the Flask app
    app.run(port=5000, host="0.0.0.0", debug=False, use_reloader=False)

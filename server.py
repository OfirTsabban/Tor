import socket
import threading
import diffieHelmanHelper
import utils
import sqlite3
import random
from flask import Flask, request

app = Flask(__name__)


def initialize_database():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            password TEXT,
            key TEXT
        )
    """)
    conn.commit()
    conn.close()

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

def get_usernames():
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute("SELECT name FROM users")
    usernames = [row[0] for row in cur.fetchall()]
    con.close()
    return usernames

def random_order():
    usernames = get_usernames()
    names = [username[0] for username in usernames]  # Extracting usernames from the list
    return random.sample(names, k=min(3, len(names)))  # Randomly sample up to 3 usernames

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

def create_packet(target_website_path):
    order = random_order()
    packet = target_website_path

    for username in order:
        key = get_userkey(username)
        url = get_userurl(username)
        packet = [utils.decrypt_message(packet, key), url]

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
    message = "ENTER USERNAME: "
    conn.send(message.encode())
    name = conn.recv(1024).decode()
    if not name:
        name = ""
    message = "ENTER PASSWORD: "
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
        cur.execute("INSERT INTO users (name, password, key) VALUES (?, ?, ?)", (username, password, key))
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
    return {'key': key}

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
    # Start the Flask app
    app.run(port=5000, host="0.0.0.0", debug=False, use_reloader=False)

import socket
import threading
import diffieHelmanHelper
import utils
import sqlite3
import DatabaseUtils
import random

def start_connection():
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)
    return server_socket

def handle_client(conn, address):
    print("Connection from: " + str(address))

    con = sqlite3.connect("users.db")
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    if res.fetchone() is None:
        cur.execute("CREATE TABLE users(name, password, key, url)")

    message = "message type:1/HELLO!\nENTER 1 TO CONNECT\nENTER 2 TO REGISTER\n"
    conn.send(message.encode())

    server_menu(conn)

    conn.close()

def server_menu(conn):
    while True:
        choice = conn.recv(1024).decode()
        if not choice:
            break
        if choice != "1" and choice != "2":
            break
        user_info = get_user_info(conn)
        name = user_info[0]
        password = user_info[1]
        if authentication(name, password, choice, conn) == False:
            return "can't connect\n"
    while True:
        web = conn.recv(1024).decode()
        if not web:
            return "couldn't reach the page\n"
        data = forward_message(web)
        conn.send(data.encode())

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

def create_packet(data):
    rout = random_order()
    packet = "message type:2/" + data
    for node in rout:
        key = DatabaseUtils.get_userkey(node)
        url = DatabaseUtils.get_userurl(node)
        packet = "message type:2/" + utils.decrypt(packet, key) + url
    return packet

def random_order():
    usernames = DatabaseUtils.get_usernames()
    names = ""
    for username in usernames:
        names += username[0]
        names += ","
    names = names[:-1]
    names = names.split()
    return random.choices(names, k=3)

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

def authentication(username, password, mode, conn):
    if mode == 1:
        if username in DatabaseUtils.get_usernames():
            if password == DatabaseUtils.get_userpassword(username):
                return True
        return False
    if mode == 2:
        DatabaseUtils.add_user(name, password, diffie_helman(conn), url)
    return True

def server_program():
    server_socket = start_connection()

    while True:
        conn, address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, address))
        client_thread.start()

if __name__ == '__main__':
    server_program()

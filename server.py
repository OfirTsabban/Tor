import socket
import diffieHelmanHelper
import utils
import sqlite3
import DatabaseUtils

def start_connection(): #we need to send data to a specific port & ip so when server becomes multy server it will change
    host = socket.gethostname()
    port = 5000
    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    return conn

def server_program():
    #Creating database
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    if res.fetchone() is None:
        cur.execute("CREATE TABLE users(name, password, key, url)")

    conn = start_connection()
    #needs to be a thread bc its multy server
    print("Connection from: " + str(address))
    message = "message type:1/HELLO!\nENTER 1 TO CONNECT\nENTER 2 TO REGISTER\n"
    conn.send(message.encode())
    server_menu(conn)
    conn.close()  # close the connection

def server_menu(conn): #needs to be on a thread, might have some changes
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
            return "couldnt reach the page\n"
        #open this on a thread
        data = forward_message(web)
        conn.send(data.encode())

def forward_message(data):  #need to get ip & port. this is only on a thread, check and commit
    message_recived = False
    fail = False
    packet = create_packet(data)

    conn = start_connection()
    conn.send(packet.encode())

    while message_recived == False:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            fail = True
            break
        else:
            message_recived = True
    if fail == True:
        data = "couldnt reach the page\n"
    return data

def create_packet(data): #check and commit --- check if need to change url to ip and port
    rout = random_order()
    packet = "message type:2/" + data
    for node in rout:
        key = DatabaseUtils.get_userkey(node)
        url = DatabaseUtils.get_userurl(node)
        packet = "message type:2/" + utils.decrypt(packet, key) + url
    return packet

def random_order(): #check amd commit
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
    conn.send(data.encode())  # send message
    data = conn.recv(1024).decode()  # receive response
    b2 = int(diffieHelmanHelper.get_result(str(data)))
    key = pow(b2, a) % P
    print(key)
    return key

def get_user_info(conn):
    message = "ENTER USERNAME: "
    conn.send(message.encode())
    name = conn.recv(1024).decode()
    if not name:
    # if data is not received break
        name=""
    message= "ENTER PASSWORD: "
    conn.send(message.encode())
    password = conn.recv(1024).decode()
    if not password:
        # if data is not received break
        password=""
    return (name,password)

def authentication(username, password, mode, conn): #check and commit
    if mode == 1:
        if username in DatabaseUtils.get_usernames():
            if password == DatabaseUtils.get_userpassword(username):
                return True
        return False
    if mode == 2:
        DatabaseUtils.add_user(name, password, diffie_helman(conn), url)
    return true
if __name__ == '__main__':
    server_program()

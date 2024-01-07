import socket
import diffieHelmanHelper

#we need to add data base of user id and rather they have a key already.

def server_program():
    no_key = True #change after building db.
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        if no_key == True:
            key = diffie_helman(conn)
        if no_key == False:
            data = forward_message()
        conn.send(data.encode())  # send data to the client
    conn.close()  # close the connection

def forward_message():
    data = "later on"
    return data

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


if __name__ == '__main__':
    server_program()

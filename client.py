import socket
import diffieHelmanHelper

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        if str(data) == "1":
            key = diffie_helman(str(data), client_socket)
            print(key)
        if str(data) == "2":
            packet = client_socket.recv(1024).decode()  # receive response
            data = message_forwarding(packet)
            client_socket.send(data.encode())  # send message
        message = input(" -> ")
        print('Received from server: ' + message)  # show in terminal
        #server checks if user already has a key.

    client_socket.close()  # close the connection

def message_forwarding(packet): 
    message_recived = False
    fail = False
    while message_recived == False:
        port = 5000
        #get ip & port from packet
        server_socket = socket.socket()  # get instance
        #look closely. The bind() function takes tuple as argument
        server_socket.bind((host, port))  # bind host address and port together
        server_socket.listen(1)
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                fail = True
                break
            message_recived = True
    if fail == True:
        data = "couldnt reach the page\n"
    return data

def diffie_helman(data, socket):
    data = socket.recv(1024).decode()  # receive response
    P = diffieHelmanHelper.get_P_G(data, "P:")
    G = diffieHelmanHelper.get_P_G(data, "G:")
    a = diffieHelmanHelper.get_a(P)
    b2 = int(diffieHelmanHelper.get_result(data))
    b = pow(G, a) % P
    data = f"P:{P},G:{G},b:{b}"
    socket.send(data.encode())
    return pow(b2, a) % P

if __name__ == '__main__':
    client_program()


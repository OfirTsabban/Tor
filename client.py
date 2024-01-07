import socket
import diffieHelmanHelper

KEY = 0
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
        message = input(" -> ")
        print('Received from server: ' + message)  # show in terminal
        #server checks if user already has a key.

    client_socket.close()  # close the connection

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


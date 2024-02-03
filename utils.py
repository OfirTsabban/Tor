from cryptography.fernet import Fernet
import requests
import pickle
import socket


def move_package_and_remove_encrepion(node_key,data):
    decrypted_message = decrypt_message(node_key, data)
    decreptList = []
    if decrypted_message.type() == str:
        response = requests.get(decrypted_message)
        return response
    elif decrypted_message.type() == list:
        next_node_url = decreptList[0]
        forward_message(next_node_url, decrypted_message)
    else:
        print("error get data")
    return ""

def move_package_back_and_add_encrepion(node_key,data,url):
    message_encrypt = encrypt_message(node_key, data)
    forward_message(url, data)

def generate_key():
    return Fernet.generate_key()

def encrypt_message(key, message):

    # Serialize the message if it's a list
    if isinstance(message, list):
        message = pickle.dumps(message)
    # Ensure the message is in bytes
    if isinstance(message, str):
        message = message.encode()

    f = Fernet(key)
    return f.encrypt(message)

def get_back_the_answer():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    # Listen for incoming connections (max 5 clients in the queue)
    server_socket.listen(5)
    print('Server listening on {}:{}'.format(*server_address))

    while True:
        # Wait for a connection from a client
        print('Waiting for a connection...')
        client_socket, client_address = server_socket.accept()
        print('Accepted connection from {}:{}'.format(*client_address))

        # Handle the client connection (you can customize this part)
        try:
            # Perform operations with the client socket
            # For example, you can receive and send data
            data = client_socket.recv(1024)
            return data
            # Send a response back to the client
            client_socket.sendall(b'Thank you for connecting!')

        finally:
            # Clean up the connection
            client_socket.close()

def decrypt_message(key, message):
    # Ensure the message is in bytes
    if isinstance(message, str):
        message = message.encode()

    f = Fernet(key)
    decrypted_message = f.decrypt(message)

    # Deserialize the message if it was originally a list
    try:
        decrypted_message = pickle.loads(decrypted_message)
    except (pickle.UnpicklingError, TypeError):
        # If it's not a pickled object, continue with decoding
        decrypted_message = decrypted_message.decode()
    return decrypted_message

def forward_message(next_node_url, message):
    response = requests.post(next_node_url, data=message)
    return response.text

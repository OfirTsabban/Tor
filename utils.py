from cryptography.fernet import Fernet, InvalidToken
import requests
import pickle
import socket
import json


def move_package_and_remove_encrepion(node_key, data,headers):
    decrypted_message = decrypt_message(node_key, data)
    print("2222222222222",decrypted_message)
    decreptList = []
    if isinstance(decrypted_message, list):
        next_node_url = decrypted_message[1]
        print("next_node_url - - - ",next_node_url)
        print("decrypted_message - - - ",decrypted_message[0])
        forward_message(next_node_url, decrypted_message[0],headers)
    else:
        try:
            json_object = json.loads(decrypted_message)
            print(json_object)
            print(type(json_object))
            if isinstance(json_object, dict):
                print(1)
                response = json_object.get("googleText")
                print(response)
                return response
            else:
                print("error get data")
        except json.JSONDecodeError:
            print("decrypted_message is not valid ")
    return ""
def move_package_back_and_add_encrepion(node_key,data,url):
    print(url)
    if isinstance(data, str):
        data = data.encode()
    message_encrypt = encrypt_message(node_key, data)
    headers = {'Content-Type': 'application/json'}
    forward_message(url, message_encrypt,headers)

def generate_key():
    return Fernet.generate_key()

def connect_with_server(server_url, docker_name):
    headers = {'Content-Type': 'application/json'}
    data = {'docker_name': docker_name}
    response = requests.post(f"{server_url}/connect_docker", json=data, headers=headers).text
    response = bytes(response, 'utf-8')
    return response

def encrypt_message(key, message):
    # Ensure key is in bytes format
    if isinstance(key, str):
        key = key.encode()

    # Ensure the message is in bytes
    if isinstance(message, list):
        message = pickle.dumps(message)
    elif isinstance(message, str):
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
    print("begin - - - - -- - -- ",message)
    # Ensure the message is in bytes
    if isinstance(message, str):
        message = message.encode()

    try:
        f = Fernet(key)
        decrypted_message = f.decrypt(message)
        print("decrept message - - - - ",decrypted_message)
    except InvalidToken as e:
        print("Invalid token:", e)
        return None
    except Exception as e:
        print("Decryption error:", e)
        return None

    # Deserialize the message if it was originally a list
    try:
        decrypted_message = pickle.loads(decrypted_message)
    except (pickle.UnpicklingError, TypeError):
        # If it's not a pickled object, continue with decoding
        decrypted_message = decrypted_message.decode()
    print("end - - - - - -- - - - - ",decrypted_message)
    return decrypted_message

def forward_message(next_node_url, message,headers):
    response = requests.post(next_node_url, data=message,headers=headers)
    return response.text

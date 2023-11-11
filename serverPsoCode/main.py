import socket
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
host = '10.0.0.20'
port = 12345
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)
print("Connected to port - ", port)

# Accept a connection from a client
client_socket, client_address = server_socket.accept()
print(f"Connected to {client_address}")

# Initialize AES key
password = b"ofirAndOri"
salt = b"aaa"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    iterations=100000,
    salt=salt,
    length=32,
    backend=default_backend()
)
aes_key = kdf.derive(password)

while True:
    # Receive data from the client
    data = client_socket.recv(1024)
    if not data:
        break

    # Decrypt the received data using AES
    iv = data[:16]
    message = data[16:]
    decryptor = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend()).decryptor()
    decrypted_message = decryptor.update(message) + decryptor.finalize()

    print(f"Received (decrypted): {decrypted_message.decode('utf-8')}")

    # Send the received data back to the client
    client_socket.send(data)

# Close the connection
client_socket.close()
server_socket.close()

import socket
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = '10.0.0.20'
server_port = 12345
client_socket.connect((server_address, server_port))
print(f"Connected to {server_address}:{server_port}")

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
    # Get user input
    message = input("Enter a message to send (or 'exit' to quit): ")
    if message.lower() == 'exit':
        break

    # Encrypt the message using AES
    iv = os.urandom(16)
    encryptor = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend()).encryptor()
    encrypted_message = iv + encryptor.update(message.encode('utf-8')) + encryptor.finalize()

    # Send the encrypted message to the server
    client_socket.send(encrypted_message)

# Close the connection
client_socket.close()

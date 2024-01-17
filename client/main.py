import socket
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes



def start_client(server_host='127.0.0.1', server_port=65432):
    # Initialize AES key
    key = b"password"
    salt = b"aaa"
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),iterations=100000,salt=salt,length=32,backend=default_backend())
    aes_key = kdf.derive(key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_host, server_port))
        while True:
            message = input("Enter a website path : ")
            if message.lower() == 'exit':
                break
            # Encrypt the message using AES
            iv = os.urandom(16)
            encryptor = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend()).encryptor()
            encrypted_message = iv + encryptor.update(message.encode('utf-8')) + encryptor.finalize()
            # Send the encrypted message to the server
            s.sendall(encrypted_message)

start_client()

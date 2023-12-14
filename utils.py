from cryptography.fernet import Fernet
import requests
from flask import request

def generate_key():
    return Fernet.generate_key()

def encrypt_message(key, message):
    # Ensure the message is in bytes
    if isinstance(message, str):
        message = message.encode()

    f = Fernet(key)
    return f.encrypt(message)

def decrypt_message(key, message):
    # Ensure the message is in bytes
    if isinstance(message, str):
        message = message.encode()

    f = Fernet(key)
    decrypted_message = f.decrypt(message)

    # Decode the decrypted bytes to a string
    return decrypted_message.decode()

# Function to forward the message to the next node
def forward_message(next_node_url, message):
    response = requests.post(next_node_url, data=message)
    return response.text

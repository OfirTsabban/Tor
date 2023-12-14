from cryptography.fernet import Fernet
import requests
from flask import request

def generate_key():
    return Fernet.generate_key()

def encrypt_message(key, message):
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(key, message):
    f = Fernet(key)
    return f.decrypt(message).decode()

# Function to forward the message to the next node
def forward_message(next_node_url, message):
    response = requests.post(next_node_url, data=message)
    return response.text
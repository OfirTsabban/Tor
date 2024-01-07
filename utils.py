from cryptography.fernet import Fernet
import requests
import pickle

from flask import request

def move_package_and_remove_encrepion(node_key,data):
    decrypted_message = decrypt_message(node_key, data)
    decreptList = []
    if decrypted_message.type() == str:
        response = requests.get(decrypted_message)
        encrypted_answer = encrypt_message(node_key, response.text)
    elif decrypted_message.type() == list:
        next_node_url = decreptList[0]
        forward_message(next_node_url, decrypted_message)
    else:
        print("error get data")

    #countinu send to the next server


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


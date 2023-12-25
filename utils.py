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

# Function to forward the message to the next node
def forward_message(next_node_url, message):
    response = requests.post(next_node_url, data=message)
    return response.text

def prime_checker(p):
    # Checks If the number entered is a Prime Number or not
    if p < 1:
        return -1
    elif p > 1:
        if p == 2:
            return 1
        for i in range(2, p):
            if p % i == 0:
                return -1
            return 1

def get_result(message):
    index = message.find("b:") + 1
    return message[index:]

def primitive_check(g, p, L):
    # Checks If The Entered Number Is A Primitive Root Or Not
    for i in range(1, p):
        L.append(pow(g, i) % p)
    for i in range(1, p):
        if L.count(i) > 1:
            L.clear()
            return -1
        return 1

def get_P(): #getting P
    while 1:
        P = int(input("Enter P : "))
        if prime_checker(P) == -1:
            print("Number Is Not Prime, Please Enter Again!")
            continue
        return P

def get_G(P): #getting G
    l = []
    while 1:
        G = int(input(f"Enter The Primitive Root Of {P} : "))
        if primitive_check(G, P, l) == -1:
            print(f"Number Is Not A Primitive Root Of {P}, Please Try Again!")
            continue
        return G

def get_a(P):
    while 1: #getting secret number a
        a = input(" Enter secret number: ")
        if a >= P:
            print(f"Private Key should Be Less Than {P}!")
            continue
        return a

def get_result(message):
    index = message.find("b:") + 1
    return message[index:]

def get_P_G(message,pg):
     index = message.find(pg) + 1
     message = message[index:]
     index = message.find(",")
     return message[:index]

def not_user_diffie_helman():
    data = request.data
    P = get_P_G(data, "P:")
    G = get_P_G(data, "G:")
    a = get_a(P)
    b2 = int(get_result(b2))
    b = pow(G, a) % P
    message = f"P:{P},G:{G},b:{b}"
    request.post(message)
    return pow(b2, a) % P


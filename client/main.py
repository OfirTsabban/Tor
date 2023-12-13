import socket
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def create_client(server_host='127.0.0.1', server_port=65432):
    # Initialize AES key
    key = get_key(server_host, server_port)
    #########
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),iterations=100000,salt=salt,length=32,backend=default_backend())
    aes_key = kdf.derive(key)
    #########
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

def get_key(server_host, server_port):
    l = []
    while 1: #getting P
        P = int(input("Enter P : "))
        if prime_checker(P) == -1:
            print("Number Is Not Prime, Please Enter Again!")
            continue
        break

    while 1: #getting G
        G = int(input(f"Enter The Primitive Root Of {P} : "))
        if primitive_check(G, P, l) == -1:
            print(f"Number Is Not A Primitive Root Of {P}, Please Try Again!")
            continue
        break

    while 1: #getting secret number
        a = input(" Enter secret number: ")
        if a >= P:
            print(f"Private Key should Be Less Than {P}!")
            continue
        break
    b = pow(G, a) % P
    message = f"P:{P},G:{G},b:{b}"
    # socket connection
    client_socket = socket.socket()
    client_socket.connect((client2_host, client2_port))  # connect
    client_socket.send(message.encode())  # send message
    b2 = client_socket.recv(1024).decode() #recive message
    print('Received from server: ' + b2)  # show in terminal
    b2 = int(get_result(b2))
    key = pow(b2, a) % P
    print(key)
    #finish
    client_socket.close()  # close the connection



create_client()

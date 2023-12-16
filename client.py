import utils
import requests
import socket

# Setting up the node keys


def interactive_client(entry_node_url, entry_node_key):
    print("Interactive Tor-like Client. Type 'exit' to quit.\n")
    while True:
        message = input("Enter path of website : ")
        if message.lower() == 'exit':
            break

        encrypted_message = utils.encrypt_message(exit_node_key, message)
        # Encrypt using relay_node_key
        encrypted_message = utils.encrypt_message(relay_node_key, encrypted_message)
        # Encrypt using entry_node_key
        encrypted_message = utils.encrypt_message(entry_node_key, encrypted_message)
        # Send the encrypted message to the entry node
        response = requests.post(entry_node_url, data=encrypted_message)
        print("Response from entry node:", response.text)

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

def diffie_helman(entry_node_url):
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
    response = requests.post(entry_node_url, data=message)
    print("Response from entry node:", response.text)
    print('Received from server: ' + b2)  # show in terminal
    b2 = int(get_result(response))
    key = pow(b2, a) % P
    print(key)
    return key


# Example usage
# Set the entry node URL and key
entry_node_url = 'http://172.17.0.2:5001/node/entry'
entry_node_key = diffie_helman(entry_node_url)
# Run the interactive client
client_ip = socket.gethostbyname(socket.gethostname())
print(client_ip)

relay_node_key = b'mfXrVpzghdWnwvBYmjEcAMgd14JD4ZElH0AIQBxo-yk='
exit_node_key = b'pfUafqxk18k2eRTyLlyOlye2P5HkLu_UtfGsHdGZBDg='

interactive_client(entry_node_url, entry_node_key)

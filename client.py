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


def diffie_helman(entry_node_url):
    P = utils.get_P()
    G = utils.get_G(P)
    a = utils.get_a(P)
    b = pow(G, a) % P
    message = f"P:{P},G:{G},b:{b}"
    response = requests.post(entry_node_url, data=message)
    print("Response from entry node:", response.text)
    print('Received from server: ' + b2)  # show in terminal
    b2 = int(utils.get_result(response))
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

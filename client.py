import utils
import requests
import socket

# Setting up the node keys
entry_node_key = b'mtb9sESXDBeNMZcKHTHdRQlxwLGHH_htTvjMbNnK5Zo='
relay_node_key = b'mfXrVpzghdWnwvBYmjEcAMgd14JD4ZElH0AIQBxo-yk='
exit_node_key = b'pfUafqxk18k2eRTyLlyOlye2P5HkLu_UtfGsHdGZBDg='


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

# Example usage
# Set the entry node URL and key
entry_node_url = 'http://172.17.0.2:5001/node/entry'
# Run the interactive client
client_ip = socket.gethostbyname(socket.gethostname())
print(client_ip)
interactive_client(entry_node_url, entry_node_key)

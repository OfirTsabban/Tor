import utils
import requests
import socket
import random

first_node_url = 'http://172.17.0.2:5001/node/entry'
second_node_url = 'http://172.17.0.3:5002/node/relay'
third_node_url = 'http://172.17.0.4:5003/node/exit'

entry_node_key = b'mtb9sESXDBeNMZcKHTHdRQlxwLGHH_htTvjMbNnK5Zo='
relay_node_key = b'mfXrVpzghdWnwvBYmjEcAMgd14JD4ZElH0AIQBxo-yk='
exit_node_key = b'pfUafqxk18k2eRTyLlyOlye2P5HkLu_UtfGsHdGZBDg='

list_of_urls = [first_node_url,second_node_url,third_node_url]

# Setting up the node keys

def interactive_client(list_by_order):
    print("Interactive Tor-like Client. Type 'exit' to quit.\n")
    func_paramete_list = []
    while True:
        message = input("Enter path of website : ")
        if message.lower() == 'exit':
            break
        func_paramete_list.append(message)
        if "entry" in list_by_order[0]:
            func_paramete_list.append(entry_node_key)
            func_paramete_list.append(list_of_urls[0])
            #response = makeEncreption(message,entry_node_key,list_of_urls[0])
            if "relay" in list_by_order[1]:
                func_paramete_list.append(relay_node_key)
                func_paramete_list.append(list_of_urls[1])
                func_paramete_list.append(exit_node_key)
                func_paramete_list.append(list_of_urls[2])
                #response = makeEncreption(message,entry_node_key,list_of_urls[0],)
            elif "exit" in list_by_order[1]:
                func_paramete_list.append(exit_node_key)
                func_paramete_list.append(list_of_urls[2])
                func_paramete_list.append(relay_node_key)
                func_paramete_list.append(list_of_urls[1])

        elif "relay" in list_by_order[0]:

            func_paramete_list.append(relay_node_key)
            func_paramete_list.append(list_of_urls[1])

            if "entry" in list_by_order[1]:
                func_paramete_list.append(entry_node_key)
                func_paramete_list.append(list_of_urls[0])
                func_paramete_list.append(exit_node_key)
                func_paramete_list.append(list_of_urls[2])

            elif "exit" in list_by_order[1]:
                func_paramete_list.append(exit_node_key)
                func_paramete_list.append(list_of_urls[2])
                func_paramete_list.append(entry_node_key)
                func_paramete_list.append(list_of_urls[0])

        elif "exit" in list_by_order[0]:

            func_paramete_list.append(exit_node_key)
            func_paramete_list.append(list_of_urls[2])

            if "entry" in list_by_order[1]:
                func_paramete_list.append(entry_node_key)
                func_paramete_list.append(list_of_urls[0])
                func_paramete_list.append(relay_node_key)
                func_paramete_list.append(list_of_urls[1])

            elif "relay" in list_by_order[1]:
                func_paramete_list.append(relay_node_key)
                func_paramete_list.append(list_of_urls[1])
                func_paramete_list.append(entry_node_key)
                func_paramete_list.append(list_of_urls[0])

        response = makeEncreption(func_paramete_list)
        print("Response from entry node:", response.text)

def makeEncreption(func_paramete_list):
        encrypted_message = utils.encrypt_message(func_paramete_list[1], func_paramete_list[0])
        # Encrypt using relay_node_key
        argument_list = [encrypted_message,func_paramete_list[4]]
        encrypted_message = utils.encrypt_message(func_paramete_list[3], argument_list)
        argument_list = [encrypted_message,func_paramete_list[6]]
        # Encrypt using entry_node_key
        encrypted_message = utils.encrypt_message(func_paramete_list[5], argument_list)
        # Send the encrypted message to the entry node
        response = requests.post(func_paramete_list[2], data=encrypted_message)
        return response
# Example usage
# Set the entry node URL and key
# Run the interactive client
#client_ip = socket.gethostbyname(socket.gethostname())
#print(client_ip)

def random_orders_to_nodes():
    my_list = [first_node_url,second_node_url ,third_node_url]
    first_node = random.choice(my_list)
    my_list.remove(first_node)
    second_node = random.choice(my_list)
    my_list.remove(second_node)
    third_node = my_list[0]
    newList = [first_node,second_node,third_node]
    return newList

def diffie_helman(entry_node_url):
    P = utils.get_P()
    G = utils.get_G(P)
    a = utils.get_a(P)
    b = pow(G, a) % P
    message = f"P:{P},G:{G},b:{b}"
    response = requests.post(entry_node_url, data=message)
    print("Response from entry node:", response.text)
    b2 = int(utils.get_result(response))
    print('Received from server: ' + b2)  # show in terminal
    key = pow(b2, a) % P
    print(key)
    return key

if __name__ == "__main__":
    entry_node_key = diffie_helman(list_of_urls[0])
    relay_node_key = diffie_helman(list_of_urls[1])
    exit_node_key = diffie_helman(list_of_urls[2])
    list_by_order = random_orders_to_nodes()
    interactive_client(list_by_order)

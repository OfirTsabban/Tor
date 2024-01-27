import utils
import random
import diffieHelmanHelper
import requests

first_node_url = 'http://172.17.0.2:5001/node/entry'
second_node_url = 'http://172.17.0.3:5002/node/relay'
third_node_url = 'http://172.17.0.4:5003/node/exit'

list_of_urls = [first_node_url,second_node_url,third_node_url]

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

def diffie_helman(data, socket):
    data = socket.recv(1024).decode()  # receive response
    P = diffieHelmanHelper.get_P_G(data, "P:")
    G = diffieHelmanHelper.get_P_G(data, "G:")
    a = diffieHelmanHelper.get_a(P)
    b2 = int(diffieHelmanHelper.get_result(data))
    b = pow(G, a) % P
    data = f"P:{P},G:{G},b:{b}"
    socket.send(data.encode())
    return pow(b2, a) % P

if __name__ == "__main__":
    entry_node_key = list_of_urls[0]
    relay_node_key = list_of_urls[1]
    exit_node_key = list_of_urls[2]
    interactive_client(list_by_order)


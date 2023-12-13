import socket
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def start_server(host='0.0.0.0', port=65432):
    # Initialize AES key
    key = b"password"
    salt = b"aaa"
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),iterations=100000,salt=salt,length=32,backend=default_backend())
    aes_key = kdf.derive(key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # Decrypt the received data using AES
                iv = data[:16]
                message = data[16:]
                decryptor = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend()).decryptor()
                decrypted_message = decryptor.update(message) + decryptor.finalize()
                print(f"Received (decrypted): {decrypted_message.decode('utf-8')}")
                conn.sendall(data)  # Echo back the received data (optional)

def get_key():



start_server()

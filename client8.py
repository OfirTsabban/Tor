import sys
import requests
import tkinter as tk
import webview
from tkinter.scrolledtext import ScrolledText
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript
import socket
import threading
import diffieHelmanHelper
import webbrowser
import json
import utils
import requests
from flask import Flask, request, render_template
from threading import Thread
from tkinter import Tk, Button, Label, Entry, messagebox

gui_stufe = []
name = None
# Server URL
SERVER_URL = "http://10.0.0.15:5000"

app = Flask(__name__)


@app.route('/search', methods=['GET', 'POST'])
def search():
    data = request.json
    serach_text = data["googleText"]
    print("Search text:", serach_text)
    startProcces(data)
    return "Valid response"

@app.route('/back_way', methods=['POST'])
def back_way():
    data = request.data
    data = data.decode()
    headers = {'Content-Type': 'application/json'}
    response = requests.post(SERVER_URL + "/decrypt_packet", json=data, headers=headers).text
    print("secsessssssssssssssss - - - - - -- - -- - ")
    showUI(response)
    return "1"

def showUI(response):
    app = QApplication(sys.argv)
    #content = "<html><body><h1>Hello, World!</h1></body></html>"  # Example content
    viewer = WebsiteViewer(response)
    viewer.show()
    sys.exit(app.exec_())
def startProcces(data):
    global name
    data = {
        'website': data,
        'name': name,
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(SERVER_URL + "/create_packet", json=data, headers=headers).text
    #    response_data = json.loads(response)
    # Assuming 'response' contains the JSON string
    response_data = json.loads(response)

    # Extract values of 'encrypted_message' and 'first_url' from the dictionary
    encrypted_message = response_data['encrypted_message']
    original_encrypted_message = encrypted_message.encode()
    first_url = response_data['first_url']
    print(first_url)
    print(original_encrypted_message)
    headers = {"Sender-Info": "10.0.0.15:8000"}
    utils.forward_message(first_url, original_encrypted_message,headers)


class WebsiteViewer(QMainWindow):
    def __init__(self, content):
        super().__init__()
        self.setWindowTitle("Website Viewer")
        self.resize(800, 600)

        layout = QVBoxLayout()
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.load_website(content)

    def load_website(self, content):
        # Load the website content into the web view
        self.web_view.setHtml(content)
        # Inject JavaScript to capture search query
        self.web_view.page().runJavaScript("""
            document.querySelector('form').addEventListener('submit', function(event) {
                event.preventDefault();
                var searchInput = document.querySelector('input[name="q"]');
                if (searchInput) {
                    window.pywebchannel_1.sendMessage('searchQuery', searchInput.value);
                }
            });
        """)

    @pyqtSlot(str)
    def handle_search_query(self, query):
        print("Search query:", query)


def request_docker_keys():
    # Assuming some logic to request Docker keys from the server
    response = requests.get(f"{SERVER_URL}/get_docker_keys")
    print(response.text)


def second_mode_logic():
    # Add your logic for the second mode here
    print("Second Mode Logic")


def create_registration_window():
    registration_window = Tk()
    registration_window.title("Registration")

    def done_button_click():
        global name
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        registration_window.destroy()  # Destroy the window before further operations

        response = register_user(username, password)
        print(response)
        if response == '1':
            name = username
            open_target_path_screen()
            return "12"
        else:
            messagebox.showerror("Error", "Incorrect fields. Please try again.")

    label = Label(registration_window, text="Register a new account:", font=("Helvetica", 40))
    label.pack()

    username_label = Label(registration_window, text="Username:", font=("Helvetica", 30))
    username_label.pack()

    username_entry = Entry(registration_window, font=("Helvetica", 25))
    username_entry.pack()

    password_label = Label(registration_window, text="Password:", font=("Helvetica", 30))
    password_label.pack()

    password_entry = Entry(registration_window, show="*", font=("Helvetica", 25))
    password_entry.pack()

    done_button = Button(registration_window, text="DONE", command=done_button_click, width=20, height=2)
    done_button.pack()

    registration_window.mainloop()

def register_user(username, password):
    print(f"Registering user: {username}, {password}")

    user_key = utils.generate_key()

    data = {
        'username': username,
        'password': password,
        'type': 'register',
        'key': user_key.decode()
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(SERVER_URL + "/register_user", json=data, headers=headers).text
    return response


def create_login_window():
    login_window = Tk()
    login_window.title("Login")

    def done_button_click():
        global name
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        login_window.destroy()

        response = login_user(username, password)

        if response == '1':
            name = username
            open_target_path_screen()
        else:
            messagebox.showerror("Error", "Incorrect fields. Please try again.")

    label = Label(login_window, text="Login to your account:", font=("Helvetica", 40))
    label.pack()

    username_label = Label(login_window, text="Username:", font=("Helvetica", 30))
    username_label.pack()

    username_entry = Entry(login_window, font=("Helvetica", 25))
    username_entry.pack()

    password_label = Label(login_window, text="Password:", font=("Helvetica", 30))
    password_label.pack()

    password_entry = Entry(login_window, show="*", font=("Helvetica", 25))
    password_entry.pack()

    done_button = Button(login_window, text="DONE", command=done_button_click, width=20, height=2)
    done_button.pack()

    login_window.mainloop()


def login_user(username, password):
    print(f"Logging in user: {username}, {password}")

    data = {
        'username': username,
        'password': password,
        'type': 'login'
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(SERVER_URL + "/login_user", json=data, headers=headers).text
    return response


def open_target_path_screen():
    url = "http://10.0.0.15:9000/"  # Replace with your Flask server's IP address
    webbrowser.register('chrome', None,
    webbrowser.BackgroundBrowser("C:\\Program Files\Google\Chrome\Application\chrome.exe"))
    webbrowser.get('chrome').open(url)

def deleteGui():
    for element in gui_stufe:
        element.destroy()


def open_registration_window():
    deleteGui()
    registration_window = Thread(target=create_registration_window)
    registration_window.start()


def open_login_window():
    deleteGui()
    login_window = Thread(target=create_login_window)
    login_window.start()


def first_mode():
    print("First Mode - GUI, login, register, etc.")

    main_window = Tk()
    main_window.title("Main Window")

    register_button = Button(main_window, text="Register", command=open_registration_window, font=("Helvetica", 80))
    register_button.pack()

    login_button = Button(main_window, text="Login", command=open_login_window, font=("Helvetica", 80))
    login_button.pack()

    if register_button not in gui_stufe:
        gui_stufe.append(register_button)

    if login_button not in gui_stufe:
        gui_stufe.append(login_button)

    if main_window not in gui_stufe:
        gui_stufe.append(main_window)

    main_window.mainloop()


if __name__ == '__main__':
    Thread(target=app.run, kwargs={'port': 8000, 'host': "0.0.0.0", 'debug': False, 'use_reloader': False}).start()
    first_mode()

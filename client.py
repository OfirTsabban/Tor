import socket
import threading
import diffieHelmanHelper
import utils
import requests
from flask import Flask, request, render_template
from threading import Thread
from tkinter import Tk, Button, Label, Entry, messagebox

# Server URL
SERVER_URL = "http://your-server-url"  # Replace with your server's URL

app = Flask(__name__)

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

    # Function to handle the DONE button click
    def done_button_click():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        # Call the registration logic
        response = register_user(username, password)

        if response == '1':
            messagebox.showinfo("Registration Successful", "Registration successful. You can now enter the target path.")
            open_target_path_screen()
            registration_window.destroy()
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
    # Add logic to send registration data to the server
    print(f"Registering user: {username}, {password}")

    # Assuming you want to generate a new key during registration
    user_key = utils.generate_key()

    # Send data to the server for registration, including the new key
    data = {
        'username': username,
        'password': password,
        'type': 'register',
        'key': user_key.decode()  # Convert bytes to string for transmission
    }

    # Send the data to the server and get the response
    response = requests.post(f"{SERVER_URL}/register_user", json=data).text
    return response

def create_login_window():
    login_window = Tk()
    login_window.title("Login")

    # Function to handle the DONE button click
    def done_button_click():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        # Call the login logic
        response = login_user(username, password)

        if response == '1':
            messagebox.showinfo("Login Successful", "Login successful. You can now enter the target path.")
            open_target_path_screen()
            login_window.destroy()
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
    # Add logic to send login data to the server
    print(f"Logging in user: {username}, {password}")

    # Send data to the server for login
    data = {
        'username': username,
        'password': password,
        'type': 'login'
    }

    # Send the data to the server and get the response
    response = requests.post(f"{SERVER_URL}/login_user", json=data).text
    return response

def open_target_path_screen():
    target_path_window = Tk()
    target_path_window.title("Enter Target Path")

    label = Label(target_path_window, text="Enter the target path:")
    label.pack()

    target_path_entry = Entry(target_path_window)
    target_path_entry.pack()

    def done_button_click():
        target_path = target_path_entry.get()
        if not target_path:
            messagebox.showerror("Error", "Please fill in the target path.")
            return

        print("Target Path:", target_path)

        # You can add additional logic here based on the entered target path

        # Close the target path window after DONE
        target_path_window.destroy()

    done_button = Button(target_path_window, text="DONE", command=done_button_click, width=20, height=2)
    done_button.pack()

    target_path_window.mainloop()

def open_registration_window():
    registration_thread = Thread(target=create_registration_window)
    registration_thread.start()

def open_login_window():
    login_thread = Thread(target=create_login_window)
    login_thread.start()

def first_mode():
    print("First Mode - GUI, login, register, etc.")

    main_window = Tk()
    main_window.title("Main Window")

    # Button to open registration window
    register_button = Button(main_window, text="Register", command=open_registration_window, font=("Helvetica", 80))
    register_button.pack()

    # Button to open login window
    login_button = Button(main_window, text="Login", command=open_login_window, font=("Helvetica", 80))
    login_button.pack()

    main_window.mainloop()

if __name__ == '__main__':
    # Start the Flask server for the second mode
    Thread(target=app.run, kwargs={'port': 5001, 'host': "0.0.0.0", 'debug': False, 'use_reloader': False}).start()

    # Call the first mode from the main
    first_mode()

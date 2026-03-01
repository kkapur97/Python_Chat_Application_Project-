import socket
import threading
from tkinter import *

# -----------------------------
# Configuration
# -----------------------------
HOST = "127.0.0.1"  # Server IP
PORT = 12345        # Server Port

# Create socket and connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


# -----------------------------
# Function to receive messages
# -----------------------------
def receive_messages():
    """
    Continuously listens for messages from the server
    and displays them in the chat box.
    """
    while True:
        try:
            message = client.recv(1024).decode("utf-8")

            # If server sends 'bye', close client
            if message.lower() == "bye":
                chat_box.insert(END, "Server ended the chat.\n")
                client.close()
                root.quit()
                break

            chat_box.insert(END, message + "\n")

        except:
            break


# -----------------------------
# Function to send messages
# -----------------------------
def send_message():
    """
    Sends message typed by user to server.
    If user types 'bye', connection closes gracefully.
    """
    message = entry.get()

    if message.lower() == "bye":
        client.send("bye".encode("utf-8"))
        client.close()
        root.quit()
    else:
        client.send(("Client: " + message).encode("utf-8"))

    entry.delete(0, END)


# -----------------------------
# GUI Setup
# -----------------------------
root = Tk()
root.title("Chat Client")

chat_box = Listbox(root, width=50, height=20)
chat_box.pack()

entry = Entry(root, width=40)
entry.pack(side=LEFT, padx=5, pady=5)

send_button = Button(root, text="Send", command=send_message)
send_button.pack(side=LEFT)

# Start receiving thread
threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()


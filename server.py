import socket
import threading
from tkinter import *

# -----------------------------
# Configuration
# -----------------------------
HOST = "127.0.0.1"
PORT = 12345

# Create server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []  # List to store connected clients


# -----------------------------
# Receive messages from clients
# -----------------------------
def receive_messages(client):
    """
    Receives messages from a client and broadcasts them.
    If client sends 'bye', remove and close connection.
    """
    while True:
        try:
            message = client.recv(1024).decode("utf-8")

            if message.lower() == "bye":
                chat_box.insert(END, "A client disconnected.\n")
                clients.remove(client)
                client.close()
                break

            chat_box.insert(END, message + "\n")
            broadcast(message, client)

        except:
            clients.remove(client)
            client.close()
            break


# -----------------------------
# Broadcast message to all clients
# -----------------------------
def broadcast(message, sender):
    """
    Sends message to all connected clients
    except the sender.
    """
    for client in clients:
        if client != sender:
            client.send(message.encode("utf-8"))


# -----------------------------
# Accept new client connections
# -----------------------------
def accept_connections():
    """
    Continuously accepts new clients
    and starts a thread for each.
    """
    while True:
        client, addr = server.accept()
        chat_box.insert(END, f"Connected: {addr}\n")
        clients.append(client)

        thread = threading.Thread(target=receive_messages, args=(client,))
        thread.start()


# -----------------------------
# Server GUI Send Message
# -----------------------------
def send_message():
    """
    Allows server to send message to all clients.
    """
    message = entry.get()

    if message.lower() == "bye":
        broadcast("bye", None)
        server.close()
        root.quit()
    else:
        chat_box.insert(END, "Server: " + message + "\n")
        broadcast("Server: " + message, None)

    entry.delete(0, END)


# -----------------------------
# GUI Setup
# -----------------------------
root = Tk()
root.title("Chat Server")

chat_box = Listbox(root, width=50, height=20)
chat_box.pack()

entry = Entry(root, width=40)
entry.pack(side=LEFT, padx=5, pady=5)

send_button = Button(root, text="Send", command=send_message)
send_button.pack(side=LEFT)

threading.Thread(target=accept_connections, daemon=True).start()

root.mainloop()
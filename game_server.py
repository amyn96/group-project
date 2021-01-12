import tkinter as tk
from tkinter import *
import socket
import threading
import sys
import os
from time import sleep
from PIL import ImageTk, Image


win = tk.Tk()
#win.iconbitmap("icon.ico")
win.configure(background='grey')
win.title("Sever")

#BACKGROUD
bg = ImageTk.PhotoImage(file = "background.jpg")
mylabel = Label(win, image = bg)
mylabel.place(x=0, y=0, relwidth=1,relheight=1)

# START AND STOP BUTTON
topFrame = tk.Frame(win)
btnStart = tk.Button(topFrame, text="Start", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# DISPLAY ADDRESS AND PORT
middleFrame = tk.Frame(win)
lblHost = tk.Label(middleFrame, text = "Address: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# DISPLAY CLIENT LIST
clientFrame = tk.Frame(win)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=10, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

# SERVER
server = None
HOST_ADDR = "192.168.43.50"
HOST_PORT = 8000
client_name = " "
clients = []
clients_names = []
player_data = []


# FUNCTION TO START (SERVER)
def start_server():
    global server, HOST_ADDR, HOST_PORT # code is fine without this
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print (socket.AF_INET)
    print (socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(6)

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Address: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# FUNCTION TO STOP (SERVER)
def stop_server():
    global server
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)
    restart = sys.executable
    os.execl(restart, restart, *sys.argv)

# FUNCTION TO ACCEPT CLIENTS
def accept_clients(the_server, y):
    while True:
        if len(clients) < 2:
            client, addr = the_server.accept()
            clients.append(client)

            # use a thread so as not to clog the gui thread
            threading._start_new_thread(send_receive_client_message, (client, addr))

# FUNCTION TO RECEIVE AND SEND MESSAGE TO CLIENTS
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, player_data, player0, player1

    client_msg = " "

    # WELCOME MESSAGE
    client_name = client_connection.recv(4096)
    client_name.decode()
    if len(clients) < 2:
        message = "welcome1"
        client_connection.send(message.encode())
    else:
        message = "welcome2"
        client_connection.send(message.encode())

    clients_names.append(client_name)
    # UPDATE CLIENT'S LIST
    update_client_names_display(clients_names)

    if len(clients) > 1:
        sleep(1)

        # SEND OPPONENT NAME
        op1 = "opponentName$" + str(clients_names[1].decode())
        op2 = "opponentName$" + str(clients_names[0].decode())
        clients[0].send(op1.encode())
        clients[1].send(op2.encode())

    while True:
        data = client_connection.recv(4096)
        if not data: break

        # GET PLAYER'S CHOICE
        player_choice = data[11:len(data)]

        msg = {
            "choice": player_choice,
            "socket": client_connection
        }

        if len(player_data) < 2:
            player_data.append(msg)

        if len(player_data) == 2:
            # SEND PLAYER1/2 CHOICES
            op1c = "$opponentChoice" + str(player_data[1].get("choice").decode())
            op2c = "$opponentChoice" + str(player_data[0].get("choice").decode())
            print(op1c)
            print(op2c)
            player_data[0].get("socket").send(op1c.encode())
            player_data[1].get("socket").send(op2c.encode())

            player_data = []

    # FIND CLIENT INDEX AND REMOVE THEM FROM LIST
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    client_connection.close()
    # UPDATE CLIENT'S LIST
    update_client_names_display(clients_names)


# RETURN THE CLIENT'S LIST
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# UPDATE CLIENT'S LIST WHEN NEW CLIENT CONNECT OR DISCONNECT
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+b"\n")
    tkDisplay.config(state=tk.DISABLED)



win.mainloop()

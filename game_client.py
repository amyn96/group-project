
import tkinter as tk
from tkinter import *
import socket
from time import sleep
from PIL import ImageTk, Image
import threading

# MAIN GAME'S WINDOW AND VARIABLE
win = tk.Tk()
win.iconbitmap("icon.ico")
win.title("Game Client")
your_name = ""
opponentName = ""
gameRound = 0
game_timer = 4
yourMoves = ""
opponentMoves = ""
TOTAL_NO_OF_ROUNDS = 5
yourScore = 0
opponentScore = 0

# NETWORK
client = None
HOST_ADDR = "192.168.43.50"
HOST_PORT = 8080

#BACKGROUD
bg = ImageTk.PhotoImage(file = "background.jpg")
mylabel = Label(win, image = bg)
mylabel.place(x=0, y=0, relwidth=1,relheight=1)

# MAIN WINDOW
topWelFrame= tk.Frame(win)
lbl_name = tk.Label(topWelFrame, text = "Name:")
lbl_name.pack(side=tk.LEFT)
ent_name = tk.Entry(topWelFrame)
ent_name.pack(side=tk.LEFT)
btn_connect = tk.Button(topWelFrame, text="Connect", command=lambda : connect())
btn_connect.pack(side=tk.LEFT)
topWelFrame.pack(side=tk.TOP)

topMsgFrame = tk.Frame(win)
lineLabel = tk.Label(topMsgFrame, text="________________________________________________________").pack()
welcomeLine = tk.Label(topMsgFrame, text="")
welcomeLine.pack()
LineLable = tk.Label(topMsgFrame, text="_______________________________________________________")
LineLable.pack_forget()
topMsgFrame.pack(side=tk.TOP)

# PLAYER'S NAME SECTION
topFrame = tk.Frame(win)
topLeftFrame = tk.Frame(topFrame, highlightbackground="red", highlightcolor="red", highlightthickness=1)
yourNameLabel = tk.Label(topLeftFrame, text="Your name: " + your_name, font = "Helvetica 13 bold")
opponentNameLabel = tk.Label(topLeftFrame, text="Opponent: " + opponentName)
yourNameLabel.grid(row=0, column=0, padx=5, pady=8)
opponentNameLabel.grid(row=1, column=0, padx=5, pady=8)
topLeftFrame.pack(side=tk.LEFT, padx=(10, 10))

# TIMER SECTIONS
topRightFrame = tk.Frame(topFrame, highlightbackground="red", highlightcolor="red", highlightthickness=1)
gameRoundLabel = tk.Label(topRightFrame, text="ROUND (x) GAME WILL START IN ", foreground="green", font = "Helvetica 14 bold")
timerLabel = tk.Label(topRightFrame, text=" ", font = "Helvetica 24 bold", foreground="green")
gameRoundLabel.grid(row=0, column=0, padx=5, pady=5)
timerLabel.grid(row=1, column=0, padx=5, pady=5)
topRightFrame.pack(side=tk.RIGHT, padx=(10, 10))

topFrame.pack_forget()

middle_frame = tk.Frame(win)

lineLabel = tk.Label(middle_frame, text="___________________________________________________________").pack()
lineLabel = tk.Label(middle_frame, text="**** PLAYERS MOVES ****", font = "Helvetica 13 bold", foreground="blue").pack()
lineLabel = tk.Label(middle_frame, text="___________________________________________________________").pack()

roundFrame = tk.Frame(middle_frame)
roundLabel = tk.Label(roundFrame, text="Round")
roundLabel.pack()
lbl_yourMoves = tk.Label(roundFrame, text="MOVES: " + "None", font = "Helvetica 13 bold")
lbl_yourMoves.pack()
lbl_opponentMoves = tk.Label(roundFrame, text="OPPONNENT MOVES: " + "None")
lbl_opponentMoves.pack()
lbl_result = tk.Label(roundFrame, text=" ", foreground="blue", font = "Helvetica 14 bold")
lbl_result.pack()
roundFrame.pack(side=tk.TOP)

finalFrame = tk.Frame(middle_frame)
lineLabel = tk.Label(finalFrame, text="___________________________________________________________").pack()
finalResultLabel = tk.Label(finalFrame, text=" ", font = "Helvetica 13 bold", foreground="blue")
finalResultLabel.pack()
lineLabel = tk.Label(finalFrame, text="____________________________________________________________").pack()
finalFrame.pack(side=tk.TOP)

middle_frame.pack_forget()

# BUTTONS PART 1
buttonFrame = tk.Frame(win)
prock = Image.open("rockUp.png")
pr = prock.resize((100,100), Image.ANTIALIAS)
photo_rock = ImageTk.PhotoImage(pr)
ppaper = Image.open("paperUp.png")
pp = ppaper.resize((100,100), Image.ANTIALIAS)
photo_paper = ImageTk.PhotoImage(pp)
pscissor = Image.open("scissorUp.png")
ps = pscissor.resize((100,100), Image.ANTIALIAS)
photo_scissors = ImageTk.PhotoImage(ps)

# BUTTONS PART 2
btn_rock = tk.Button(buttonFrame, text="Rock", command=lambda : choice("rock"), state=tk.DISABLED, image=photo_rock)
btn_paper = tk.Button(buttonFrame, text="Paper", command=lambda : choice("paper"), state=tk.DISABLED, image=photo_paper)
btn_scissors = tk.Button(buttonFrame, text="Scissors", command=lambda : choice("scissors"), state=tk.DISABLED, image=photo_scissors)
btn_rock.grid(row=0, column=0)
btn_paper.grid(row=0, column=1)
btn_scissors.grid(row=0, column=2)
buttonFrame.pack(side=tk.BOTTOM)

# GAME MECHANISMS
def game_logic(you, opponent):
    winner = ""
    rock = "rock"
    paper = "paper"
    scissors = "scissors"
    player0 = "you"
    player1 = "opponent"

    if you == opponent:
        winner = "draw"
    elif you == rock:
        if opponent == paper:
            winner = player1
        else:
            winner = player0
    elif you == scissors:
        if opponent == rock:
            winner = player1
        else:
            winner = player0
    elif you == paper:
        if opponent == scissors:
            winner = player1
        else:
            winner = player0
    return winner

# ENABLE OR DISABLE BUTTONS
def enable_disable_buttons(todo):
    if todo == "disable":
        btn_rock.config(state=tk.DISABLED)
        btn_paper.config(state=tk.DISABLED)
        btn_scissors.config(state=tk.DISABLED)
    else:
        btn_rock.config(state=tk.NORMAL)
        btn_paper.config(state=tk.NORMAL)
        btn_scissors.config(state=tk.NORMAL)

# ENTERS NAME AND CONNECT TO GAME
def connect():
    global your_name
    if len(ent_name.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        your_name = ent_name.get()
        yourNameLabel["text"] = "Your name: " + your_name
        connect_to_server(your_name)

# FUNCTION FOR COUTDOWN
def count_down(my_timer, nothing):
    global gameRound
    if gameRound <= TOTAL_NO_OF_ROUNDS:
        gameRound = gameRound + 1

    gameRoundLabel["text"] = "Game round " + str(gameRound) + " starts in"

    while my_timer > 0:
        my_timer = my_timer - 1
        print("game timer is: " + str(my_timer))
        timerLabel["text"] = my_timer
        sleep(1)

    enable_disable_buttons("enable")
    roundLabel["text"] = "Round - " + str(gameRound)
    finalResultLabel["text"] = ""

# FUNCTION FOR PLAYER CHOICE
def choice(arg):
    global yourMoves, client, gameRound
    yourMoves = arg
    lbl_yourMoves["text"] = "Your choice: " + yourMoves

    if client:
        gr = "gameRound"+str(gameRound)+yourMoves
        client.send(gr.encode())
        enable_disable_buttons("disable")

# CONNECT TO SERVER
def connect_to_server(name):
    global client, HOST_PORT, HOST_ADDR, your_name

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST_ADDR, HOST_PORT))
    names = name.encode()
    client.send(names)

    # DISABLE WIDGETS
    btn_connect.config(state=tk.DISABLED)
    ent_name.config(state=tk.DISABLED)
    lbl_name.config(state=tk.DISABLED)
    enable_disable_buttons("disable")

    # START TRHEAD
    threading._start_new_thread(receive_message_from_server, (client, "m"))

# RECEIVE MESSAGE FROM SERVER
def receive_message_from_server(sck, m):
    global your_name, opponentName, gameRound
    global yourMoves, opponentMoves, yourScore, opponentScore

    while True:
        from_server = sck.recv(4096)
        fromS = str(from_server.decode())
        if not from_server: break

        # RECEIVE WELCOME MESSAGE FROM SERVER
        if fromS.startswith("welcome"):
            print("yes")
            if fromS == "welcome1":
                welcomeLine["text"] = "Server says: Welcome " + your_name + "! Waiting for other player"
            elif fromS == "welcome2":
                welcomeLine["text"] = "Server says: Welcome " + your_name + "! Game will start soon"
            LineLable.pack()

        elif fromS.startswith("opponentName$"):
            print(fromS)
            opponentName = fromS.replace("opponentName$", "")
            opponentNameLabel["text"] = "Opponent: " + opponentName
            topFrame.pack()
            middle_frame.pack()

            # WHEN 2 USER CONNECTED, GAME WILL START
            threading._start_new_thread(count_down, (game_timer, ""))
            welcomeLine.config(state=tk.DISABLED)
            LineLable.config(state=tk.DISABLED)

        elif fromS.startswith("$opponentMoves"):
            print("yes 3")
            # GET OPPONENT'S CHOICE
            opponentMoves = fromS.replace("$opponentMoves", "")

            # CONDITION FOR THE GAME MECHANICS
            who_wins = game_logic(yourMoves, opponentMoves)
            round_result = " "
            if who_wins == "you":
                yourScore = yourScore + 1
                round_result = "WIN"
            elif who_wins == "opponent":
                opponentScore = opponentScore + 1
                round_result = "LOSS"
            else:
                round_result = "DRAW"

            # UPDATE THE GUI AFTER MOVES
            lbl_opponentMoves["text"] = "Opponent choice: " + opponentMoves
            lbl_result["text"] = "Result: " + round_result

            # GAME ROUNDS
            if gameRound == TOTAL_NO_OF_ROUNDS:
                # compute final result
                final_result = ""
                color = ""

                # SCORING
                if yourScore > opponentScore:
                    final_result = "(You Won!!!)"
                    color = "yellow"
                elif yourScore < opponentScore:
                    final_result = "(You Lost!!!)"
                    color = "red"
                else:
                    final_result = "(Draw!!!)"
                    color = "black"

                finalResultLabel["text"] = "FINAL RESULT: " + str(yourScore) + " - " + str(opponentScore) + " " + final_result
                finalResultLabel.config(foreground=color)

                enable_disable_buttons("disable")
                gameRound = 0

            # START TIMER
            threading._start_new_thread(count_down, (game_timer, ""))


    sck.close()


win.mainloop()

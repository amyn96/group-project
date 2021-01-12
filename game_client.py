import tkinter as tk
import socket
import threading
import sys
import os
from tkinter import *
from time import sleep
from PIL import ImageTk, Image


# MAIN GAME'S WINDOW AND VARIABLE
win = tk.Tk()
win.iconbitmap("icon.ico")
win.title("Game Client")
playerName = ""
opponentName = ""
gameRound = 0
gTimer = 4
playerMoves = ""
opponentMoves = ""
totalRounds = 5
playerScore = 0
opponentScore = 0

# NETWORK
client = None
HOST_ADDR = "192.168.43.50"
HOST_PORT = 8000

#BACKGROUD
bg = ImageTk.PhotoImage(file = "background.jpg")
mylabel = Label(win, image = bg)
mylabel.place(x=0, y=0, relwidth=1,relheight=1)

# MAIN WINDOW
welcomeTopFrame= tk.Frame(win)
nameLabel = tk.Label(welcomeTopFrame, text = "Name:")
nameLabel.pack(side=tk.LEFT)
getName = tk.Entry(welcomeTopFrame)
getName.pack(side=tk.LEFT, padx = 7)
connectBtn = tk.Button(welcomeTopFrame, text="Connect", command=lambda : connect(), bg = "green")
connectBtn.pack(side=tk.LEFT, padx = 5)
restartBtn = tk.Button(welcomeTopFrame, text="Disconnect", command=lambda : disconnect(), bg = "red")
restartBtn.pack(side=tk.LEFT)
welcomeTopFrame.pack(side=tk.TOP)

MsgTopFrame = tk.Frame(win)
lineLabel = tk.Label(MsgTopFrame, text="______________________________________________________________").pack()
lbl_welcome = tk.Label(MsgTopFrame, text="")
lbl_welcome.pack()
serverLineLabel = tk.Label(MsgTopFrame, text="_______________________________________________________")
serverLineLabel.pack_forget()
MsgTopFrame.pack(side=tk.TOP)

# PLAYER'S NAME SECTION
topFrame = tk.Frame(win)
topLeftFrame = tk.Frame(topFrame, highlightbackground="red", highlightcolor="red", highlightthickness=1)
playerNameLabel = tk.Label(topLeftFrame, text="Your name: " + playerName, font = "Helvetica 13 bold")
Lbl_opponent_name = tk.Label(topLeftFrame,text="Opponent: " + opponentName)
playerNameLabel.grid(row=0, column=0, padx=5, pady=8)
Lbl_opponent_name.grid(row=1, column=0, padx=5, pady=8)
topLeftFrame.pack(side=tk.LEFT, padx=(10, 10))

# TIMER SECTIONS
topRightFrame = tk.Frame(topFrame, highlightbackground="red", highlightcolor="red", highlightthickness=1)
gameRoundLabel = tk.Label(topRightFrame, text="ROUND (x) GAME WILL START IN ", foreground="green", font = "Helvetica 14 bold")
lbl_timer = tk.Label(topRightFrame, text=" ", font = "Helvetica 24 bold", foreground="green")
gameRoundLabel.grid(row=0, column=0, padx=5, pady=5)
lbl_timer.grid(row=1, column=0, padx=5, pady=5)
topRightFrame.pack(side=tk.RIGHT, padx=(10, 10))

topFrame.pack_forget()

middleFrame = tk.Frame(win)

lineLabel = tk.Label(middleFrame, text="___________________________________________________________").pack()
lineLabel = tk.Label(middleFrame, text="**** PLAYERS MOVES ****", font = "Helvetica 13 bold", foreground="blue").pack()
lineLabel = tk.Label(middleFrame, text="___________________________________________________________").pack()

GameRoundFrame = tk.Frame(middleFrame)
lbl_round = tk.Label(GameRoundFrame, text="Round")
lbl_round.pack()
lbl_your_choice = tk.Label(GameRoundFrame, text="MOVES: " + "None", font = "Helvetica 13 bold")
lbl_your_choice.pack()
lbl_opponent_choice = tk.Label(GameRoundFrame, text="OPPONENT'S MOVES: " + "None")
lbl_opponent_choice.pack()
lbl_result = tk.Label(GameRoundFrame, text=" ", foreground="blue", font = "Helvetica 14 bold")
lbl_result.pack()
GameRoundFrame.pack(side=tk.TOP)

finalFrame = tk.Frame(middleFrame)
lineLabel = tk.Label(finalFrame, text="___________________________________________________________").pack()
lbl_final_result = tk.Label(finalFrame, text=" ", font = "Helvetica 13 bold", foreground="blue")
lbl_final_result.pack()
lineLabel = tk.Label(finalFrame, text="____________________________________________________________").pack()
finalFrame.pack(side=tk.TOP)

middleFrame.pack_forget()

# BUTTONS PART 1
btnFrame = tk.Frame(win)
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
btn_rock = tk.Button(btnFrame, text="Rock", command=lambda : move("rock"), state=tk.DISABLED, image=photo_rock)
btn_paper = tk.Button(btnFrame, text="Paper", command=lambda : move("paper"), state=tk.DISABLED, image=photo_paper)
btn_scissors = tk.Button(btnFrame, text="Scissors", command=lambda : move("scissors"), state=tk.DISABLED, image=photo_scissors)
btn_rock.grid(row=0, column=0)
btn_paper.grid(row=0, column=1)
btn_scissors.grid(row=0, column=2)
btnFrame.pack(side=tk.BOTTOM)

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
    global playerName
    if len(getName.get()) < 1:
        tk.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        playerName = getName.get()
        playerNameLabel["text"] = "Your name: " + playerName
        connectServer(playerName)

def disconnect():
    global dis, result
    dis = Toplevel(win)
    dis.title("disconnect")
    dis.geometry("150x100")
    dis.config(bg="white")
    textLabel = tk.Label(finalFrame, text="PLAYER HAS DISCONNECTED!!", bg="white")
    textLabel.pack()
    restart = sys.executable
    os.execl(restart, restart, *sys.argv)

def popMsg(round_result):
    global pop, result
    pop = Toplevel(win)
    pop.title("result")
    pop.geometry("250x150")
    pop.config(bg="white")
    iwin1 = Image.open("win.png")
    iwin2 = iwin1.resize((300, 200), Image.ANTIALIAS)
    result = ImageTk.PhotoImage(iwin2)

    my_frame = Frame(pop)
    my_frame.pack(pady = 5)

    if round_result == "WIN":
        iwin1 = Image.open("win.png")
        iwin2 = iwin1.resize((250, 150), Image.ANTIALIAS)
        result = ImageTk.PhotoImage(iwin2)
    elif round_result == "LOSS":
        iwin1 = Image.open("lose.png")
        iwin2 = iwin1.resize((250, 150), Image.ANTIALIAS)
        result = ImageTk.PhotoImage(iwin2)
    elif round_result == "DRAW":
        iwin1 = Image.open("draw.png")
        iwin2 = iwin1.resize((250, 150), Image.ANTIALIAS)
        result = ImageTk.PhotoImage(iwin2)

    pic = Label(my_frame, image=result, borderwidth=0)
    pic.grid(row=0, column=0, padx=10)

# FUNCTION FOR COUTDOWN
def count_down(my_timer, nothing):
    global gameRound
    if gameRound <= totalRounds:
        gameRound = gameRound + 1

    gameRoundLabel["text"] = "Game round " + str(gameRound) + " starts in"

    while my_timer > 0:
        my_timer = my_timer - 1
        print("game timer is: " + str(my_timer))
        lbl_timer["text"] = my_timer
        sleep(1)

    enable_disable_buttons("enable")
    lbl_round["text"] = "Round - " + str(gameRound)
    lbl_final_result["text"] = ""

# FUNCTION FOR PLAYER CHOICE
def move(arg):
    global playerMoves, client, gameRound
    playerMoves = arg
    lbl_your_choice["text"] = "MOVES: " + playerMoves

    if client:
        gr = "Game_Round"+str(gameRound)+playerMoves
        client.send(gr.encode())
        enable_disable_buttons("disable")

# CONNECT TO SERVER
def connectServer(name):
    global client, HOST_PORT, HOST_ADDR, playerName

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST_ADDR, HOST_PORT))
    names = name.encode()
    client.send(names) # Send name to server after connecting

    # DISABLE WIDGETS
    connectBtn.config(state=tk.DISABLED)
    getName.config(state=tk.DISABLED)
    nameLabel.config(state=tk.DISABLED)
    enable_disable_buttons("disable")

    # START TRHEAD
    threading._start_new_thread(serverMsg,(client, "m"))


# RECEIVE MESSAGE FROM SERVER
def serverMsg(sck, m):
    global playerName, opponentName, gameRound
    global playerMoves, opponentMoves, playerScore, opponentScore

    while True:
        from_server = sck.recv(4096)
        fromS = str(from_server.decode())
        if not from_server: break

        # RECEIVE WELCOME MESSAGE FROM SERVER
        if fromS.startswith("welcome"):
            print("yes")
            if fromS == "welcome1":
                lbl_welcome["text"] = "Server says: Welcome " + playerName + "! Waiting for player 2"
            elif fromS == "welcome2":
                lbl_welcome["text"] = "Server says: Welcome " + playerName + "! Game will start soon"
            serverLineLabel.pack()

        elif fromS.startswith("opponentName$"):
            print(fromS)
            opponentName = fromS.replace("opponentName$", "")
            Lbl_opponent_name["text"] = "Opponent: " + opponentName
            topFrame.pack()
            middleFrame.pack()

            # WHEN 2 USER CONNECTED, GAME WILL START
            threading._start_new_thread(count_down, (gTimer, ""))
            lbl_welcome.config(state=tk.DISABLED)
            serverLineLabel.config(state=tk.DISABLED)

        elif fromS.startswith("$opponentChoice"):
            print("yes 3")
            # GET OPPONENT'S CHOICE
            opponentMoves = fromS.replace("$opponentChoice", "")

            # CONDITION FOR THE GAME MECHANICS
            who_wins = game_logic(playerMoves, opponentMoves)
            round_result = " "
            if who_wins == "you":
                playerScore = playerScore + 1
                round_result = "WIN"
                popMsg(round_result)
            elif who_wins == "opponent":
                opponentScore = opponentScore + 1
                round_result = "LOSS"
                popMsg(round_result)
            else:
                round_result = "DRAW"
                popMsg(round_result)

            # UPDATE THE GUI AFTER MOVES
            lbl_opponent_choice["text"] = "OPPONENT'S MOVE: " + opponentMoves
            lbl_result["text"] = "Result: " + round_result

            # GAME ROUNDS
            if gameRound == totalRounds:
                # compute final result
                final_result = ""
                color = ""

                # SCORING
                if playerScore > opponentScore:
                    final_result = "(You Won!!!)"
                    color = "yellow"
                elif playerScore < opponentScore:
                    final_result = "(You Lost!!!)"
                    color = "red"
                else:
                    final_result = "(Draw!!!)"
                    color = "black"

                # FINAL SCORE
                lbl_final_result["text"] = "FINAL RESULT: " + str(playerScore) + " - " + str(opponentScore) + " " + final_result
                lbl_final_result.config(foreground=color)

                enable_disable_buttons("disable")
                gameRound = 0

            # START TIMER
            threading._start_new_thread(count_down, (gTimer, ""))

    sck.close()

win.mainloop()

import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
#var
username="no"
class var:
    join_msg=" joined"
    debug_usr_name="Client_Test"
    # null is disabled
    # enabled is enabled
    debug_enabled="null"
    seperator="<SEP>"
    serverid="Server"
    leave="left"
init()


colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX,
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX,
    Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX,
    Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW
]


client_color = random.choice(colors)

host_ip=input("Enter host IP: ")
host_port=input("Enter host PORT: ")
serverHost = host_ip
serverPort = int(host_port)
separator_token = var.seperator # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {serverHost}:{serverPort}...")
# connect to the server
s.connect((serverHost, serverPort))
print("[+] Connected.")

if var.debug_enabled != "enabled":
    username = input("Enter name: ")
elif var.debug_enabled == "enabled":
    username=var.debug_usr_name

print("[*] Logged in as", username)
print("Colors: Blue, Cyan, Green, Lime, Magenta, Red, Yellow, White, Anything else = Random")
colorInputFirst = input("Enter color: ")
color_input = colorInputFirst.lower()
if (color_input == "blue"):
    client_color = Fore.BLUE
elif (color_input == "cyan"):
    client_color = Fore.CYAN
elif (color_input == "green"):
    client_color = Fore.GREEN
elif (color_input == "lime"):
    client_color = Fore.LIGHTGREEN_EX
elif (color_input == "magenta"):
    client_color = Fore.MAGENTA
elif (color_input == "red"):
    client_color = Fore.RED
elif (color_input == "yellow"):
    client_color = Fore.YELLOW
elif (color_input == "white"):
    client_color = Fore.WHITE
elif (color_input != "white"):
    client_color = random.choice(colors)
usr_join_msg = f"{username}{var.join_msg}"
date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
usr_join_msg = f"{client_color}[{date_now}] {var.serverid}{separator_token}{usr_join_msg}\n"
s.send(usr_join_msg.encode())


def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    # input message we want to send to the server
    to_send =  input()
    # a way to exit the program
    if to_send.lower() == 'q':
        break
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    to_send = f"{client_color}[{date_now}] {username}{separator_token}{to_send}"
    # finally, send the message
    s.send(to_send.encode())

# close the socket
s.close()


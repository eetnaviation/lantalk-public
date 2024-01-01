import socket
from threading import Thread
import time

host_ip=input("Enter IP: ")
host_port=input("Enter PORT: ")
serverHost = host_ip
serverPort = int(host_port)
enableChatLogging = "y" # Insert "y" for YES and "n" for NO
separator_token = "<SEP>" # Do not modify

f = open("logfile.txt", "a")
f.write("Logfile initialized" + "\n")
f.close()

# initialize list/set of all connected client's sockets
client_sockets = set()
# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((serverHost, serverPort))
# listen for upcoming connections
s.listen(5)
print(f"[*] Listening as {serverHost}:{serverPort}")

def listen_for_client(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            client_sockets.remove(cs)
        else:
            # if we received a message, replace the <SEP>
            # token with ": " for nice printing
            msg = msg.replace(separator_token, ": ")
            if (enableChatLogging == "y"):
                removalValue = 5
                fixedMsg = msg[removalValue:]
                logInput = fixedMsg + "\n"
                f = open("logfile.txt", "a")
                f.write(logInput)
                f.close()
            else:
                print("Server chat logging is disabled")
        # iterate over all connected sockets
        for client_socket in client_sockets:
            # and send the message
            client_socket.send(msg.encode())

while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

while True:
    time.sleep(2)
    print(f"[*] Users lol")

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()
import socket
import threading
import time

IP = '127.0.0.1'
PORT = 1128
my_socket = socket.socket()
my_socket.connect((IP, PORT))
username = ""

def timesEpoch():
    return int(time.time())

def rec():
    global my_socket
    global username
    while True:
        data = my_socket.recv(1024)
        print(data)

t = threading.Thread(target=rec)
t.start()
username = input("Enter your name: ")
my_socket.send(("200" + username).encode())

timeLast = timesEpoch()

while True:
    # if timesEpoch() == timeLast:
    #     timeLast += 1
    my_socket.send(("300" + str(len(username)).zfill(2) + username + input("")).encode())

import socket
import threading

IP = '127.0.0.1'
PORT = 8821

my_socket = socket.socket()
my_socket.connect((IP, PORT))

def job():
      while True:
            my_socket.send(input("Enter a name: ").encode())

t = threading.Thread(target=job)
t.start()

while True:
      print(my_socket.recv(1024).decode())

#300000001905AdminT0018my name is michael

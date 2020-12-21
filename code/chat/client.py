import socket
import threading
import sys

IP = '127.0.0.1'
PORT = 8821

my_socket = socket.socket()
my_socket.connect((IP, PORT))

def job():
      while True:
            my_socket.send(raw_input())
            sys.stdout.write("\033[F") #back to previous line
            sys.stdout.write("\033[K") #clear line

t = threading.Thread(target=job)
t.start()

while True:
      try:
        sys.stdout.write("\033[F") #back to previous line
        sys.stdout.write("\033[K") #clear line
        print(my_socket.recv(1024))
        print("Enter a name: ")
      except:
            pass


# while True:
#     t1 = threading.Thread(target=inputsFun, args=())
#     t2 = threading.Thread(target=recFun, args=())
#     t1.start()
#     t2.start()
#     my_socket.send(name)
#     print("The server sent: " + rec)
#     # t1.join()
#     #data = my_socket.recv(1024)
#     # t2.join()

my_socket.close()

import socket
import threading

IP = '0.0.0.0'
PORT = 1128

server_socket = socket.socket()
server_socket.bind((IP, PORT))
server_socket.listen(1)
print("The server run.")
listClients = []
listThreads = []
dictUsersSocket = {}

def acceptClients():
    global server_socket
    global listClients
    global listThreads

    while True:
        try:
            (client_socket, client_address) = server_socket.accept()
            listClients.append(client_socket)
            listThreads.append(threading.Thread(target=rec, args=(client_socket,)))
            listThreads[len(listThreads) - 1].start()
        except:
            pass

def rec(client):
    global listClients
    global dictUsersSocket
    isExit = False

    while not isExit:
        data = client.recv(1024)
        if len(data) != 0:
            data = data.decode()
            if data[:3] == "200":
                dictUsersSocket[data[3:]] = client
            elif data[:3] == "300":
                data = data[3:]
                lenUsername = int(data[:2])
                data = data[2:]

                username = data[:lenUsername]
                data = data[lenUsername:]

                for user in dictUsersSocket:
                    if user != username:
                        print("data", data)
                        print("user", user)
                        dictUsersSocket[user].send(data.encode())
        else:
            print("logout")
            isExit = True
            userLogout = ""
            for i in dictUsersSocket:
                if dictUsersSocket[i] == client:
                    userLogout = i
            print("logout", userLogout)
            del dictUsersSocket[userLogout]
            listClients.remove(client)


t = threading.Thread(target=acceptClients)
t.start()

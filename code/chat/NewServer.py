import socket
import select

def send_waiting_messages(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        for i in open_client_sockets:
            i.send(data.encode())
        messages_to_send.remove(message)


server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8821))
server_socket.listen(5)


open_client_sockets = []
messages_to_send = []

while True:
    rlist, wlist, xlist = select.select( [server_socket] + open_client_sockets, [], [] )
    for current_socket in rlist:
        if current_socket is server_socket:
            (new_socket, address) = server_socket.accept()
            open_client_sockets.append(new_socket)
            #print("open_client_sockets:", open_client_sockets)
        else:
            try:
                data = current_socket.recv(1024).decode()
            except:
                pass
            if data == "":
                open_client_sockets.remove(current_socket)
                print("Connection with client closed.")
            else:
                print(data)
                messages_to_send.append((current_socket, '' + data))#Hello,
                try:
                    send_waiting_messages(wlist)
                except:
                    pass

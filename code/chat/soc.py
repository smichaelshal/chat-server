import socket
import select

def send_waiting_messages(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        #if client_socket in wlist:
        for i in open_client_sockets:
            i.send(data)
        messages_to_send.remove(message)
        # client_socket.send(data)
        # messages_to_send.remove(message)

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
        else:
            data = current_socket.recv(1024)
            if data == "":
                open_client_sockets.remove(current_socket)
                print "Connection with client closed."
            else:
                print data
                messages_to_send.append((current_socket, '' + data))#Hello,
                send_waiting_messages(wlist)

# import socket
#
# IP = '0.0.0.0'
# PORT = 1129
# exit = False
# ServertRun = False
#
# server_socket = socket.socket()
# server_socket.bind((IP, PORT))
# server_socket.listen(1)
#
# (client_socket, client_address) = server_socket.accept()
#
# client_name = client_socket.recv(1024)
# client_socket.send("Hello "+ client_name)
# client_socket.close()
# server_socket.close()

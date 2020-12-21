import socket
import threading
import time
import copy

def job():
    global serverUDP
    global names
    global data
    while True:
        if len(data) != 0:
            if len(data) >= 1024:
                datas =  data[:1024]
                data = data[1024:]
            else:
                datas = data
                data = b""

            cp = copy.deepcopy(names)
            for i in cp:
                serverUDP.sendto(datas, names[i])
                print(datas)
        else:
            pass

data = b""

serverUDP = socket.socket(type=socket.SOCK_DGRAM)
serverUDP.bind(("0.0.0.0", 6688))
t = threading.Thread(target=job)
names = {}
#data = None
#while not data:

# if data[0] == 49:
#     data = data[1:]
#     names[data] = address
#print("data", data)
#print("names", names)
t.start()
while True:
    data, address = serverUDP.recvfrom(1024)

    if data[0] == 49:
        data = data[1:]
        names[data] = address
    #print("data", data)
    #print("names", names)

serverUDP.close()

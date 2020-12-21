import socket
import threading
import time

def timesEpoch():
    return int(time.time())

def job():
    global clientUDP
    sum = 0
    username = ""
    ot = b""


    while True:
        dataToSend = "0"
        if sum == 0:
            username = input("Enter your name: ")
            ot = username[0]
            clientUDP.send(("1" + username).encode())
        elif len(dataToSend) != 0:
            dataToSend = input("")
            a = ""
            for i in range(0,500):
                a += str(i)

            print("lens", len(a))

            dataToSend = a
            while len(dataToSend) >= 1023:
                clientUDP.send(("2" + dataToSend[:1023]).encode())
                dataToSend = dataToSend[1023:]

            clientUDP.send(("2" + dataToSend).encode("UTF-8"))
            dataToSend = ""

        sum += 1
clientUDP = socket.socket(type=socket.SOCK_DGRAM)
clientUDP.connect(("127.0.0.1", 6688))
t = threading.Thread(target=job)
t.start()
timesLast = timesEpoch()
isOne = True
sumMsg = 0
while True:
    data, address = clientUDP.recvfrom(1024)
    print(len(data))
    sumMsg += len(data)
    timeNow = timesEpoch()
    #print(timeNow, timesLast, timeNow == timesLast)
    # if timeNow == timesLast or isOne:
    #     print(sumMsg)
    #     sumMsg = 0
    #     timesLast = timesEpoch() + 1
    #     isOne = False

clientUDP.close()

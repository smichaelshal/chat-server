import socket
import threading
import copy


IsGrafik = False
lenMaxId = 7
isExitGroup = False
isLoginSuccess = True
IsOut = False
dateMSG = []
day = ""
month = ""
year = ""
idGroupGlobal = 0
otherData = {}

IP = '127.0.0.1'
PORT = 8802


username = ""
listGroup = {}
dataGroups = {}
groupNow = ""

threadIsOpenUDP = threading.Lock()
isOpenUDP = False

#Client UDP
clientUDP = ""
PORT_UDP = 6688
inInCall = False


lenMaxId = 7

def sendCall():
    global clientUDP
    global username
    global inInCall
    global idGroupGlobal

    for i in range(1):#while True:
        dataToSend = "IsUDPClientMSG"
        while len(dataToSend) >= 1024:
            clientUDP.send(creatDataCall(idGroupGlobal, username, dataToSend))
            dataToSend = dataToSend[1024:]
        clientUDP.send(creatDataCall(idGroupGlobal, username, dataToSend))



def creatDataCall(id, username, data):
    global lenMaxId
    lenMaxUsername = 2
    typeMsg = 702
    lenMaxId = 7

    msg = "{}{}{}{}".format(typeMsg,
                        str(id).zfill(lenMaxId),
                        str(len(username)).zfill(lenMaxUsername), username, data) #len username + username

    return msg.encode()

def creatClientUDP():
    global clientUDP
    global IP
    global PORT_UDP
    inInCall = True

    clientUDP = socket.socket(type=socket.SOCK_DGRAM)
    print(0)
    clientUDP.connect((IP, PORT_UDP))
    print(1)

    threadSendCall = threading.Thread(target=sendCall)
    print(2)
    threadSendCall.start()
    print(3)

    while inInCall:
        print(4)
        data, address = clientUDP.recvfrom(1024)
        print(5)
        print(data)
        print(6)

    clientUDP.close()
    # print(7)

isOpenUDP = True
tempIsOpenUDP = True
data = "jjjj"
id = 1
username = "michael"

msgs = creatDataCall(id, username, data)
print(msgs)
msgs = b"700" + msgs[3:]
print(msgs)

if tempIsOpenUDP:
    threadUDPClient = threading.Thread(target=creatClientUDP)
    threadUDPClient.start()

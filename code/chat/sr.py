import threading
import socket
import copy

path = r'/Users/michaelshalitin/Desktop/1/תיכנות/db/DB/'
threadLock = threading.Lock()
dbUsers = []
dbGroups = []
exit = False
isLogin = False
tempClient = 0
getAddress = ""

isJob = False
typeMsg = ""
data = ""
isOpenUDP = False

IP = "0.0.0.0"#socket.gethostname()#
PORT = 8802

#Server UDP
PORT_UDP = 6688
serverUDP = ""
buffer = ""
lenToSend = 1024
lenToRead = 1024


usersIp = {}
groupsData = {}
groupsUsers = {}
usersGroups = {}
newDataGroup = {}
usersSocket = {}# usersSocket[username] = <socket>
idNamesGroup = {}# idNamesGroup[id] = "nameGruop"
onlinUsers = []
onlinUsersGroup = {}
listTempClient = []

#Server UDP
callGrupsUsers = {}# callGrupsUsers[id] = {"username": address} # address = (IP, PORT)
callUsers = {}#callUsers[username] = address # address = (IP, PORT)




#Server
server_socket = socket.socket()
open_client_sockets = []
messages_to_send = []

#Keys

#DB
threadLockDBUsers = threading.Lock()
threadLockDBGroups = threading.Lock()
threadLockDBGroup = threading.Lock()

#Vars
threadLockUsers = threading.Lock()
threadLockGroups = threading.Lock()
threadLockLogin = threading.Lock()


threadLockDictGroup = threading.Lock()
threadLockDictGroupUsers = threading.Lock()
threadLockDictNewDataGroup = threading.Lock()

#Server UDP Keys
threadLockCallUsers = threading.Lock()
threadLockCallGrupsUsers = threading.Lock()
threadLockIsOpenUDP = threading.Lock()
threadLockBuffer = threading.Lock()


def creatServerUDP():
    print("creatServerUDP->>>-")
    global threadLockIsOpenUDP
    global threadLockCallUsers
    global threadLockCallGrupsUsers
    global threadLockBuffer

    global callGrupsUsers
    global callUsers
    global isOpenUDP
    global PORT_UDP
    global IP
    global serverUDP
    global buffer

    global lenToSend
    global lenToRead

    copyIsOpenUDP = False

    with threadLockIsOpenUDP:
        isOpenUDP = True
        if isOpenUDP:
            copyIsOpenUDP = True

    serverUDP = socket.socket(type=socket.SOCK_DGRAM)
    serverUDP.bind((IP, PORT_UDP))

    print("copyIsOpenUDP", copyIsOpenUDP)


    while copyIsOpenUDP:
        print("=")
        getData, getAddress = serverUDP.recvfrom(1024)
        getData = getData.decode()

        threadProcessing = threading.Thread(target=processing, args=(getData,))
        threadProcessing.start()
        #processing(getData)

def creatDataCall(id, username, data):
    global lenMaxId
    lenMaxUsername = 2
    typeMsg = 702
    lenMaxId = 7

    msg = "{}{}{}{}".format(typeMsg,
                        str(id).zfill(lenMaxId),
                        str(len(username)).zfill(lenMaxUsername), username, data) #len username + username

    return msg.encode()


def statusUDP(typeMsg, getData):
    global threadLockCallUsers
    global threadLockCallGrupsUsers
    global callGrupsUsers
    global callUsers

    print(0)
    typeMsg = 700
    getData = "000000107michael"
    global serverUDP
    if typeMsg == 700:
          print("UDP-login")
          idGroup = int(getData[:7])
          getData = getData[7:]

          lenUsername = int(getData[:2])
          getData = getData[2:]

          username = getData[:lenUsername]
          getData = getData[lenUsername:]

          with threadLockCallUsers:
              callUsers[username] = getAddress

          with threadLockCallGrupsUsers:
              try:
                  callGrupsUsers[idGroup][username] = getAddress
              except:
                  callGrupsUsers[idGroup] = {}
                  callGrupsUsers[idGroup][username] = getAddress
    elif typeMsg == 702:
        print("UDP-call")

        idGroup = int(getData[:7])
        getData = getData[7:]

        lenUsername = int(getData[:2])
        getData = getData[2:]

        username = getData[:lenUsername]
        getData = getData[lenUsername:]

        dataToSending = creatDataCall(idGroup, username, getData)

        dictAddressToSend = {}
        with threadLockCallGrupsUsers:
            dictAddressToSend = copy.copy(callGrupsUsers[idGroup])

            for username in dictAddressToSend:
                serverUDP.sendto(dataToSending, dictAddressToSend[username])



def processing(getData):
    typeMsg = int(getData[:3])
    getData = getData[3:]
    print("a-")
    statusUDP(typeMsg, getData)
    print("b-")



print("make call")
tempIsOpenUDP = False
with threadLockIsOpenUDP:
    if isOpenUDP:
        tempIsOpenUDP = isOpenUDP

if not tempIsOpenUDP:
    threadUDPServer = threading.Thread(target=creatServerUDP)
    threadUDPServer.start()
    print("st1")

#Server

import threading
import pandas as pd
import os
import time
import hashlib
import re
import socket
import select
import ast
import copy
import base64

path = r'/Users/michaelshalitin/Desktop/1/תיכנות/db/DB/'
threadLock = threading.Lock()
dbUsers = []
dbGroups = []
exit = False
isLogin = False
tempClient = 0

isJob = False
typeMsg = ""
data = ""
isOpenUDP = False

IP = "10.0.0.14"#socket.gethostname()#
PORT = 8805

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

listClients = []
dictUsersSocket = {}
listClients = []
listThreads = []
dictThreads = {}

sumThreading = 0

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

def getPermission(username):
    global dbUsers
    sum = 0
    index = 0
    for i in dbUsers["username"]:
        if i == username:
            index = sum
        sum += 1

    return dbUsers["permission"][index]

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


    global serverUDP
    if typeMsg == 700 and False:
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
    elif typeMsg == 702 and False:
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
    statusUDP(typeMsg, getData)

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

    while copyIsOpenUDP:
        getData, getAddress = serverUDP.recvfrom(1024)
        getData = getData.decode()

        threadProcessing = threading.Thread(target=processing, args=(getData,))
        threadProcessing.start()
        #processing(getData)


def sendDataUDP():
    global threadLockBuffer
    global threadLockIsOpenUDP

    global buffer
    global serverUDP
    global callGrupsUsers
    global callUsers

    global lenToSend
    global lenToRead

    copyIsSendUDP = False
    copyBufferToSend = ""

    copyLenToSend = lenToSend
    copyLenToRead = lenToRead
    datasToSend = ""

    with threadLockIsOpenUDP:
        if isOpenUDP:
            copyIsSendUDP = True

    with threadLockBuffer:
        copyBufferToSend = buffer

    while copyIsSendUDP:
        lenBuffer = len(copyBufferToSend)
        if lenBuffer != 0:
            if lenBuffer >= 1024:
                pass

def changePassword(username, newPassword):
    global dbUsers
    listPasswords = []
    with threadLockUsers:
        sum = 0
        for i in dbUsers["username"]:
            if i == username:
                index = sum
            sum += 1
        sum = 0
        for i in dbUsers["password"]:
            if sum == index:
                listPasswords.append(newPassword)
            else:
                listPasswords.append(i)
            sum += 1
        dbUsers["password"] = listPasswords
def changeName(OldUsername, newUsername):
    global dbUsers
    global dbGroups
    global groupsUsers
    global usersGroups
    global usersSocket
    global onlinUsers
    global onlinUsersGroup
    sum = 0

    listUsername = []
    with threadLockUsers:
        for i in dbUsers["username"]:
            if i == OldUsername:
                listUsername.append(newUsername)
            else:
                listUsername.append(i)
        dbUsers["username"] = listUsername
    listListUsersGroup = []

    with threadLockGroups:
        for usersGroup in dbGroups["users"]:
            listUsersGroup = []
            for users in  ast.literal_eval(usersGroup):
                if users == OldUsername:
                    listUsersGroup.append(newUsername)
                else:
                    listUsersGroup.append(users)
            listListUsersGroup.append(listUsersGroup)
    dbGroups["users"] = listListUsersGroup

    strUsers = ""
    for i in groupsUsers:
        strUsers = ""
        for j in groupsUsers[i][1]:
            strUsers += j
        strUsers = strUsers.replace(OldUsername, newUsername)
        groupsUsers[i][1] = strUsers

    listUsers = []
    try:
        usersGroups[newUsername] = usersGroups.pop(OldUsername)
    except:
        pass

    try:
        usersSocket[newUsername] = usersSocket.pop(OldUsername)
    except:
        pass

    try:
        onlinUsers[onlinUsers.index(OldUsername)] = newUsername
    except:
        pass
    try:
        onlinUsersGroup[newUsername] = onlinUsersGroup.pop(OldUsername)
    except:
        pass
def changeNameGroup(id, newName):
    global dbGroups
    global groupsUsers
    #usersGroups


    index = 0
    sum = 0
    for i in dbGroups["id"]:
        if i == id:
            index = sum
        sum += 1

    sum = 0
    listNames = []
    for i in dbGroups["group"]:
        if sum == index:
            listNames.append(newName)
        else:
            listNames.append(i)
        sum += 1

    dbGroups["group"] = listNames

    groupsUsers[id][0] = newName

    FindIdGroups()

def job(current_socket):
    global isJob
    global typeMsg
    global data

    isJob = False

    typeMsg = current_socket.recv(3).decode()
    data = current_socket.recv(1024).decode()

    isJob = True

def openData(data):
    isEnd = data[0]
    data = data[1:]
    newData = ""

    while isEnd != "T":
        newData +=  data[:1023]
        data = data[1023:]

        isEnd = data[1]
        data = data[1:]

    lenData = int(data[:4])
    data = data[4:]
    newData += data[:lenData]
    return newData

def listToStr(list, username):
    global dbGroups
    if len(list) == 0:
        return "'04NULL, 4NULL'"
    dict = dictDB(dbGroups, "group", "id")

    data = ""
    lenMaxName = 2
    lenMaxId = 7

    # print("list", list)
    newDict = {}

    for i in list:
        try:
            newDict[i] += 2
        except:
            newDict[i] = 0

        newListIdGroupOfUser = []
        listIdGroupOfUser = dict[i]
        # print("listIdGroupOfUser", listIdGroupOfUser)
        # print("usersGroups", usersGroups)
        # data += "'{}{}{}',".format(str(len(i)).zfill(lenMaxName), i, str(listIdGroupOfUser[0]).zfill(lenMaxId))
        for j in listIdGroupOfUser:
            if j in usersGroups[username]:
                data += "'{}{}{}',".format(str(len(i)).zfill(lenMaxName), i, str(j).zfill(lenMaxId))
            # print(newDict)
            # newDict[i] -= 1


    return data[:-1]
    #data += "'" + i + "'" + ","

def FindIdGroupsToUser(username):
    global groupsUsers
    global usersGroups

    for idGroup in groupsUsers:
        listUsersGroup = groupsUsers[idGroup][1]
        listUsersGroup = ast.literal_eval(listUsersGroup)
        for name in listUsersGroup:
            if name == username:
                try:
                    usersGroups[username].append(idGroup)
                except:
                    usersGroups[username] = []
                    usersGroups[username].append(idGroup)
    return usersGroups

def createResponseGetListGroup(username):
    #get name group and users, generates a message to the server to create a new group
    lenMaxList = 6
    typeMsg = 480
    listGroupsOfUser = FindGroupsToUser(username)
    listGrups = listToStr(listGroupsOfUser, username)
    msg = "{}{}{}".format(typeMsg, str(len(listGrups)).zfill(lenMaxList), listGrups)
    #print(msg)
    Bmsg = msg.encode()
    return Bmsg

def FindGroupsToUser(username):
    global usersGroups
    try:
        a = usersGroups[username][0]
        b = FindNameGroupsToUser(username)
        return b
    except:
        FindIdGroupsToUser(username)
        b = FindNameGroupsToUser(username)
        return b

def FindIdGroups():
    global dbGroups
    global idNamesGroup

    idNamesGroup = dictDB(dbGroups, "id", "group")
    for id in idNamesGroup:
        idNamesGroup[id] = idNamesGroup[id][0]
    return idNamesGroup

def FindNameGroupsToUser(username):
    global usersGroups
    global idNamesGroup
    listNameGruop = []
    try:
        listIdGroup = usersGroups[username]
    except:
        listIdGroup = []


    try:
        listIdGroup = usersGroups[username]
    except:
        return []
    for id in listIdGroup:
        listNameGruop.append(idNamesGroup[id])
    return listNameGruop

def getUsernamePassword(data):
    lenUsername = int(data[:2])
    username =  data[2:lenUsername + 2]
    password_hash = data[lenUsername + 2:]
    return (username, password_hash)

def getListGroups(data):
    lenUsername = int(data[:2])
    username =  data[2:lenUsername + 2]
    return username

#
# def acceptClients():
#     global server_socket
#     global listClients
#     global listThreads
#
#     while not exit:
#         try:
#             (client_socket, client_address) = server_socket.accept()
#             listClients.append(client_socket)
#             listThreads.append(threading.Thread(target=rec, args=(client_socket,)))
#             #listThreads[len(listThreads) - 1].start()
#             for i in listThreads:
#                 try:
#                     i.start()
#                 except:
#                     pass
#         except:
#             pass

def rec(client, numOfThread):#rrrrrrr
    global listClients
    global dictUsersSocket
    global onlinUsersGroup
    global usersSocket
    global onlinUsers

    myUsername = ""

    isExitClient = False

    while not isExitClient and not exit:
        try:
            typeMsg = client.recv(3).decode()
            data = client.recv(1024).decode()
        except:
            pass
        if len(data) != 0:
            try:
                typeMsg = int(typeMsg)
                valStatus = status(typeMsg, data, client)
                if typeMsg == 200 or typeMsg == 470 or (typeMsg == 450 and valStatus != None):#ppppp
                    myUsername = valStatus
                # elif typeMsg == 450:
                #
                #     dataTemp = data
                #     print(0)
                #     lenOldUsernameTempTemp = int(dataTemp[:2])
                #     print(1)
                #     dataTemp = dataTemp[2:]
                #     print(2)
                #
                #     OldUsernameTemp = dataTemp[:lenOldUsernameTempTemp]
                #     print(3)
                #     dataTemp = dataTemp[lenOldUsernameTempTemp:]
                #     print(4)
                #
                #
                #     lennewUsernameTempTemp = int(dataTemp[:2])
                #     print(5)
                #     dataTemp = dataTemp[2:]
                #     print(6)
                #
                #     newUsernameTemp = dataTemp[:lennewUsernameTempTemp]
                #     print(7)
                #
                #     isSuccessTemp = True
                #     print(8)
                #
                #     for i in dbUsers["username"]:
                #         print(9)
                #         if i == newUsernameTemp:
                #             print(10)
                #             isSuccessTemp = False
                #             print(11)
                #     if isSuccessTemp:
                #         print(12)
                #         myUsername = newUsernameTemp
                #         print(13)
                # valStatus = status(typeMsg, data, client)

            except:
                pass
        else:
            isExitClient = True
            userLogout = ""
            usernameOut = myUsername
            for i in dictUsersSocket:
                if dictUsersSocket[i] == client:
                    userLogout = i
            print("logout")
            listClients.remove(client)
            del dictThreads[numOfThread]
            try:
                del onlinUsersGroup[usernameOut]
            except:
                pass
            try:
                del usersSocket[usernameOut]
            except:
                pass

            try:
                onlinUsers.remove(usernameOut)
            except:
                pass

            print("Connection with client closed.")



        #
        #     for usernameOut in tempUsersSocket:
        #         if usersSocket[usernameOut] is current_socket:
        #             try:
        #                 del onlinUsersGroup[usernameOut]
        #             except:
        #                 pass
        #             try:
        #                 del usersSocket[usernameOut]
        #             except:
        #                 pass
        #             try:
        #                 onlinUsers.remove(usernameOut)
        #             except:
        #                 pass
        #
        #
        #     print("Connection with client closed.")
        # else:
        #     messages_to_send.append((current_socket, data))
        #     try:
        #         pass#send_waiting_messages(wlist)
        #     except:
        #         pass

def server():
    global server_socket
    global open_client_sockets
    global messages_to_send
    global exit
    global isLogin
    global tempClient
    global usersSocket
    global typeMsg
    global data

    global server_socket
    global listClients
    global listThreads
    global sumThreading
    #
    server_socket.bind((IP, PORT))#???#socket.gethostname()
    server_socket.listen(5)#???
    print("The server run")

    while not exit:
        try:

            (client_socket, client_address) = server_socket.accept()
            listClients.append(client_socket)
            #listThreads.append(threading.Thread(target=rec, args=(client_socket,)))
            dictThreads[sumThreading] = threading.Thread(target=rec, args=(client_socket,sumThreading))
            sumThreading += 1
            #listThreads[len(listThreads) - 1].start()
            for num in dictThreads:
                try:
                    dictThreads[num].start()
                except:
                    pass

        except:#setblocking()
            pass
    # if exit:
    #     print("a")
    #     for i in listClients:
    #         i.setblocking(0)
    #         print("b")

    #
    # for i in dictThreads:#stop()
    #     dictThreads[i].stop()
#


    # print("The server run")
    # while not exit:
    #     rlist, wlist, xlist = select.select( [server_socket] + open_client_sockets, [], [] )
    #     for current_socket in rlist:
    #         if current_socket is server_socket:
    #             (new_socket, address) = server_socket.accept()
    #             open_client_sockets.append(new_socket)
    #
    #             with threadLockLogin:
    #                 isLogin = True
    #                 tempClient = new_socket
    #                 listTempClient.append(new_socket)
    #         else:
    #             try:
    #                 typeMsg = current_socket.recv(3).decode()
    #                 data = current_socket.recv(1024).decode()
    #
    #                 try:
    #                     typeMsg = int(typeMsg)
    #                     status(typeMsg, data)
    #                 except:
    #                     pass
    #             except:
    #                 pass
    #             if data == "":
    #                 open_client_sockets.remove(current_socket)
    #                 tempUsersSocket = copy.copy(usersSocket)
    #                 for usernameOut in tempUsersSocket:
    #                     if usersSocket[usernameOut] is current_socket:
    #                         try:
    #                             del onlinUsersGroup[usernameOut]
    #                         except:
    #                             pass
    #                         try:
    #                             del usersSocket[usernameOut]
    #                         except:
    #                             pass
    #                         try:
    #                             onlinUsers.remove(usernameOut)
    #                         except:
    #                             pass
    #
    #
    #                 print("Connection with client closed.")
    #             else:
    #                 messages_to_send.append((current_socket, data))
    #                 try:
    #                     pass#send_waiting_messages(wlist)
    #                 except:
    #                     pass
def send_waiting_messages(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        for i in open_client_sockets:
            i.send(data.encode())
        messages_to_send.remove(message)
        #del usersSocket[username]

def createResponseId(id):
    lenMaxId = 7
    typeMsg = 421

    msg = "{}{}".format(typeMsg, str(id).zfill(7))
    Bmsg = msg.encode()
    return Bmsg

def status(typeMsg, data, tempClient):
    global isLogin
    global groupsData
    global exit
    global onlinUsersGroup
    global listTempClient
    global usersSocket
    if typeMsg < 100:
        print("error")
    elif typeMsg < 200:
        print("system")
    elif typeMsg < 300:
        print("login")
        newDAata = getUsernamePassword(data)
        username, password = newDAata
        isSuccess = login(username, password)[0]
        if not (username in onlinUsers):
            tempClient.send(str(isSuccess)[0].encode())
            print("isSuccess", isSuccess)
            with threadLockLogin:
                isLogin = True
                if isLogin and isSuccess:
                    isLogin = False
                    usersSocket[username] = tempClient#????
                    onlinUsers.append(username)
            return username
        else:
            tempClient.send(str(not isSuccess)[0].encode())


    elif typeMsg < 400:
        if typeMsg == 300:
            print("Send msg")
            idGroup = data[:7]
            data = data[7:]

            lenUsername = int(data[:2])
            data = data[2:]

            username = data[:lenUsername]
            data = data[lenUsername:]

            data = openData(data)
            if data == "SYS.QUIT" and (getPermission(username) == 7):#or username == "michael"# )
                exit = True
                for user in onlinUsersGroup:
                    usersSocket[user].send(CreateMsgSub(onlinUsersGroup[user]))
            elif data == "logout":
                pass
                # newOnlinUsersGroup = {}
                # for i in onlinUsersGroup:
                #     if i != username:
                #         newOnlinUsersGroup[username] = onlinUsersGroup[username]
                # onlinUsersGroup = newOnlinUsersGroup
                # print('onlinUsersGroup-', onlinUsersGroup)
            listToSend = []
            msg = creatMSG(int(idGroup), username, data)

            listToSend = []
            for user in ast.literal_eval(groupsUsers[int(idGroup)][1]):
                if user in onlinUsers:
                    listToSend.append(user)

            for user in usersSocket:
                if user in listToSend:
                    usersSocket[user].send(msg)
            makeMsg(int(idGroup), username, data)#pppppp
            #
            # for user in ast.literal_eval(groupsUsers[int(idGroup)][1]):
            #     if user in onlinUsers:
            #         if onlinUsersGroup[user] == int(idGroup):
            #             listToSend.append(user)
            #


            # for user in usersSocket:
            #     #if user in listToSend:
            #     usersSocket[user].send(msg)
            # makeMsg(int(idGroup), username, data)#pppppp

            # try:
            #     for user in ast.literal_eval(groupsUsers[int(idGroup)][1]):
            #         if user in onlinUsers:
            #             if onlinUsersGroup[user] == int(idGroup):
            #                 listToSend.append(user)
            #
            #     for user in usersSocket:
            #         if user in listToSend:
            #             usersSocket[user].send(msg)
            #     makeMsg(int(idGroup), username, data)#pppppp
            # except:
            #     usersSocket[username].send(msg)

        elif typeMsg == 310:
            print("Send file")
    elif typeMsg < 500:
        if typeMsg == 400:
            print("add user to group")
            idGroup = int(data[:7])
            data = data[7:]

            lenUsername = int(data[:2])
            data = data[2:]

            username = data[:lenUsername]

            addUserToGroup(idGroup, username)

            try:
                usersGroups[username].append(idGroup)
            except:
                pass


        elif typeMsg == 410:
            print("sub user to group")
            idGroup = int(data[:7])
            print("a")
            data = data[7:]
            print("b")
            lenUsername = int(data[:2])
            print("c")
            data = data[2:]
            print("d")
            username = data[:lenUsername]
            print("e")
            subUserToGroup(idGroup, username)
            print("f")


        elif typeMsg == 420:
            print("new group")

            lenUsername = int(data[:2])
            data = data[2:]
            username = data[:lenUsername]
            data = data[lenUsername:]
            lenNameGroup = int(data[:2])
            data = data[2:]
            nameGroup = data[:lenNameGroup]
            data = data[lenNameGroup:]
            listUsersStr = data

            listUsers = ast.literal_eval(listUsersStr)
            newListUsers = []

            for i in dbUsers["username"]:
                if i in listUsers:
                    newListUsers.append(i)

            listUsers = newListUsers

            idGroup = createNewGroup(nameGroup, listUsers)
            dataToSend = createResponseId(idGroup)
            usersSocket[username].send(dataToSend)

            groupsUsers[idGroup] = [nameGroup, str(listUsers)]

            for user in listUsers:
                usersGroups[user] = idGroup

            idNamesGroup[idGroup] = nameGroup

            onlinUsersGroup[username] = idGroup


            # print("nameGroup:", nameGroup)
            # print(lenUsername, username, lenNameGroup, nameGroup, listUsersStr)
            #exit = True


        elif typeMsg == 430:
            print("change name of group")
            id = int(data[:7])
            data = data[7:]

            lenName = int(data[:2])
            data = data[2:]

            newName = data[:lenName]

            changeNameGroup(id, newName)

        elif typeMsg == 440:
            print("cmp")
        elif typeMsg == 450:

            # print("change name of user")
            # print("---------------------------------------------")
            # print("groupsUsers", groupsUsers)
            # print("usersGroups", usersGroups)
            # print("usersSocket", usersSocket)
            # print("onlinUsers", onlinUsers)
            # print("onlinUsersGroup", onlinUsersGroup)
            # print("listClients", listClients)
            # print("dictUsersSocket", dictUsersSocket)
            # print("listClients", listClients)
            # print("listThreads", listThreads)
            # print("dictThreads", dictThreads)
            # print("---------------------------------------------")

            lenOldUsername = int(data[:2])
            data = data[2:]

            OldUsername = data[:lenOldUsername]
            data = data[lenOldUsername:]


            lenNewUsername = int(data[:2])
            data = data[2:]

            newUsername = data[:lenNewUsername]

            isSuccess = True

            for i in dbUsers["username"]:
                if i == newUsername:
                    isSuccess = False
                    print("isSuccess", isSuccess)

            usersSocket[OldUsername].send(str(isSuccess)[0].encode())
            if isSuccess:
                changeName(OldUsername, newUsername)

                return newUsername

        elif typeMsg == 460:
            print("change password of user")


            lenUsername= int(data[:2])
            data = data[2:]
            username = data[:lenUsername]
            data = data[lenUsername:]

            newPassword = data
            changePassword(username, newPassword)
        elif typeMsg == 470:
            print("register")
            newDAata = getUsernamePassword(data)
            username, password = newDAata
            password = password[:-1]
            #print(username, password)
            isSuccess = register(username, password)
            print("Is success:", isSuccess)
            tempClient.send(str(isSuccess)[0].encode())
            with threadLockLogin:
                isLogin = True
                if isLogin and isSuccess:
                    isLogin = False
                    usersSocket[username] = tempClient
                    onlinUsers.append(username)
                    return username

        elif typeMsg == 480:
            print("listGroups")

            username = getListGroups(data)
            # print(0)

            dataToSend = createResponseGetListGroup(username)
            # print(1)
            print("dataToSend", dataToSend)
            usersSocket[username].send(dataToSend)
            # print(2)
            with threadLockLogin:
                # print(3)
                isLogin = True
                # print(4)
                if isLogin and isSuccess:
                    # print(5)
                    isLogin = False
                    # print(6)
                    usersSocket[username] = tempClient
                    # print(7)
            # print(8)

        elif typeMsg == 490:
            print("Request DB Group")
            idGroup = int(data[:7])
            data = data[7:]
            username = data
            dataGroup = makeMsgDBGroup(idGroup)
            newData = b"491"
            newData += createSendData(dataGroup)
            usersSocket[username].send(newData[:3])
            newData = newData[3:]

            groupsData[idGroup] = getDBGroup(idGroup)
            # while newData[0] != b'T':
            #     usersSocket[username].send(newData[:1024])
            #     newData = newData[1024:]
            usersSocket[username].send(newData[:1024])
            newData = newData[1024:]
            usersSocket[username].send(newData)
            onlinUsersGroup[username] = idGroup
        elif typeMsg == 492:
            print("logout from group")

            idGroup = int(data[:7])
            data = data[7:]
            lenUsername = int(data[:2])
            data = data[2:]

            username = data[:lenUsername]
            data = data[lenUsername:]

            # newOnlinUsersGroup = {}
            # print("onlinUsersGroup", onlinUsersGroup, ";")
            # for i in onlinUsersGroup:
            #     # print(7)
            #     if i != username:
            #         newOnlinUsersGroup[username] = onlinUsersGroup[username]
            # onlinUsersGroup = newOnlinUsersGroup
            usersSocket[username].send(creatMSG(idGroup, username, "EXIT"))

    elif typeMsg < 600:
        print("Ok")
    elif typeMsg < 700:
        print("Out user from group")
    elif typeMsg < 800:
        if typeMsg == 700:
            print("make call")
            tempIsOpenUDP = False
            with threadLockIsOpenUDP:
                if isOpenUDP:
                    tempIsOpenUDP = isOpenUDP

            if not tempIsOpenUDP:
                threadUDPServer = threading.Thread(target=creatServerUDP)
                threadUDPServer.start()

        elif typeMsg == 710:
            print("cut call")

def creatMSG(id, username, data):
    global lenMaxId
    lenMaxUsername = 2
    typeMsg = 300
    lenMaxId = 7

    msg = "{}{}{}{}".format(typeMsg,#type msg
                        str(id).zfill(lenMaxId),
                        str(len(username)).zfill(lenMaxUsername), username) #len username + username
    msg = msg.encode()
    msg += createSendData(data)
    return msg


def createSendData(data):
    #get data, preparing the data for sending
    lenData = len(data)
    newData = b""
    nowData = ""
    lenSend = 1024
    while len(data) >= lenSend:
        nowData = "F"
        nowData += data[:lenSend - 1]
        data = data[lenSend - 1:]
        newData += nowData.encode()
    lenRest = str(len(data)).zfill(len(str(lenSend)))
    rest = "T{}{}".format(lenRest, data)
    newData += rest.encode()
    return newData

def makeSendAllDB(id):
    with threadLockDictGroup:
        pass

def strToList(str):
    chars = "[]'\" "
    for i in str:
        if i in chars:
            str = str.replace(i, "")
    return str

def addUserToGroup(id, user):
    global dbGroups
    global groupsUsers


    strList = groupsUsers[id][1]
    list = ast.literal_eval(strList)
    list.append(user)
    groupsUsers[id][1] = str(list)

    listStr = dbGroups["users"][id]
    list = ast.literal_eval(listStr)
    list.append(user)
    dbGroups["users"][1] = list

def CreateMsgSub(id):
    #global lenMaxId
    lenMaxId = 7
    typeMsg = 600
    msg = "{}{}".format(typeMsg,#type msg
                        str(id).zfill(lenMaxId))
    msg = msg.encode()
    return msg

def subUserToGroup(id, user):
    global dbGroups
    global groupsUsers

    global usersSocket
    global onlinUsersGroup
    global usersGroups

    strList = groupsUsers[id][1]
    print(1)
    list = ast.literal_eval(strList)
    print(2)
    del list[list.index(user)]
    print(3)
    groupsUsers[id][1] = str(list)
    print(4)

    listStr = dbGroups["users"][id]
    print(5)
    print("listStr", listStr)
    try:
        list = ast.literal_eval(listStr)
    except:
        list = listStr
    print(6)
    del list[list.index(user)]
    print(7)
    dbGroups["users"][1] = list
    print(8)
#
    del onlinUsersGroup[user]
    print(9)

    del usersGroups[user][usersGroups[user].index(id)]
    print(10)

    try:
        usersSocket[user].send(CreateMsgSub(id))
        print(11)
    except:
        print(12)
    print(13)

def saveDBGroups():
    global groupsData
    global path

    with threadLockDictGroup:
        for id in groupsData:
            local_path = f'{path}groups/{id}.csv'
            updateDBGroups(groupsData[id], local_path)

def timesEpoch():
    return int(time.time())

def timesAll(timer=None):
    #return the time
    if timer is None:
        TimeVar = timesEpoch()
    else:
        TimeVar = timer
    TimeVar = time.localtime(TimeVar)
    times = "{}/{}/{}-{}/{}/{}".format(TimeVar.tm_year, TimeVar.tm_mon, TimeVar.tm_mday, TimeVar.tm_hour,  TimeVar.tm_min, TimeVar.tm_sec )
    return times

def firstStart(nameFile):
    global path
    listFiles = os.listdir(path)
    return not(nameFile in listFiles)

def createDBFirst():
    nameFileUsers = 'db_users.csv'
    nameFileGroup = 'db_groups.csv'

    if firstStart(nameFileUsers):

        id = 0
        username = "Admin"
        password = "1234"
        password_hash = hashlib.sha224(password.encode()).hexdigest().upper()
        permission = 7

        db_user = pd.DataFrame({'id': [id],
                                       'username': [username],
                                       'password': [password_hash],
                                       'permission': [permission]
                                       })

        db_user.to_csv(f'{path}{nameFileUsers}', index=False)
    if firstStart(nameFileGroup):
        id = 0
        name = "GroupOne"
        users = ["Admin"]

        db_group = pd.DataFrame({'id': [id],
                                       'group': [name],
                                       'users': [users],
                                       })
        db_group.to_csv(f'{path}{nameFileGroup}', index=False)

        username = "Admin"
        date = timesAll()
        dataMsg = date
        epoch = timesEpoch()
        idGroup = 0
        idMsg = 0
        local_path = f'{path}groups/{idGroup}.csv'
        db_group = pd.DataFrame({'id': [idMsg],
                                    'date': [date],
                                    'username': [username],
                                    'data': [dataMsg],
                                    'epoch': [epoch]
                                    })

        db_group.to_csv(local_path, index=False)

def pdToList(db, row):
    arr = []
    for i in db[row]:
        arr.append(i)
    return arr

def lastValue(db, row):
    return (db[row][len(db[row]) - 1]) + 1

def addVarDBUser(username, password, permission = 0):
    global dbUsers
    with threadLockUsers:
        id = lastValue(dbUsers, "id")
        #password_hash = hashlib.sha224(password.encode()).hexdigest().upper()
        password_hash = password
        db_user = pd.DataFrame({'id': [id],
                                       'username': [username],
                                       'password': [password_hash],
                                       'permission': [permission]
                                       })

        dbUsers = dbUsers.append(db_user, ignore_index=True)

def dictDB(db, row, *args):
    listRow = []
    dict = {}
    index = 0
    for i in db[row]:
        listRow.append(i)
    for i in listRow:
        dict[i] = []

    lens = len(listRow)
    index = 0

    for i in args:
        for j in db[i]:
            dict[listRow[index]].append(j)
            index += 1
            if index > lens - 1:
                index = 0
    return dict

def dictDBForEach(db, row, *args):
    listRow = []
    dict = {}
    listArgs = []

    for i in db[row]:
        listRow.append(i)

    sum = 0

    for i in args:
        listArgs.append([])
        for j in db[i]:
            listArgs[sum].append(j)
        sum += 1

    for i in range(len(listRow)):
        dict[listRow[i]] = [listArgs[0][i], listArgs[1][i]]

    return dict

def findIndex(db, row, value):
    dbRow = db[row]
    index = 0
    for i in dbRow:
        if i == value:
            return index
        index += 1
    return -1

def login(username, password, ip = 0):
    global dbUsers
    dict = dictDB(dbUsers, "username", "password", "id")
    try:
        passwordDB = dict[username][0]

        #password_hash = hashlib.sha224(password.encode()).hexdigest().upper()
        if passwordDB == password:
            usersIp[username] = ip
            return (True, username, password, dict[username][1])
        return (False, username, password)
    except:
        return (False, username, password)


def register(username, password, ip = 0, permission = 0):
    global dbUsers
    global exit
    #exit = True
    listName = pdToList(dbUsers, "username")
    if not (username in listName):
        addVarDBUser(username, password, permission)
        usersIp[username] = ip
        return True
    return False

def readDBUsers(path):
    with threadLockDBUsers:
        data = pd.read_csv(path)
        return data

def readDBGroups(path):
    with threadLockDBGroups:
        data = pd.read_csv(path)
        return data

def updateDBUsers(db, path):
    with threadLockDBUsers:
        db.to_csv(path, index=False)

def updateDBGroups(db, path):
    with threadLockDBGroups:
        db.to_csv(path, index=False)

def downloadDbUsers():
    global path

    local_path = f'{path}db_users.csv'
    data = readDBUsers(local_path)
    return data

def downloadDbGroups():
    global path

    local_path = f'{path}db_groups.csv'
    data = readDBGroups(local_path)
    return data

def downloadDbGroup(id):
    global path
    local_path = f'{path}groups/{id}.csv'

    data = readDBGroups(local_path)
    return data

def createNewGroup(name, users):
    global dbGroups
    global path

    with threadLockGroups:
        id = lastValue(dbGroups, "id")
        db_group = pd.DataFrame({'id': [id],
                                       'group': [name],
                                       'users': [users]
                                       })

        dbGroups = dbGroups.append(db_group, ignore_index=True)# ignore_index=True
        newGroup(id)

        return id

def newGroup(id):
    global path
    global groupsData
    global groupsUsers

    with threadLockDBGroup:
        local_path = f'{path}groups/{id}.csv'


        username = "Admin"
        date = timesAll()
        dataMsg = date
        epoch = timesEpoch()

        db_group = pd.DataFrame({'id': [0],
                                    'date': [date],
                                    'username': [username],
                                    'data': [dataMsg],
                                    'epoch': [epoch]
                                    })

        db_group.to_csv(local_path, index=False)

        with threadLockDictGroup:
            groupsData[id] = db_group

        # with threadLockDictGroupUsers:#???
        #     groupsUsers[id] = username#???

        with threadLockDictNewDataGroup:
            newDataGroup[id] = dataMsg

def sendMsg(id, msg):
    pass

def makeMsg(id, user, data):
    global groupsData
    global newDataGroup

    date = timesAll()
    epoch = timesEpoch()

    with threadLockDictGroup:
        try:
            DBdataGroup = groupsData[id]


            idMsg = lastValue(DBdataGroup, "id")#kkkkkkk
            db_group = pd.DataFrame({'id': [idMsg],
                                        'date': [date],
                                        'username': [user],
                                        'data': [data],
                                        'epoch': [epoch]
                                        })

            groupsData[id] = DBdataGroup.append(db_group, ignore_index=True)
            sendMsg(id, data)
        except:
            DBdataGroup = downloadDbGroup(id)
            idMsg = lastValue(DBdataGroup, "id")
            db_group = pd.DataFrame({'id': [idMsg],
                                        'date': [date],
                                        'username': [user],
                                        'data': [data],
                                        'epoch': [epoch]
                                        })
            DBdataGroup = DBdataGroup.append(db_group, ignore_index=True)

            groupsData[id] = DBdataGroup
            sendMsg(id, data)



            with threadLockDictNewDataGroup:
                newDataGroup[id] = idMsg
def getDBGroup(id):
    with threadLockDictGroup:
        try:
            DBdataGroup = groupsData[id]
            return DBdataGroup
        except:
            DBdataGroup = downloadDbGroup(id)
            return DBdataGroup

def makeMsgDBGroup(id):
    global groupsData
    try:
        DBdataGroup = groupsData[id]#=======
    except:
        DBdataGroup = getDBGroup(id)


    dataDictDB = dictDB(DBdataGroup, "id", "date", "username", "data", "epoch")
    data = ""
    for i in dataDictDB:
        data += '('
        data += str(i)
        data += str(dataDictDB[i])
        data += ')'
    data = data.replace("'", "")
    return data




def getDBGroupFromSerevr(datas):
    regex = r'\((.*?)\)'
    pattern = re.compile(regex)
    matching = pattern.finditer(datas)
    divs = ""
    arr = []
    for i in matching:
        arr.append(datas[i.span()[0]: i.span()[1]][1:-1])

    sumI = 0
    for i in arr:
        for j in range(5):
            if j == 0:
                regex = r'(.*?)\['
                pattern = re.compile(regex)
                matching = pattern.finditer(i)
            elif j == 1:
                regex = r'(\d*?)/(\d*?)/(\d*?)\-(\d*?)/(\d*?)/(\d*?),'
                pattern = re.compile(regex)
                matching = pattern.finditer(i)
            elif j == 2:
                regex = r',(.*?),'
                pattern = re.compile(regex)
                matching = pattern.finditer(i)
            elif j == 3:
                pass
            elif j == 4:
                regex = r', (\d*?)\]'
                pattern = re.compile(regex)
                matching = pattern.finditer(i)

            for k in matching:
                info = i[k.span()[0]: k.span()[1] - 1]
                if j == 2:
                    first = k.span()[1] - 1
                elif j == 4:
                    last = k.span()[0]
                    data = i[first+2:last]

            if j == 0:
                id = info.replace(" ", "")
                id = id.replace(",", "")
            elif j == 1:
                date = info.replace(" ", "")
                date = date.replace(",", "")
            elif j == 2:
                name = info.replace(" ", "")
                name = name.replace(",", "")
            elif j == 3:
                pass
            elif j == 4:
                epoch = info.replace(" ", "")
                epoch = epoch.replace(",", "")


        db_group = pd.DataFrame({'id': id,
                                    'date': [date],
                                    'username': [name],
                                    'data': [data],
                                    'epoch': [epoch]
                                    })
        if sumI == 0:
            dbGroups = db_group
        else:
            dbGroups = dbGroups.append(db_group, ignore_index=True)#, ignore_index=True
        sumI += 1

    return dbGroups

def saveMainDB():
    global dbUsers
    global dbGroups
    global path
    local_path = f'{path}db_users.csv'
    updateDBUsers(dbUsers, local_path)

    local_path = f'{path}db_groups.csv'
    updateDBGroups(dbGroups, local_path)

def saveDB():
    saveMainDB()
    saveDBGroups()

def main():
    global dbUsers
    global dbGroups
    global path
    global groupsData
    global groupsUsers
    global usersGroups
    global idNamesGroup

    createDBFirst()
    dbUsers = downloadDbUsers()
    dbGroups = downloadDbGroups()

    groupsUsers = dictDB(dbGroups, "id", "group", "users")
    FindIdGroups()

    server()
    saveDB()

if __name__ == '__main__':
    main()

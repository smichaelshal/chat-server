#client
import os
import time
import hashlib
import socket
import threading
import ast
import pandas as pd
import re
import sys
import string
import platform
import random
import getpass

#getpass.getpass(prompt='Enter your password: ', stream=None)#___

#platform.system()
#Darwin mac
#windows windows
#Linux linux

#Global variables

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
sumRound = 0
varOsRuns = ""

IP = '10.0.0.14'
PORT = 8805

my_socket = socket.socket()
my_socket.connect((IP, PORT))#'localhost'

username = ""
listGroup = {}
dataGroups = {}
groupNow = ""
isIn = False

threadIsOpenUDP = threading.Lock()
isOpenUDP = False

#Client UDP
clientUDP = ""
PORT_UDP = 6688
inInCall = False

#Functions
def WhatIsOsRuns():
    global varOsRuns
    varOsRuns = platform.system()

def printMsg(data="", endTemp=None):
    if isinstance(endTemp, str):
        print(data, end=endTemp)
    else:
        print(data, end="\n")

def PRINT(data="", endTemp="\n"):
    global IsGrafik

    if not IsGrafik:
        printMsg(data, endTemp)
    else:
        pass

def creatDataCall(id, username, data):
    global lenMaxId
    lenMaxUsername = 2
    typeMsg = 702
    lenMaxId = 7

    msg = "{}{}{}{}".format(typeMsg,
                        str(id).zfill(lenMaxId),
                        str(len(username)).zfill(lenMaxUsername), username, data) #len username + username

    return msg.encode()
def sendCall():
    global clientUDP
    global username
    global inInCall
    global idGroupGlobal

    while True:
        dataToSend = "IsUDPClientMSG"
        while len(dataToSend) >= 1024:
            clientUDP.send(creatDataCall(idGroupGlobal, username, dataToSend))
            dataToSend = dataToSend[1024:]
        clientUDP.send(creatDataCall(idGroupGlobal, username, dataToSend))


def creatClientUDP():
    global clientUDP
    global IP
    global PORT_UDP
    inInCall = True

    clientUDP = socket.socket(type=socket.SOCK_DGRAM)
    clientUDP.connect((IP, PORT_UDP))

    threadSendCall = threading.Thread(target=sendCall)
    threadSendCall.start()
    while inInCall:
        data, address = clientUDP.recvfrom(1024)
        PRINT(data)

    clientUDP.close()

def clearLine(data = ""):
    global varOsRuns
    osRuns = varOsRuns

    if not IsGrafik:
        if osRuns == "Darwin" or osRuns == "Linux":
            sys.stdout.write("\033[F") #back to previous line
            sys.stdout.write("\033[K") #clear line
            time.sleep(0.00001)
        elif osRuns == "Windows":
            pass
            # spaces = " " * 100
            # sys.stdout.write('%s\r' % spaces)
            # sys.stdout.flush()
            # sys.stdout.write('\b')
            #
            # sys.stdout.write('%s\r' % data)
            # sys.stdout.flush()
            # #time.sleep(0.2)
            # sys.stdout.write('\b')

def openDataRecv():
    isEnd = my_socket.recv(1).decode()
    data = ""
    while isEnd != "T":
        data += my_socket.recv(1023).decode()
        isEnd = my_socket.recv(1).decode()

    lenData = int(my_socket.recv(4).decode())
    data += my_socket.recv(lenData).decode()
    return data

def Gateway():
    global username
    global isLoginSuccess
    global isIn
    global sumRound

    while not isIn:
        clearScreen()
        toLogin = ""

        while toLogin != 'Y' and toLogin != 'N':
            if sumRound != 0:
                if not IsGrafik:
                    PRINT("Login problem, username or password incorrect.")
                #isLoginSuccess = True


            if not IsGrafik:
                sumRound = 0
                PRINT("You need to log in, if you have an account written 'Y' otherwise write 'N' and sign up for the app: ", "")
                toLogin = input("")

        if(toLogin == 'Y'):
            username = loginSend()
        elif (toLogin == 'N'):
            username = registerSend()

        isSuccess = my_socket.recv(1).decode()
        if isSuccess == "T":
            isIn = True
            mainMenu()

        elif toLogin == 'N' and isSuccess == "F":
            if not IsGrafik:
                PRINT("Username Busy Try a different username.")
        elif toLogin == 'Y' and isSuccess == "F":
            isLoginSuccess = False

        toLogin = ""
        username = ""
        isLoginSuccess = True
        isIn = False
        isSuccess = "F"


def register(username, password, permission = 0):
        #send to server the username and password
        lenMaxUsername = 2
        typeMsg = 470 # 400 add user
        usernameAndPassword = "{}{}{}{}{}".format(typeMsg, str(len(username)).zfill(lenMaxUsername), username, hash(password), permission)
        bUsernameAndPassword = usernameAndPassword.encode("UTF-8")
        return bUsernameAndPassword

def clearScreen():
    global varOsRuns
    osRuns = varOsRuns

    if not IsGrafik:
        osRuns = platform.system()
        if osRuns == "Darwin" or  osRuns == "Linux":
            clear = lambda: os.system('clear') #on Linux System
            clear()
        elif osRuns == "Windows":
            clear = lambda: os.system('cls') #on Linux System
            clear()

def loginSend():
    global sumRound
    dataOk = True
    while dataOk:
        if not IsGrafik:
            PRINT("Enter your username: ", "")
            username = input("")

            #PRINT("Enter your password: ", "")
            #password = input("")#___
            password = getpass.getpass(prompt='Enter your password: ', stream=None)
            sumRound += 1
        dataOk = not (checkLogin(username) and checkLogin(password))

    data = login(username, password)
    sendData(data)
    return username

def registerSend():
    global sumRound
    dataOk = True

    while dataOk:
        if not IsGrafik:
            PRINT("Enter your username: ", "")
            username = input("")

            #PRINT("Enter your password: ", "")
            #password = input("")#___
            password = getpass.getpass(prompt='Enter your password: ', stream=None)
            sumRound += 1
        dataOk = not (checkLogin(username) and checkLogin(password))

    data = register(username, password)
    sendData(data)
    return username

def sendData(data):
    global my_socket
    my_socket.send(data)

def job(id):
    global username
    global isExitGroup
    global IsOut
    global threadIsOpenUDP
    global isOpenUDP

    data = ""
    #IsCall = True
    while not isExitGroup:
        data = input("")

        if data == "SYS.BACK" or IsOut:
            isExitGroup = True
            data = "logout"
            my_socket.send(creatLogOutMSG(id, username))
            IsOut = False
        elif "SYS.NAME=" in data:
            index = data.index("=")
            newName = data[index + 1:]
            my_socket.send(changeNameGroup(id, newName))
        elif "SYS.ADD=" in data:
            index = data.index("=")
            usernameToAdd = data[index + 1:]
            my_socket.send(addUserToGroup(id, usernameToAdd))
        elif "SYS.SUB=" in data:
            index = data.index("=")
            usernameToSub = data[index + 1:]
            my_socket.send(subUserToGroup(id, usernameToSub))
        elif data == "SYS.CALL": #or IsCall:
            isOpenUDP = True
            tempIsOpenUDP = False
            data = "jjjj"

            msgs = creatDataCall(id, username, data)
            PRINT(msgs)
            msgs = b"700" + msgs[3:]
            PRINT(msgs)

            my_socket.send(msgs)
            with threadIsOpenUDP:
                if isOpenUDP:
                    tempIsOpenUDP = isOpenUDP

            if tempIsOpenUDP:
                threadUDPClient = threading.Thread(target=creatClientUDP)
                threadUDPClient.start()

        else:
            if isOk(data):
                my_socket.send(creatMSG(id, username, data))
                clearLine(data)
            else:
                if not IsGrafik:
                    PRINT("\nsystem say>> The message not supported.\n")

def isOk(data):
    if len(data) == 0:
        return False
    #abc = string.ascii_letters
    #numbers = string.digits
    allLetters = string.printable
    #punctuation = string.PRINTable#?

    for letter in data:
        if not (letter in allLetters):
            return False
    return True

def hash(password):
    #get password, return the hash of the password, (sha224, length 56)
    password_hash = hashlib.sha224(password.encode()).hexdigest().upper()
    return password_hash

def changeName(name, newName):
    global lenMaxId
    lenMaxName = 2
    typeMsg = 450
    msg = "{}{}{}{}{}".format(typeMsg,#type msg
                        str(len(name)).zfill(lenMaxName), name,
                        str(len(newName)).zfill(lenMaxName), newName) #len username + username
    msg = msg.encode()
    return msg

def changePassword(username, newPassword):
    global lenMaxId
    password_hash = hash(newPassword)
    lenMaxName = 2
    typeMsg = 460
    msg = "{}{}{}{}".format(typeMsg,#type msg
                        str(len(username)).zfill(lenMaxName), username, password_hash)
    msg = msg.encode()
    return msg

def changeNameGroup(id, name):
    global lenMaxId
    lenMaxName = 2
    typeMsg = 430
    msg = "{}{}{}{}".format(typeMsg,#type msg
                        str(id).zfill(lenMaxId),
                        str(len(name)).zfill(lenMaxName), name) #len username + username
    msg = msg.encode()
    return msg

def RequestDBGroup(id):
    global lenMaxId
    global username

    typeMsg = 490
    msg = "{}{}{}".format(typeMsg,#type msg
                        str(id).zfill(lenMaxId), username)
    msg = msg.encode()
    return msg

def checkLogin(inputs):
    #get input in login return true if the input is OK else return false
    if inputs == "":
        return False
    lens = len(inputs)
    if lens > 50:
        return False
    ABC = "abcdefghijklmnopqrstuvwxyz"
    ABC += ABC.upper()
    chars = "_"
    numbers = "0123456789"

    for i in inputs:
        if not (i in ABC or i in chars or i in numbers):
            return False
    return True

def addUserToGroup(id, usernameToAdd):
    global lenMaxId
    lenMaxUsername = 2
    typeMsg = 400

    msg = "{}{}{}{}".format(typeMsg, str(id).zfill(lenMaxId), str(len(usernameToAdd)).zfill(lenMaxUsername),usernameToAdd).encode()
    return msg


def subUserToGroup(id, usernameToSub):
    global lenMaxId
    lenMaxUsername = 2
    typeMsg = 410

    msg = "{}{}{}{}".format(typeMsg, str(id).zfill(lenMaxId), str(len(usernameToSub)).zfill(lenMaxUsername),usernameToSub).encode()
    return msg

def times():
    #return the time
    TimeVar = time.gmtime()
    times = "{}/{}/{}-{}/{}/{}".format(TimeVar.tm_year, TimeVar.tm_mon, TimeVar.tm_mday, TimeVar.tm_hour,  TimeVar.tm_min, TimeVar.tm_sec )
    return times

def login(username, password):
    #send to server the username and password
    lenMaxUsername = 2
    typeMsg = 200 # 400 add user
    usernameAndPassword = "{}{}{}{}".format(typeMsg, str(len(username)).zfill(lenMaxUsername), username, hash(password))
    bUsernameAndPassword = usernameAndPassword.encode("UTF-8")
    return bUsernameAndPassword
    #send bUsernameAndPassword

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

def createGroup(name, users):
    #get name group and users, generates a message to the server to create a new group
    global username
    lenMaxName = 2
    lenMaxUsers = 4
    typeMsg = 420
    strUsers = ",".join(users)
    msg = "{}{}{}{}{}{}".format(typeMsg, str(len(username)).zfill(lenMaxName), username, str(len(name)).zfill(lenMaxName), name, str(users))#str(len(users)).zfill(lenMaxUsers), strUsers)
    Bmsg = msg.encode()
    return Bmsg

def creatMSG(id, username, data):
    global lenMaxId
    lenMaxUsername = 2
    typeMsg = 300
    msg = "{}{}{}{}".format(typeMsg,#type msg
                        str(id).zfill(lenMaxId),
                        str(len(username)).zfill(lenMaxUsername), username) #len username + username
    msg = msg.encode()
    msg += createSendData(data)
    return msg

def creatLogOutMSG(id, username):
    global lenMaxId
    lenMaxUsername = 2
    typeMsg = 492
    msg = "{}{}{}{}".format(typeMsg,#type msg
                        str(id).zfill(lenMaxId),
                        str(len(username)).zfill(lenMaxUsername), username) #len username + username
    msg = msg.encode()
    return msg

def makeRequestListGroups(username):
    global lenMaxId
    lenMaxUsername = 2
    typeMsg = 480
    msg = "{}{}{}".format(typeMsg,#type msg
                        str(len(username)).zfill(lenMaxUsername), username)
    msg = msg.encode()
    return msg

def sendRequestListGroups(username):
    data = makeRequestListGroups(username)
    sendData(data)

def lensList(list):
    sum = 0
    for i in list:
        sum += 1
    return sum
def groups():
    global username
    global isExitGroup
    global idGroupGlobal
    global otherData

    global year
    global month
    global day
    global IsOut

    while not isExitGroup:
        typeMsg = int(my_socket.recv(3).decode())
        idGroup = int(my_socket.recv(7).decode())
        lenUsername = 0
        usernames = ""

        if typeMsg == 600:
            IsOut = True
            PRINT("IsOut")
        else:#???
            lenUsername = int(my_socket.recv(2).decode())
            usernames = my_socket.recv(lenUsername).decode()

            data = openDataRecv()
            times = timesAll()

            if idGroupGlobal != idGroup:
                try:
                    otherData[idGroup] += 1
                except:
                    otherData[idGroup] = 1
                #PRINT("otherData", otherData)
                groups()

            else:
                listBigTime, smallTime = date(times)
                if (listBigTime[0] != year) and (listBigTime[1] != month) and (listBigTime[2] != day):
                    year = listBigTime[0]
                    month = listBigTime[1]
                    day = listBigTime[2]
                    PRINT("{}/{}/{}".format(year, month, day))
                else:
                    if listBigTime[0] != year:
                        year = listBigTime[0]
                        PRINT(listBigTime[0])

                    if listBigTime[1] != month:
                        month = listBigTime[1]
                        PRINT("{}/{}".format(listBigTime[0], listBigTime[1]))

                    if listBigTime[2] != day:
                        day = listBigTime[2]
                        PRINT("{}/{}".format(listBigTime[1], listBigTime[2]))
                    PRINT(smallTime + " " + usernames + " " + data)
    mainMenu()

def mainMenu():
    global username
    global isExitGroup
    global idGroupGlobal
    global otherData

    global year
    global month
    global day

    clearScreen()
    commands = ""
    if not IsGrafik:
        PRINT("Welcome!!!")
        PRINT("Commands: To enter group mode write 'groups' and to enter user settings mode write 'user': ", "")
        commands = input("")
    if commands.lower() == "groups":
        sendRequestListGroups(username)
        typeMsg = my_socket.recv(3).decode()
        try:
            len = my_socket.recv(6).decode()
            akk = int(len)
            len = akk
        except:
            pass
        listStr = "[{}]".format(my_socket.recv(len).decode())
        listUsersGroup = ast.literal_eval(listStr)
        listGroup = {}
        for i in listUsersGroup:
            lens = int(i[:2])
            nameGroup = i[2:2+lens]
            if nameGroup == "NULL":
                break
            id = int(i[2+lens:])
            # listGroup[nameGroup] = id
            try:
                listGroup[nameGroup] += 0
                listGroup[nameGroup + str(id)] = id#str(j).zfill(lenMaxId)
            except:
                listGroup[nameGroup] = id
            # print(listGroup)


        sum = 0
        lenList = lensList(listGroup) - 1
        if not IsGrafik:
            PRINT("You have {} grups.\n".format(lenList + 1))

        for i in listGroup:
            PRINT(i, "")
            if sum != lenList:
                PRINT(", ","")
            sum += 1
        PRINT("\n")
        nameGroup = ""

        while not checkLogin(nameGroup):
            if not IsGrafik:
                PRINT("To create a new group or join an existing group, enter the group name: ", "")
                nameGroup = input("")
                # print("listGroup", listGroup)
        if not (nameGroup in listGroup):
            if not IsGrafik:
                PRINT("Write the usernames of the group members (Enter each name in between).\n")
            users = [username]
            nameUser = ""
            while nameUser != "QUIT":
                PRINT("Enter a username of group member: ", "")
                nameUser = input("")
                if nameUser != "QUIT" and checkLogin(nameUser):
                    users.append(nameUser)

            a = createGroup(nameGroup, users)
            sendData(a)
            typeMsg = my_socket.recv(3).decode()
            idGroup = int(my_socket.recv(7).decode())

            # listGroup[idGroup] = nameGroup

            listGroup[nameGroup] = idGroup

            # print("idGroup", idGroup)
            # print("nameGroup", nameGroup)
            # print("listGroup", listGroup)
            idGroupGlobal = idGroup
            print("listGroup", listGroup)



            mainMenu()

        else:

            idGroup = listGroup[nameGroup]
            otherData[idGroup] = 0
            idGroupGlobal = idGroup
            data = RequestDBGroup(idGroup)
            sendData(data)
            typeMsg = my_socket.recv(3).decode()

            data = openDataRecv()

            groupDB = getDBGroupFromSerevr(data)
            dataGroups[idGroup] = groupDB
            printGroup(nameGroup, groupDB)

            myMsg = ""
            isExitGroup = False
            t = threading.Thread(target=job, args=(idGroup,))
            t.start()
            groups()

    elif commands.lower() == "user":
        clearScreen()
        isChangeName = ""
        if not IsGrafik:
            PRINT("User settings")
            PRINT("Do you want to change the username? (Press 'Y' or 'N'): ", "")
            isChangeName = input("")

        if isChangeName == "Y":
            newName = ""
            while not checkLogin(newName):
                newName = ""
                if not IsGrafik:
                    PRINT("Enter the new username: ", "")
                    newName = input("")
                if not checkLogin(newName):
                    if not IsGrafik:
                        PRINT("Username is invalid.")
            msgNewName = changeName(username, newName)
            sendData(msgNewName)

            isSuccess = my_socket.recv(1).decode()

            if isSuccess == "T":
                username = newName
            else:
                if not IsGrafik:
                    PRINT("Your chosen username will be taken.")
        isChangePassword = ""
        if not IsGrafik:
            PRINT("Do you want to change the password? (Press 'Y' or 'N'): ", "")
            isChangePassword = input("")

        if isChangePassword == "Y":
            newPassword = ""
            while not checkLogin(newPassword):
                if not IsGrafik:
                    #PRINT("Enter the new password: ", "")
                    #newPassword = input("")#___
                    newPassword = getpass.getpass(prompt='Enter the new password: ', stream=None)
                if not checkLogin(newPassword):
                    if not IsGrafik:
                        PRINT("Password is invalid.")

            msgNewPassword = changePassword(username, newPassword)
            sendData(msgNewPassword)

        mainMenu()
    mainMenu()
#dictDBForEach(groupDB, "epoch", "username", "data" )
def dictDBForEach(db, row, *args):
    listRow = []
    dict = {}
    listArgs = []

    for i in db[row]:
        listRow.append(i)
    sum = 0

    listRow = doubleData(listRow)

    for i in args:
        listArgs.append([])
        for j in db[i]:
            listArgs[sum].append(j)
        sum += 1

    for i in range(len(listRow)):
        dict[listRow[i]] = [listArgs[0][i], listArgs[1][i]]
        # try:
        #     a = dict[listRow[i]][0]
        #     dict[listRow[i]] = [listArgs[0][i], listArgs[1][i]]
        # except:
        #     dict[listRow[i]] = [listArgs[0][i], listArgs[1][i]]
    return dict

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

def date(date):
    global year
    global month
    global day

    index = date.index("-")
    bigTime = date[:index]
    smallTime = date[index + 1:]

    timeStr = ""
    listBigTime = []
    listSmallTime = []

    for i in bigTime:
        if i != "/":
            timeStr += i
        else:
            listBigTime.append(timeStr)
            timeStr = ""
    listBigTime.append(timeStr)
    timeStr = ""

    smallTime = smallTime.replace("/", ":")


    return (listBigTime, smallTime)

def printGroup(nameGroup, groupDB):
    global year
    global month
    global day

    clearScreen()
    sum = 0
    PRINT(nameGroup + "\n")
    smallTime = ""
    spaces = " " * 0

    datas = dictDBForEach(groupDB, "epoch", "username", "data" )
    listTimes = []

    for i in datas:
        listTimes.append(float(i))

    #listTimes = doubleData(listTimes)

    listTimes.sort()
    for i in listTimes:
        data = datas[str(i)]
        dates = timesAll(i)

        if sum == 0:
            listBigTime, smallTime = date(dates)

            year = listBigTime[0]
            month = listBigTime[1]
            day = listBigTime[2]
            if not IsGrafik:
                PRINT(spaces + "{}/{}/{}".format(year, month, day))
                PRINT("The group was created\n")
        else:
            listBigTime, smallTime = date(dates)

            if (listBigTime[0] != year) and (listBigTime[1] != month) and (listBigTime[2] != day):
                year = listBigTime[0]
                month = listBigTime[1]
                day = listBigTime[2]
                if not IsGrafik:
                    PRINT(spaces + "{}/{}/{}".format(year, month, day))
            else:
                if listBigTime[0] != year:
                    year = listBigTime[0]
                    if not IsGrafik:
                        PRINT(spaces + listBigTime[0])

                if listBigTime[1] != month:
                    month = listBigTime[1]
                    if not IsGrafik:
                        PRINT(spaces + "{}/{}".format(listBigTime[0], listBigTime[1]))

                if listBigTime[2] != day:
                    day = listBigTime[2]
                    if not IsGrafik:
                        PRINT(spaces + "{}/{}".format(listBigTime[1], listBigTime[2]))
        if not IsGrafik and sum != 0:
            dataTemp = data[1]
            if dataTemp == "nan":
                dataTemp = "NaN"
            PRINT(smallTime + " " + data[0] + " " + dataTemp)
        sum += 1

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
            dbGroups = dbGroups.append(db_group)
        sumI += 1
    return dbGroups

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

def doubleData(arr):
    tempArr = []
    for i in arr:
        if arr.count(i) > 1:
            tempArr.append(str(float(i) + random.random()))
        else:
            tempArr.append(str(float(i)))
    return tempArr

def getIsGrafik():
    global IsGrafik
    if len(sys.argv) > 1 and sys.argv[1] == "true":
        pass
        #IsGrafik = True


def main():
    global username
    global listGroup
    getIsGrafik()
    WhatIsOsRuns()

    Gateway()
    # try:
    #     Gateway()
    # except:
    #     if not IsGrafik:
    #         PRINT("is EXIT")



if __name__ == '__main__':
    main()

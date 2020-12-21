while not exit:
      rlist, wlist, xlist = select.select( [server_socket] + open_client_sockets, [], [] )
      for current_socket in rlist:
          if current_socket is server_socket:
              (new_socket, address) = server_socket.accept()
              #print("new_socket", new_socket.getpeername())
              open_client_sockets.append(new_socket)

              with threadLockLogin:
                  isLogin = True
                  tempClient = new_socket
                  # print("getsockname", tempClient.getsockname())
                  # print("fileno", tempClient.fileno())

                  listTempClient.append(new_socket)
          else:
              #t = threading.Thread(target=job, args=(current_socket,))
              try:
                  typeMsg = current_socket.recv(3).decode()
                  data = current_socket.recv(1024).decode()
                  # t = threading.Thread(target=job))
                  #if not isJob:
                      #t.start()
                  try:
                      typeMsg = int(typeMsg)
                      status(typeMsg, data)
                  except:
                      pass
              except:
                  pass
              if data == "":
                  open_client_sockets.remove(current_socket)
                  tempUsersSocket = copy.copy(usersSocket)
                  for usernameOut in tempUsersSocket:
                      if usersSocket[usernameOut] is current_socket:
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
              else:
                  messages_to_send.append((current_socket, data))
                  try:
                      pass#send_waiting_messages(wlist)
                  except:
                      pass

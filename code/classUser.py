import threading
import pandas as pd
import os
import time

path = r'/Users/michaelshalitin/Desktop/db/DB/db_groups.csv'
#Keys

#DB
threadLockDBUsers = threading.Lock()
threadLockDBGroup = threading.Lock()

#Vars
threadLockUsers = threading.Lock()

class User:
    def __init__(self, name, password, id = None):
        self.name = name
        self.password = password
        self.id = id

    def create_group(self, name, users):

# def main():
#     pass
#
# if __name__ == '__main__':
#     main()

# importing libraries

from funcs.functions import *
import sqlite3




try:
    """Connecting to sqlite database"""
    connection = sqlite3.connect("users.db")
    print("[+] Connect successfully :)")

except Exception as error:
    print("[-] Can not connect to sqlite database :(", str(error))
    exit()

else:
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE if not exists USERS (username TEXT, email TEXT, password TEXT)")

    req = input(">> First one sign in into wallet (login or register) ? ").casefold()

    if req == 'register':
    
        # call function register_user()
        register_user()

    elif req == 'login':
        
        # call function login_user()
        login_user()            
    
    else:
        print("[-] Command is unknown !!")


    cursor.close()
    connection.close()   



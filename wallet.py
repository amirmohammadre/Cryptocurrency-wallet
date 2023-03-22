#importing libraries
from validate_email import validate_email
import rsa
import time
import sqlite3
import getpass
import hashlib
import os



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

        while True:

            username = input(">> Please enter a username: ")
            email    = input(">> Enter your Email Address: ")
            password = getpass.getpass(">> Enter your password: ")


            """Checking the validity of the email address with packages validate_email and py3dns"""
            email_valid = validate_email(email, verify = True)


            if username.isidentifier() and len(password) >= 8 and email_valid:
            
                hash_pass = hashlib.sha256(password.encode())
        
                cursor.execute("INSERT OR REPLACE INTO USERS (username, email, password) VALUES (\"%s\", \"%s\", \"%s\");" 
                                % (username, email, hash_pass.hexdigest()))
                
                connection.commit()
            
            
                print("[+] You are joined into cryptocurrency wallet :D".center(100,"*"))
                time.sleep(2)


                os.mkdir('{}'.format(username))
                os.chdir('{}'.format(username))


                """Generated public key and private key with algorithme RSA"""
                public_key, private_key = rsa.newkeys(1024)

                with open("public-{}.pem".format(username), "wb") as f:
                    f.write(public_key.save_pkcs1("PEM"))

                print("[+] Generated successfully RSA Public Key".center(100, "+"))
                time.sleep(2)

                with open("secret-{}.pem".format(username), "wb") as f:
                    f.write(private_key.save_pkcs1("PEM"))

                print("[+] Generated successfully RSA Secret Key".center(100, "+"))
                time.sleep(2)


                f_pub = open("public-{}.pem".format(username), "r")

                for line in f_pub:
                    print(line.strip())
                
                f_pub.close()            

                exit()


            else:
                print("[-] The fields are invalid !! ")
                continue


    elif req == 'login':
        
        while True:
        
            uname          = input("Enter your username: ")
            password_check = getpass.getpass("Enter your password: ")

            password_hash_check = hashlib.sha256(password_check.encode())
            hexadecimal_password_hash_check = password_hash_check.hexdigest()                  

            
            cursor.execute("SELECT password from USERS WHERE username = ?", (uname, ))
            valid_pass = cursor.fetchall()
            

            """Convert list to string"""
            raw_valid_pass = "".join(map(str, valid_pass[0][0]))


            """Check user login in to system"""
            if hexadecimal_password_hash_check == raw_valid_pass:
                print("[+] Login was successful :)")
                
                os.chdir('{}'.format(uname))

                pub_uname = open("public-{}.pem".format(uname), "r")
                for line in pub_uname:
                    print(line.strip())
                
                pub_uname.close()   


                exit()


            else:
                print("[-] Login Failed :( try again")
                continue
        
        
    else:
        print("[-] Command is unknown !!")



    cursor.close()
    connection.close()   














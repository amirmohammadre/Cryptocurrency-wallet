from validate_email import validate_email
from Crypto.PublicKey import RSA
import subprocess
import time
import getpass
import hashlib
import os
import sqlite3



connection = sqlite3.connect("users.db")
cursor = connection.cursor()



##################################################################
#            Function for register user into system 
##################################################################
def register_user():

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


                # call function generate_public_and_private_key
                create_public_and_private_key(username)


            else:
                print("[-] The fields are invalid !! ")
                continue


##################################################################
#  Function for generate secret key and public key for each user 
##################################################################
def create_public_and_private_key(username:str):

    """Generated public key and private key with algorithme RSA"""

    key      = RSA.generate(2048)
    
    with open("public-{}.pem".format(username), "wb") as f:
        f.write(key.publickey().exportKey("PEM"))

    print("[+] Generated successfully RSA Public Key".center(100, "+"))
    time.sleep(2)

    with open("secret-{}.pem".format(username), "wb") as f:
        f.write(key.exportKey("PEM"))

    print("[+] Generated successfully RSA Secret Key".center(100, "+"))
    time.sleep(2)


    f_pub = open("public-{}.pem".format(username), "r")

    for line in f_pub:
        print(line.strip())
                
    f_pub.close()            

    exit()


##################################################################
#            Function process login user into system 
##################################################################
def login_user():

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

            # call function send_public_key
            send_public_key(uname)  

        else:
            print("[-] Login Failed :( try again")
            continue


##################################################################
#            Transfer public key to remote server 
##################################################################
def send_public_key(uname:str):
    
    h_name          = input("Enter the IP address of the remote server: ")
    server_username = input("username of the remote server: ")
    path_desired    = input("path desired for transfer file to remote server: ")

    p   = subprocess.Popen(["scp", "public-{}.pem".format(uname), "{su}@{hn}:{pd}"
                        .format(su = server_username, hn = h_name, pd = path_desired ) ])
    sts = os.waitpid(p.pid, 0)


    exit()




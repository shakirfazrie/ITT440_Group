import socket #import socket library
import os     #
import tqdm
import time
import sys
import getpass
import emoji

class Client:
    print('\n******************************************************')
    print('\n\tWelcome To Secure File Transfer system\t')
    print('\n\t\tMade with Python\t\t')
    txt = emoji.emojize(":snake:")
    x = txt.center(45," ")
    print(x)
    print('\n******************************************************')
    cl = '\tClient\n'
    
    #create socket (TCP Protocol)
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect_to_server()
 
    #create a connection to the server
    def connect_to_server(self):
        self.target_ip = input(str('\tPlease Enter Server Ip Address : '))
        self.target_port = input('\tPlease Enter Server Port Number : ')

        #receive connection from server
        self.sock.connect((self.target_ip,int(self.target_port)))

        self.main()

    def main(self):
        #verify a new user
        New = input('\t\nWhich user are you? [ y - new user | n - old user] :')
        self.sock.send(New.encode())   #send input user to server
        if New == 'y':   #if new user
            username = input('\tEnter New Username : ')
            self.sock.send(username.encode())

            password = getpass.getpass('\tEnter New Password : ', stream=None)
            self.sock.send(password.encode())

            #register new user
            register = self.sock.recv(1024)

            if register.decode() == "continue":
                print('\t\t\nPlease Re-enter Your Credential')

                #login new registered user
                username = input('\tEnter Username : ')
                self.sock.send(username.encode())

                password = getpass.getpass('\tEnter Password : ', stream=None)
                self.sock.send(password.encode())

                #if the username and password does not exist in the login.txt
                login = self.sock.recv(1024)
                if login.decode() == "Not-a-user":
                    print("\tYour Credential Could Not Be Verified ! Connection will be terminate !")

                    self.sock.shutdown(socket.SHUT_RDWR)
                    self.sock.close()
                    sys.exit()
                else:
                    print(login.decode())  #print welcome new user

        else:   #if not a new user
            print('\t\t\nPlease Enter Your Credential\n')
            username = input('\tEnter Username : ')
            self.sock.send(username.encode())

            password = getpass.getpass('\tEnter Password : ', stream=None)
            self.sock.send(password.encode())

            #if username and password does not exist in login.txt
            login = self.sock.recv(1024)
            if login.decode() == "Not-a-user":
                print("\tYour Credential Could Not Be Verified ! Connection will be terminate !")

                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
                sys.exit()
            else:
                print(login.decode())  #print welcome back
        print('\n-----------------------------------------------------')
        print("\t\n To Terminate The Connection, Enter 'exit'")
        print('\n-----------------------------------------------------')
        while 1:
            #input requested file name 
            file_name = input('\t\nPlease Enter File Name On Server : ')
            if file_name == "exit":
                sys.exit()

            else:
                self.sock.send(file_name.encode())  #client send file name to server

            confirm = self.sock.recv(1024)
            if confirm.decode() == "File Is Not Available In The Server":
                exist = "\t\nFile Is Not Availabe In The Server.\n"
                print('----------------------------------------------------')
                continue

            else:   #if file exist in the server
                write_name = file_name
                if os.path.exists(write_name): os.remove(write_name)

                #file download from the sever
                with open(write_name,'wb') as file:
                    while 1:
                        data = self.sock.recv(1024)

                        if not data:
                            break

                        file.write(data)
                        break

                print('\t\nFile Successfully Download From The Server.\n')
                print('-----------------------------------------------------')
                continue
client = Client()

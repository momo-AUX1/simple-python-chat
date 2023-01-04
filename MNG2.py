import socket
import time
import random
import platform
import codecs
import datetime
import base64
import sys



print("==================================================")
print("[+] johnny chat app version 2")
name = input("[?] Enter your name:")
A = input("[+] please chose your role -1 server -2 client:")
print("==================================================")
ver = platform.uname().release
sys = platform.uname().system
OS = sys + ver
PXR = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
passw = PXR.split()
password = ''.join(random.sample(PXR, k=6))
date = datetime.datetime.now()

if A == "1":
    L = 0
    print("[!] you are the host convo")
    enc = ""
    while L < 1:
        choose = int(input("[?] please insert encryption method 1- ascii, 2- UTF-8:"))
        if choose == 1:
            enc = "ascii"
            print("[+] encryption method set:", enc)
            L = 1
        elif choose == 2:
            enc = "utf-8"
            print("[+] encryption method set:", enc)
            L = 1
        else: 
            print("[-] please insert a valid encryption method:")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[+] creating host socket...")
    L1 = 0
    while L1 < 1:
        IP = int(input("[?] Please insert prefered ip method -1 localhost -2 private ip -3 custom ip:"))
        if IP == 1:
            IP = "0.0.0.0"
            print("[+] IP set:", IP)
            L1 = 1
        elif IP == 2:
            host = socket.gethostname()
            IP = socket.gethostbyname(host)
            print("[+] IP set:", IP)
            L1 = 1
        elif IP == 3:
            IP = input("[?] Enter custom IP address:")
            print("[+] IP set:", IP)
            L1 = 1
        else:
            print("[-] please enter a valid IP method.")
    L2 = 0
    port = int(input("[?] please enter a port method -1 default -2 custom:"))
    if port == 1:
        port = 9999
        print("[+] port set:", port)
        L2 = 1
    elif port == 2:
        port = int(input("[?] please enter a port"))
        print("[+] port set:", port)
        L2 = 1
    else:
        print("[-] didn't specify a correct port method assuming default")
        port = 9999
        print("[+] port set:", port)
        L2 = 1
    try:
        s.bind((IP, port))
        print("[+] binding", IP, ":", port,".....")
    except:
        print("[-] could not bind", IP, ":", port)
        print("[x] the program will exit in 5 seconds")
        time.sleep(5)
        sys.exit()
    try:
        s.listen(1)
        print("[+] successfully binded", IP, ":", port)
        print("[+] listening for incoming connections....")
        print("[!] the password for connection is:", password)
    except:
        print("[-] failed to listen for incoming connections")
        print("[x] the program will exit in 5 seconds")
        time.sleep(5)
        sys.exit()
    connection, address = s.accept()
    print("[+] successfully connected to:", address)
    print("[!] awaiting password challenge....")
    print("[!] password challenge remainder:", password)
    code = connection.recv(4096)
    WX = 0
    while WX < 1:
        if code.decode("utf-8") == password:
            print("[+] password was encoded in UTF-8 and correcly matched host password")
            print("[+] matching host and client encryption:", enc)
            connection.send(enc.encode("ascii"))
            WX = 1
        elif code.decode("ascii") == password:
            print("[+] password was encoded in ASCII and correcly matched host password")
            print("[+] matching host and client encryption:", enc)
            connection.send(enc.encode("ascii"))
            WX = 1
        else:
            print("[!] Password or encryption did not match host.")
            print("[x] the program will exit in 5 seconds")
            exi = "exit"
            connection.send(exi.encode("ascii"))
            time.sleep(5)
            sys.exit()
            break
    while True:
        try:
            message = connection.recv(4096)
            print("[+]", message.decode(enc))
            res = input("[?] enter your reply:")
            save = False
            response = name + "(" + OS + ")" + ":" + res 
            if res == "/save":
                print("[!] input gotten started saving convo")
                save = not save
                if save == True:
                    with open("client_convo.txt", "a+") as f:
                        f.write("")
                        xcx = 0
                        if xcx < 1:
                            f.write("================================================================")
                            f.write("/n")
                            f.write("convo log from", date)
                            f.write("/n")
                            f.write("================================================================")
                            f.write("/n")
                            xcx = 1
                        f.write(res)
                        f.write("/n")
                elif save == False:
                    print("[!] stopped saving the convo")
                        
            elif res == "exit":
                print("[!] input recieved exit the program will exit in 5 seconds")
                time.sleep(5)
                sys.exit()
            elif res == "commands":
                print("[+] command received: exit - closes the chat  /save saves the convo to a text file [DOESN'T WORK")

            connection.send(response.encode(enc))
        except:
            print("[!] lost connection to client the program will exit in 5 seconds")
            time.sleep(5)
            sys.exit()
if A == "2":
    print("[!] you are the client of this convo")
    enc = "ascii" 
    IP = input("[+] Enter host IP address:")
    print("[+] host IP:", IP)
    port = int(input("[+] enter host port:"))
    print("host port:", port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("[+] creating a client socket...")
    try:
        s.connect((IP, port))
        print("[!] trying to connect to:", IP , ":", port)
    except:
        print("[x] failed to connect to", IP , ":", port)
        print("[x] the program will exit in 5 seconds.")
        time.sleep(5)
        sys.exit()
    A = input("[!] insert host password:")
    s.send(A.encode(enc))
    enc = s.recv(4096).decode("ascii")
    if enc == "exit":
        print("[!] host refused the password")
        time.sleep(5)
        print("[x] password did not match the host. exiting")
        time.sleep(2)
        sys.exit()
        
    else:
        print("[+] host accepted the password")
        print("[!] synced encryption with host:", enc)
    while True:
        try:
            res = input("[?] enter your message:")
            save = False
            response = name + "(" + OS + ")" + ":" +res 
            if res == "/save":
                print("[!] input gotten started saving convo")
                save = not save
                if save == True:
                    with open("host_convo.txt", "a+") as x:
                        x.write("")
                        xcx = 0
                        if xcx < 1:
                            x.write("================================================================")
                            x.write("/n")
                            x.write("convo log from", date)
                            x.write("/n")
                            x.write("================================================================")
                            x.write("/n")
                            xcx = 1
                        x.write(res)
                        x.write("/n")
                elif save == False:
                    print("[!] stopped saving the convo")
                        
            elif res == "exit":
                print("[!] input recieved exit the program will exit in 5 seconds")
                time.sleep(5)
                sys.exit()
            elif res == "commands":
                print("[+] command received: exit - closes the chat  /save saves the convo to a text file[DOESN'T WORK]")

            s.send(response.encode(enc))
            message = s.recv(4096)
            print("[+]", message.decode(enc))
        except:
            print("[!] lost connection to host the program will exit in 5 seconds")
            time.sleep(5)
            sys.exit()



        
    

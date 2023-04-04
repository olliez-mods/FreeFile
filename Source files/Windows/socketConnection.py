import socket
import os
import sendFile
import receiveFile
import updateProgram
import FileName

SEPARATOR = "<SEPARATOR>"
buffer_size = 4096 # send/receive 4096 bytes each time step



host = "freefile.my.to"
#host = "localhost"
port = 1020

# connects to the server and returns the socket, or returns -1 if couldn't connect
def connect():
    s = socket.socket()

    # turns the hostname to an ip
    try:
        host_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[+] Could not resolve {host}.")
        return -1
    
    print(f"[+] Connecting to {host}({host_ip}):{port}")
    try:
        s.connect((host, port))
    except:
        print("Connected made an error oops.")
        return -1
    s.settimeout(3)

    # once we connect, we want the server to asend us a message saying that it sees us
    try:
        received = s.recv(buffer_size).decode()
        if(received == "imhere"):
            print("[+] Connected.")
            return s
    except:
        pass
    print("[+] Could not connect to server")
    return -1

def getFileName(code):
    # return -2 if the code won't work
    if len(code) != 2:
        return -2
    if not code.isalpha():
        return -2

    # connect to server, if cant connect return -1
    s = connect()
    if(s == -1):
        return -1

    file_name = FileName.getName(s, code.upper())
    s.close()
    return file_name


def rcvFile(code, path, file_name, pb = -1, lb = -1):
    s = connect()
    if(s == -1):
        return -1
    receiveFile.receive(s, code.upper(), path, file_name, pb, lb)
    s.close()

def update(pb = -1, lb = -1):
    s = connect()
    if(s == -1):
        return -1
    success = updateProgram.update(s, pb, lb)
    s.close()
    return success
    

def sndFile(filename, pb = -1, lb = -1):
    s = connect()
    if(s == -1):
        return -1
    code = sendFile.send(s, filename, pb, lb)
    s.close()
    return code


if __name__ == "__main__":
    file_name = ""
    s = socket.socket()
    while True:
        command = input("Command: ")
        if command == "quit" or command == "q" or command == "exit":
            s.close()
            break
        if command.split(" ")[0] == "send":
            print("Code:", sndFile(command.split(" ")[1]))
        if command.split(" ")[0] == "get":
            print("Requesting file")
            code = command.split(" ")[1]
            file_name = getFileName(code)
            if file_name != -1 and file_name != -2:
                path = input("Path or q: ")
                if path != "q":
                    rcvFile(code, path, file_name)




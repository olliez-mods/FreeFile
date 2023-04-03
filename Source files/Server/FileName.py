import os
#import tqdm
import random
import time

SEPARATOR = "<SEPARATOR>"
buffer_size = 4096

    
def getName(client_socket, address, token):
    try:
        
        client_socket.send("rdy".encode())
    
        code = client_socket.recv(buffer_size).decode()
        print(str(token) + ": Received:", code)

        if len(code) != 2:
            print(str(token) + ": Unexpected data received (Error)")
            client_socket.send("cdeWrngLngth".encode())
            return
        if not code.isalpha():
            print(str(token) + ": Unexpected data received (Error)")
            client_socket.send("cdeWrngFrmt".encode())
            return
        if not os.path.exists("files/" + str(code) + ".info"):
            print(str(token) + ": No file with that code (Error)")
            client_socket.send("cdeWrngNme".encode())
            return
        
        #writing incoming file to a new file called "code"
        with open("files/" + str(code) + ".info", "r") as f:
            content = f.read(buffer_size).split("\n")
            
        print(str(token) + ": File name is:", content[1])
        client_socket.send(content[1].encode())
        
    except Exception as err:
        print(err)
        print(str(token) + ": Unexpected error when transmiting file name (Error)")


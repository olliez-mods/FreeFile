import os
#import tqdm
import random
import time

SEPARATOR = "<SEPARATOR>"
buffer_size = 4096

LETTERS = ""
with open("letters.txt", "r") as f:
    LETTERS = f.read(4096).split(" ")


# use random.choice() to pick a random letter, save the file and a config file with that letter combo
# and retun to user

def getCode():
    return random.choice(LETTERS)
    
def receive(client_socket, address, token):
    try:
        code = getCode()
        
        client_socket.send("rdy".encode())
    
        received = client_socket.recv(buffer_size).decode()
        print(str(token) + ": Received:",received)

        if len(received.split(SEPARATOR)) != 2:
            print(str(token) + ": Unexpected data received (Error)")
            return
        
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename("files/"+filename)

        print(str(token) + ": Receiving", filename, "of size:", int(filesize)/1000000, "|", code)

        #writing incoming file to a new file called "code"
        #progress = tqdm.tqdm(range(int(filesize)), str(token) + ": Receving file", unit="B", unit_scale=True, unit_divisor=1024)
        with open("files/" + code, "wb") as f:
            while True:
                bytes_read = client_socket.recv(buffer_size)
                #print(bytes_read)
                if bytes_read == b"fileTrnsferComplte":
                    #progress.close()
                    break
                f.write(bytes_read)
                #progress.update(len(bytes_read))

        # create the files data file, will be called "code".info
        with open("files/" + code + ".info", "w") as f:
                f.write(str(address[0]) + "\n" + str(filename) + "\n" + str(filesize))
                
        print(str(token) + ": FileTransferd")
        client_socket.send("succs".encode())
        time.sleep(0.2)
        client_socket.send(code.encode())
        
    except Exception as err:
        print(err)
        print(str(token) + ": Unexpected error when receiving a file (Error)")


import os
import time

SEPARATOR = "<SEPARATOR>"
buffer_size = 4096

#gets the information concerning the file from the "code".info file
def getFileInfo(code):
    with open("files/" +code + ".info", "r") as f:
        content = f.read().split("\n")
    return content[1],content[0],content[2]

def send(client_socket, token):
    try:
        client_socket.send("rdy".encode())

        #receive the file code form the client
        received = client_socket.recv(buffer_size).decode()
        code = received

        #these values are returned by getFileInfo
        filename, address, filesize = getFileInfo(code)
    
    
        # remove absolute path if there is
        filename = os.path.basename(filename)


    
        print(str(token) + ": Sending", filename, "Size",filesize, "|",code,"|")

        filesize = os.path.getsize("files/"+code)
        client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
        time.sleep(0.2)

        with open("files/" + code, "rb") as f:
            while True:
                bytes_read = f.read(buffer_size)
                if not bytes_read:
                    time.sleep(1)
                    client_socket.sendall(b"fileTrnsferComplte")
                    break
                client_socket.sendall(bytes_read)
        print(str(token) + ": FileTransferd")
    except Exception as err:
        print(err)
        print(str(token) + ": Unexpected error when sending a file (Error)")


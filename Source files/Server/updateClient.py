import os
import time

SEPARATOR = "<SEPARATOR>"
buffer_size = 4096


def update(client_socket, token):
    try:
        client_socket.send("rdy".encode())

        #these values are returned by getFileInfo
        filename = "Free File.exe"
        filesize = os.path.getsize("Free File.exe")

    
        print(str(token) + ": Sending new EXE with size",filesize)

        client_socket.send(f"{filesize}".encode())
        time.sleep(0.2)

        with open(filename, "rb") as f:
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


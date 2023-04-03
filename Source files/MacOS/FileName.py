import time

SEPARATOR = "<SEPARATOR>"
buffer_size = 4096

def getName(s, code):
    s.send("getFleNme".encode())

    print("waiting")
    # The server will say that is ready
    received = s.recv(buffer_size).decode()

    if received != "rdy":
        print("Error from server-side")
        return -1
    print("Server is ready to transmit file name")

    if code == "":
        print("No code")
        return -2
    s.send(str(code).encode())

    file_name = s.recv(buffer_size).decode()

    if file_name == "cdeWrngLngth":
        print("Wrong length")
        return -2
    if file_name == "cdeWrngFrmt":
        print("Wrong format")
        return -2
    if file_name == "cdeWrngNme":
        print("No such code")
        return -3

    print("File name is:", file_name)
    return file_name
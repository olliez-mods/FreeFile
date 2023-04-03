import socket
import os
import time

SEPARATOR = "<SEPARATOR>"
buffer_size = 4096

# s is socket
def send(s, file_name, pb, lb):

    #let server know we want to send them a file
    s.send("sndFile".encode())

    # this lets us know the server is ready
    response = s.recv(buffer_size).decode()
    if response != "rdy":
        print("[+] Error from server-side")
        return -1
    print("[+] Server ready to receive file")

    # get info on our file
    file_size = os.path.getsize(file_name)

    #send file info to the server
    s.send(f"{os.path.basename(file_name)}{SEPARATOR}{file_size}".encode())
    time.sleep(0.2)

    # update is a counter once it passes x, the progress bar will update (this reduces lag)
    update = 0
    bytes_sent = 0
    if lb != -1:
        lb['text'] = 0
    if pb != -1:
        pb['maximum'] = file_size
        pb['value'] = 0


    # open the file and send it in chunks of size buffer-size
    with open(file_name, "rb") as f:
        while True:
            bytes_read = f.read(buffer_size)
            #progress.update(len(bytes_read))
            if not bytes_read:
                # send this message to signal that we finished
                time.sleep(1)
                s.sendall(b"fileTrnsferComplte")
                break
            s.sendall(bytes_read)
            bytes_sent += len(bytes_read)
            update += 1
            if update > 400:
                update = 0
                if pb != -1:
                    pb['value'] += len(bytes_read)*400
                if lb != -1:
                    lb['text'] = str(int(bytes_sent*100/file_size)) + "%"


    #wait for confirmation that the fle transferred successfully
    try:
        response = s.recv(buffer_size).decode()
    except:
        print("[+] server didnt respond")
        return -1
    if response == "succs":
        print("[+] File transfer successful")
        #waiting to receive the file code
        code = s.recv(buffer_size).decode()
        lb['text'] = "100%"
        pb['value'] = pb['maximum']
        return code
    else:
        print("[+] Error transferring file")
        lb['text'] = "Error"
        return -2
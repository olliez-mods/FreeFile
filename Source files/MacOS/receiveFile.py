import os
import time

SEPARATOR = "<SEPARATOR>"
buffer_size = 4096

def receive(s, code, path, file_name, pb, lb):
    s.send("rcvFile".encode())

    # this lets us know the server is ready
    response = s.recv(buffer_size).decode()
    if response != "rdy":
        print("[+] Error from server-side")
        return -1
    print("[+] Server ready to send file")

    s.send(code.encode())

    received = s.recv(buffer_size).decode()

    svr_file_name, file_size = received.split(SEPARATOR)
    # remove absolute path if there is
    svr_file_name = os.path.basename(svr_file_name)

    print("Receiving", svr_file_name, "of size:", file_size, "as", file_name, "|" + str(code) + "|")

    file_size = int(file_size)
    # update is a counter once it passes x, the progress bar will update (this reduces lag)
    update = 0
    update_amount = 0

    if lb != -1:
        lb['text'] = "0%"
    if pb != -1:
        pb['maximum'] = file_size
        pb['value'] = 0

    with open(path + "/" + file_name, "wb") as f:
        while True:
            bytes_read = s.recv(buffer_size)
            if bytes_read == b"fileTrnsferComplte":
                break
            f.write(bytes_read)

            update_amount += len(bytes_read)
            update += 1
            if update > 400:
                update = 0
                if pb != -1:
                    pb['value'] = update_amount
                if lb != -1:
                    lb['text'] = str(int(update_amount*100/file_size)) + "%"

    lb['text'] = "100%"
    pb['value'] = pb['maximum']
    print("FileTransferd")


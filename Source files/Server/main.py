import socket
import os
import receiveFile
import sendFile
import FileName
import updateClient
import threading
import random
import time

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 1020

buffer_size = 4096
SEPARATOR = "<SEPARATOR>"

TIMEOUT_TIME = 1200  #Seconds, 33.333.. minutes

client_threads = {}

def get_token():
        choice = random.randint(1000,9999)
        while(choice in client_threads):
                choice = random.randint(1000,9999)
        return choice
        

def client_connection(client_socket, address, token):
    try:
        client_socket.setblocking(1)
        received = client_socket.recv(buffer_size).decode()
        print(str(token) + ": Received:",received)
        if(received == "sndFile"):
            receiveFile.receive(client_socket, address, token)
        if(received == "rcvFile"):
            sendFile.send(client_socket, token)
        if(received == "getFleNme"):
            FileName.getName(client_socket, address, token)
        if(received == "updateEXE"):
             updateClient.update(client_socket, token)
        print(str(token) + ": Client Disconnected")
    except Exception as err:
        print(err)
        print(str(token) + ": Unexpected Disocnnect from client (Error)")
    del client_threads[token]


s = socket.socket()
s.bind((SERVER_HOST,SERVER_PORT))
s.setblocking(0)
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

time_start = time.time()
time_passed = 0

while True:
    try:
        #We expect this to fail when there not a new connection
        client_socket, address = s.accept()
        client_socket.send("imhere".encode())
        found = True
        print(f"\n\n[+] {address} is connected.")
        token = get_token()
        #Create a thread to pass our client_socket and other values to
        client_thread = threading.Thread(target=lambda: client_connection(client_socket, address, token), daemon=True)
        client_threads[token] = [client_thread, address, client_socket, time_passed]
        print("Token:", str(token) + ", Address: [" + str(address[0]) + "]")
        client_thread.start()
    except:
        pass
    time_passed = int(time.time() - time_start)

    try:
        threads_to_kill = []
        for key in client_threads:
            if time_passed - client_threads[key][3] > TIMEOUT_TIME:
                threads_to_kill.append(key)
                print(str(key) + ": Client took too long (Error)")
            
        for key in threads_to_kill:
            client_threads[key][2].close()
            client_threads[key][0]._stop()
            del client_threads[key]
    except:
        print("\nError in the old thread removal loop (Error)\n")


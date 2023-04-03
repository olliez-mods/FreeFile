import sys
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import threading
import socketConnection


def msg_user(title, msg):
    tk.messagebox.showinfo(title,  msg)
def sendFile():
    global running, running_thread
    if not running:
        running_thread = threading.Thread(target=sendFile_thread, daemon=True)
        running_thread.start()
def sendFile_thread():
    global running, running_thread
    running = True

    file_path = filedialog.askopenfilename()
    if(file_path == ""):
        running = False
        return
        
    print(file_path)
    filename = socketConnection.sndFile(file_path, pb = progressBar, lb = label)
    if(filename == -1):
        msg_user("ERROR", "Server connection error")
    elif(filename == -2):
        msg_user("ERROR", "Error when sending a file")
    else:
        entry.delete(0, tk.END)
        entry.insert(0, filename)

    running = False


# Start of the chain to receive a file
def rcvFile():
    global running, running_thread, code
    if not running:

        # creating a thread to receive the file, while also updating the loading bar
        running_thread = threading.Thread(target=rcvFile_thread, daemon=True)
        running_thread.start()
# This thread receives the file, updates the loading bar, and saves the file in storage
def rcvFile_thread():
    global running, running_thread
    running = True

    code = entry.get()

    # calling socketConnection.getFileName, wich will contact server and get the name of the file before prompting
    # the user for as location for the file
    file_name = socketConnection.getFileName(code)
    if(file_name == -1):
        msg_user("ERROR", "Server connection error")
    elif file_name == -2:
        entry['bg'] = "red"
        time.sleep(0.1)
        entry['bg'] = "cornsilk3"
        time.sleep(0.1)
        entry['bg'] = "red"
        time.sleep(0.1)
        entry['bg'] = "cornsilk3"
        running = False
        
    elif file_name == -3:
        msg_user("ERROR", "Server could not find your file")
    else :
        whole_file_path = filedialog.asksaveasfile(initialfile=file_name)
        if not whole_file_path:
            running = False
            return

        file_path = os.path.dirname(whole_file_path.name)
        file_name = os.path.basename(whole_file_path.name)

        socketConnection.rcvFile(code, file_path, file_name, pb = progressBar, lb = label)

    running = False

def cancel():
    global running, running_thread, kill
    if running:
        sys.exit()


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Free File")
    window.geometry("240x85")
    window.maxsize(240, 85)
    window.minsize(240, 85)

    window.attributes('-topmost', True)

    running = False
    kill = False
    running_thread = -1


    codeLabel = tk.Label(
        text = "Code:",
        fg="Black")
    codeLabel.place(x=5,y=5)

    entry = tk.Entry(
        fg="black",
        bg="cornsilk3",
        width=18)
    entry.place(x=50,y=5)

    sendButton = tk.Button(
        text="Upload",
        bg="white",
        fg="black",
        command=sendFile)
    sendButton.place(x=5, y=30)

    getButton = tk.Button(
        text="Download",
        bg="white",
        fg="black",
        command=rcvFile)
    getButton.place(x=80,y=30)

    cancelButton = tk.Button(
        text="Stop",
        bg="white",
        fg="black",
        command=cancel)
    cancelButton.place(x=173,y=30)

    label = tk.Label(
        text = "0%",
        fg="Black")
    label.place(x=5,y=62)

    progressBar = ttk.Progressbar(
        orient='horizontal',
        mode='determinate',
        length=180,
        maximum=100,)
    progressBar.place(x=40,y=65)

    window.mainloop()
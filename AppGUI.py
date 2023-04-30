import psutil
import time
from tkinter import *   


UPDATE_DELAY = 1

running = False
root = Tk()
uploadSpeed = Label(root,text = "work?", bd='10')
io = psutil.net_io_counters()
bytes_sent, bytes_recv = io.bytes_sent, io.bytes_recv
def startProcess():
    uploadSpeed.config(text = "Gotcha")
    print("work")
    #running = True
    updateText()

def get_size(bytes):

    for unit in ['','K','M','G','T','P']:
        if(bytes < 1024):
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def calculateUploadSpeed():
    #time.sleep(UPDATE_DELAY)

    io_2 = psutil.net_io_counters()
    global bytes_sent
    global bytes_recv
    us = io_2.bytes_sent - bytes_sent 
    ds = io_2.bytes_recv-bytes_recv
    uploadSpeed5 = get_size(us / UPDATE_DELAY)
    """print(f"Upload: {get_size(io_2.bytes_sent)}   "
          f", Download: {get_size(io_2.bytes_recv)}   "
          f", Upload Speed: {get_size(us / UPDATE_DELAY)}/s   "
          f", Download Speed: {get_size(ds / UPDATE_DELAY)}/s      ", end="\r")
    """
    bytes_sent, bytes_recv = io_2.bytes_sent, io_2.bytes_recv
    return uploadSpeed5

def updateText():
    uploadSpeed.config(text= calculateUploadSpeed())
    #print("YAYY");
    root.update()
    root.after(100, updateText)

#def getRoot():
def main():
    #root = Tk()
    root.geometry('1000x700')
    # Start Button
    


    uploadLabel = Label(root, text = 'Upload Speed:', bd = '10')
    uploadLabel.place(x=10, y = 200)


    #uploadSpeed = Label(root, text = "work?", bd='10')
    uploadSpeed.place(x=10, y= 300)

    btn = Button(root, text = 'Click me !', bd = '5',
                          command = startProcess)

    #update()

    # Set the position of button on the top of window.  
    btn.pack(side = 'top')   
 
    root.mainloop()

main()

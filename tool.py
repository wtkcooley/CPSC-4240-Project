from time import sleep
import psutil
import datetime
import pandas as pd
from tkinter import *

TITLE = "CPSC 4200 Final - System Monitor Tool"
WIDTH = 1080 #px
HEIGHT = 720 #px
MAX_PROCESSES = 20
UPDATE_INTERVAL = 1000 #ms
FONTSIZE = 8
CELL_WIDTH = 16
WINDOW = Tk()

"""Builds Dataframe of Process info.

:param process_df: data frame with all process info
:param system_info: data frame with all system info
:result: Updates WINDOW with new info
"""
def get_process_info():      
    #Creating lists to store the corresponding information
    cpu_usage= []
    memory_usage = []
    memory_usage_percentage = []
    pids = []
    name = [] 
    status =[]
    create_time =[]
    threads =[]

    num_proc = 0

    #Getting application process information using psutil
    for process in psutil.process_iter():
        if num_proc >= MAX_PROCESSES:
            break
        num_proc = num_proc + 1
        pids.append(process.pid)
        name.append(process.name())

        cpu_usage.append(process.cpu_percent(interval=1)/psutil.cpu_count())
        memory_usage.append(round(process.memory_info().rss/(1024*1024),2))
        memory_usage_percentage.append(round(process.memory_percent(),2))
        create_time.append(datetime.datetime.fromtimestamp(
                            process.create_time()).strftime("%H:%M:%S - %m/%d/%Y"))
        status.append(process.status())
        threads.append(process.num_threads())
        
    #Saving the process information in a python dictionary
    data = {"PIds":pids,
            "Name": name,
            "CPU %":cpu_usage,
            "Memory Usages (MB)":memory_usage,
            "Memory %": memory_usage_percentage,
            "Status": status,
            "Created Time": create_time,
            "Threads": threads,
            }
            
    #Converting the dictionary into Pandas DataFrame
    process_df = pd.DataFrame(data)

    #Setting the index to pids
    process_df = process_df.set_index("PIds")

    #sorting the process 
    process_df = process_df.sort_values(by='Memory Usages (MB)', ascending=False)

    #Adding MB at the end of memory
    process_df["Memory Usages (MB)"] = process_df["Memory Usages (MB)"].astype(str) + " MB"

    return process_df

# Helper function for formating Network info
def get_size(bytes):
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024

def get_network_info():
    io = psutil.net_io_counters(pernic=True)
    sleep(1)
    data = []
    for iface, iface_io in io.items():
        upload_speed, download_speed = io[iface].bytes_sent - iface_io.bytes_sent, io[iface].bytes_recv - iface_io.bytes_recv
        data.append({
            "iface": iface, 
            "Upload": get_size(io[iface].bytes_sent),
            "Upload Speed": f"{get_size(upload_speed)}/s",
            "Download Speed": f"{get_size(download_speed)}/s",
        })
    io = io
    df = pd.DataFrame(data)
    df.sort_values("Upload", inplace=True, ascending=False)
    return df

"""Builds TKinter Window GUI.

:param process_df: data frame with all process info
:param system_info: data frame with all system info
:result: Updates WINDOW with new info
"""
def make_gui(process_df, network_df):
    # Get length of Process Dataframe
    r, c = process_df.shape
    # Make Dataframe a list
    li = [process_df.columns.values.tolist()] + process_df.values.tolist()

    # Add process info to Tkinter grid
    i, j = 0, 0
    for i in range(r):
        for j in range(c):
            e = Label(WINDOW, text=str(li[i][j]),width=CELL_WIDTH, fg='blue',
                        font=('Arial',FONTSIZE,'bold'))
            e.grid(row=i, column=j)
    
    # Add Network Label and spacing to Tkinter Grid
    e = Label(WINDOW, text="",width=CELL_WIDTH, fg='blue',
                        font=('Arial',FONTSIZE,'bold'))
    e.grid(row=i+1, column=0)
    e = Label(WINDOW, text="Network Status",width=CELL_WIDTH, fg='blue',
                        font=('Arial',FONTSIZE,'bold'))
    e.grid(row=i+2, column=0)

    # Get length of network dataframe + x value of previous dataframe
    r, c = network_df.shape
    row = process_df.shape[0] + 3

    # Convert network dataframe to list
    li = [network_df.columns.values.tolist()] + network_df.values.tolist()

    # Add network data to Tkinter grid
    for i in range(r):
        for j in range(c):
            e = Label(WINDOW, text=str(li[i][j]),width=CELL_WIDTH, fg='blue',
                        font=('Arial',FONTSIZE,'bold'))
            e.grid(row=(i + row), column=j)


# Recursively get sys info and update GUI
def update():
    process_df = get_process_info()
    network_df = get_network_info()
    make_gui(process_df, network_df)
    WINDOW.after(1000, update)

def main():
    # Setup GUI
    WINDOW.title(TITLE)
    #WINDOW.geometry(str(WIDTH)+"x"+str(HEIGHT))

    # Call update to get system info and fill in GUI
    update()

    # Launch GUI
    WINDOW.mainloop()

if __name__ == '__main__':
   main()
import psutil
import datetime
import pandas as pd
from tkinter import *

TITLE = "CPSC 4200 Final - System Monitor Tool"
WIDTH = 720 #px
HEIGHT = 1080 #px
MAX_PROCESSES = 5

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
            "CPU Percentage (%)":cpu_usage,
            "Memory Usages (MB)":memory_usage,
            "Memory Percentage (%)": memory_usage_percentage,
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

"""Builds TKinter Window GUI.

:param process_df: data frame with all process info
:param system_info: data frame with all system info
:returns: Tkinter GUI window
"""
def make_gui(window, process_df):
    r, c = process_df.shape
    
    process_df = get_process_info()
    for col in process_df.columns:
        print(col)

    li = [process_df.columns.values.tolist()] + process_df.values.tolist()
    print(li)

    for i in range(r):
        for j in range(c):
            e = Label(window, text=str(li[i][j]),width=20, fg='blue',
                        font=('Arial',16,'bold'))
            e.grid(row=i, column=j)


def main():
    # Run diagnostics on system and get a data frame with process info
    process_df = get_process_info()

    # Create GUI and use dataframe to fill in info
    window = Tk()
    window.title(TITLE)
    make_gui(window, process_df)

    # Launch GUI
    window.mainloop()

if __name__ == '__main__':
   main()
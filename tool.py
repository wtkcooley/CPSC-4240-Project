import psutil
import cpu_usage

print('The CPU usage is: ', cpu_usage.get_cpu_usage())

def main():
    import psutil # for the linux process data and cpu usage

    print(f"Process Name\tPID\tCPU Usage")
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            processName = proc.name()
            processID = proc.pid
            if cpu_usage.get_cpu_usage_by_pid(processID) > 0.0:
                print(f"{processName}\t{processID}\t{cpu_usage.get_cpu_usage_by_pid(processID)}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


if __name__ == '__main__':
   main()
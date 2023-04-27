import psutil

def get_cpu_usage(time=1):
    return psutil.cpu_percent(time)

def get_cpu_usage_by_pid(pid, time=1):
    p = psutil.Process(pid)
    return p.cpu_percent(time)
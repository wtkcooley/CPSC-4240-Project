import psutil

def get_cpu_usage(time=4):
    return psutil.cpu_percent(time)
import psutil

# get the current process
process = psutil.Process()

# get the memory info
mem_info = process.memory_info()

# print the memory usage
print(f"Memory used by current process: {mem_info.rss / (1024*1024):.2f} MB")


import psutil

def get_ram_info():
    try:
        mem = psutil.virtual_memory()
        total = round(mem.total / (1024 ** 3), 2)
        used = round(mem.used / (1024 ** 3), 2)
        available = round(mem.available / (1024 ** 3), 2)
        percent = mem.percent

        return (
            f"RAM Status:\n"
            f"Total: {total} GB\n"
            f"Used: {used} GB\n"
            f"Available: {available} GB\n"
            f"Usage: {percent}%"
        )
    except Exception as e:
        return f"Error fetching RAM info: {e}"

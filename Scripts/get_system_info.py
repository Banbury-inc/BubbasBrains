import psutil
import time
import pywifi
import subprocess
# Create a function to retrieve CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1, percpu=True)
def catch_cpu_usage():
    while True:
        cpu_percentages = get_cpu_usage()
        for i, cpu_percentage in enumerate(cpu_percentages):
            print(f"CPU Core {i}: {cpu_percentage}%")
        time.sleep(1)
# Function to retrieve memory usage information
def get_memory_usage():
    memory_info = psutil.virtual_memory()
    return {
        "total": memory_info.total,
        "available": memory_info.available,
        "used": memory_info.used,
        "free": memory_info.free,
        "percent": memory_info.percent,
    }
def catch_memory_usage():
    # Continuously stream memory usage information
    while True:
        memory_usage = get_memory_usage()
        print("Memory Usage:")
        print(f"Total: {memory_usage['total']} bytes")
        print(f"Available: {memory_usage['available']} bytes")
        print(f"Used: {memory_usage['used']} bytes")
        print(f"Free: {memory_usage['free']} bytes")
        print(f"Percent Used: {memory_usage['percent']}%")
    
        time.sleep(5)  # Adjust the interval as needed (e.g., 5 seconds)
    # Get the current WiFi signal strength
def get_device_name():
    try:
        # Run a command to retrieve the hostname (device name)
        completed_process = subprocess.run(['hostname'], stdout=subprocess.PIPE, text=True, check=True)

        # Extract the device name from the command output
        device_name = completed_process.stdout.strip()
        return device_name
    except subprocess.CalledProcessError as e:
        # Handle any command execution errors
        print(f"Error: {e}")
        return None
# Create a function to retrieve Wi-Fi signal strength
def main():
    name =get_device_name()
    print(name)
if __name__ == "__main__":
    main()
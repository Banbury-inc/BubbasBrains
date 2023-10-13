import time
import subprocess
class SystemInfo:

    @staticmethod
    def catch_cpu_usage():
        while True:
            cpu_percentages = SystemInfo.get_cpu_usage()
            for i, cpu_percentage in enumerate(cpu_percentages):
                print(f"CPU Core {i}: {cpu_percentage}%")
            time.sleep(1)

    @staticmethod
    def catch_memory_usage():
        while True:
            memory_usage = SystemInfo.get_memory_usage()
            print("Memory Usage:")
            print(f"Total: {memory_usage['total']} bytes")
            print(f"Available: {memory_usage['available']} bytes")
            print(f"Used: {memory_usage['used']} bytes")
            print(f"Free: {memory_usage['free']} bytes")
            print(f"Percent Used: {memory_usage['percent']}%")
            time.sleep(5)

    @staticmethod
    def get_device_name():
        try:
            completed_process = subprocess.run(['hostname'], stdout=subprocess.PIPE, text=True, check=True)
            device_name = completed_process.stdout.strip()
            return device_name
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            return None

def main():
    name = SystemInfo.get_device_name()
    print("Hello World")

if __name__ == "__main__":
    main()

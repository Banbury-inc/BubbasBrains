import sys
import argparse
from communication_agent.communication_agent import CommunicationAgent
from task_management_agent.task_management_agent import TaskManagementAgent
from vision_agent.camera import Camera
import psutil
import time
class HealthAgent:
    def __init__(self):
        pass
    def log_message(message):
        role = "Health Agent"
        message = "Health Agent Initialized"
        HealthAgent.log_message(role, message)
    def check_system():
        while True:
            cpu_usage = HealthAgent.get_cpu_usage()
            memory_usage = HealthAgent.get_memory_usage()
            disk_usage = HealthAgent.get_disk_usage()
            print(f"CPU Usage: {cpu_usage}%")
            print(f"Memory Usage: {memory_usage}%")
            print(f"Disk Usage: {disk_usage}%")
            print("="*50) 
            print(f"Running Programs: {TaskManagementAgent.running_programs}%")
            print("="*50)
            if cpu_usage > 90:
                print("CPU usage is too high, notifying task management agent") 
                message = "CPU Usage is too high, notifying task management agent"
                HealthAgent.log_message(message)
                TaskManagementAgent.manage_usage()
            if memory_usage > 90:
                print("Memory usage is too high, notifying task management agent") 
                message = "Memory usage is too high, notifying task management agent"
                HealthAgent.log_message(message) 
            if disk_usage > 90:
                print("Disk usage is too high, notifying task management agent") 
                message = "Disk usage is too high, notifying task management agent"
                HealthAgent.log_message(message)
 
            time.sleep(10)
    def get_cpu_usage():
        return psutil.cpu_percent(interval=1)
    def get_memory_usage():
        memory_info = psutil.virtual_memory()
        return memory_info.percent
    def get_disk_usage(path="/"):
        disk_info = psutil.disk_usage(path)
        return disk_info.percent

    def run(self):
        role = "Health Agent"
        message = "Health Agent Initialized"
        CommunicationAgent.log_message(role, message)
        print("Health Agent initialized")
        HealthAgent.check_system()



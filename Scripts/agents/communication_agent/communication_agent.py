import sys
import argparse
import logging
import os
import argparse
import time
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log
from adafruit_servokit import ServoKit
import serial.tools.list_ports

class CommunicationAgent:
    def __init__(self):
        self.setup_logger()
        self.role = "Communication Agent" 
#        self.output = videoOutput("webrtc://@:8554/output")
    def setup_logger(self):
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Build the full path to the log file within that directory
        log_filename = os.path.join(script_dir, 'workflow.log')
        # Check if the file already exists
        if os.path.exists(log_filename):
            os.remove(log_filename)
        # Configure logging settings
        logging.basicConfig(filename=log_filename,
                            level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')
    def run_server():
        from task_management_agent.task_management_agent import TaskManagementAgent
        TaskManagementAgent.start_program("backend server", "high", True) 
        os.chdir("Scripts/api/projectname")
        os.system("python3 manage.py runserver 192.168.1.51:4001")
        print("Backend server is running under 192.168.1.51:4001")
    def run(self):
        role = "Communication Agent"
        print("Communication Agent initialized")
        message = "Communication Agent has been initiated"
        self.log_message(role, message)
        CommunicationAgent.run_server() 
        message = "Backend server is running under 192.168.1.51:4001"
        self.log_message(role, message)
    def startFollowMode():
        NavigationAgent.followMode(run=True)
        print("Follow mode initiated")
    def stopFollowMode():
        NavigationAgent.followMode(run=False)


    @staticmethod
    def log_message(role, message):
        logging.info(' ' + role + '\n' + '\n' + 'Message: ' + message + '\n')

#    def videoStream(self, img):
        # render the image

#        output = videoOutput("webrtc://@:8554/output")
#        output.Render(img)

if __name__ == "__main__":
    agent = CommunicationAgent()
    agent.run()

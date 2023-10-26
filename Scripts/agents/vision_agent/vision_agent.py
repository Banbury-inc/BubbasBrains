import sys
import argparse
from communication_agent.communication_agent import CommunicationAgent
from vision_agent.camera import Camera
import logging




class VisionAgent:
    def __init__(self):
        pass
    def log_message(message):
        role = "Vision Agent"
        CommunicationAgent.log_message(role, message)
    def run(self):
        message = "Vision Agent Initialized"
        VisionAgent.log_message(message)
        print("Vision Agent initialized")
        try:
            Camera.run(self) 
            VisionAgent.log_message("Camera sucessfully streaming at 192.168.1.51:8554")
            print("Camera sucessfully streaming at 192.168.1.51:8554")
        except Exception as e:
            message = ("An error occured: " +  str(e))
            VisionAgent.log_message(message)


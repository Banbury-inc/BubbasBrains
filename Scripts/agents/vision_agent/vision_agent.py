

import sys
import argparse
from communication_agent.communication_agent import CommunicationAgent
from vision_agent.camera import Camera





class VisionAgent:
    def __init__(self):
        pass
    def log_message():
        role = "Task Management Agent"
        message = "Task Management Agent Initialized"
        CommunicationAgent.log_message(role, message)
 
    def run(self):
        role = "Vision Agent"
        message = "Vision Agent Initialized"
        CommunicationAgent.log_message(role, message)
        print("Vision Agent initialized")
        try:
            Camera.run(self) 
        except:
            print("camera not working")

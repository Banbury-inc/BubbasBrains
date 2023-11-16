import sys
import argparse
import time
from vision_agent.vision_agent import VisionAgent, Object
from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log
from adafruit_servokit import ServoKit
import serial.tools.list_ports
class NavigationAgent:
    def __init__(self):
        # Initialize instance variables in the __init__ method
        self.serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        self.baud_rate = 115200  # Adjust this to match your device's baud rate
        self.ser = serial.Serial(self.serial_port, self.baud_rate)
        print(f"Connected to {self.serial_port} at {self.baud_rate} baud")


    def run(self):
        # Use functions or classes from the imported module
        print("Navigation Agent Initialized")  

        while True:
            pass
    def moveMotors(self,leftWheel, rightWheel):
        # Commands go from L1 to L9 and R1 to R9
        user_input = leftWheel
        self.ser.write(user_input.encode('utf-8'))
        user_input = rightWheel
        self.ser.write(user_input.encode('utf-8'))
    def followMode(run):
        if run == True:
            if Object.Area < 50000:
                    print("Bubbabot needs to move closer") 
                    if Object.centerX < 533:
                        NavigationAgent.moveMotors("L6", "R7")
                    if Object.centerX >= 533:
                        if Object.centerX < 746:
                            NavigationAgent.moveMotors("L7", "R7")
                        if Object.centerX >= 746:
                            NavigationAgent.moveMotors("L7", "R6")
            if Object.Area > 50000:
                if Object.Area < 80000:
                    if Object.centerX < 533:
                        NavigationAgent.moveMotors("L2", "R6")
                    if Object.centerX >= 533:
                        if Object.centerX < 746:
                            NavigationAgent.moveMotors("L5", "R5")
                        if Object.centerX >= 746:
                            NavigationAgent.moveMotors("L6", "R2")
                if Object.Area > 80000:
                    if Object.centerX < 533:
                        NavigationAgent.moveMotors("L1", "R3")
                    if Object.centerX >= 533:
                        if Object.centerX < 746:
                            NavigationAgent.moveMotors("L1", "R1")
                        if Object.centerX >= 746:
                            NavigationAgent.moveMotors("L3", "R1")
        elif run == False:
            pass
                        

from communication_agent.communication_agent import CommunicationAgent
from adafruit_servokit import ServoKit
class MotorControlAgent:

    def __init__(self):
        pass
    def log_message(message):
        role = "Motor Control Agent"
        CommunicationAgent.log_message(role, message)
    def initialize_arm():
        MotorControlAgent.arm_position(90,90,45)
    def arm_position(elbowangle, wristangle, shoulderangle):
        kit = ServoKit(channels=16)
        kit.servo[2].angle = elbowangle
        kit.servo[3].angle = wristangle
        kit.servo[4].angle = shoulderangle
        message = "Arm has been moved to Elbow Angle: " + str(elbowangle) + " Wrist Angle: " + str(wristangle) + " Shoulder Angle: " + str(shoulderangle)
        MotorControlAgent.log_message(message)
        return elbowangle, wristangle, shoulderangle
    def run(self):
        message = "Motor Control Agent Initialized"
        MotorControlAgent.log_message(message)
        print("Motor Control Agent initialized")
        MotorControlAgent.initialize_arm()


from adafruit_servokit import ServoKit


# Initialize the ServoKit with the specified I2C bus and address
kit = ServoKit(channels=16)


elbowangle = 90
wristangle = 90
shoulderangle = 90


# Elbow
# 0 - 180
kit.servo[2].angle = elbowangle


# Wrist
# 0 - 180 
kit.servo[3].angle = wristangle


# Shoulder Movement
# 30 - 180 
kit.servo[5].angle = shoulderangle



while elbowangle < 180:
    elbowangle += 1
    kit.servo[2].angle = elbowangle


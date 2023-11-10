
from adafruit_servokit import ServoKit


# Initialize the ServoKit with the specified I2C bus and address
kit = ServoKit(channels=16)


elbowangle = 0
wristangle = 75
shoulderangle = 45
handangle = 140

# Elbow
# 0 - 180
kit.servo[2].angle = elbowangle


# Wrist
# 0 - 180 
kit.servo[3].angle = wristangle


# Shoulder Movement
# 30 - 180 
kit.servo[4].angle = shoulderangle

# Hand
# 0 - 110
kit.servo[1].angle = handangle



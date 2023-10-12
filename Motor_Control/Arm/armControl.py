
from adafruit_servokit import ServoKit


# Initialize the ServoKit with the specified I2C bus and address
kit = ServoKit(channels=16)





# Elbow
# 0 - 180
kit.servo[2].angle = 90


# Wrist
# 0 - 180 
kit.servo[3].angle = 90


# Shoulder Movement
# 30 - 180 
kit.servo[5].angle = 90
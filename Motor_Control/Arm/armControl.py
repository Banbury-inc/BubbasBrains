
from adafruit_servokit import ServoKit


# Initialize the ServoKit with the specified I2C bus and address
kit = ServoKit(channels=16)

kit.servo[2].angle = 90
kit.servo[1].angle = 90
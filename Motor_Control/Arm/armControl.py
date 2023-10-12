import time
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
def moveshoulderup():
    while shoulderangle < 30:
        shoulderangle += 1
        kit.servo[5].angle = shoulderangle
        time.sleep(0.01)
def moveshoulderdown():
    while shoulderangle > 180:
        shoulderangle -= 1
        kit.servo[5].angle = shoulderangle
        time.sleep(0.01)
def moveelbowup():
    while elbowangle < 30:
        elbowangle += 1
        kit.servo[2].angle = elbowangle
        time.sleep(0.01)
def moveelbowdown():
    while elbowangle > 180:
        elbowangle -= 1
        kit.servo[2].angle = elbowangle
        time.sleep(0.01)
def movewristup():
    while wristangle < 30:
        wristangle += 1
        kit.servo[3].angle = wristangle
        time.sleep(0.01)
def movewristdown():
    while wristangle > 180:
        wristangle -= 1
        kit.servo[3].angle = wristangle
        time.sleep(0.01)

def main():
    moveshoulderup()
    moveshoulderdown()
    moveelbowup()
    moveelbowdown()
    movewristup()
    movewristdown()


if __name__ == '__main__':
    main()
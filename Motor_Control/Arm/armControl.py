import time
from adafruit_servokit import ServoKit
def moveshoulderup(kit, shoulderangle):

    print("Moving shoulder up")
    while shoulderangle < 180:
        shoulderangle += .5
        kit.servo[4].angle = shoulderangle
        time.sleep(0.05)
def moveshoulderdown(kit, shoulderangle):
    print("Moving shoulder down")
    while shoulderangle > 30:
        shoulderangle -= .5
        kit.servo[4].angle = shoulderangle
        time.sleep(0.05)
def moveelbowup(kit, elbowangle):
    print("Moving elbow up")
    while elbowangle < 180:
        elbowangle += .5
        kit.servo[2].angle = elbowangle
        time.sleep(0.05)
def moveelbowdown(kit, elbowangle):
    print("Moving elbow down")
    while elbowangle > 30:
        elbowangle -= .5
        kit.servo[2].angle = elbowangle
        time.sleep(0.05)
def movewristup(kit, wristangle):
    print("Moving wrist up")
    while wristangle < 180:
        wristangle += .5
        kit.servo[3].angle = wristangle
        time.sleep(0.05)
def movewristdown(kit, wristangle):
    print("Moving wrist down")
    while wristangle > 30:
        wristangle -= .5
        kit.servo[3].angle = wristangle
        time.sleep(0.05)

def main():

    print("Starting command")
    # Initialize the ServoKit with the specified I2C bus and address
    kit = ServoKit(channels=16)
    elbowangle = 40
    wristangle = 40
    shoulderangle = 40
    kit.servo[4].angle = shoulderangle
    kit.servo[2].angle = elbowangle
    kit.servo[3].angle = wristangle
    while 1 == 1:
        moveshoulderup(kit, shoulderangle)
        moveshoulderdown(kit, shoulderangle)
        moveelbowup(kit, elbowangle)
        moveelbowdown(kit, elbowangle)
        movewristup(kit, wristangle)
        movewristdown(kit, wristangle)


if __name__ == '__main__':
    main()
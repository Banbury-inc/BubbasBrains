import time
from adafruit_servokit import ServoKit
def moveshoulderup(shoulderangle):
    while shoulderangle < 30:
        shoulderangle += 1
        kit.servo[5].angle = shoulderangle
        time.sleep(0.01)
def moveshoulderdown(shoulderangle):
    while shoulderangle > 180:
        shoulderangle -= 1
        kit.servo[5].angle = shoulderangle
        time.sleep(0.01)
def moveelbowup(elbowangle):
    while elbowangle < 30:
        elbowangle += 1
        kit.servo[2].angle = elbowangle
        time.sleep(0.01)
def moveelbowdown(elbowangle):
    while elbowangle > 180:
        elbowangle -= 1
        kit.servo[2].angle = elbowangle
        time.sleep(0.01)
def movewristup(wristangle):
    while wristangle < 30:
        wristangle += 1
        kit.servo[3].angle = wristangle
        time.sleep(0.01)
def movewristdown(wristangle):
    while wristangle > 180:
        wristangle -= 1
        kit.servo[3].angle = wristangle
        time.sleep(0.01)

def main():

    print("Starting command")
    # Initialize the ServoKit with the specified I2C bus and address
    kit = ServoKit(channels=16)


    elbowangle = 120
    wristangle = 120
    shoulderangle = 120

    # Elbow
    # 0 - 180
    kit.servo[2].angle = elbowangle

    # Wrist
    # 0 - 180 
    kit.servo[3].angle = wristangle

    # Shoulder Movement
    # 30 - 180 
    kit.servo[5].angle = shoulderangle

    moveshoulderup(shoulderangle)
    moveshoulderdown(shoulderangle)
    moveelbowup(elbowangle)
    moveelbowdown(elbowangle)
    movewristup(wristangle)
    movewristdown(wristangle)


if __name__ == '__main__':
    main()
import time
from adafruit_servokit import ServoKit
def moveshoulderup(kit, shoulderangle):
    while shoulderangle < 30:
        shoulderangle += 1
        kit.servo[5].angle = shoulderangle
        time.sleep(0.01)
def moveshoulderdown(kit, shoulderangle):
    while shoulderangle > 180:
        shoulderangle -= 1
        kit.servo[5].angle = shoulderangle
        time.sleep(0.01)
def moveelbowup(kit, elbowangle):
    while elbowangle < 30:
        elbowangle += 1
        kit.servo[2].angle = elbowangle
        time.sleep(0.01)
def moveelbowdown(kit, elbowangle):
    while elbowangle > 180:
        elbowangle -= 1
        kit.servo[2].angle = elbowangle
        time.sleep(0.01)
def movewristup(kit, wristangle):
    while wristangle < 30:
        wristangle += 1
        kit.servo[3].angle = wristangle
        time.sleep(0.01)
def movewristdown(kit, wristangle):
    while wristangle > 180:
        wristangle -= 1
        kit.servo[3].angle = wristangle
        time.sleep(0.01)

def main():

    print("Starting command")
    # Initialize the ServoKit with the specified I2C bus and address
    kit = ServoKit(channels=16)


    elbowangle = 80
    wristangle = 80
    shoulderangle = 80

    # Elbow
    # 0 - 180
    kit.servo[2].angle = elbowangle

    # Wrist
    # 0 - 180 
    kit.servo[3].angle = wristangle

    # Shoulder Movement
    # 30 - 180 
    kit.servo[5].angle = shoulderangle

    moveshoulderup(kit, shoulderangle)
    moveshoulderdown(kit, shoulderangle)
    moveelbowup(kit, elbowangle)
    moveelbowdown(kit, elbowangle)
    movewristup(kit, wristangle)
    movewristdown(kit, wristangle)


if __name__ == '__main__':
    main()
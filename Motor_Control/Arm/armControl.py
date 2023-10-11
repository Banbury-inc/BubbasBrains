import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
armStart = "startup"

def armInit():
    for i in range(16):

        kit.servo[i].angle = 90
        kit.servo[i].angle = 90
        time.sleep(1)



while True :
    if armStart ==  "startup":
        armStrart = armInit()

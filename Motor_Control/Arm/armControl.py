import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
armStart = "startup"

def armInit():
    kit.servo[2].angle = 90
    time.sleep(1)



while True :
    if armStart ==  "startup":
        armStrart = armInit()

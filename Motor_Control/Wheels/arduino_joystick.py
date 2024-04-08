
from machine import Pin, ADC
import time

# Pin definitions
CLK1 = 2   # encoder CLK input
CLK2 = 3   # encoder CLK input
DT1 = 4    # encoder DT input
DT2 = 5    # encoder DT input
SW1 = 16   # A2 proximity switch to set encoder home
SW2 = 17   # A3 proximity switch to set encoder home
M1A = 9    # turn motor output 1
M1B = 8    # turn motor output 2
M2A = 7    # turn motor output 1
M2B = 6    # turn motor output 2

# Constants
switchAngle = -50   # angle of switch (5 DEG. PAST 0 ANGLE)
angleAccuracy = 10  # accuracy needed for steering = accuracy / 360 * encoderCount / 2
setAngleLF = 900    # INTEGER THAT IS 10 TIMES TRUE ANGLE
counter1 = 10000    # for homing purposes set at 10000
setAngleRF = setAngleLF
counter2 = counter1
joyBuff = 20        # buffer to create dead space in joystick center
angle = setAngleLF
setAngleLR = setAngleLF
setAngleRR = setAngleLF
thr = 0             # throttle output

# Pin setup
clk1 = Pin(CLK1, Pin.IN)
dt1 = Pin(DT1, Pin.IN)
m1a = Pin(M1A, Pin.OUT)
m1b = Pin(M1B, Pin.OUT)

clk2 = Pin(CLK2, Pin.IN)
dt2 = Pin(DT2, Pin.IN)
m2a = Pin(M2A, Pin.OUT)
m2b = Pin(M2B, Pin.OUT)

sw1 = ADC(Pin(SW1))
sw2 = ADC(Pin(SW2))

# Interrupt setup
counter1 = 0
counter2 = 0

# Function definitions
def encoder1(pin):
    global counter1
    if dt1.value():
        counter1 += 1
    else:
        counter1 -= 1

def encoder2(pin):
    global counter2
    if dt2.value():
        counter2 += 1
    else:
        counter2 -= 1

# Attach interrupts
clk1.irq(trigger=Pin.IRQ_RISING, handler=encoder1)
clk2.irq(trigger=Pin.IRQ_RISING, handler=encoder2)

# Main loop
while True:
    # Set angle with read switch input
    if sw1.read() > 100:
        counter1 = switchAngle
    if sw2.read() > 100:
        counter2 = switchAngle

    # turn to requested angle MOTOR1
    if counter1 > setAngleLR + angleAccuracy:
        m1a.value(0)
        m1b.value(1)
    elif counter1 < setAngleLR - angleAccuracy:
        m1a.value(1)
        m1b.value(0)
    else:
        m1a.value(0)
        m1b.value(0)

    # turn to requested angle MOTOR2
    if counter2 > setAngleRR + angleAccuracy:
        m2a.value(0)
        m2b.value(1)
    elif counter2 < setAngleRR - angleAccuracy:
        m2a.value(1)
        m2b.value(0)
    else:
        m2a.value(0)
        m2b.value(0)

    # JOYSTICK
    thr = map(ADC(7).read(), 0, 1025, 255, -255)  # read turn input
    if thr > joyBuff:
        m2a.write(thr)
    else:
        m2a.write(0)

    angle = map(ADC(6).read(), 0, 1025, 1700, 100)  # read turn input
    if angle < 901:
        setAngleLF = angle
        if setAngleLF < 0:
            setAngleLF = 0    # over turn safety
        if setAngleLF > 1800:
            setAngleLF = 1800  # over turn safety
        if setAngleLF > 900 - joyBuff and setAngleLF < 900 + joyBuff:
            setAngleLF = 900
            setAngleRF = 900
        else:
            setAngleRF = abs(atan(((tan((setAngleLF / 10) * 3.14159 / 180) * 21.5) + 40) / 21.5) * 180 / 3.14159) * 10
    else:
        setAngleRF = angle
        if setAngleRF < 0:
            setAngleRF = 0    # over turn safety
        if setAngleRF > 1800:
            setAngleRF = 1800  # over turn safety
        if setAngleRF > 900 - joyBuff and setAngleRF < 900 + joyBuff:
            setAngleLF = 900
            setAngleRF = 900
        else:
            setAngleLF = map(abs(atan(((tan((setAngleRF / 10) * 3.14159 / 180) * 21.5) + 40) / 21.5) * 180 / 3.14159) * 10, 0, 1800, 1800, 0)
    setAngleLR = map(setAngleLF, 0, 1800, 1800, 0)
    setAngleRR = map(setAngleRF, 0, 1800, 1800, 0)
    print(setAngleLR, " / ", setAngleRR)

    time.sleep(0.1)

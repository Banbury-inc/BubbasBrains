import RPi.GPIO as GPIO
import time
import serial

# Motor control pins setup
LPWM = 3         # Left motor PWM pin
RPWM = 9         # Right motor PWM pin
Ldir = 11        # Left motor direction pin
Rdir = 12        # Right motor direction pin

# PWM and motor control variables
minPWM = 100     # Minimum PWM signal
maxPWM = 150     # Maximum PWM signal
rangeLow = 1     # Input range for drive always starts at 1
rangeStop = 5    # Stop position for inputs
rangeHigh = (rangeStop - rangeLow) + rangeStop # Calculate the input range for the drive
LRun = rangeStop # How fast the left motor runs (set this variable to the stop number to use)
RRun = rangeStop # How fast the right motor runs (1-4 reverse / 5 stop / 6-9 forward)
DTime = 0.5      # Amount of time required at stop before changing direction of a motor (seconds)

# Serial communication setup
ser = serial.Serial('/dev/ttyS0', 115200) # Adjust '/dev/ttyS0' to your serial port

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LPWM, GPIO.OUT)
GPIO.setup(RPWM, GPIO.OUT)
GPIO.setup(Ldir, GPIO.OUT)
GPIO.setup(Rdir, GPIO.OUT)

# PWM initialization
pwmL = GPIO.PWM(LPWM, 1000) # Set PWM frequency to 1000 Hz
pwmR = GPIO.PWM(RPWM, 1000)
pwmL.start(minPWM)
pwmR.start(minPWM)

# Function to map range
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Main loop
try:
    while True:
        if ser.in_waiting > 0:
            inChar = ser.read().decode('utf-8')
            inputNumber = ord(inChar) - 48

            # Left motor control logic
            if LRun < rangeStop + 1 and inputNumber > rangeStop:
                DTime = time.time() + DTime
            if LRun > rangeStop - 1 and inputNumber < rangeStop:
                DTime = time.time() + DTime
            LRun = inputNumber

            # Right motor control logic
            if RRun < rangeStop + 1 and inputNumber > rangeStop:
                DTime = time.time() + DTime
            if RRun > rangeStop - 1 and inputNumber < rangeStop:
                DTime = time.time() + DTime
            RRun = inputNumber

            # Motor control based on direction and speed
            if time.time() < DTime:
                pwmL.ChangeDutyCycle(minPWM)
                pwmR.ChangeDutyCycle(minPWM)
                GPIO.output(Ldir, GPIO.HIGH if LRun < rangeStop else GPIO.LOW)
                GPIO.output(Rdir, GPIO.HIGH if RRun < rangeStop else GPIO.LOW)
            else:
                if LRun == rangeStop:
                    pwmL.ChangeDutyCycle(minPWM)
                elif LRun < rangeStop:
                    pwmL.ChangeDutyCycle(map_value(LRun, rangeStop, rangeLow, minPWM, maxPWM))
                elif LRun > rangeStop:
                    pwmL.ChangeDutyCycle(map_value(LRun, rangeStop, rangeHigh, minPWM, maxPWM))

                if RRun == rangeStop:
                    pwmR.ChangeDutyCycle(minPWM)
                elif RRun < rangeStop:
                    pwmR.ChangeDutyCycle(map_value(RRun, rangeStop, rangeLow, minPWM, maxPWM))
                elif RRun > rangeStop:
                    pwmR.ChangeDutyCycle(map_value(RRun, rangeStop, rangeHigh, minPWM, maxPWM))

        time.sleep(0.01)

except KeyboardInterrupt:
    pwmL.stop()
    pwmR.stop()
    GPIO.cleanup()
    ser.close()

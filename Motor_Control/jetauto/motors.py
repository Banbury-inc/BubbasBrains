import smbus
import time

# Define I2C address of the motor controller
MOTOR_CONTROLLER_ADDRESS = 0x34

# Define registers for motor control

REG_MOTOR1_SPEED = 0x33
REG_MOTOR2_SPEED = 0x34
REG_MOTOR3_SPEED = 0x35
REG_MOTOR4_SPEED = 0x36

# Open I2C bus
bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1, change to 0 if using /dev/i2c-0

# Function to set motor speed
def set_motor_speed(motor, speed):
    bus.write_byte_data(MOTOR_CONTROLLER_ADDRESS, motor, speed)

# Function to stop all motors
def stop_motors():
        set_motor_speed(REG_MOTOR1_SPEED, 0)
        set_motor_speed(REG_MOTOR2_SPEED, 0)
        set_motor_speed(REG_MOTOR3_SPEED, 0)
        set_motor_speed(REG_MOTOR4_SPEED, 0)

# Move motors forward
def move_forward(speed):
    set_motor_speed(REG_MOTOR1_SPEED, -speed)
    set_motor_speed(REG_MOTOR2_SPEED, speed)
    set_motor_speed(REG_MOTOR3_SPEED, speed)
    set_motor_speed(REG_MOTOR4_SPEED, -speed)

# Move motors backward
def move_backward(speed):
    set_motor_speed(REG_MOTOR1_SPEED, speed)
    set_motor_speed(REG_MOTOR2_SPEED, -speed)
    set_motor_speed(REG_MOTOR3_SPEED, -speed)
    set_motor_speed(REG_MOTOR4_SPEED, speed)

# Move motors left (assuming differential drive)
def move_left(speed):
    set_motor_speed(REG_MOTOR1_SPEED, -speed)
    set_motor_speed(REG_MOTOR2_SPEED, -speed)
    set_motor_speed(REG_MOTOR3_SPEED, speed)
    set_motor_speed(REG_MOTOR4_SPEED, speed)

# Move motors right (assuming differential drive)
def move_right(speed):
    set_motor_speed(REG_MOTOR1_SPEED, speed)
    set_motor_speed(REG_MOTOR2_SPEED, speed)
    set_motor_speed(REG_MOTOR3_SPEED, -speed)
    set_motor_speed(REG_MOTOR4_SPEED, -speed)

# Main function to test motor movement
def main():


    while True:
        command = input("give a command -->")
        if command == "w":
            move_forward(100)
        if command == "s":
            move_backward(100)
        if command == "a":
            move_left(100)
        if command == "d":
            move_right(100)
        if command == "x":
           stop_motors() 
 
if __name__ == "__main__":
    main()

from adafruit_servokit import ServoKit
import serial.tools.list_ports
import time
# process frames until EOS or the user exits
serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
baud_rate = 115200  # Adjust this to match your device's baud rate
ser = serial.Serial(serial_port, baud_rate)
print(f"Connected to {serial_port} at {baud_rate} baud")




user_input = "L200n"
ser.write(user_input.encode('utf-8'))
user_input = "R200n"
ser.write(user_input.encode('utf-8'))
time.sleep(5)

user_input = "L300n"
ser.write(user_input.encode('utf-8'))
user_input = "R300n"
ser.write(user_input.encode('utf-8'))
time.sleep(5)

user_input = "L200n"
ser.write(user_input.encode('utf-8'))
user_input = "R200n"
ser.write(user_input.encode('utf-8'))
time.sleep(5)

user_input = "L300n"
ser.write(user_input.encode('utf-8'))
user_input = "R300n"
ser.write(user_input.encode('utf-8'))
time.sleep(3)

user_input = "L100n"
ser.write(user_input.encode('utf-8'))
user_input = "R100n"
ser.write(user_input.encode('utf-8'))
time.sleep(3)


user_input = "L200n"
ser.write(user_input.encode('utf-8'))
user_input = "R200n"
ser.write(user_input.encode('utf-8'))


time.sleep(5)
user_input = "L300n"
ser.write(user_input.encode('utf-8'))
user_input = "R300n"
ser.write(user_input.encode('utf-8'))

time.sleep(5)
user_input = "L300n"
ser.write(user_input.encode('utf-8'))
user_input = "R300n"
ser.write(user_input.encode('utf-8'))


user_input = "L200n"
ser.write(user_input.encode('utf-8'))
user_input = "R200n"
ser.write(user_input.encode('utf-8'))





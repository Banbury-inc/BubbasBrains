
import serial
import time

# Define the serial port and baud rate
port = "/dev/ttyUSB0"  # Update this with the correct port if needed
baud_rate = 9600

# Open the serial port
try:
    ser = serial.Serial(port, baud_rate)
    print(f"Serial port {port} opened successfully.")
except serial.SerialException as e:
    print(f"Failed to open serial port {port}: {e}")
    exit()

try:
    # Send a command to the Arduino
    ser.write(b"Hello Arduino!\n")
    print("Sent message to Arduino.")

    # Read response from Arduino
    response = ser.readline().decode().strip()
    print(f"Received message from Arduino: {response}")

    # Close the serial port
    ser.close()
    print("Serial port closed.")
except Exception as e:
    print(f"Error occurred: {e}")
    ser.close()  # Close serial port on error

# screen /dev/ttyUSB0 9600


import serial

# Define the serial port and baud rate
serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
baud_rate = 9600  # Adjust this to match your device's baud rate

ser = None  # Initialize ser outside of the try block

try:
    # Open the serial port
    ser = serial.Serial(serial_port, baud_rate)
    print(f"Connected to {serial_port} at {baud_rate} baud")

    while True:
        # Get user input and send it to the serial port
        user_input = input("Enter data to send (or press Enter to quit): ")
        if user_input:
            ser.write(user_input.encode('utf-8'))  # Encode the string as bytes

except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    # Close the serial port when done
    if ser is not None and ser.is_open:
        ser.close()
        print("Serial port closed")
import serial

# Define the serial port and baud rate
serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
baud_rate = 9600  # Adjust this to match your device's baud rate

try:
    # Open the serial port
    ser = serial.Serial(serial_port, baud_rate)
    print(f"Connected to {serial_port} at {baud_rate} baud")

    while True:
        # Read data from the serial port (change the byte size as needed)
        received_data = ser.read(1)  # Read one byte at a time
        if received_data:
            print(f"Received: {received_data.decode('utf-8')}")  # Assuming UTF-8 encoding

        # Get user input and send it to the serial port
        user_input = input("Enter data to send (or press Enter to quit): ")
        if user_input:
            ser.write(user_input.encode('utf-8'))  # Encode the string as bytes

except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    # Close the serial port when done
    if ser.is_open:
        ser.close()
        print("Serial port closed")

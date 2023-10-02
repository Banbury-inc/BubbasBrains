import serial
import time

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
        if not user_input:
            break

        # Clear the input buffer
        ser.flushInput()

        # Send the command
        ser.write(bytes(user_input, 'utf-8'))  # Encode the string as bytes

        # Wait for a response (adjust the delay as needed)
        time.sleep(1)

        # Read and display data coming back from Arduino (if available)
        if ser.in_waiting > 0:
            received_data = ser.read(ser.in_waiting).decode('utf-8')
            print(f"Received: {received_data}")

except serial.SerialException as e:
    print(f"Error: {e}")
finally:
    # Close the serial port when done
    if ser is not None and ser.is_open:
        ser.close()
        print("Serial port closed")

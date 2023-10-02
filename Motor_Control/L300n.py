import serial
import time


def L300n():
    # Define the serial port and baud rate
    serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
    baud_rate = 9600  # Adjust this to match your device's baud rate

    ser = None  # Initialize ser outside of the try block

    try:
        # Open the serial port
        ser = serial.Serial(serial_port, baud_rate)
        print(f"Connected to {serial_port} at {baud_rate} baud")

        def send_command(command):
            ser.write(command.encode('utf-8'))

        while True:
            # Get user input
            user_input = "L300n"

            if user_input == 'q':
                break

            # Send the user input as a command
            send_command(user_input)

    except serial.SerialException as e:
        print(f"Error: {e}")
    finally:
        # Close the serial port when done
        if ser is not None and ser.is_open:
            ser.close()
            print("Serial port closed")

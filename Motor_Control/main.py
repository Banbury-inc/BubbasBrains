import serial
import time
import L300n
import L400n
def main():

    serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
    baud_rate = 9600  # Adjust this to match your device's baud rate


    ser = None  # Initialize ser outside of the try block


    ser = serial.Serial(serial_port, baud_rate)

    print(f"Connected to {serial_port} at {baud_rate} baud")


    user_input = "L400n"


    ser.write(user_input.encode('utf-8'))


    print("Command sent to arduino")

    time.sleep(15)


    print("Timer finished, closing port")
    ser.close()


    print("Serial port closed")

if __name__ == "__main__":
    main()

import serial
import time
import L300n
import L400n
def main():
    while True:
        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port
        baud_rate = 9600  # Adjust this to match your device's baud rate


        ser = None  # Initialize ser outside of the try block


        ser = serial.Serial(serial_port, baud_rate)

        print(f"Connected to {serial_port} at {baud_rate} baud")
        count = 0
        while count < 3000:
            user_input = "L400n"
        

            ser.write(user_input.encode('utf-8'))

            count = count + 1
            
            print(count)


        print("Timer finished, closing port")
        ser.close()


        print("Serial port closed")

        serial_port = '/dev/ttyUSB0'  # Adjust this to match your serial port

        baud_rate = 9600  # Adjust this to match your device's baud rate


        ser = None  # Initialize ser outside of the try block


        ser = serial.Serial(serial_port, baud_rate)

        print(f"Connected to {serial_port} at {baud_rate} baud")
        count = 0
        while count < 3000:
            user_input = "L300n"
        

            ser.write(user_input.encode('utf-8'))

            count = count + 1
            
            print(count)


        print("Timer finished, closing port")
        ser.close()


        print("Serial port closed")

if __name__ == "__main__":
    main()

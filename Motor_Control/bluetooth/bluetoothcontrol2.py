
import bluetooth
import threading
import time

# Raspberry Pi's Bluetooth address (replace with your Raspberry Pi's address)
raspberry_pi_address = "E4:5F:01:FB:B2:F8"

# Function to send command continuously
def send_command(sock, stop_event):
    while not stop_event.is_set():
        try:
            sock.send(command)
        except bluetooth.btcommon.BluetoothError as e:
            print(f"Bluetooth Error: {e}")
            break
        time.sleep(1)  # Add a delay between sends if needed

# Create a Bluetooth socket and connect to the Raspberry Pi
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((raspberry_pi_address, 1))  # Use the correct RFCOMM channel

# Initial command
command = "Hello, Raspberry Pi!"

# Create a threading event to control the loop
stop_event = threading.Event()

# Start the sending thread
sending_thread = threading.Thread(target=send_command, args=(sock, stop_event))
sending_thread.start()

try:
    while True:
        # Get new command from user
        new_command = input("Enter new command (or 'exit' to quit): ")
        if new_command.lower() == 'exit':
            break
        command = new_command
except KeyboardInterrupt:
    pass
finally:
    # Signal the thread to stop and wait for it to finish
    stop_event.set()
    sending_thread.join()
    sock.close()

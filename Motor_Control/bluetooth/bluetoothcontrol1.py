
import bluetooth

# Raspberry Pi's Bluetooth address (replace with your Raspberry Pi's address)
raspberry_pi_address = "E4:5F:01:FB:B2:F8"

# Create a Bluetooth socket and connect to the Raspberry Pi
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((raspberry_pi_address, 1))  # Use the correct RFCOMM channel

# Send a command to the Raspberry Pi
command = "Hello, Raspberry Pi!"
while True:
    sock.send(command)




# Close the Bluetooth connection
#sock.close()

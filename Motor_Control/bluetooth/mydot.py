
import bluetooth

# Create a Bluetooth server socket
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
port = 1  # Bluetooth port (RFCOMM)

# Bind the server socket to a specific Bluetooth port
server_socket.bind(("", port))

# Listen for incoming connections (1 is the maximum number of queued connections)
server_socket.listen(1)

print("Waiting for a Bluetooth connection...")
client_socket, client_info = server_socket.accept()
print(f"Accepted connection from {client_info}")

while True:
    try:
        # Receive data from the client
        data = client_socket.recv(1024).decode("utf-8")

        if not data:
            break

        # Process the received command (replace with your own logic)
        if data == "led_on":
            # Execute a command when "led_on" is received
            print("Turning LED on")
            # Add your code to control hardware here

        elif data == "led_off":
            # Execute a command when "led_off" is received
            print("Turning LED off")
            # Add your code to control hardware here

    except Exception as e:
        print(f"Error: {e}")
        break

# Close the client and server sockets
client_socket.close()
server_socket.close()

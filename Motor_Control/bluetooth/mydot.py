
import bluetooth

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(("", port))
server_sock.listen(1)

print("Waiting for a connection...")
client_sock, address = server_sock.accept()
print("Accepted connection from ", address)

try:
    while True:
        data = client_sock.recv(1024)
        print("Received [%s]" % data)
        # Here you can add code to process the received data and perform actions

except IOError:
    pass

print("Disconnected.")
client_sock.close()
server_sock.close()


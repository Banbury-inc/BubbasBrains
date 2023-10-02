import serial.tools.list_ports
#import drivers
import time

ports = serial.tools.list_ports.comports()
serialInst1 = serial.Serial()

portList = []
packetB = ""

for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))

val = input("Select Port: ttyUBS")
portVal = "/dev/ttyUSB" + str(val)

serialInst1.baudrate = 9600
serialInst1.port = portVal  
serialInst1.open()
# end setup COM port to use


# Listen to COM port (data from arduino)
while True:
    if serialInst1.in_waiting:
        packet = serialInst1.readline()
        packetB = packet.decode('utf-8').rstrip('\n')
        print(packetB)

    val = input("data to send")
    seriaInst1.write(bytes(val, 'utf-8'))


import time
from adafruit_servokit import ServoKit

# Connect to the I2C bus and address
i2c_bus_number = 1  # Adjust this to the correct I2C bus number
device_address = 0x71  # Adjust this to the correct device address

# Initialize the ServoKit with the specified I2C bus and address
kit = ServoKit(channels=16, address=device_address, i2c=i2c_bus_number)

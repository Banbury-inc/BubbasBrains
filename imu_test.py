import board
import busio

print("Hello World!")

i2c = busio.I2C(board.SCL, board.SDA)
print(i2c.scan())
print("I2C initialized!")
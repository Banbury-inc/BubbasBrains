import time
import smbus2
import board
import busio # Replace with the actual IMU library
from adafruit_mpu6050 import MPU6050

# Initialize the I2C bus
bus = smbus2.SMBus(1)  # Replace with the correct bus number if needed

# Create an instance of your IMU class
# imu = IMU()  # Replace with the actual instantiation code for your IMU
i2c = busio.I2C(board.SCL, board.SDA)

imu = MPU6050(i2c)
# Main loop to read data from the IMU


try:
    while True:
        # Read sensor data from the IMU
        accel_data = imu.acceleration
#        gyro_data = imu.read_gyroscope()
#        mag_data = imu.read_magnetometer()
#        orientation = imu.read_orientation()

        # Print the data to the console
        print(f"Acceleration (m/s^2): {accel_data}")
#        print(f"Gyroscope (rad/s): {gyro_data}")
#        print(f"Magnetometer (uT): {mag_data}")
#        print(f"Orientation (degrees): {orientation}")

        # Add a delay to control the data sampling rate
        time.sleep(1)  # Adjust the delay as needed

except KeyboardInterrupt:
    pass

# Cleanup and close the IMU connection
#imu.close()

import smbus2
import time


# DO NOT TOUCH - WORKING


# Define the I2C bus number and IMU address
bus_number = 7  # This may vary depending on your hardware
imu_address = 0x6B  # This is the default I2C address for ISM330DHCX

# Create an I2C bus object
bus = smbus2.SMBus(bus_number)

# Initialize the IMU
def init_imu():
    try:
        # Enable the accelerometer and gyroscope
        bus.write_byte_data(imu_address, 0x10, 0b00111000)  # CTRL1_XL register
        bus.write_byte_data(imu_address, 0x11, 0b00111000)  # CTRL2_G register
        return True
    except Exception as e:
        print(f"Error initializing the IMU: {e}")
        return False

# Read accelerometer and gyroscope data
def read_imu_data():
    try:
        # Read accelerometer data (X, Y, Z)
        accel_data = [bus.read_byte_data(imu_address, 0x28 + i) for i in range(6)]
        accel_x = (accel_data[1] << 8) | accel_data[0]
        accel_y = (accel_data[3] << 8) | accel_data[2]
        accel_z = (accel_data[5] << 8) | accel_data[4]

        # Read gyroscope data (X, Y, Z)
        gyro_data = [bus.read_byte_data(imu_address, 0x22 + i) for i in range(6)]
        gyro_x = (gyro_data[1] << 8) | gyro_data[0]
        gyro_y = (gyro_data[3] << 8) | gyro_data[2]
        gyro_z = (gyro_data[5] << 8) | gyro_data[4]

        return (accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z)
    except Exception as e:
        print(f"Error reading IMU data: {e}")
        return None

if __name__ == "__main__":
    if init_imu():
        print("IMU initialized successfully.")

        while True:
            imu_data = read_imu_data()
            if imu_data:
                accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = imu_data
                print(f"Acceleration (raw): X={accel_x}, Y={accel_y}, Z={accel_z}")
                print(f"Gyroscope (raw): X={gyro_x}, Y={gyro_y}, Z={gyro_z}")
                print()

            time.sleep(1)

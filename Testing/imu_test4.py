import smbus2
import time
# mg = milligravity 
# mdps = millidegrees per second


# Define the I2C bus number and IMU address
bus_number = 7  # This may vary depending on your hardware
imu_address = 0x6B  # This is the default I2C address for ISM330DHCX

# Sensor sensitivity and scale settings (example values)
accel_sensitivity = 0.061  # Sensitivity in mg/digit (specific to your sensor)
gyro_sensitivity = 8.75  # Sensitivity in mdps/digit (specific to your sensor)

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

# Convert raw data to meaningful units
def convert_to_meaningful_units(raw_data, sensitivity):
    return raw_data * sensitivity

if __name__ == "__main__":
    if init_imu():
        print("IMU initialized successfully.")

        while True:
            imu_data = read_imu_data()
            if imu_data:
                accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z = imu_data
                
                # Convert to meaningful units
                accel_x_mg = convert_to_meaningful_units(accel_x, accel_sensitivity)
                accel_y_mg = convert_to_meaningful_units(accel_y, accel_sensitivity)
                accel_z_mg = convert_to_meaningful_units(accel_z, accel_sensitivity)
                
                gyro_x_mdps = convert_to_meaningful_units(gyro_x, gyro_sensitivity)
                gyro_y_mdps = convert_to_meaningful_units(gyro_y, gyro_sensitivity)
                gyro_z_mdps = convert_to_meaningful_units(gyro_z, gyro_sensitivity)

                print(f"Acceleration (mg): X={accel_x_mg:.2f}, Y={accel_y_mg:.2f}, Z={accel_z_mg:.2f}")
                print(f"Gyroscope (mdps): X={gyro_x_mdps:.2f}, Y={gyro_y_mdps:.2f}, Z={gyro_z_mdps:.2f}")
                print()

            time.sleep(1)

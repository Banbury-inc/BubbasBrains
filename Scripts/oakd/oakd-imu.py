
import depthai as dai
import time

# Create a pipeline
pipeline = dai.Pipeline()

# Define a source - IMU
imu = pipeline.createIMU()

# Enable acceleration and gyroscope data
imu.enableIMUSensor([dai.IMUSensor.ACCELEROMETER_RAW, dai.IMUSensor.GYROSCOPE_RAW], 100)

# Allow IMU to send data to the host by setting the frequency
imu.setBatchReportThreshold(1)
imu.setMaxBatchReports(10)

# Link IMU to XLinkOut to send IMU data to the host
xoutImu = pipeline.createXLinkOut()
xoutImu.setStreamName("imu")

imu.out.link(xoutImu.input)

# Connect to device and start the pipeline
with dai.Device(pipeline) as device:

    # Output queue for IMU data
    imuQueue = device.getOutputQueue(name="imu", maxSize=50, blocking=False)

    while True:
        imuData = imuQueue.get()  # Blocking call, will wait until a new data has arrived
        
        # Access and print accelerometer data
        
        print(imuData)
        # Limit the output to 10 samples per second
        time.sleep(0.1)


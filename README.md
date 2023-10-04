# Bubbas Brains

"Bubba's Brains" is an advanced AI system powered by an Nvidia Jetson Nano. This versatile system offers a wide range of capabilities, including Object Detection, Live 3D Reconstruction, precise GPS mapping with inch-level accuracy, an extensive API library, and a Software Development Kit (SDK) for future enhancements. Designed for deployment on various robots, its primary focus in its prototype phase is agricultural tasks like planting, seeding, and harvesting, with the potential to expand its functionality to accomplish diverse tasks in the future.

## Facilities Management

"Bubba's Brains" with its advanced AI capabilities and the Nvidia Jetson Nano can be highly applicable to facilities management in several ways:

1. Asset Tracking - Purchase/Sale, Leasing, Tax Management, Expense Management
2. Navigation and Mapping - Space Management
3. Maintenance and Repairs - Moves/Additions/Changes, Project Planning, Condition Assesments
4. Energy Efficiency - Airlfow, Solar Home Design, Heat Distribution
6. Security and Surveilance - Object Detection, Alerts/Alarms
8. Task Automation - Cleaning/Maintenance Schedules, Routine Inspections
9. Safety and Compliance - Fire Alarms, Smoke Detectors, Fire Extinguisher

## Basic Architecture

* Object Detection - Yolov8
* 3D Data Processing - Open3D

![alt text](https://github.com/Banbury-inc/BubbasBrains/blob/main/assets/Architecture.png)


## Pipeline

1. Take video with NVIDIA Jetson
2. Convert MOV file to JPEG file
3. Use WebODM command line argument to convert JPEG files into a pointcloud file
4. View the pointcloud file through custom web app


## Hardware

1. NVIDIA Orin NX Developer Kit
2. SparkFun 9DoF IMU Breakout - ISM330DHCX
3. UC-261 5MP Arducam Camera
 
## Software


* Ubuntu 20.04.6
* Python 3.8.10

## Run Server

gunicorn -c gunicorn_config.py app:app


## Motor Speeds



![alt text](https://github.com/Banbury-inc/BubbasBrains/blob/main/assets/Motor_Speeds.png)
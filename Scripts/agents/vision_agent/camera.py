

import sys
import argparse
import cv2




class Camera:
    def __init__(self):
        pass
 
    def run(self):

        from task_management_agent.task_management_agent import TaskManagementAgent
        TaskManagementAgent.start_program("camera", "high", True) 
        # Open the webcam (0 is usually the default camera)
        cap = cv2.VideoCapture(0)
        # Check if the camera opened successfully
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return
        # Loop to continuously get frames from the camera
        while True:
            # Read a frame from the webcam
            ret, frame = cap.read()
            # If the frame was successfully grabbed, display it
            if ret:
                cv2.imshow('Webcam Stream', frame)
                # Break the loop if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print("Error: Could not read frame.")
                break
        # Release the camera and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()


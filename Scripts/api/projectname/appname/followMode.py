import torch
import numpy as np
import cv2
from time import time
from ultralytics import YOLO

from supervision.draw.color import ColorPalette
from supervision.tools.detections import Detections, BoxAnnotator


class ObjectDetection:

    def __init__(self, capture_index):
       
        self.capture_index = capture_index
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)
        
        self.model = self.load_model()
        
        self.CLASS_NAMES_DICT = self.model.model.names
    
        self.box_annotator = BoxAnnotator(color=ColorPalette(), thickness=3, text_thickness=3, text_scale=1.5)
    

    def load_model(self):
       
        model = YOLO("yolov8n.pt")  # load a pretrained YOLOv8n model
        model.fuse()
    
        return model


    def predict(self, frame):
       
        results = self.model(frame, verbose= False)
        
        return results
    

    def plot_bboxes(self, results, frame):
        
        xyxys = []
        confidences = []
        class_ids = []
        
        # Extract detections for person class
        for result in results[0]:
            class_id = result.boxes.cls.cpu().numpy().astype(int)
            
            if class_id == 0:
                
                xyxys.append(result.boxes.xyxy.cpu().numpy())
                confidences.append(result.boxes.conf.cpu().numpy())
                class_ids.append(result.boxes.cls.cpu().numpy().astype(int))
        top_left_height = 0
        top_left_width = 0
        bottom_right_height = 0
        bottom_right_width = 0 

        if len(xyxys) > 0 and xyxys[0].shape ==(1,4):
            numbers = xyxys[0][0]
            top_left_width, top_left_height, bottom_right_width, bottom_right_height = numbers

        # The array prints out top left corner, bottom right corner, 
            print("Top Left Width:", top_left_width)
            print("Top Left Height:", top_left_height)
            print("Bottom Right Width:", bottom_right_width)
            print("Bottom Right Height:", bottom_right_height)
            print("")
#        print(xyxys) 
        # The dimensions of the frame is 1280 x 720, so we need to figure out a way to write an if statement 
        # saying that if most of the frame is above or below the dead center, move the motor upwards or downwards.
        # Dead center horizontally is 360. We can take the average of the two points and it will either be 
        # above or below the horizontal average of 640. If that is the case, we can call a function to move
        # the motor.         

        horizontal_average = (bottom_right_height + top_left_height) / 2
        print("Horizontal Average", horizontal_average)
        if horizontal_average > 360:
            print("The camera is too high")
        if horizontal_average == 0:
            print("There is no horizontal average")
        if horizontal_average < 240:
            print("The camera is too low")
        if horizontal_average > 240:
            if horizontal_average < 480:
                print("The camera is juuuuuuuuust right")
        if horizontal_average > 480:
            print("The camera is too high")
        





        # Setup detections for visualization
        detections = Detections(
                    xyxy=results[0].boxes.xyxy.cpu().numpy(),
                    confidence=results[0].boxes.conf.cpu().numpy(),
                    class_id=results[0].boxes.cls.cpu().numpy().astype(int),
                    )
        
    
        # Format custom labels
        self.labels = [f"{self.CLASS_NAMES_DICT[class_id]} {confidence:0.2f}"
        for _, confidence, class_id, tracker_id
        in detections]

        for prediction in self.labels:
            class_label, confidence = prediction.split()[:2]
            if class_label == 'person' and float(confidence) > 0.8:
                print("A person is detected!")






        # Annotate and display frame
        frame = self.box_annotator.annotate(frame=frame, detections=detections, labels=self.labels)
        
        return frame

   
    
    def __call__(self):

        cap = cv2.VideoCapture(self.capture_index)
        assert cap.isOpened()
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
      
        while True:
          
            start_time = time()
            
            ret, frame = cap.read()
            assert ret
            
            results = self.predict(frame)
            frame = self.plot_bboxes(results, frame)
            
            end_time = time()
            fps = 1/np.round(end_time - start_time, 2)
             
            cv2.putText(frame, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
            
            cv2.imshow('YOLOv8 Detection', frame)
 
            if cv2.waitKey(5) & 0xFF == 27:
                
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        
    
detector = ObjectDetection(capture_index=0)
detector()
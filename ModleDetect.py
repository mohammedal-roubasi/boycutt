from typing import Any
from ultralytics import YOLO
import cv2 
import numpy as np 
import torch 
from time import time


class objectDetect:

    def __init__(self,model_name) :
        self.model=self.load_model(model_name)
        self.device ='cuda' if torch.cuda.is_available() else 'cpu'
        print('using divec ',self.device)

    def load_model(self,model_name):
        model= YOLO(model_name)  
        model.fuse() #تحسين السرعه 
        return model
    
    def predict(self,frame):
        results=self.model(frame)
        return results
    
    
    '''  
    fouction accept path of real image ond save detected image and return path of detected image
    
    '''
    def imageDetect(self, image_path: str) -> tuple:
        im2 = cv2.imread(image_path)
        results = self.model.predict(source=im2, save=True)  # Save predictions as labels
        name_image = results[0].path
        path = results[0].save_dir
        full_path_detect_image = f"{path}/{name_image}"
        accuracy = results[0].boxes.conf[0].item() if results[0].boxes is not None and len(results[0].boxes) > 0 else 0.0

        return name_image, path, accuracy  # Return accuracy as well
        '''
    founction accept frame and make detect of frame and return detected frame
    
    '''

    def web_cam (self,frame) :
         results = self.model(frame)
            
                    # Visualize the results on the frame
         annotated_frame = results[0].plot()
         return annotated_frame
    '''
    founction accept path video and make detect of video 
    
    '''
    def video_naw (self,video_path) :
         cap = cv2.VideoCapture(video_path)  # Capture video from default camera
         

         while cap.isOpened():
                success, frame = cap.read()

                if success:
                    # Run YOLOv8 inference on the frame
                    results = self.model(frame)
            
                    # Visualize the results on the frame
                    annotated_frame = results[0].plot()
            
                    # Display the annotated frame
                    cv2.imshow("YOLOv8 Inference", annotated_frame)
            
                    # Break the loop if 'q' is pressed
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                else:
                    break    
         cap.release()
         cv2.destroyAllWindows()       
           

#model_name = 'best.pt'  # Replace with your YOLO model file
#detector = objectDetect(model_name)
#detector.web_cam()  # Run the object detection loop
0#detector.video_naw('5.mp4')  
#detector.image('cola.jpg')      

# Load a model
#model = YOLO('yolov8m-seg.pt')  # load an official model
#model = YOLO('path/to/best.pt')  # load a custom model
#results = model.predict(source="0",show=True)
# Predict with the model
#results = model('bus.jpg',save=True)  # predict on an image\

print()
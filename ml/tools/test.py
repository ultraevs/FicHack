import torch
import cv2
from ultralytics import YOLO
import os

class YOLO_:
    def __init__(self, model_path="ground.pt"):
        self.model = YOLO(model_path)

    def scan(self, image):
        results = self.model(image, save=True, conf=0.1)
        #return results
    
    #def 

YOLO_ = YOLO_()

image_folder = './origin-ground'
cnt = 0
for filename in os.listdir(image_folder):
    if filename.lower().endswith('.jpg'):
        cnt += 1
        image_path = os.path.join(image_folder, filename)
        image = cv2.imread(image_path)
        results = YOLO_.scan(image)
        os.rename('runs/detect/predict/image0.jpg', f'runs/detect/predict/image_{cnt}.jpg')
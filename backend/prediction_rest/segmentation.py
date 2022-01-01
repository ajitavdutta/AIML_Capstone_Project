from django.conf import settings
from yolov5 import detect
import numpy as np
import pydicom
import cv2
import os


class Segmentation:
    def __init__(self, filename):
        self.pixel_array = None
        self.dcm_filename = filename
        self.filename = os.path.basename(filename).split('.')[0]
        self.png_filename = os.path.join(settings.SEGMENT_RUN_PATH, self.filename + '.png')
        self.preprocess_input()

    def preprocess_input(self):
        print('In segmentation.preprocess_input')
        self.pixel_array = []
        image = pydicom.dcmread(self.dcm_filename).pixel_array
        image = cv2.resize(image, (settings.SEGMENTATION_IMG_SIZE,
                                   settings.SEGMENTATION_IMG_SIZE),
                           interpolation=cv2.INTER_NEAREST)
        image = np.expand_dims(image, -1)
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        cv2.imwrite(self.png_filename, image)

    def predict(self):
        detect.run(source=self.png_filename,
                   weights=settings.WEIGHTS_PATH,
                   imgsz=(settings.SEGMENTATION_IMG_SIZE, settings.SEGMENTATION_IMG_SIZE),
                   conf_thres=0.38, max_det=4,
                   iou_thres=0.45,
                   line_thickness=1,
                   exist_ok=True,
                   save_txt=True,
                   save_conf=True,
                   project=settings.PREDICTION_PATH)

        return f"exp{os.path.sep}{self.filename}.png"

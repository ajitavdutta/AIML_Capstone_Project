from tensorflow.keras.applications import densenet
from django.conf import settings
from PIL import Image
import numpy as np
import pydicom
import cv2
import os


class Classification:
    def __init__(self, model, filename):
        self.pixel_array = None
        self.model = model
        self.filename = filename
        self.preprocess_input()

    def preprocess_input(self):
        self.pixel_array = []
        image = pydicom.dcmread(os.path.join(settings.MEDIA_ROOT, self.filename)).pixel_array
        image = cv2.resize(image, (settings.CLASSIFICATION_IMG_SIZE,
                                   settings.CLASSIFICATION_IMG_SIZE),
                           interpolation=cv2.INTER_NEAREST)
        image = Image.fromarray(image)
        image = image.convert('RGB')
        image = np.array(image, dtype=np.float32)
        image = densenet.preprocess_input(np.array(image, dtype=np.float32))
        self.pixel_array.append(image)
        self.pixel_array = np.array(self.pixel_array)

    def predict(self):
        predict = settings.CLASSIFICATION_MODEL.predict(self.pixel_array)
        print(predict)
        predict = np.round(predict).astype(int)
        print(predict)
        return predict[0][0]
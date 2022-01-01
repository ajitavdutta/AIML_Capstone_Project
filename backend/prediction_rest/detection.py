from skimage.transform import resize
from django.conf import settings
from skimage import measure
import numpy as np
import pydicom
import cv2
import os


class Detection:
    def __init__(self, model, filename):
        self.pixel_array = None
        self.model = model
        self.filename = filename
        self.prediction = []
        self.preprocess_input()

    def preprocess_input(self):
        print('In detection.Detection.preprocess_input')
        img = pydicom.dcmread(self.filename).pixel_array
        img = resize(img, (settings.DETECTION_IMG_SIZE,
                           settings.DETECTION_IMG_SIZE),
                     mode='reflect')
        img = np.expand_dims(img, -1)
        self.pixel_array = [img]
        self.pixel_array = np.array(self.pixel_array)

    def predict(self):
        print('In detection.Detection.detect')
        self.prediction = []
        preds = settings.DETECTION_MODEL.predict(self.pixel_array)

        for pred in preds:
            comp = pred[:, :, 0] > 0.5
            comp = measure.label(comp)

            for region in measure.regionprops(comp):
                # retrieve x, y, height and width
                y, x, y2, x2 = region.bbox
                h = y2 - y
                w = x2 - x
                self.prediction.append([x, y, w, h])
        print(self.prediction)

    def generate_image(self, image_name):
        print('In detection.Detection.generate_image(', image_name, ')')

        if not self.prediction:
            return False

        img = pydicom.dcmread(self.filename).pixel_array
        img = cv2.resize(img, (256, 256), interpolation=cv2.INTER_NEAREST)
        img = np.expand_dims(img, -1)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        for pred in self.prediction:
            x = pred[0]
            y = pred[1]
            w = pred[2]
            h = pred[3]
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, 'Pneumonia', (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 0.75, (0, 0, 255), 1)

        return cv2.imwrite(os.path.join(settings.PREDICTION_PATH, image_name), img)

from tensorflow.keras.applications import densenet
from django.conf import settings
from skimage.transform import resize
from skimage import measure
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

    def classify(self):
        predict = settings.CLASSIFICATION_MODEL.predict(self.pixel_array)
        print(predict)
        predict = np.round(predict).astype(int)
        print(predict)
        return predict[0][0]


class Detection:
    def __init__(self, model, filename):
        self.pixel_array = None
        self.model = model
        self.filename = filename
        self.prediction = []
        self.preprocess_input()

    def preprocess_input(self):
        print('In custom_models.Detection.preprocess_input')
        img = pydicom.dcmread(self.filename).pixel_array
        img = resize(img, (settings.DETECTION_IMG_SIZE,
                           settings.DETECTION_IMG_SIZE),
                     mode='reflect')
        img = np.expand_dims(img, -1)
        self.pixel_array = [img]
        self.pixel_array = np.array(self.pixel_array)

    def detect(self):
        print('In custom_models.Detection.detect')
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
        print('In custom_models.Detection.generate_image(', image_name, ')')

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

        PRED_ROOT = os.path.join(settings.MEDIA_ROOT, 'prediction')
        if not os.path.exists(PRED_ROOT):
            os.makedirs(PRED_ROOT, exist_ok=True)
        return cv2.imwrite(os.path.join(PRED_ROOT, image_name), img)

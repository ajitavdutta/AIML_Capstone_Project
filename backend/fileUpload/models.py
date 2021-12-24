from django.conf import settings
from django.db import models
from PIL import Image
import numpy as np
import pydicom
import uuid
import cv2
import os


def generate_filename(instance, filename):
    ext = filename.split(".")[-1]
    filename = "{}.{}".format(uuid.uuid4(), ext)
    return os.path.join('dicom', filename)


# Create your models here.
class UploadFile(models.Model):
    file = models.FileField(upload_to=generate_filename)

    def save(self, *args, **kwargs):
        super(UploadFile, self).save(*args, **kwargs)
        image_path = os.path.join(settings.MEDIA_ROOT, self.file.name)
        image_name = os.path.basename(image_path).replace('.dcm', '.png')
        image = pydicom.dcmread(image_path).pixel_array
        image = Image.fromarray(image)
        image = np.array(image, dtype=np.float32)
        image = (image - image.min()) / (image.max() - image.min()) * 255.0
        image = image.astype(np.uint8)
        image_path = os.path.join(settings.MEDIA_ROOT, 'png', image_name)
        cv2.imwrite(image_path, image)

    def __str__(self):
        return self.file.name

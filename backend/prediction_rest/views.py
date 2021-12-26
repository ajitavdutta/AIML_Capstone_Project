from tensorflow.keras.applications.densenet import preprocess_input as DensePreprocess
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from fileUpload.models import UploadFile
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from PIL import Image
import numpy as np
import pydicom
import cv2
import os


# Create your views here.
class PredictView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def __predict_data__(self, filename):
        print('In PredictView.__predict_data__')

        x = []

        # model_path = os.path.join(settings.BASE_DIR, 'library', 'model', 'DenseNet201.h5')
        # model = keras.models.load_model(model_path)

        image = pydicom.dcmread(os.path.join(settings.MEDIA_ROOT, filename)).pixel_array
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_NEAREST)
        image = Image.fromarray(image)
        image = image.convert('RGB')
        image = np.array(image, dtype=np.float32)
        image = DensePreprocess(np.array(image, dtype=np.float32))
        x.append(image)
        x = np.array(x)

        predict = settings.CLASSIFICATION_MODEL.predict(x)
        print(predict)
        predict = np.round(predict).astype(int)
        print(predict)
        return predict[0][0]

    def get(self, request, *args, **kwargs):
        print('In PredictView.get')
        params = request.GET.get('id')
        if params is None:
            print('Param id not found.')
            return Response("Mandatory Parameter 'id' not provided in the request.", status=status.HTTP_400_BAD_REQUEST)

        upload_file = UploadFile.objects.filter(id=params)
        # print(uploadFile.values_list('file').get(id=params)[0])
        predict = self.__predict_data__(upload_file.values_list('file').get(id=params)[0])
        response = {}
        if predict == 1:
            response['predict'] = 'Pneumonia'
        else:
            response['predict'] = 'Non-Pneumonia'

        return Response(response)

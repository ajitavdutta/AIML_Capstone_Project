from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .classification import Classification
from .segmentation import Segmentation
from rest_framework.reverse import reverse
from fileUpload.models import UploadFile
from rest_framework.views import APIView
from rest_framework import status
from urllib.parse import urlparse
from .detection import Detection
from django.conf import settings
import os


# Create your views here.
class PredictView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def __predict_data__(self, filename):
        print('In PredictView.__predict_data__')
        label = 'Non-Pneumonia'
        image = None

        clf = Classification(model=settings.CLASSIFICATION_MODEL,
                             filename=os.path.join(settings.MEDIA_ROOT, filename))
        result = clf.predict()
        if result == 1:
            label = 'Pneumonia'

        # detect = Detection(model=settings.DETECTION_MODEL,
        #                    filename=os.path.join(settings.MEDIA_ROOT, filename))
        # detect.predict()
        # if detect.generate_image(os.path.basename(filename).replace('.dcm', '.png')):
        #     image = os.path.basename(filename).replace('.dcm', '.png')

        segment = Segmentation(os.path.join(settings.MEDIA_ROOT, filename))
        image = segment.predict()

        return label, image

    def get(self, request, *args, **kwargs):
        print('In PredictView.get')
        params = request.GET.get('id')
        if params is None:
            print('Param id not found.')
            return Response("Mandatory Parameter 'id' not provided in the request.", status=status.HTTP_400_BAD_REQUEST)

        upload_file = UploadFile.objects.filter(id=params)
        print(upload_file.values_list('file').get(id=params)[0])
        predict, image = self.__predict_data__(upload_file.values_list('file').get(id=params)[0])
        response = {'predict': predict}
        if image is not None:
            parsed_url = urlparse(reverse('predict_get', request=request))
            root_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
            url = '{}{}/{}'.format(root_url, 'media/prediction', image)
            response['predict_image'] = url
        return Response(response)

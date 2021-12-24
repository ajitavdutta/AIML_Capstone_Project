from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import FileUploadSerializer
from rest_framework.response import Response
from fileUpload.models import UploadFile
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
import pydicom
import os


# Create your views here.
class FileGetView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        print('In FileGetView.get')
        params = request.GET.get('id')
        if params is None:
            files = UploadFile.objects.all()
            serializer = FileUploadSerializer(files, many=True, context={'request': self.request})
        else:
            file = UploadFile.objects.filter(id=params)
            serializer = FileUploadSerializer(file, many=True, context={'request': self.request})

        return Response(serializer.data)


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def __get_tags(self, filename):
        tags = []
        image_path = os.path.join(settings.MEDIA_ROOT, filename)
        metadata = pydicom.dcmread(image_path, stop_before_pixels=True)
        fmt_data = metadata.formatted_lines()
        for data in fmt_data:
            arr = data.split(':')
            tags.append({'tag': (arr[0].split(')')[1][:-2].strip()), 'value': arr[1].replace("'", "").strip()})

        return tags

    def post(self, request, *args, **kwargs):
        print('In FileUploadView.get')
        serializer = FileUploadSerializer(data=request.data, context={'request': self.request})
        if serializer.is_valid():
            serializer.save()
            model = UploadFile.objects.filter(id=serializer.data['id']).first()
            tags = self.__get_tags(model.file.name)
            resp = {}
            resp.update(serializer.data)
            resp['tags'] = tags
            # print(resp)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(resp, status=status.HTTP_201_CREATED)
        else:
            print('error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

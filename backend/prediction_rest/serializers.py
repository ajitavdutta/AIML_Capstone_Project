from rest_framework import serializers
from fileUpload.models import UploadFile
from rest_framework.reverse import reverse
from urllib.parse import urlparse


class PredictionSerializer(serializers.ModelSerializer):
    img_class = serializers.IntegerField()
    img_label = serializers.CharField(max_length=50)
    file_url = serializers.SerializerMethodField('get_file_url')

    def get_file_url(self, obj):
        request = self.context['request']
        parsed_url = urlparse(reverse('predict_get', request=request))
        root_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
        name = obj.file.name.replace('.dcm', '.png')
        name = name.replace('dicom/', 'png/')
        url = '{}{}/{}'.format(root_url, 'media', name)
        return url

    class Meta:
        model = UploadFile
        fields = '__all__'

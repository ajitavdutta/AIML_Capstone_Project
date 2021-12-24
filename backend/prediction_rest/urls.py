from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    re_path(r'(?P<id>[0-9A-Fa-f-]+)', views.PredictView.as_view(), name='predict_get'),
    path('', views.PredictView.as_view(), name='predict_get'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

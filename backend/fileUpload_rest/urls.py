from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('upload/', views.FileUploadView.as_view(), name='files_list'),
    re_path(r'(?P<id>[0-9A-Fa-f-]+)', views.FileGetView.as_view(), name='files_get'),
    path('', views.FileGetView.as_view(), name='files_get'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

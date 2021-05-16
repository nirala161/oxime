from django.urls import path
from . import views

#from video_content.views import upload_video,display



app_name='oxime'

urlpatterns=[
    path('',views.index,name='index'),
    path('upload/',views.upload_data,name='upload'),
    path('display/',views.display,name='display'),
]


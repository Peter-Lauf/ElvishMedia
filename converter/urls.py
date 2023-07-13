from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.conf.urls import include

# Define the urls for the converter app
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('videos.urls')),
    path('api/upload/', views.video_upload, name='video_upload'),
    path('api/convert/', views.convert_video, name='convert_video'),
    path('api/delete/', views.delete_video, name='delete_video'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
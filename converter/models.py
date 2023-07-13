from django.db import models
import os
class Video(models.Model):
    video = models.FileField(upload_to='uploads/videos') # Upload the video to the media/uploads/videos folder

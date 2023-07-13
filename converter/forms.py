from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    video = forms.FileField()
    class Meta: # Meta class to define the model and fields, see models.py
        model = Video
        fields = ['video']
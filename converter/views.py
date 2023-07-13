from django.contrib import messages
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .forms import VideoForm
from .convert import convert_file
import os
from django.conf import settings


def index(request):
    "Renders the home page with the form for uploading a file."
    context = {}
    context['form'] = VideoForm() # Create a form instance, see forms.py
    template_name = "home.html"
    return render(request, template_name, context)



@api_view(['POST'])
def video_upload(request):
    "Uploads the video file to the server and proceeds to convert to requested format."
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES) # Create a form instance and populate it with data from the request
        if form.is_valid(): # Validate the form
            upload = form.save()
            upload.save()  # Save the files to the media, see forms.py and models.py
            return JsonResponse({'success': True, 'file': upload.video.name.split('/')[-1]}) # Return a Json response with the uploaded file name
    return JsonResponse({'success': False})



@ api_view (['POST'])
def convert_video(request):
    "Converts the video file to the requested format."
    if request.method == 'POST':

        upload_file_name = request.POST.get('file_name', None)
        output_format = request.POST.get('output_format', None)
        conversion = convert_file(upload_file_name, output_format)

        if not conversion:
            return JsonResponse({'success': False}) # If the conversion fails, return a Json response with success = False
        if conversion:
            output_file = upload_file_name.split('.')[0] + output_format # Get the name for the converted file
            # Send the converted file names(!) as a Json response back to the client
            return JsonResponse({
                    'success': True, 
                    'file': output_file, 
                    'output_format': output_format, 
                    })
    return JsonResponse({'success': False, "error":"Invalid request"}) # If the request is not POST, return a Json response with success = False


@ api_view (['POST'])
def delete_video(request):
    "Deletes the video file from the server."
    if request.method == 'POST':
        
        upload_file_name = request.POST.get('file_name', None) # Get the file name from the request
        path = os.path.join(settings.MEDIA_ROOT + '\\uploads\\videos\\', upload_file_name) # Get the path to the file
        os.remove(path) # Delete the file
        
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, "error":"Invalid request"})
        




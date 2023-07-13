import os
import subprocess
import imageio_ffmpeg as ff
from django.conf import settings


def get_video_codec(output_format):
    codec_map = {
        ".webm": ("libvpx-vp9", "-lossless 1"),  # libvpx-vp9, libvpx, libvorbis
        ".mkv": ("ffv1", ""),  # ffv1, libx264, libx265
        ".flv": ("flv", "-q:v 0"),  # flv, libx264, libx265
        ".vob": ("mpeg2video", "-q:v 0"),  # mpeg2video, libx264, libx265
        ".avi": ("ffv1", ""),  # ffv1, mpeg4, msmpeg4v2
        ".mov": ("prores_ks", "-profile:v hq"),  # prores_ks, libx264, libx265
        ".wmv": ("wmv2", "-q:v 0"),  # wmv2, wmv1, vc1
        ".mp4": ("libx265", "-crf 0"),  # libx265, libx264, mpeg4
        ".mpg": ("mpeg2video", "-q:v 0"),  # mpeg2video, libx264, libx265
        ".mpeg": ("mpeg2video", "-q:v 0"),  # mpeg2video, libx264, libx265
        ".3gp": ("libx264", "-crf 0")  # libx264, libx265, mpeg4
    }
    if output_format.lower() not in codec_map:
        raise ValueError(f"Unsupported output format: {output_format}")
    return codec_map.get(output_format.lower(), ("libx264", "-crf 0"))


def get_audio_codec(output_format):
    codec_map = {
        ".webm": "libopus",
        ".mkv": "aac",
        ".flv": "libmp3lame",
        ".vob": "ac3",
        ".avi": "libmp3lame",
        ".mov": "aac",
        ".wmv": "wmav2",
        ".mp4": "aac",
        ".mpg": "mp2",
        ".mpeg": "mp2",
        ".3gp": "aac"
    }
    if output_format.lower() not in codec_map:
        raise ValueError(f"Unsupported audio output format: {output_format}")
    return codec_map.get(output_format.lower(), "aac")


# Convert video codec to FFV1

def convert_file(file_name, output_format):
    folder = settings.MEDIA_ROOT+'\\uploads\\videos\\' # Define uploads file path
    input_file = os.path.join(folder, file_name) # Define input file path
    output_file = os.path.join(folder, os.path.splitext(input_file)[0] + output_format) # Define output file path
 
    video_codec, quality_flag = get_video_codec(output_format) # Get video codec
    audio_codec = get_audio_codec(output_format)   # Get audio codec

    intermediate_file = folder + "intermediate_video.mkv" # Define intermediate file path

    ffmpeg_path = ff.get_ffmpeg_exe() # Get ffmpeg.exe path

    cmd_ffv1 = f'"{ffmpeg_path}" -i "{input_file}" -async 1 -c:v ffv1 -level 3 -coder 1 -context 1 -g 1 -slices 24 -slicecrc 1' \
               f' -b:v 0 -c:a copy -row-mt 1 "{intermediate_file}"' # FFV1 command for converting to intermediate file    
    try:
        subprocess.check_output(cmd_ffv1, shell=True, stderr=subprocess.STDOUT) # Run FFV1 command for converting to intermediate file
        print(f"Successfully re-encoded {input_file} using FFV1 codec to {intermediate_file}")
    except subprocess.CalledProcessError as e: # If error occurs during conversion to intermediate file
        print(f"Error occurred while re-encoding {input_file} using FFV1 codec: {e}")
        return False

# Convert to final format.

    cmd_convert = f'"{ffmpeg_path}" -i "{intermediate_file}" -async 1 -c:v {video_codec} {quality_flag} -b:v 0' \
                  f' -c:a {audio_codec}  -map 0 -map_metadata 0 -row-mt 1 "{output_file}"' # Final command for converting to final file
    try:
        subprocess.check_output(cmd_convert, shell=True, stderr=subprocess.STDOUT) # Run final command for converting to final file
        os.remove(intermediate_file) # Delete intermediate file
        return True
    except subprocess.CalledProcessError as e: # If error occurs during conversion to final file
        print(f"Error occurred while converting {intermediate_file} to {output_file}: {e}")
        os.remove(intermediate_file)
        return False

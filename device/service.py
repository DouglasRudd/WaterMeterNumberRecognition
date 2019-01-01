from device import ffmpeg
from device import http_client as http


def take_picture_and_return_it(path_to_folder, device_url):
    http.get_raw_image_and_save_it(path_to_folder, device_url)
    image = ffmpeg.saveImageOnDisk(path_to_image=path_to_folder)
    #image = ffmpeg.saveImageInMemory(path_to_image=path_to_folder)
    return image

import cv2


def save_image_as_jpeg_ad_return_url_ot_it(user, image):
    path_to_image_as_jpg = user.path_to_image+'/'+user.oib+'.jpg'
    cv2.imwrite(path_to_image_as_jpg, image)
    return path_to_image_as_jpg


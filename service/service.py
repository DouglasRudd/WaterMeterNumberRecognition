from device import service as device_service
from processing import service as ocr
from repository import manager
from domain.models import Korisnik, KorisnikData, MetaDataAboutImageGetting
import datetime
import pytz
from image import service as image_service


def do_the_job_for_one_user(oib):
    predicted_float = -1.0
    predicted_as_string = ''
    # 1. dohvati po oibu 54941759440 korisnik
    user = manager.get_user_for_oib(user_oib=oib)
    # 2. s pathom do foldera gdje treba biti slika i s ip adressom uslikaj sliku, spremi je i vrati je
    image = device_service.take_picture_and_return_it(path_to_folder=user.path_to_image,
                                                      device_url=user.device_ip_adress)
    #2.5 Spremi sliku u korisnicki folder kao jpeg i dohvati path do foldera, da je poslije u bazu
    #cv2.imwrite(path_to_image_as_jpg, image)
    path_to_image_as_jpg = image_service.save_image_as_jpeg_ad_return_url_ot_it(user=user, image=image)
    # 3. procesiraj sliku i v rati predktirane znamenke
    try:
        predicted_as_string = ocr.get_predicted_numbers_as_string_from_image(image)
        predicted_float = float(predicted_as_string)
    except ValueError as err:
        print(err.args)
    # 4. Napravi modele
    timestamp = datetime.datetime.now().replace(tzinfo=pytz.timezone('Europe/Zagreb'))
    print str(timestamp)
    last_pic_taken_domain = MetaDataAboutImageGetting(status='1', time_last_pic_taken=timestamp)
    user_data_domain = KorisnikData(__get_image_as_binary(path_to_image_as_jpg), predicted_as_string,
                                    predicted_float, timestamp)
    # 5. Zapisi sve u bazu za tog korisnika
    manager.save_data_for_user(user_oib=user.oib, last_pic_taken_domain=last_pic_taken_domain,
                               user_data_domain=user_data_domain)


def __get_image_as_binary(url_to_image):
    with open(url_to_image, "rb") as imageFile:
        f = imageFile.read()
        return bytearray(f)


if __name__ == "__main__":
    #do_the_job_for_one_user('54941759440')
    do_the_job_for_one_user('test')

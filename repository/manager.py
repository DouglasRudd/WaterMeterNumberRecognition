from repository import persistence
from domain import models
import datetime
# from contextlib import contextmanager
# from sqlalchemy.orm import Session
from app import config
from domain.models import Korisnik

def save_data_for_user(user_oib, last_pic_taken_domain, user_data_domain):
    with config.session_scope() as session:
        persistence.save_data_for_exsisting_user(session, user_oib, last_pic_taken_domain, user_data_domain)

def get_user_for_oib(user_oib):
    with config.session_scope() as session:
        user = persistence.get_user_for_oib(session, user_oib)
        return Korisnik(user.name, user.oib, user.device_ip_adress, user.salary, user.tstamp, user.path_to_image)


if __name__ == "__main__":
    user = models.Korisnik('Burketic', '54941759449', 'http://192.168.1.66', 3200.43, datetime.datetime.utcnow(), 'G:/UtilityMeterAppFolder/54941759440'+'54941759449')
    last_pic_taken = models.MetaDataAboutImageGetting(status='0', time_last_pic_taken=datetime.datetime.utcnow())
    user_data = models.KorisnikData(slika='../resources/watermeter2.png', predicted='00007', stanje=7.0, tstamp=datetime.datetime.utcnow())

    with config.session_scope() as session:
        persistence.save_data_for_exsisting_user(session, '54941759440', last_pic_taken, user_data)

    with config.session_scope() as session:
        persistence.save_user(session, user)

    user = get_user_for_oib('54941759440')
    print user.name, user.device_ip_adress, user.oib, user.salary

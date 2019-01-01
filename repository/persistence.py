from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime, Sequence, BLOB
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
import datetime
from PIL import Image
import io


Base = declarative_base()

class Korisnik(Base):
    __tablename__ = 'korisnici'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(250), nullable=False)
    oib = Column(String(11))
    device_ip_adress = Column(String(100))
    salary = Column(Float)
    tstamp = Column(DateTime(timezone=True), server_default=func.now())
    path_to_image = Column(String)


    def __init__(self, name, oib, device_ip_adress, salary, tstapm, path_to_image):
        self.name = name
        self.oib = oib
        self.device_ip_adress = device_ip_adress
        self.salary = salary
        self.tstamp = tstapm
        self.path_to_image = path_to_image

    def __repr__(self):
        return '<id {}>'.format(self.id)

class MetaDataAboutImageGetting(Base):
    __tablename__ = 'meta_data_about_image_getting'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, Sequence('last_pic_taken_id_seq'), primary_key=True)
    id_korisnika = Column(Integer, ForeignKey('korisnici.id'))
    status = Column(String)
    time_last_pic_taken = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user = relationship("Korisnik", back_populates="meta_data_about_images_getting")

    def __init__(self, status, time_last_pic_taken=None):
        self.status = status
        my_date = datetime.datetime.utcnow()
        new_date = my_date.replace(hour=my_date.hour+2)
        self.time_last_pic_taken = new_date

    def __repr__(self):
        return '<id {}>'.format(self.id)

class KorisnikData(Base):
    __tablename__ = 'korisnik_data'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, Sequence('user_data_seq'), primary_key=True)
    id_korisnika = Column(Integer, ForeignKey('korisnici.id'))
    slika = Column(BLOB)
    predicted = Column(String)
    stanje = Column(Float)
    tstamp = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("Korisnik", back_populates="user_data")

    def __init__(self, slika, predicted, stanje, tstamp):
        self.slika = slika
        self.predicted = predicted
        self.stanje = stanje
        my_date = datetime.datetime.utcnow()
        new_date = my_date.replace(hour=my_date.hour+2)
        self.tstamp = new_date

    def __repr__(self):
        return '<id {}>'.format(self.id)

def __get_image_as_binary(url_to_image):
    with open(url_to_image, "rb") as imageFile:
        f = imageFile.read()
        return bytearray(f)



def get_user_for_oib(session, user_oib):
    __add_relatonships()
    user = session.query(Korisnik).filter(Korisnik.oib == user_oib).one()
    return user


def save_data_for_exsisting_user(session, user_oib, last_pic_taken, user_data):
    __add_relatonships()

    user = session.query(Korisnik).filter(Korisnik.oib == user_oib).one()
    #print user.name

    user.meta_data_about_images_getting.append(MetaDataAboutImageGetting(status=last_pic_taken.status,
                                                                         time_last_pic_taken=None))
    user.user_data.append(KorisnikData(slika=user_data.slika, predicted=user_data.predicted,
                                       stanje=user_data.stanje, tstamp=None))

def save_user(session, user_domain):
    __add_relatonships()
    user = Korisnik(user_domain.name, user_domain.oib, user_domain.device_ip_adress, user_domain.salary, datetime.datetime.utcnow(), user_domain.path_to_image)
    session.add(user)

def __add_relatonships():
    if not hasattr(Korisnik, 'last_pics_taken') and not hasattr(Korisnik, 'user_data'):
        Korisnik.meta_data_about_images_getting = relationship("MetaDataAboutImageGetting",
                                                               order_by=MetaDataAboutImageGetting.id,
                                                               back_populates="user")
        Korisnik.user_data = relationship("KorisnikData", order_by=KorisnikData.id, back_populates="user")



if __name__ == "__main__":

    __add_relatonships()

    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = create_engine('postgresql://postgres:ivavedran@localhost:5432/utilitymeter')

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)


    # SQLAlchemy SESSIONS

    '''Sessions give you access to Transactions, whereby on success you can commit the transaction
    or rollback one incase you encounter an error'''

    Session = sessionmaker(bind=engine)
    session = Session()

    # Insert multiple data in this session, similarly you can delete
    user1 = Korisnik('Vito', '54941759446', 'http://192.168.1.66', 3200.43, datetime.datetime.utcnow(),
                     'G:/UtilityMeterAppFolder/'+'54941759446')
    user2 = Korisnik('Boris', '54941759447', 'http://192.168.1.67', 3500.43, datetime.datetime.utcnow(),
                     'G:/UtilityMeterAppFolder/'+'54941759447')

    user1.meta_data_about_images_getting = [MetaDataAboutImageGetting(status='0', time_last_pic_taken=datetime.datetime.utcnow())]
    user1.user_data = [KorisnikData(slika=__get_image_as_binary('../resources/watermeter2.png'), predicted='00007',
                                    stanje=7.0, tstamp=datetime.datetime.utcnow())]

    session.add(user1)
    session.add(user2)

    try:
        print 'bla'
        #session.commit()
    # You can catch exceptions with &nbsp;SQLAlchemyError base class
    except SQLAlchemyError as e:
        session.rollback()
        print (str(e))

    #Get data
    for user in session.query(Korisnik).all():
        print ("name of the user is", user.name)
        print ("oib of the user is", user.oib)

    user = session.query(Korisnik).filter(Korisnik.name == 'Vito').one()
    image = Image.open(io.BytesIO(user.user_data[0].slika))
    image.show()
    user = session.query(Korisnik).filter(Korisnik.name == 'Boris').one()
    user.user_data = [KorisnikData(slika=__get_image_as_binary('../resources/watermeter2.png'), predicted='00007',
                                   stanje=7.0, tstamp=datetime.datetime.utcnow())]
    session.add(user)
    #rolback for test
    session.rollback()
    #Close the connection
    engine.dispose()

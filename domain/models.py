class Korisnik:
    def __init__(self, name, oib, device_ip_adress, salary, tstapm, path_to_image):
        self.name = name
        self.oib = oib
        self.device_ip_adress = device_ip_adress
        self.salary = salary
        self.tstamp = tstapm
        self.path_to_image = path_to_image

    def __repr__(self):
        return '<id {}>'.format(self.id)

class MetaDataAboutImageGetting:
    def __init__(self, status, time_last_pic_taken):
        self.status = status
        self.time_last_pic_taken = time_last_pic_taken

    def __repr__(self):
        return '<id {}>'.format(self.id)

class KorisnikData:
    def __init__(self, slika, predicted, stanje, tstamp):
        self.slika = slika
        self.predicted = predicted
        self.stanje = stanje
        self.tstamp = tstamp

    def __repr__(self):
        return '<id {}>'.format(self.id)
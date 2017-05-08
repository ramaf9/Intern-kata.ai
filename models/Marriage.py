import time

class Marriage(object):
    """
        Marriage class sebagai model
        untuk mengetahui atribut dari
        tabel marriage
    """
    # constructor awal
    def __init__(self, id, husbandId, wifeId, startDate, endDate):
        self.id = id
        self.husbandId = husbandId
        self.wifeId = wifeId
        self.startDate = startDate
        self.endDate = endDate

    # kembalikan atribut id
    def getId(self):
        return self.id

    # kembalikan atribut suami
    def getHusband(self):
        return self.husbandId

    # kembalikan atribut istri
    def getWife(self):
        return self.wifeId

    # kembalikan tanggal pernikahan
    def getMarriageDate(self):
        return self.startDate

    # kembalikan tanggal perceraian
    def getDivorceDate(self):
        return self.endDate

    # mengembalikan apakah telah bercerai
    def isEnded(self):
        # cek waktu & convert satuan waktu
        if self.endDate and self.endDate <= time.strftime("%Y-%m-%d"):
            return True
        else:
            return False

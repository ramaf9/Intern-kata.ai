import collections

class Repo(object):
    """
        Repo class untuk penyimpanan dan pencarian data
        dalam bentuk OrderedDict
    """
    # OrderedDict untuk tabel person
    dictPerson = collections.OrderedDict({})
    # OrderedDict untuk tabel marriage
    dictMarriage = collections.OrderedDict({})

    def addPerson(self, person):
        """
            params: Person class
            menambahkan object person ke dalam
            list
        """
        self.dictPerson[person.id] = person

    def addMarriage(self, marriage):
        """
            params: Marriage class
            menambahkan object marriage ke dalam
            list
        """
        self.dictMarriage[marriage.id] = marriage

    def getPersonById(self, id):
        """
            params: String id
            mencari dan mengembalikan person
            berdasarkan id
        """
        try:
            return self.dictPerson[id]
        except KeyError:
            return False

    def getMarriageById(self,id):
        """
            params: String id
            mencari dan mengembalikan marriage
            berdasarkan id
        """
        return self.dictMarriage[id]

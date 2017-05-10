from Marriage import Marriage
from database import Repo
from helpers import Graph

class Person(Repo, Marriage):
    """
        Class person inherit dari repo & marriage
        untuk mengetahui atribut dari tabel person
        dan relasi antar person
    """
    def __init__(self, id, name, gender, birth_date, fatherId, motherId):
        self.id = id
        self.name = name
        self.gender = gender.lower()
        self.birth_date = birth_date
        self.fatherId = fatherId
        self.motherId = motherId

    def getId(self):
        """
            mengembalikan atribut id
        """
        return self.id

    def isMale(self):
        """
            mengecek apa gender person
            adalah laki-laki
        """
        if self.gender == "male":
            return True
        else:
            return False

    def isFemale(self):
        """
            mengecek apa gender person
            adalah perempuan
        """
        if self.gender == "female":
            return True
        else:
            return False

    def getName(self):
        """
            mengembalikan nama person
        """
        return self.name

    def getBirthDate(self):
        """
            mengembalikan tanggal lahir
        """
        return self.birth_date

    def getFather(self):
        """
            mengembalikan id dari ayah
        """
        return self.fatherId

    def getMother(self):
        """
            mengembalikan id dari ibu
        """
        return self.motherId

    def isMarried(self):
        """
            mengecek apakah person sudah menikah atau belum
        """
        self.is_married = False
        # looping dari list marriage
        for i, v in self.dictMarriage.items():
            # bila ditemukan id pada husband atau wife
            if self.id == v.getHusband() or self.id == v.getWife() :
                # return true
                self.is_married = True
                break
        return self.is_married

    def isDivorced(self):
        """
            mengecek apakah person sudah pernah menikah dan bercerai
        """
        self.is_divorced = False
        # looping dari list marriage
        for i, v in self.dictMarriage.items():
            # cek id pada wife atau husband dan ambil tanggal cerai
            if (self.id == v.getHusband() or self.id == v.getWife()) and v.getDivorceDate() :
                # return true
                self.is_divorced = True
                break
        return self.is_divorced

    def isParent(self, child):
        """
            mengembalikan apakah person merupakan
            orang tua dari anak
        """
        # set default
        self.is_parent = False
        # cek id dari orang tua anak
        if self.id == child.getFather() or self.id == child.getMother():
            self.is_parent = True
        return self.is_parent

    def isStepParent(self, child):
        """
            mengembalikan apakah person merupakan
            mertua dari anak
        """
        # set default
        self.is_stepparent = False
        # set pasangan default
        spouse = False
        # looping setiap list marriage
        for i, v in child.dictMarriage.items():
            # cek pasangan dari anak
            if child.id == v.getHusband():
                spouse = v.getWife()
                break
            elif child.id == v.getWife():
                spouse = v.getHusband()
                break
        if spouse:
            parent = self.getPersonById(spouse)
            # cek apakah orang tua pasangan sama dengan person
            if self.id == parent.getFather() or self.id == parent.getMother():
                self.is_stepparent = True
        return self.is_stepparent

    def getSpouse(self):
        """
            mengembalikan pasangan dari person
        """
        spouse = False
        # looping setiap list marriage
        for i, v in self.dictMarriage.items():
            # cek pasangan dari person
            if self.id == v.getHusband() and not v.isEnded():
                spouse = v.getWife()
                break
            elif self.id == v.getWife() and not v.isEnded():
                spouse = v.getHusband()
                break
        # cek bila pasangan ada
        if spouse:
            # kembalikan pasangan
            return [self.getPersonById(spouse)]
        else:
            return []

    def getFormerSpouse(self):
        """
            mengembalikan mantan pasangan
        """
        # set default
        spouse = False
        # loop list marriage
        for i, v in self.dictMarriage.items():
            # cek apakah sudah menikah dan memiliki tanggal cerai
            if self.id == v.getHusband() and v.getDivorceDate():
                spouse = v.getWife()
            elif self.id == v.getWife() and v.getDivorceDate():
                spouse = v.getHusband()
        if spouse:
            # kembalikan nilai pasangan
            return [self.getPersonById(spouse)]
        else:
            return []

    def getParents(self):
        """
            mengembalikan kedua orang tua person
        """
        parents = []
        # cari person berdasarkan id ayah
        father = self.getPersonById(self.getFather())
        if father:
            parents.append(father) # tambahkan ke array
        # cari person berdasarkan id ibu
        mother = self.getPersonById(self.getMother())
        if mother:
            parents.append(mother) # tambahkan ke array
        return parents

    def getChildren(self):
        """
            mengembalikan semua anak dari person
        """
        childrens = []
        # loop tiap person
        for i, v in self.dictPerson.items():
            # cek id person dengan id ayah atau ibu
            if self.id == v.getFather() or self.id == v.getMother():
                childrens.append(v) # tambahkan ke array
        return childrens

    def getSiblings(self, gender = True):
        """
            mengembalikan semua saudara (perempuan, laki2)
            dari person
        """
        # set default array
        siblings = []
        person = ''
        # looping tiap list person
        for i, v in self.dictPerson.items():
            # apabila person bukan merupakan diri sendiri dan memiliki orang tua yang sama
            if not gender:
                if gender == 'male':
                    is_gender = v.isMale()
                elif gender == 'female':
                    is_gender = v.isFemale()
                else:
                    is_gender = True
            else:
                is_gender = True

            if (self.getId() != v.getId() and self.getFather() == v.getFather() and self.getMother() == v.getMother()) and is_gender :
                person = v.getId()
                # cari orang dari id
                sib = self.getPersonById(person)
                siblings.append(sib) # tambahkan array
        return siblings

    def getSisters(self):
        """
            mengembalikan saudara perempuan dari person
        """
        sisters = self.getSiblings('female')
        return sisters

    def getBrothers(self):
        """
            mengembalikan saudara laki-laki dari person
        """
        brothers = self.getSiblings('male')
        return brothers

    def getStepChildren(self):
        """
            mengembalikan mantu dari person
        """
        # set default array
        stepchildrens = []
        person = ''
        spouse = ''
        # loop tiap list person
        for i, v in self.dictPerson.items():
            # cek apakah id sama dengan orang tua
            if self.id == v.getFather() or self.id == v.getMother():
                person = v.getId()
                # loop untuk tiap pernikahan
                for i, v in self.dictMarriage.items():
                    # ambil nilai pasangan
                    if person == v.getHusband():
                        spouse = v.getWife()
                        # cari orang dari id spouse
                        x = self.getPersonById(spouse)
                        stepchildrens.append(x)
                    elif person == v.getWife():
                        spouse = v.getHusband()
                        # cari orang dari id spouse
                        x = self.getPersonById(spouse)
                        stepchildrens.append(x)
        return stepchildrens

    def __getStepSiblings(self, gender = None):
        """
            mengembalikan saudara laki2 atau perempuan
        """
        print('GENDERKU %s' %gender)
        # set default
        stepbrothers = []
        person = ''
        spouse = ''
        for i, v in self.dictMarriage.items():
            if self.id == v.getHusband():
                spouse = self.getPersonById(v.getWife())
                for i, v in self.dictPerson.items():
                    # ambil value gender menjadi getGender
                    if gender:
                        if gender == 'male':
                            is_gender = v.isMale()
                        elif gender == 'female':
                            is_gender = v.isFemale()
                        else:
                            is_gender = True
                    # cek nilai orang tua pasangan dengan orang tua person dan laki2
                    if (spouse.getFather() == v.getFather() and spouse.getMother() == v.getMother()) and is_gender:
                        if v.getId() != spouse.getId():
                            person = v.getId()
                            # cari orang dari id
                            b = self.getPersonById(person)
                            stepbrothers.append(b)
            elif self.id == v.getWife():
                spouse = self.getPersonById(v.getHusband())
                for i, v in self.dictPerson.items():
                    # ambil value gender menjadi getGender
                    if gender:
                        if gender == 'male':
                            is_gender = v.isMale()
                        elif gender == 'female':
                            is_gender = v.isFemale()
                        else:
                            is_gender = True
                    # cek nilai orang tua pasangan dengan orang tua person dan laki2
                    if (spouse.getFather() == v.getFather() and spouse.getMother() == v.getMother()) and is_gender:
                        if v.getId() != spouse.getId():
                            person = v.getId()
                            # cari orang dari id
                            b = self.getPersonById(person)
                            stepbrothers.append(b)

        return stepbrothers


    def getStepSisters(self):
        """
            mengembalikan saudara perempuan dari pasangan person
        """
        # set default
        stepsisters = self.__getStepSiblings('female')
        return stepsisters

    def getStepBrothers(self):
        """
            mengembalikan saudara laki2 dari pasangan person
        """
        # set default
        stepbrothers = self.__getStepSiblings('male')
        return stepbrothers

    def getStepMother(self):
        """
            mengembalikan ibu mertua dari person
        """
        person = ''
        spouse = ''
        stepmother = False
        # loop tiap pernikahan
        for i, v in self.dictMarriage.items():
            # cek apakah id = suami
            if self.id == v.getHusband():
                # ambil nilai pasangan
                spouse = self.getPersonById(v.getWife())
                # ambil ibu pasangan
                stepmother = spouse.getMother()
            # cek apakah id = istri
            elif self.id == v.getWife():
                # ambil nilai pasangan
                spouse = self.getPersonById(v.getHusband())
                # ambil ibu pasangan
                stepmother = spouse.getMother()

        stepmother = self.getPersonById(stepmother)
        if stepmother:
            return [stepmother]
        else:
            return []

    def getStepFather(self):
        """
            mengembalikan bapak mertua dari person
        """
        person = ''
        spouse = ''
        stepfather = False
        # loop tiap pernikahan
        for i, v in self.dictMarriage.items():
            # cek apakah id = suami
            if self.id == v.getHusband():
                # ambil nilai pasangan
                spouse = self.getPersonById(v.getWife())
                # ambil ayah pasangan
                stepfather = spouse.getFather()
            elif self.id == v.getWife():
                # ambil nilai pasangan
                spouse = self.getPersonById(v.getHusband())
                # ambil ayah pasangan
                stepfather = spouse.getFather()
        stepfather = self.getPersonById(stepfather)
        if stepfather:
            return [stepfather]
        else:
            return []

    def getUncles(self):
        """
            mengembalikan tante dari person
        """
        uncles = []
        person = ''
        # cek semua kakek nenek
        # ambil value tiap kakek nenek
        gp = self.getGrandParents()
        fathergf = gp[0].getId() # id kakek dari ayah
        mothergf = gp[1].getId() # id kakek dari ibu
        fathergm = gp[2].getId() # id nenek dari ayah
        mothergm = gp[3].getId() # id nenek dari ibu
        # loop tiap person
        for i, v in self.dictPerson.items():

            # cek apakah orang tua tiap orang = kakek nenek dan laki2
            if ((fathergf == v.getFather() or mothergf == v.getFather()) and (fathergm == v.getMother() or mothergm == v.getMother())) and v.isMale():
                if self.getFather() != v.getId():
                    person = v.getId()
                    # cari orang dari id
                    u = self.getPersonById(person)
                    uncles.append(u)
        return uncles

    def getAunties(self):
        """
            mengembalikan tante dari person
        """
        aunties = []
        person = ''
        gp = self.getGrandParents()
        # cek semua kakek nenek
        # ambil value tiap kakek nenek
        fathergf = gp[0].getId() # id kakek dari ayah
        mothergf = gp[1].getId() # id kakek dari ibu
        fathergm = gp[2].getId() # id nenek dari ayah
        mothergm = gp[3].getId() # id nenek dari ibu
        # looping tiap person
        for i, v in self.dictPerson.items():
            # cek apakah orang tua tiap orang = kakek nenek dan perempuan
            if ((fathergf == v.getFather() or mothergf == v.getFather()) and (fathergm == v.getMother() or mothergm == v.getMother())) and v.isFemale():
                if self.getMother() != v.getId():
                    person = v.getId()
                    u = self.getPersonById(person)
                    aunties.append(u)
        return aunties

    def getGrandFathers(self):
        """
            mengembalikan kakek dari person
            atau orang tua dari kedua orang tua person
        """
        # set default value
        grandfathers = []
        # ambil person dari id ayah ayah
        fathergf = self.getPersonById(self.getFather())
        if fathergf:
            fathergf = self.getPersonById(fathergf.getFather())
            if fathergf:
                grandfathers.append(fathergf)
        # ambil person dari id ayah ibu
        mothergf = self.getPersonById(self.getMother())
        if mothergf:
            mothergf = self.getPersonById(mothergf.getFather())
            if mothergf:
                grandfathers.append(mothergf)

        return grandfathers

    def getGrandMothers(self):
        """
            mengembalikan nenek dari person
            atau orang tua dari kedua orang tua person
        """
        # set default value
        grandmothers = []
        # ambil person dari id ibu ayah
        fathergm = self.getPersonById(self.getFather())
        if fathergm:
            fathergm = self.getPersonById(fathergm.getMother())
            if fathergm:
                grandmothers.append(fathergm)
        # ambil person dari id ibu ibu
        mothergm = self.getPersonById(self.getMother())
        if mothergm:
            mothergm = self.getPersonById(mothergm.getMother())
            if mothergm:
                grandmothers.append(mothergm)

        return grandmothers


    def getGrandParents(self):
        """
            mengembalikan semua kakek nenek
        """
        grandparents = []
        # ambil dari fungsi getGrandFathers
        gf = self.getGrandFathers()
        if gf:
            grandparents.extend(gf)
        # ambil dari fungsi getGrandMothers
        gm = self.getGrandMothers()
        if gm:
            grandparents.extend(gm)
        return grandparents

    def getGrandChildren(self):
        """
            mengembalikan semua cucu dari person
        """
        grandchildren = []
        person = ''
        personchild = ''
        # looping tiap list person
        for i, v in self.dictPerson.items():
            # cek orang id orang tua
            if self.getId() == v.getFather() or self.getId() == v.getMother():
                person = v.getId()
                c = self.getPersonById(person)
                # loop person
                for i, v in self.dictPerson.items():
                    # cek id orang tua dari anak kakek nenek
                    if c.getId() == v.getFather() or c.getId() == v.getMother():
                        # ambil tiap anak
                        personchild = v.getId()
                        gc = self.getPersonById(personchild)
                        grandchildren.append(gc)
        return grandchildren

    def getCousins(self):
        """
            mengembalikan semua saudara sepupu
            dari person
        """
        cousins = []
        uncle_auntie = []
        # ambil dari om
        uncle = self.getUncles()
        # ambil dari tante
        auntie = self.getAunties()
        # cek apakah nilai tidak false
        if uncle:
            uncle_auntie.append(uncle)
        if auntie:
            uncle_auntie.append(auntie)
        # loop tiap list person
        for i,v in self.dictPerson.items():
            # ambil orang tua tiap orang
            child_father = v.getFather()
            child_mother = v.getMother()
            child = v
            # disamakan dengan tiap om dan tante
            for vv in uncle_auntie:
                if child_father == vv[0].getId() or child_mother == vv[0].getId():
                    cousins.append(v)
        return cousins

    def getNephews(self):
        """
            mengembalikan semua keponakan
            dari person
        """
        nephews = []
        # ambil semua saudara
        siblings = self.getSiblings()
        # loop tiap list person
        for i, v in self.dictPerson.items():
            # ambil orang tua tiap orang
            child_father = v.getFather()
            child_mother = v.getMother()
            child = v
            # samakan dengan orang tua saudara
            for vv in siblings:
                if child_father == vv.getId() or child_mother == vv.getId():
                    nephews.append(child)
        return nephews

    def find(self, text):
        """
            mencari orang dengan relasi tertentu
            menggunakan natural language
        """
        # potong tiap kata menjadi array
        text_array = text.lower().split('of')
        # reverse array
        text_array = text_array[::-1]
        person = []
        current_person = []
        # set current person
        current_person.append(self)
        # loop untuk tiap kata
        for i in text_array:
            new_current_person = []
            # loop tiap person
            for c in current_person:
                # replace semua whitespace
                i = i.replace(" ", "")
                a = None

                # ambil semua relasi
                if i == 'parent':
                    a = c.getParents()
                elif i == 'spouse':
                    a = c.getSpouse()
                elif i == 'formerspouse':
                    a = c.getFormerSpouse()
                elif i == 'children':
                    a = c.getChildren()
                elif i == 'uncle':
                    a = c.getUncles()
                elif i == 'auntie':
                    a = c.getAunties()
                elif i == 'grandfather':
                    a = c.getGrandFathers()
                elif i == 'grandmother':
                    a = c.getGrandMothers()
                elif i == 'grandparent':
                    a = c.getGrandParents()
                elif i == 'grandchildren':
                    a = c.getGrandChildren()
                elif i == 'stepsister':
                    a = c.getStepSisters()
                elif i == 'stepbrother':
                    a = c.getStepBrothers()
                elif i == 'stepchildren':
                    a = c.getStepChildren()
                elif i == 'stepfather':
                    a = c.getStepFather()
                elif i == 'stepmother':
                    a = c.getStepMother()
                elif i == 'brother':
                    a = c.getBrothers()
                elif i == 'sister':
                    a = c.getSisters()
                elif i == 'sibling':
                    a = c.getSiblings()
                elif i == 'nephew':
                    a = c.getNephews()
                elif i == 'cousin':
                    a = c.getCousins()
                else:
                    return None

                # cek apakah person terdapat dalam current_person
                not_in = True
                for item in a:
                    for cp in new_current_person:
                        # apabila id ditemukan
                        if item.getId() == cp.getId():
                            not_in = False
                            break
                    if not_in:
                        not_in = True
                        # tambahkan ke array
                        new_current_person.append(item)
            # tambahkan ke array utama
            current_person = new_current_person
        person = current_person
        return person

    def relationTo(self,person2):
        """
            mengembalikan relasi antara person dengan person2
            sebagai string yang dipisahkan oleh kata of
        """
        # set node graph
        graph = Graph.personGraph(Repo)
        # ambil path terkecil
        path = Graph.shortest_path(graph, self.getId(), person2.getId())
        nlp = []
        # loop tiap path
        for idx, i in enumerate(path):
            # set perbandingan
            cp = self.getPersonById(i)
            cp2 = self.getPersonById(path[idx+1])
            # cari hubungan terdekat antara person dengan person2
            text = cp.getNodeRelation(cp2)['relation']
            if text:
                # tambahkan ke array
                nlp.append(text)

            if idx == len(path)-2:
                break
        # kembalikan nilai join dengan of
        return ' of '.join(nlp[::-1])

    def getNodeRelation(self,person2):
        """
            mengembalikan relasi terdekat dari person
            (parent, spouse, children, siblings)
        """
        value = {}
        value['relation'] = False
        # ambil nilai orang tua
        a = self.getParents()
        if a:
            for i in a:
                if i.getId() == person2.getId():
                    value['relation'] = "parent"
                    value['current_person'] = i
                    break
        # ambil nilai pasangan
        a = self.getSpouse()
        if a:
            for i in a:
                if i.getId() == person2.getId():
                    value['relation'] = "spouse"
                    value['current_person'] = i
                    break
        # ambil nilai anak
        a = self.getChildren()
        if a:
            for i in a:
                if i.getId() == person2.getId():
                    value['relation'] = "children"
                    value['current_person'] = i
                    break
        # ambil nilai saudara laki2
        a = self.getBrothers()
        if a:
            for i in a:
                if i.getId() == person2.getId():
                    value['relation'] = "brother"
                    value['current_person'] = i
                    break
        # ambil nilai saudara perempuan
        a = self.getSisters()
        if a:
            for i in a:
                if i.getId() == person2.getId():
                    value['relation'] = "sister"
                    value['current_person'] = i
                    break
        return value

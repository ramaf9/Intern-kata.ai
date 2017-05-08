import time
import csv
import collections
from models import Marriage, Person
from database.Repo import Repo
from helpers import Graph


def importMarriageCSV(filePath):
    """
        params: string path csv
        membaca dan menambahkan data Marriage ke repo
    """
    #baca csv
    for line in open(filePath):
        row = line.split(';')
        if row[4] == 'null':
            row[4] = None
        a = Marriage(row[0], row[1], row[2], row[3], row[4])
        x = Repo()
        x.addMarriage(a)


def importPersonCSV(filePath):
    """
        params: string path csv
        membaca dan menambahkan data person ke repo
    """
    #baca csv
    for line in open(filePath):
        row = line.split(';')
        a = Person(row[0], row[1], row[2], row[3], row[4], row[5])
        x = Repo()
        x.addPerson(a)

if __name__ == '__main__':
    # import data
    importMarriageCSV("marriage.csv")
    importPersonCSV("person.csv")
    x = Repo()
    person = x.getPersonById("0000590103")
    person2 = x.getPersonById("0000590118")
    child = x.getPersonById("0000590118")
    # cek apakah id terdapat pada list person
    if person and child and person2:
        print('Person Name :%s'%person.getName())
        print('Task 3')
        print('Person is married :%s' %person.isMarried())
        print('Person is divorced :%s' %person.isDivorced())
        print('Person is biological parent of child :%s' %person.isParent(child))
        print('Person is step parent of child :%s' %person.isStepParent(child))
        print('\nTask 4')
        print('Person spouse %s'%person.getSpouse())
        print('Person former spouse %s'%person.getFormerSpouse())
        print('Person parent %s'%person.getParents())
        print('Person children %s'%person.getChildren())
        print('Person siblings %s'%person.getSiblings())
        print('Person sisters %s'%person.getSisters())
        print('Person brothers %s'%person.getBrothers())
        print('Person step children %s'%person.getStepChildren())
        print('Person step sisters %s'%person.getStepSisters())
        print('Person step brothers %s'%person.getStepBrothers())
        print('Person step mother %s'%person.getStepMother())
        print('Person step father %s'%person.getStepFather())
        print('Person uncles %s' %person.getUncles())
        print('Person aunties %s' %person.getAunties())
        print('Person grandfather %s'%person.getGrandFathers())
        print('Person grandmother %s'%person.getGrandMothers())
        print('Person grandparents %s'%person.getGrandParents())
        print('Person grandchildren %s'%person.getGrandChildren())
        print('Person cousins %s'%person.getCousins())
        print('Person nephews %s'%person.getNephews())
        print('\nTask 4')
        print(Graph.getRelationRoot(person, person2))
        find = 'parent'
        print('Find person %s : %s'%(find,person.find(find)))
        print('Get relation of two person : %s' %person.relationTo(person2))

    else:
        print(person)

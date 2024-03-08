
class Film:
    no_instances = 0
    def __init__(self, id, titlu, descriere, gen):
        '''
        Creeaza un nou film cu un id unic, titlu, descriere, gen
        :param id: id-ul serialului
        :type id: str (sa contina doar cifre)
        :param titlu: titlul filmului
        :type titlu: str
        :param descriere: scurta descriere a filmului
        :type descriere: str
        :param gen: genul filmului
        :type gen: str
        '''

        self.__id = id
        self.__titlu = titlu
        self.__descriere = descriere
        self.__gen = gen
        self.__film_curent = [self.__id, self.__titlu, self.__descriere, self.__gen]
        Film.no_instances += 1


    def getID(self):
        return self.__film_curent[0]

    def getTitlu(self):
        return self.__film_curent[1]

    def getDescriere(self):
        return self.__film_curent[2]

    def getGen(self):
        return self.__film_curent[3]

    def setID(self, value):
        self.__film_curent[0] = value

    def setTitlu(self, value):
        self.__film_curent[1] = value

    def setDescriere(self, value):
        self.__film_curent[2] = value

    def setGen(self, value):
        self.__film_curent[3] = value

    def isdigit(self):
        return self.getID().isdigit()

    def isalpha(self):
        return self.getGen().isalpha()

    def GetDisplay(self):
        return self.__film_curent

    def __eq__(self, added_film):
        
        '''Verifica egalitatea dintre doua ID-uri filme
        :param other:
        :return:'''

        return self.getID() == added_film.getID()

    def __str__(self):
        return "ID: " + str(self.getID()) + "; Titlu film: " + self.getTitlu() + '; Gen film: '+ str(self.getGen())

class Client:
    no_instances = 0
    def __init__(self, id, nume, cnp):
        '''
        Creeaza un nou client cu un id unic, un nume si cnp unic
        :param id: id-ul clientului
        :type id: str (sa contina doar cifre)
        :param nume: numele clientului
        :type nume: str
        :param cnp: cnp-ul clientului
        :type cnp: str (contine doar 13 caractere care vor fi numai cifre)

        '''

        self.__id = id
        self.__nume = nume
        self.__cnp = cnp
        Client.no_instances += 1

    def getID(self):
        return self.__id

    def getNume(self):
        return self.__nume

    def getCNP(self):
        return self.__cnp

    def setID(self, value):
        self.__id = value

    def setNume(self, value):
        self.__nume = value

    def setCNP(self, value):
        self.__cnp = value

    def isdigitID(self):
        return self.getID().isdigit()

    def isdigitCNP(self):
        return self.getCNP().isdigit()

    def isalphaNume(self):
        return self.getNume().isalpha()

    def __eq__(self, other):
        '''
        Verifica egalitatea dintre doua ID-uri client
        :param other:
        :return:
        '''

        return self.getID() == other.getID() or self.getCNP() == other.getCNP()


class Inchiriere:
    def __init__(self, film, client, data):
        self.__film = film
        self.__client = client
        self.__data = data

    def getFilm(self):
        return self.__film

    def getClient(self):
        return self.__client

    def getData(self):
        return self.__data

    def setFilm(self, value):
        self.__film = value

    def setClient(self, value):
        self.__client = value

    def setData(self, value):
        self.__data = value

    def __eq__(self, other):
        '''
        Verifica egalitatea dintre doua inchirieri
        Nu ese posibil ca acelasi client sa inchirieze acelasi film
        :param other: Inchiriere
        :return: True daca inchirierile sunt egale, False altfel
        :rtype: bool
        '''
        if self.__film == other.__film and self.__client == other.__client:
            return True
        return False

    def __str__(self):
        return 'Film: ' + str(self.__film.getTitlu()) + ' [' + str(self.__film.getGen()) + ']' + ' - ' + 'Client: ' + str(self.__client.getNume()) +  '[' + str(self.__client.getID()) + '];  Data: ' + str(self.__data)
# teste

def test_create_film():
    film1 = Film('2', 'Black Panther', 'este un supererou din benzile desenate', 'actiune')
    assert (film1.getID() == '2')
    assert (film1.getTitlu() == 'Black Panther')
    assert (film1.getDescriere() == 'este un supererou din benzile desenate')
    assert (film1.getGen() == 'actiune')

    film1.setID('123')
    film1.setTitlu('The Star')
    film1.setDescriere('este o comedie romantica')
    film1.setGen('comedie')

    assert (film1.getID() == '123')
    assert (film1.getTitlu() == 'The Star')
    assert (film1.getDescriere() == 'este o comedie romantica')
    assert (film1.getGen() == 'comedie')


def test_create_client():
    client1 = Client('2', 'Maria', '1234567890123')
    assert (client1.getID() == '2')
    assert (client1.getNume() == 'Maria')
    assert (client1.getCNP() == '1234567890123')

    client1.setID('3')
    client1.setNume('Sorina')
    client1.setCNP('9876543210123')

    client1 = Client('3', 'Sorina', '9876543210123')
    assert (client1.getID() == '3')
    assert (client1.getNume() == 'Sorina')
    assert (client1.getCNP() == '9876543210123')


def test_equal():
    client1 = Client('2', 'Maria', '1234567890123')
    client2 = Client('2', 'Bogdan','2344939395942')
    assert (client1 == client2)
    client1.setID('3')
    assert (client1 != client2)
    client2.setCNP('1234567890123')
    assert (client1 == client2)

def test_create_inchiriere():
    film1 = Film('2', 'Black Panther', 'este un supererou din benzile desenate', 'actiune')
    client1 = Client('2', 'Maria', '1234567890123')

    inchiriere = Inchiriere(film1, client1, 25)

    assert (inchiriere.getFilm() == film1)
    assert (inchiriere.getClient() == client1)
    assert (inchiriere.getData() == 25)

def test_equal_inchiriere():
    film1 = Film('2', 'Black Panther', 'este un supererou din benzile desenate', 'actiune')
    client1 = Client('2', 'Maria', '1234567890123')

    inchiriere1 = Inchiriere(film1, client1, 25)
    inchiriere2 = Inchiriere(film1, client1, 20)
    assert(inchiriere1 == inchiriere2)

    client2 = Client('3', 'Bogdan', '2344939395942')
    inchiriere3 = Inchiriere(film1, client2, 10)
    assert (inchiriere2 != inchiriere3)


def run_tests():
    test_create_film()
    test_create_client()
    test_equal()
    test_create_inchiriere()
    test_equal_inchiriere()

run_tests()
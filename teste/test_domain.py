import unittest
from domain.entities import *
from domain.Exceptions import *
from repository.film_repo import *
from service.film_service import *

class TestCaseDomain(unittest.TestCase):
    def setUp(self) -> None:
        repo_film = InMemoryRepository()
        repo_client = InMemoryRepository()
        repo_inch = InMemoryRepository()
        validator = FilmValidator()
        self.__srv = Service(repo_film, repo_client, repo_inch, validator)

    def test_create_film(self):
        film1 = Film('2', 'Black Panther', 'este un supererou din benzile desenate', 'actiune')
        self.assertTrue(film1.getID() == '2')
        self.assertTrue(film1.getTitlu() == 'Black Panther')
        self.assertTrue(film1.getDescriere() == 'este un supererou din benzile desenate')
        self.assertTrue(film1.getGen() == 'actiune')

        film1.setID('123')
        film1.setTitlu('The Star')
        film1.setDescriere('este o comedie romantica')
        film1.setGen('comedie')

        self.assertTrue(film1.getID() == '123')
        self.assertTrue(film1.getTitlu() == 'The Star')
        self.assertTrue(film1.getDescriere() == 'este o comedie romantica')
        self.assertTrue(film1.getGen() == 'comedie')

    def test_create_clienti(self):
        client1 = Client('2', 'Maria', '1234567890123')
        self.assertTrue(client1.getID() == '2')
        self.assertTrue(client1.getNume() == 'Maria')
        self.assertTrue(client1.getCNP() == '1234567890123')

        client1.setID('3')
        client1.setNume('Sorina')
        client1.setCNP('9876543210123')

        client1 = Client('3', 'Sorina', '9876543210123')
        self.assertTrue(client1.getID() == '3')
        self.assertTrue(client1.getNume() == 'Sorina')
        self.assertTrue(client1.getCNP() == '9876543210123')

    def test_equal(self):
        client1 = Client('2', 'Maria', '1234567890123')
        client2 = Client('2', 'Bogdan', '2344939395942')
        self.assertTrue(client1 == client2)
        client1.setID('3')
        self.assertTrue(client1 != client2)
        client2.setCNP('1234567890123')
        self.assertTrue(client1 == client2)

    def test_create_inchiriere(self):
        film1 = Film('2', 'Black Panther', 'este un supererou din benzile desenate', 'actiune')
        client1 = Client('2', 'Maria', '1234567890123')

        inchiriere = Inchiriere(film1, client1, 25)

        self.assertTrue(inchiriere.getFilm() == film1)
        self.assertTrue(inchiriere.getClient() == client1)
        self.assertTrue(inchiriere.getData() == 25)

    def test_equal_inchiriere(self):
        film1 = Film('2', 'Black Panther', 'este un supererou din benzile desenate', 'actiune')
        client1 = Client('2', 'Maria', '1234567890123')

        inchiriere1 = Inchiriere(film1, client1, 25)
        inchiriere2 = Inchiriere(film1, client1, 20)
        self.assertTrue(inchiriere1 == inchiriere2)

        client2 = Client('3', 'Bogdan', '2344939395942')
        inchiriere3 = Inchiriere(film1, client2, 10)
        self.assertTrue(inchiriere2 != inchiriere3)

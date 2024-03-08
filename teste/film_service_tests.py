import unittest

from domain.validators import FilmValidator
from domain.Exceptions import Validation, InchiriereaDejaExista, InchiriereNotFoundException
from repository.film_repo import FilmFileRepo, InMemoryRepository, RepositoryException
from service.film_service import Service

class TestCaseFilmService(unittest.TestCase):
    def setUp(self) -> None:
        repo_film = InMemoryRepository()
        repo_client = InMemoryRepository()
        repo_inch = InMemoryRepository()
        validator = FilmValidator()
        self.__srv = Service(repo_film, repo_client, repo_inch, validator)

    def test_add_film(self):

        film = self.__srv.add_film("1", "The Star", "este un film frumos", "comedie")
        self.assertTrue(film.getID() == '1')
        self.assertTrue(film.getTitlu() == 'The Star')
        film_list = self.__srv.get_toate_filmele()
        self.assertTrue(len(film_list) == 1)
        self.assertTrue(film_list[0] == film)

    def test_delete_by_id_film(self):
        film = self.__srv.add_film("1", "Deadpool", "este un film frumos", "actiune")
        deleted_film = self.__srv.delete_by_id_film('1')

        self.assertTrue(len(self.__srv.get_toate_filmele()) == 0)
        self.assertTrue(deleted_film.getTitlu() == 'Deadpool')
        self.assertTrue(deleted_film.getGen() == 'actiune')
        self.assertTrue(deleted_film.getDescriere() == 'este un film frumos')
        self.assertRaises(ValueError, self.__srv.delete_by_id_film,'2')

    def test_get_toate_filmele(self):

        self.__srv.add_film('1', 'The Sea', 'este o comedie romantica', 'comedie')
        self.__srv.add_film('2', 'The Master', 'este un film de actiune', 'actiune')
        self.assertIsInstance(self.__srv.get_toate_filmele(), list)
        self.assertTrue(len(self.__srv.get_toate_filmele()) == 2)

    def test_update_film(self):

        self.__srv.add_film('1', 'The Sea', 'este o comedie romantica', 'comedie')
        updated_film = self.__srv.update_film('1', 'See', 'este un film de mister', 'mister')

        self.assertTrue(updated_film.getGen() == 'mister')
        self.assertTrue(updated_film.getTitlu() == 'See')
        self.assertTrue(updated_film.getDescriere() == 'este un film de mister')
        self.assertRaises(ValueError, self.__srv.update_film, '34def', 'See', 'este un film de mister', 'mister')

    def test_find_film_by_id(self):
        self.__srv.add_film('1', 'The Sea', 'este o comedie romantica', 'comedie')
        self.assertTrue(self.__srv.find_film_by_id, '1')
        self.__srv.add_film('2', 'The Master', 'este un film de actiune', 'actiune')
        self.assertRaises(ValueError, self.__srv.find_film_by_id, '3')

    def test_add_client(self):
        client = self.__srv.add_client("1", "Maria", "1234567890123")
        self.assertTrue(client.getID() == '1')
        self.assertTrue(client.getNume() == 'Maria')
        client_list = self.__srv.get_toti_clientii()
        self.assertTrue(len(client_list) == 1)
        self.assertTrue(client_list[0] == client)
        self.assertRaises(RepositoryException, self.__srv.add_client, "1", "Radu", "1234567890000")

    def test_get_toti_clientii(self):
        self.__srv.add_client("1", "Maria", "1234567890123")
        self.__srv.add_client('902', 'Luiza', '2344565567888')
        self.__srv.add_client('910', 'Bogdan', '2393249203023')
        self.assertTrue(type(self.__srv.get_toti_clientii()) == list)
        self.assertTrue(len(self.__srv.get_toti_clientii()) == 3)

    def test_update_client(self):
        'White box'
        self.__srv.add_client('910', 'Bogdan', '2393249203023')
        updated_client = self.__srv.update_client('910', "Maria", "1234567890123")
        self.assertTrue(updated_client.getCNP() == '1234567890123')
        self.assertTrue(updated_client.getNume() == 'Maria')
        self.assertRaises(ValueError, self.__srv.update_client, '-2md4', 'Maria', '1234567890123')

    def test_update_client_black(self):
        'Black box'
        self.__srv.add_client('910', 'Bogdan', '2393249203023')
        updated_client = self.__srv.update_client('910', "Maria", "1234567890123")
        self.assertTrue(updated_client.getCNP() == '1234567890123')
        self.assertTrue(updated_client.getNume() == 'Maria')


    def test_delete_by_id_client(self):
        client = self.__srv.add_client("1", "Maria", "1234567890123")
        deleted_client = self.__srv.delete_by_id_client('1')

        self.assertTrue(len(self.__srv.get_toti_clientii()) == 0)
        self.assertTrue(deleted_client.getNume() == 'Maria')
        self.assertTrue(deleted_client.getID() == '1')
        self.assertTrue(deleted_client.getCNP() == '1234567890123')
        self.assertRaises(ValueError, self.__srv.delete_by_id_client, '2')

    def test_find_client_by_id(self):
        self.__srv.add_client("1", "Maria", "1234567890123")
        self.assertTrue(self.__srv.find_client_by_id, '1')
        self.assertRaises(ValueError, self.__srv.find_client_by_id, '3')

    def test_create_inchiriere(self):
        film = self.__srv.add_film("1", "The Star", "este un film frumos", "comedie")
        client = self.__srv.add_client("1", "Maria", "1234567890123")
        inchiriere = self.__srv.create_inchiriere('1', '1', 13)
        self.assertTrue(inchiriere.getClient() == self.__srv.find_client_by_id('1'))
        self.assertTrue(inchiriere.getData() == 13)
        self.assertRaises(InchiriereaDejaExista, self.__srv.create_inchiriere, '1', '1', 25)
        self.assertRaises(ValueError, self.__srv.create_inchiriere, '2', '1', 15)
        self.assertRaises(ValueError, self.__srv.create_inchiriere, '1', '2', 10)
        self.assertRaises(ValueError, self.__srv.create_inchiriere, '1', '1', -2)

    def test_returnare_inchiriere(self):
        film = self.__srv.add_film("1", "The Star", "este un film frumos", "comedie")
        client = self.__srv.add_client("1", "Maria", "1234567890123")
        inchiriere = self.__srv.create_inchiriere('1', '1', 13)
        self.assertTrue(self.__srv.delete_inchiriere('1', '1'))
        self.assertRaises(ValueError, self.__srv.delete_inchiriere, '2', '1')
        self.assertRaises(ValueError, self.__srv.delete_inchiriere, '1', '2')

    def test_get_all(self):
        film = self.__srv.add_film("1", "The Star", "este un film frumos", "comedie")
        client = self.__srv.add_client("1", "Maria", "1234567890123")
        inchiriere = self.__srv.create_inchiriere('1', '1', 13)
        film = self.__srv.add_film("2", "The Star", "este un film frumos", "comedie")
        client = self.__srv.add_client("4", "Maria", "1234567890125")
        inchiriere = self.__srv.create_inchiriere('2', '4', 3)
        no_inchirieri = self.__srv.get_all()
        self.assertTrue(len(no_inchirieri) == 2)
        self.assertFalse(len(no_inchirieri) == 1)

    def test_get_sorted_by_name_inchirieri(self):
        '''
        AICI
        :return:
        '''
        film = self.__srv.add_film("1", "The Star", "este un film frumos", "comedie")
        client = self.__srv.add_client("1", "Maria", "1234567890123")
        inchiriere = self.__srv.create_inchiriere('1', '1', 13)
        film = self.__srv.add_film("2", "The Star", "este un film frumos", "comedie")
        client = self.__srv.add_client("4", "Maria", "1234567890125")
        inchiriere = self.__srv.create_inchiriere('2', '4', 3)
        client = self.__srv.add_client('5', 'Ana', '1456890345123')
        inchiriere = self.__srv.create_inchiriere('1', '5', 25)
        all_inchirieri = self.__srv.get_all()
        all_inchirieri = self.__srv.get_sorted_by_name_inchirieri()




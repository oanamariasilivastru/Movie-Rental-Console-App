import unittest
from domain.entities import Film, Client, Inchiriere
from domain.Exceptions import *
from repository.film_repo import *

class TestCaseInchiriereRepoInMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.__repo = InMemoryRepository()

    def test_store_inchiriere(self):
        film1 = Film('101', 'Superstore', 'este un film', 'comedie')
        client1 = Client('922', 'Luiza', '2344565567880')
        inch = Inchiriere('101', '922', 23)
        self.__repo.store_inchiriere(inch)
        all_inchiriere = self.__repo.get_all_inchirieri()
        self.assertTrue(len(all_inchiriere) == 1)

    def test_return_inchiriere(self):
        film1 = Film('101', 'Superstore', 'este un film', 'comedie')
        client1 = Client('922', 'Luiza', '2344565567880')
        inch = Inchiriere('101', '922', 23)
        self.__repo.store_inchiriere(inch)
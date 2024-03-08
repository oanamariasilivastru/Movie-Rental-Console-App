import unittest
from domain.entities import Film
from domain.Exceptions import *
from repository.film_repo import *

class TestCaseFilmInMemoryRepo(unittest.TestCase):
    def setUp(self) -> None:
        self.__repo = InMemoryRepository()
        film1 = Film('101', 'Superstore', 'este un film', 'comedie')
        film2 = Film('102', 'Arrow', 'este un film ', 'aciune')
        film3 = Film('103', 'Modern Family', 'este un film', 'SF')
        film4 = Film('104', 'Squid Game', 'este un film', 'aventura')
        film5 = Film('105', 'See', 'este un film', 'mister')
        film6 = Film('106', 'Atypical', 'este un film', 'drama')
        film7 = Film('107', 'The X-Files', 'este un film', 'mister')
        film8 = Film('108', 'The Star', 'este un film', 'romantic')
        film9 = Film('109', 'Now you see me', 'este un film', 'mister')
        film10 = Film('110', 'The Friend', 'este un film', 'comedie')

        self.__repo.store_film(film1)
        self.__repo.store_film(film2)
        self.__repo.store_film(film3)
        self.__repo.store_film(film4)
        self.__repo.store_film(film5)
        self.__repo.store_film(film6)
        self.__repo.store_film(film7)
        self.__repo.store_film(film8)
        self.__repo.store_film(film9)
        self.__repo.store_film(film10)

    def test_find_film_by_id(self):
        p = self.__repo.find_film('105')
        self.assertTrue(p.getTitlu() == 'See')
        self.assertTrue(p.getDescriere() == 'este un film')
        self.assertTrue(p.getGen() == 'mister')

        p1 = self.__repo.find_film('1234')
        self.assertTrue(p1 is None)

    def test_get_toate_filmele(self):
        filme = self.__repo.get_toate_filmele()
        self.assertTrue(type(filme) == list)
        self.assertTrue(len(filme) == 10)

        self.__repo.delete_by_id_film('107')
        self.__repo.delete_by_id_film('101')

        filme = self.__repo.get_toate_filmele()
        self.assertTrue(len(filme) == 8)
        self.assertRaises(ValueError, self.__repo.delete_by_id_film, '100')
        film = Film('111', 'The Crown', 'este un film despre o dinastie', 'actiune')
        self.__repo.store_film(film)
        self.assertTrue(self.__repo.get_toate_filmele()[-1].getTitlu() == 'The Crown')
        self.assertTrue(self.__repo.get_toate_filmele()[-1].getGen() == 'actiune')

    def test_store_film(self):
        film1 = Film('111', 'The Crown', 'este un film despre o dinastie', 'actiune')
        self.__repo.store_film(film1)
        filme = self.__repo.get_toate_filmele()
        #aveam un set-up filme cu 10 filme, deci vor fi 11 filme cu cel nou adaugat
        self.assertTrue(len(filme) == 11)
        film2 = Film('123', 'The X-Files', 'este un film de actiune', 'actiune')
        self.__repo.store_film(film2)
        filme = self.__repo.get_toate_filmele()
        self.assertTrue(len(filme) == 12)

    def test_update_film(self):
        film = Film('1', 'The Sea', 'este o comedie romantica', 'comedie')
        film2 = Film('1', 'See', 'este un film de mister', 'mister')
        self.__repo.store_film(film)
        updated_film = self.__repo.update_film('1',film2)

        self.assertTrue(updated_film.getGen() == 'mister')
        self.assertTrue(updated_film.getTitlu() == 'See')
        self.assertTrue(updated_film.getDescriere() == 'este un film de mister')

    def test_delete_film(self):
        film1 = Film('111', 'The Crown', 'este un film despre o dinastie', 'actiune')
        self.__repo.store_film(film1)
        film2 = Film('123', 'The X-Files', 'este un film de actiune', 'actiune')
        self.__repo.store_film(film2)

        deleted_film = self.__repo.delete_by_id_film('123')
        self.assertTrue(deleted_film.getTitlu() == 'The X-Files')
        self.assertTrue(deleted_film.getDescriere() == 'este un film de actiune')
        self.assertTrue(deleted_film.getGen() == 'actiune')
        self.assertRaises(ValueError, self.__repo.delete_by_id_film, '234ff')


class TestCaseFilmRepoFile(unittest.TestCase):
    def setUp(self) -> None:
        self.__repo = FilmFileRepo('test_filme_repo.txt')
        film1 = Film('101', 'Superstore', 'este un film', 'comedie')
        film2 = Film('102', 'Arrow', 'este un film ', 'aciune')
        film3 = Film('103', 'Modern Family', 'este un film', 'SF')
        film4 = Film('104', 'Squid Game', 'este un film', 'aventura')
        film5 = Film('105', 'See', 'este un film', 'mister')
        film6 = Film('106', 'Atypical', 'este un film', 'drama')
        film7 = Film('107', 'The X-Files', 'este un film', 'mister')
        film8 = Film('108', 'The Star', 'este un film', 'romantic')
        film9 = Film('109', 'Now you see me', 'este un film', 'mister')
        film10 = Film('110', 'The Friend', 'este un film', 'comedie')

    def test_find_film_by_id(self):
        p = self.__repo.find_film('105')
        self.assertTrue(p.getTitlu() == 'See')
        self.assertTrue(p.getDescriere() == 'este un film')
        self.assertTrue(p.getGen() == 'mister')

        p1 = self.__repo.find_film('1234')
        self.assertTrue(p1 is None)

    def test_get_toate_filmele(self):
        filme = self.__repo.get_toate_filmele()
        self.assertTrue(type(filme) == list)

        self.assertRaises(ValueError, self.__repo.delete_by_id_film, '107')
        self.assertRaises(ValueError, self.__repo.delete_by_id_film, '101')

        filme = self.__repo.get_toate_filmele()
        self.assertRaises(ValueError, self.__repo.delete_by_id_film, '100')
        film = Film('111', 'The Crown', 'este un film despre o dinastie', 'actiune')
        self.assertRaises(RepositoryException, self.__repo.store_film, film)
        self.assertFalse(self.__repo.get_toate_filmele()[-1].getTitlu() == 'The Crown')
        self.assertTrue(self.__repo.get_toate_filmele()[-1].getGen() == 'actiune')

    def test_store_film(self):
        film1 = Film('111', 'The Crown', 'este un film despre o dinastie', 'actiune')
        #self.__repo.store_film(film1)
        filme = self.__repo.get_toate_filmele()
        #aveam un set-up filme cu 10 filme, deci vor fi 11 filme cu cel nou adaugat
        #self.assertTrue(len(filme) == 11)
        film2 = Film('123', 'The X-Files', 'este un film de actiune', 'actiune')
        #self.__repo.store_film(film2)
        filme = self.__repo.get_toate_filmele()

    def test_update_film(self):
        film = Film('1', 'The Sea', 'este o comedie romantica', 'comedie')
        film2 = Film('1', 'See', 'este un film de mister', 'mister')
        #self.__repo.store_film(film)
        updated_film = self.__repo.update_film('1',film2)

        self.assertTrue(updated_film.getGen() == 'mister')
        self.assertTrue(updated_film.getTitlu() == 'See')
        self.assertTrue(updated_film.getDescriere() == 'este un film de mister')





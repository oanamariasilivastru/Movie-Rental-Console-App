import unittest
from domain.entities import Film
from domain.Exceptions import *
from repository.film_repo import *

class TestCaseClientRepoInMemory(unittest.TestCase):
    def setUp(self) -> None:
        self.__repo = InMemoryRepository()
        client1 = Client('901', 'Matei', '2345678901234')
        client2 = Client('902', 'Luiza', '2344565567888')
        client3 = Client('903', 'Maria', '2394833929044')
        client4 = Client('904', 'Alina', '3330204934842')
        client5 = Client('905', 'Marian', '4994930304045')
        client6 = Client('906', 'Angela', '2948t67838348')
        client7 = Client('907', 'Vlad', '3499239299245')
        client8 = Client('908', 'Monalisa', '3949293994300')
        client9 = Client('909', 'Corina', '12359i3939278')
        client10 = Client('910', 'Bogdan', '2393249203023')


        self.__repo.store_client(client1)
        self.__repo.store_client(client2)
        self.__repo.store_client(client3)
        self.__repo.store_client(client4)
        self.__repo.store_client(client5)
        self.__repo.store_client(client6)
        self.__repo.store_client(client7)
        self.__repo.store_client(client8)
        self.__repo.store_client(client9)
        self.__repo.store_client(client10)


    def test_find_clienti(self):
        p = self.__repo.find_client('907')
        self.assertTrue(p.getNume() == 'Vlad')
        self.assertTrue(p.getCNP() == '3499239299245')

        p1 = self.__repo.find_client('207')
        self.assertTrue(p1 is None)

    def test_get_toti_clientii(self):
        clienti = self.__repo.get_toti_clientii()

        self.assertTrue(type(clienti) == list)
        self.assertTrue(len(clienti) == 10)

        self.__repo.delete_by_id_client('906')
        self.assertTrue(len(self.__repo.get_toti_clientii()) == 9)
        self.assertRaises(ValueError, self.__repo.delete_by_id_client, '304')
        client = Client('912', 'Marius', '2378459076542')
        self.__repo.store_client(client)
        self.assertTrue(self.__repo.get_toti_clientii()[-1].getNume() == 'Marius')
        self.assertTrue(self.__repo.get_toti_clientii()[-1].getCNP() == '2378459076542')
        self.assertTrue(len(self.__repo.get_toti_clientii()) == 10)

    def test_store_client(self):
        client1 = Client('912', 'Luiza', '2344565567880')
        self.__repo.store_client(client1)
        clienti = self.__repo.get_toti_clientii()
        self.assertTrue(len(clienti) == 11)
        client2 = Client('914', 'Alina', '3330204934822')
        self.__repo.store_client(client2)
        clienti = self.__repo.get_toti_clientii()
        self.assertTrue(len(clienti) == 12)
        client3 = Client('904', 'Cosmin', '3330204934852')
        self.assertRaises(RepositoryException, self.__repo.store_client, client3)

    def test_update_client(self):
        client1 = Client('908', 'Carmen', '4579246578001')
        # client8 = Client('908', 'Monalisa', '3949293994300')
        modified_client = self.__repo.update_client('908', client1)
        self.assertTrue(modified_client.getNume() == 'Carmen')
        self.assertTrue(modified_client.getCNP() == '4579246578001')

    def test_delete_by_id_client(self):
        deleted_client = self.__repo.delete_by_id_client('905')
        # client5 = Client('905', 'Marian', '4994930304045')
        self.assertTrue(deleted_client.getCNP() == '4994930304045')
        self.assertTrue(deleted_client.getNume() == 'Marian')
        self.assertRaises(ValueError, self.__repo.delete_by_id_client, '34fhw')
        self.assertRaises(ValueError, self.__repo.delete_by_id_client, '123')


class TestCaseClientRepoFile(unittest.TestCase):
       def setUp(self) -> None:
           self.__repo = ClientiFileRepo('test_clienti_repo.txt')

       def test_find_clienti(self):
           p = self.__repo.find_client('907')
           self.assertTrue(p.getNume() == 'Vlad')
           self.assertTrue(p.getCNP() == '3499239299245')

           p1 = self.__repo.find_client('207')
           self.assertTrue(p1 is None)

       def test_get_toti_clientii(self):
           clienti = self.__repo.get_toti_clientii()

           self.assertTrue(type(clienti) == list)
           self.assertRaises(ValueError, self.__repo.delete_by_id_client, '304')
           client = Client('912', 'Marius', '2378459076542')
           self.assertRaises(RepositoryException, self.__repo.store_client, client)
           self.assertTrue(self.__repo.get_toti_clientii()[-1].getNume() == 'Alina')
           self.assertTrue(self.__repo.get_toti_clientii()[-1].getCNP() == '3330204934822')

       def test_store_client(self):
           client1 = Client('922', 'Luiza', '2344565567880')
           #self.__repo.store_client(client1)
           clienti = self.__repo.get_toti_clientii()
           #self.assertTrue(len(clienti) == 11)
           client2 = Client('914', 'Alina', '3330204934822')
           #self.__repo.store_client(client2)
           clienti = self.__repo.get_toti_clientii()
           #self.assertTrue(len(clienti) == 12)
           client3 = Client('904', 'Cosmin', '3330204934852')
           #self.assertRaises(RepositoryException, self.__repo.store_client, client3)

       def tearDown(self) -> None:
           self.__repo = []



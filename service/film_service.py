import xmlrpc.client

from domain.entities import Film, Client, Inchiriere
from domain.validators import FilmValidator
from repository.film_repo import InMemoryRepository, RepositoryException
from domain.Exceptions import *

def comp_fun(el1, el2, key):
    '''
    Functia de comparare
    :param el1: element de comparat
    :param el2: celalalt element de comparat
    :param key:
    :return:
    '''
    return key(el1)[0] < key(el2)[0] and key(el1)[1] < key(el2)[1]

def bingoSort(list, n, reverse, comp_fun, key):
    '''
    Sorteaza lista de inchirieri
    :param list: lista de inchirieri
    :type list: List of Objects Inchiriere
    :param n: lungimea listei de inchirieri
    :return:
    '''
    bingo = list[0]
    nextBingo = list[0]
    bingo = min(list)
    nextBingo = max(list)
    largestEle = nextBingo
    nextElePos = 0
    while bingo < nextBingo:
        startPos = nextElePos
        for i in range (startPos, n):
            if comp_fun(list[i],bingo, key):
                aux = list[i]
                list[i] = list[nextElePos]
                list[nextElePos] = aux
                nextElePos += 1
            elif comp_fun(list[i], bingo, key):
                nextBingo = list[i]

        bingo = nextBingo
        nextBingo = largestEle


def merge(list1, l, r, m, comp_fun, key, reverse):
    '''
    Functia de merge sort
    :param list1: lista de inchirieri
    :type list1: list of objects Inchiriere
    :param l: left
    :type l: int
    :param r: right
    :type r: int
    :param m: middle
    :type m: int
    :param comp_fun: o functie lambda care ne sorteaza particularizat (dupa un criteriu)
    :type comp_fun: function
    :return:
    '''
    left_copy = list1[l:m + 1]
    r_sublist = list1[m + 1:r + 1]

    left_copy_index = 0
    r_sublist_index = 0
    sorted_index = l

    while left_copy_index < len(left_copy) and r_sublist_index < len(r_sublist):

        if comp_fun(left_copy[left_copy_index], r_sublist[r_sublist_index]):

                list1[sorted_index] = left_copy[left_copy_index]
                left_copy_index = left_copy_index + 1
        else:

                list1[sorted_index] = r_sublist[r_sublist_index]
                r_sublist_index = r_sublist_index + 1

        sorted_index = sorted_index + 1

    while left_copy_index < len(left_copy):
        list1[sorted_index] = left_copy[left_copy_index]
        left_copy_index = left_copy_index + 1
        sorted_index = sorted_index + 1

    while r_sublist_index < len(r_sublist):
        list1[sorted_index] = r_sublist[r_sublist_index]
        r_sublist_index = r_sublist_index + 1
        sorted_index = sorted_index + 1


def merge_sort(list1, l, r, comp_fun, key, reverse):
    if l >= r:
        return

    m = (l + r) // 2
    merge_sort(list1, l, m, comp_fun, key, reverse)
    merge_sort(list1, m + 1, r, comp_fun,key, reverse)
    merge(list1, l, r, m, comp_fun, key, reverse)

class Service:
    '''
    GRASP Controller
    Responsabil de efectuarea operatiilor cerute de utilizator
    Coordonareaza operatiile necesre pentru a realiza actiunea declansata de utilizator
    folosind alte obiecte (repo, validator) pentru a realiiza efectiv operatia
    '''

    def __init__(self, repo_film, repo_client, repo_inch, validator):
        '''
        Initializeaza service
        :param repo: obiect de tip repo care ne ajuta sa gestionam multimea de filme
        :type repo: FilmInMemoryRepository
        :param validator: validator pentru verificarea filmelor
        :type validator: FilmValidator
        '''

        self.__repo_film = repo_film
        self.__repo_client = repo_client
        self.__repo_inch = repo_inch
        self.__validator = validator

    def get_sorted_by_name(self):
        '''
        Returneaza inchirierile sortate dupa numele clientilor
        :return:lista de obiecte Inchiriere
        :rtype: list of Inchiere objects
        '''

        all_inchirieri = self.__repo_inch.get_all_inchirieri()
        #bingoSort(all_inchirieri, len(all_inchirieri), reverse = False, comp_fun=comp_fun, key = lambda x: (x.getClient.getNume(), x.getFilm().getTitlu()))
        merge_sort(all_inchirieri, 0, len(all_inchirieri) - 1, comp_fun=comp_fun, key = lambda x: (x.getClient.getNume(), x.getFilm().getTitlu()), reverse= False )
        return all_inchirieri

    def get_sorted_by_number(self):
        '''
        Returneaza inchirierile sortate dupa nr de filme inchiriate pentru fiecare client
        :return: dictionar cu nume si id-ul clientului si nr de film inchiriate
        :rtype: dict
        '''

        all_id_clienti_for_inchirieri = self.__repo_inch.get_all_id_clienti_for_inchirieri()
        d = {x: all_id_clienti_for_inchirieri.count(x) for x in all_id_clienti_for_inchirieri}

        merge_sort(list(d.items()), 0, len(list(d)) - 1, lambda x, y: x[1] > y[1], reverse = True)
        return d

    def get_sorted_by_inchirieri(self):
        '''
        Returneaza filmele sortate dupa nr de inchirieri
        :return: dictionar cu id-ul filmului si numarul de inchirieri
        :rtype: dict
        '''

        all_filme_inchiriate = self.__repo_inch.get_all_filme_for_inchirieri()

        d = {x: all_filme_inchiriate.count(x) for x in all_filme_inchiriate}

        merge_sort(list(d), 0, len(list(d)) - 1, lambda x,y: x[1] > y[1])
        return d
    def add_film(self, id, titlu, descriere, gen):
        '''
        Adauga film
        :param id: id-ul filmului
        :type id: str
        :param titlu: titlul filmului
        :type titlu: str
        :param descriere: descrierea filmului
        :type descriere: str
        :param gen: genul fimului
        :type gen: str
        :return: ValueError daca filmul are date invalide
        '''

        f = Film(id, titlu, descriere, gen)
        self.__validator.validateFilm(f)
        self.__repo_film.store_film(f)
        return f

    def add_client(self, id, nume, cnp):
        '''
        Adauga client

        :param id: id-ul clientului
        :type id: str
        :param nume: numele clientului
        :type nume: str
        :param cnp: cnp client
        :type cnp: str
        :return:
        '''

        c = Client(id, nume, cnp)

        self.__validator.validateClient(c)
        self.__repo_client.store_client(c)
        return c

    def get_toate_filmele(self):
        '''
        Returneaza lista cu toate filmele disponibile

        :return: lista de filme disponibile
        :rtype: list of objects de tip film
        '''

        return self.__repo_film.get_toate_filmele()

    def get_toti_clientii(self):
        '''
        Returneaza lista cu toti clientii disponibili

        :return: lista cu toti clientii disponibili
        :rtype: list of objects de tip clienti
        '''

        return self.__repo_client.get_toti_clientii()

    def delete_by_id_film(self, id):
        '''
        Sterge filmul cu id-ul respectiv
        :param id: id-ul dat
        :type id: str
        :return: filmul sters
        :rtype: Film
        :raises: ValueError daca nu exista serial cu id-ul dat
        '''
        return self.__repo_film.delete_by_id_film(id)

    def delete_by_id_client(self, id):
        '''
        Sterge clientul cu id-ul respectiv
        :param id: id-ul dat
        :type id: str
        :return: clientul sters
        :rtype: Client
        :raises: ValueError daca nu exista clientul cu id-ul dat
        '''

        return self.__repo_client.delete_by_id_client(id)

    def update_film(self, id, titlu, descriere, gen):
        '''
        Modifica filmul cu id-ul dat
        :param id: id-ul filmului de modificat
        :type id: str
        :param titlu: noul titlu al filmului
        :type titlu: str
        :param descriere: noua descriere a filmului
        :type descriere: str
        :param gen: noul gen al filmului
        :type gen: str
        :return: filmul modificat
        :rtype: Film
        :raises: ValueError daca noile date nu sunt valide sau daca nu exista film cu id dat
        '''

        f = Film(id, titlu, descriere, gen)

        self.__validator.validateFilm(f)
        return self.__repo_film.update_film(id, f)

    def update_client(self, id, nume, cnp):
        '''
        Modifica clientul cu id-ul dat
        :param id: id-ul clientului de modificat
        :type id: str
        :param nume: noul nume al clientului
        :type nume: str
        :param cnp: noul CNP al clientului
        :type cnp: str
        :return: clientul modificat
        :rtype: Client
        :raises: ValueError daca noile date nu sunt valide sau daca nu exista client cu id dat
        '''

        c = Client(id, nume, cnp)

        self.__validator.validateClient(c)
        return self.__repo_client.update_client(id, c)

    def find_film_by_id(self, id):
        '''
        Gaseste filmul cu id-ul dat
        :param id: id-ul de dat
        :type id: str
        :return: filmul cautat
        :rtype: Film
        '''
        return self.__repo_film.find_film_by_id(id)

    def find_client_by_id(self, id):
        '''
        Gaseste clientul cu id-ul dat
        :param id: id-ul de dat
        :tyoe id: str
        :return: clientul cautat
        :rtype: Client
        '''
        return self.__repo_client.find_client_by_id(id)

    def create_inchiriere(self, id_film, id_client, data):
        '''
        Creeaza o inchiriere
        :param id_film: id-ul show-ului inchiriat
        :type id_film: str
        :param id_client: id-ul clientului care inchiriaza
        :type id_client: str
        :param data: data inchirierii
        :type data: int
        :return: inchirierea creata
        :rtype: Inchiriere
        :raises: ValueError daca nu se poate realiza inchirierea (id-urile nu sunt valide
        sau nu se gasesc prin lista)
        '''

        film = self.find_film_by_id(id_film)
        if film is None:
            raise FilmNotFoundException()

        client = self.__repo_client.find_client_by_id(id_client)
        if client is None:
            raise ClientNotFoundException()

        inchiriere = Inchiriere(film, client, data)
        self.__validator.validateInchiriere(inchiriere)
        self.__repo_inch.store_inchiriere(inchiriere)
        return inchiriere

    def get_all(self):
        '''
        Returneaza toate inchirierile
        :return: list of Inchiriere objects
        '''

        return self.__repo_inch.get_all_inchirieri()

    def get_sorted_by_name_inchirieri(self):
        '''
        Returneaza inchirierile sortate dupa numele clientilor
        :return:lista de obiecte Inchiriere
        :rtype: list of Inchiere objects
        '''

        all_inchirieri = self.__repo_inch.get_all_inchirieri()
        inchirieri_sorted = sorted(sorted(all_inchirieri, key=lambda x: x.getFilm().getTitlu(), reverse=False), key = lambda x: x.getClient().getNume(), reverse=False)

        return inchirieri_sorted


    def get_sorted_by_number_inchirieri(self):
        '''
        Returneaza inchirierile sortate dupa nr de filme inchiriate pentru fiecare client
        :return: dictionar cu nume si id-ul clientului si nr de film inchiriate
        :rtype: dict
        '''

        all_id_clienti_for_inchirieri = self.__repo_inch.get_all_id_clienti_for_inchirieri()
        #i = ['apple', 'red', 'apple', 'red', 'red', 'pear']
        #d = {x: i.count(x) for x in i}
        #print d

        d = {x: all_id_clienti_for_inchirieri.count(x) for x in all_id_clienti_for_inchirieri}
        sorted_by_number_inchirieri = dict(sorted(d.items(), key = lambda x:x[1], reverse=True))

        return sorted_by_number_inchirieri

    def get_sorted_by_inchirieri_filme(self):
        '''
        Returneaza filmele sortate dupa nr de inchirieri
        :return: dictionar cu id-ul filmului si numarul de inchirieri
        :rtype: dict
        '''
        all_filme_inchiriate = self.__repo_inch.get_all_filme_for_inchirieri()

        d = {x: all_filme_inchiriate.count(x) for x in all_filme_inchiriate}
        sorted_all_filme_inchiriate = dict(sorted(sorted(d.items(), key = lambda x:x[0], reverse=False), key = lambda x:x[1], reverse = True))

        return sorted_all_filme_inchiriate

    def delete_inchiriere(self, id_film, id_client):
        '''
        Sterge inchirierea filmului dat de catre clientul dat
        :param id_film: id-ul filmului
        :type id_film: str
        :param id_client: id-ul clientului
        :return: inchirierea stearsa
        :rtype: ValueError daca nu exista aceasta inchiriere
        '''

        return self.__repo_inch.delete_inchiriere(id_film, id_client)

    def get_filme_inchiriate_by_client(self, id_client, n=3):
        '''
        Returneaza primele 3 filme inchiriate de un client dat
        :param id_client: id-ul clientului
        :type id_client: str
        :param n: numarul de filme de afisat (default 3)
        :type n: int
        :return: lista de obiecte DTO Inchiriere
        :rtype: list of Inchiriere objects
        '''

        client = self.__repo_inch.find_client_by_id(id_client)

        if client is None:
            raise ValueError("Clientul nu are inchirieri.")


        client_filme = self.__repo_inch.get_all_for_a_client(id_client)
        client_filme = client_filme[:n]

        return client_filme

'''def test_create_inchiriere():
    repo = InMemoryRepository()
    val = FilmValidator()
    #srv = Service(repo, val)
    film = srv.add_film("1", "The Star", "este un film frumos", "comedie")
    client = srv.add_client("1", "Maria", "1234567890123")
    inchiriere = srv.create_inchiriere('1', '1', 13)
    assert(inchiriere.getFilm() == repo.find_film('1'))
    assert(inchiriere.getClient() == repo.find_client('1'))
    assert(inchiriere.getData() == 13)

    try:
        srv.create_inchiriere('1', '1', 25)
        assert False
    except InchiriereaDejaExista:
        assert True

    try:
        srv.create_inchiriere('2', '1', 15)
        assert False
    except ValueError:
        assert True

    try:
        srv.create_inchiriere('1', '2', 10)
        assert False
    except ValueError:
        assert True

    try:
        srv.create_inchiriere('1', '1',  -2)
        assert False
    except ValueError:
        assert True


test_create_inchiriere()

def test_add_film():
    rep = InMemoryRepository()
    val = FilmValidator()
    srv = Service(rep, val)
    film = srv.add_film("1", "The Star", "este un film frumos", "comedie")
    assert film.getID() == '1'
    assert film.getTitlu() == 'The Star'
    film_list = srv.get_toate_filmele()
    assert len(film_list) == 1
    assert film_list[0] == film



test_add_film()

def test_add_client():
    rep = InMemoryRepository()
    val = FilmValidator()
    srv = Service(rep, val)
    client = srv.add_client("1", "Maria", "1234567890123")
    assert client.getID() == '1'
    assert client.getNume() == 'Maria'
    client_list = srv.get_toti_clientii()
    assert len(client_list) == 1
    assert client_list[0] == client

    try:
        client = srv.add_client("1", "Radu", "1234567890000")
        assert False
    except RepositoryException:
        assert True
test_add_client()

def test_delete_by_id_film():
    repo = InMemoryRepository()
    val = FilmValidator()
    srv = Service(repo, val)
    film = srv.add_film("1", "Deadpool", "este un film frumos", "actiune")
    deleted_film = srv.delete_by_id_film('1')

    assert (len(srv.get_toate_filmele()) == 0)
    assert (deleted_film.getTitlu() == 'Deadpool')
    assert (deleted_film.getGen() == 'actiune')
    assert (deleted_film.getDescriere() == 'este un film frumos')

    try:
        srv.delete_by_id_film('2')
        assert False
    except ValueError:
        assert True

test_delete_by_id_film()

def test_delete_by_id_client():
    repo = InMemoryRepository()
    val = FilmValidator()
    srv = Service(repo, val)
    client = srv.add_client("1", "Maria", "1234567890123")
    deleted_client = srv.delete_by_id_client('1')

    assert(len(srv.get_toti_clientii()) == 0)
    assert (deleted_client.getNume() == 'Maria')
    assert (deleted_client.getID() == '1')
    assert (deleted_client.getCNP() == '1234567890123')

    try:
        srv.delete_by_id_client('2')
        assert False
    except ValueError:
        assert True

test_delete_by_id_client()

def test_get_toate_filmele():
    repo = InMemoryRepository()
    validator = FilmValidator()
    test_srv = Service(repo, validator)

    test_srv.add_film('1', 'The Sea', 'este o comedie romantica', 'comedie')
    test_srv.add_film('2', 'The Master', 'este un film de actiune', 'actiune')
    assert(type(test_srv.get_toate_filmele()) == list)
    assert(len(test_srv.get_toate_filmele()) == 2)

test_get_toate_filmele()

def test_get_toti_clientii():
    repo = InMemoryRepository()
    validator = FilmValidator()
    test_srv = Service(repo, validator)
    test_srv.add_client("1", "Maria", "1234567890123")
    test_srv.add_client('902', 'Luiza', '2344565567888')
    test_srv.add_client('910', 'Bogdan', '2393249203023')
    assert(type(test_srv.get_toti_clientii()) == list)
    assert(len(test_srv.get_toti_clientii()) == 3)

test_get_toti_clientii()

def test_update_film():
    repo = InMemoryRepository()
    validator = FilmValidator()
    test_srv = Service(repo, validator)
    test_srv.add_film('1', 'The Sea', 'este o comedie romantica', 'comedie')
    updated_film = test_srv.update_film('1', 'See', 'este un film de mister', 'mister')

    assert(updated_film.getGen() == 'mister')
    assert(updated_film.getTitlu() == 'See')
    assert(updated_film.getDescriere() == 'este un film de mister')

    try:
        test_srv.update_film('34def', 'See', 'este un film de mister', 'mister')
        assert False
    except ValueError:
        assert True

test_update_film()

def test_update_client():
    repo = InMemoryRepository()
    validator = FilmValidator()
    test_srv = Service(repo, validator)
    test_srv.add_client('910', 'Bogdan', '2393249203023')
    updated_client = test_srv.update_client('910', "Maria", "1234567890123")
    assert (updated_client.getCNP() == '1234567890123')
    assert (updated_client.getNume() == 'Maria')

    try:
        test_srv.update_client('-2md4', 'Maria', '1234567890123')
        assert False
    except ValueError:
        assert True

test_update_client()

def test_add_inchiriere():
    repo = InMemoryRepository()
    validator = FilmValidator()
    test_srv = Service(repo, validator)
    test_srv.add_film('1', 'The Sea', 'este o comedie romantica', 'comedie')
    updated_film = test_srv.update_film('1', 'See', 'este un film de mister', 'mister')

    assert(updated_film.getGen() == 'mister')
    assert(updated_film.getTitlu() == 'See')
    assert(updated_film.getDescriere() == 'este un film de mister')

    try:
        test_srv.update_film('34def', 'See', 'este un film de mister', 'mister')
        assert False
    except ValueError:
        assert True

test_add_inchiriere()

def test_returnare_inchiriere():
    repo = InMemoryRepository()
    validator = FilmValidator()
    test_srv = Service(repo, validator)

    test_srv.add_film('1', 'The Sea', 'este o comedie romantica', 'comedie')
    test_srv.add_film('2', 'The Master', 'este un film de actiune', 'actiune')
    assert (type(test_srv.get_toate_filmele()) == list)
    assert (len(test_srv.get_toate_filmele()) == 2)

test_returnare_inchiriere()
'''
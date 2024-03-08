from domain.entities import Film, Client, Inchiriere
from domain.Exceptions import InchiriereaDejaExista, InchiriereNotFoundException, Exception

class RepositoryException(Exception):
    pass


class FilmFileRepo:
    def __init__(self, filename):
        self.__filename = filename

    def get_toate_filmele(self):
        '''
        Incarca datele din fisier
        :return: lista de filme din fisier
        :rtype: list of Film Objects
        '''
        try:
            f = open(self.__filename, 'r')
        except IOError:
            return
        lines = f.readlines()
        toate_filmele = []
        for line in lines:
            id, titlu, descriere, gen = [token.strip() for token in line.split(';')]

            film = Film(id, titlu, descriere, gen)
            toate_filmele.append(film)
        f.close()
        return toate_filmele

    def __save_to_file_film(self, toate_filmele):
        '''
        Salveaza filmele in fisier
        :return:
        '''
        with open(self.__filename, 'w') as f:
            for film in toate_filmele:
                film_string = str(film.getID() + ';' + str(film.getTitlu()) + ';' + str(film.getDescriere()) + ';' + str(film.getGen()) + '\n')
                f.write(film_string)

    def find_film(self, id):
        '''
        Cauta filmul cu id-ul dat
        :param id: id dat
        :type id: str
        :return: Filmul cu id-ul dat, None daca nu exista filmul cu id-ul dat
        :rtype: Film
        '''

        '''
        Complexitatea pentru aceasta functie:
        
        Cazul cel mai favorabil: id-ul cautat se afla pe prima pozitie(all_filme[0])- 1 repetitie
        T(n) = O(1)
        
        Cazul cel mai putin favorabil: id-ul cautat se afla pe ultima pozitie(all_filme[n-1]) - n-1 repetitii
        
        T(n) = O(n)
        
        Cazul mediu va fi executat de 0, 1, 2,..., n-1 ori
        T(1) = O(1)
        T(2) = O(2)
        T(3) = 0(3)
        ..........
        ..........
        
        ----------
        T(n) = (1 + 2 + ... + n-1)/n = n*(n-1)/n = O(n)
        
        OVERALL COMPLEXITY O(n)
        '''
        all_filme = self.get_toate_filmele()
        for film in all_filme:
            if film.getID() == id:
                return film
        return None

    def find_film_recursiv(self, id, crt_list):
        '''
        Gaseste filmul cu id dat, dar recursiv
        :param id: id dat
        :rtype id: str
        :return: id-ul filmului dat, None daca nu exista
        :rtype: int (>=0, <repo.size())
        '''
        if len(crt_list) ==0:
            return None
        if crt_list[0].getID() == id:
            return crt_list[0]
        crt_list = crt_list[1:]
        return self.find_film_recursiv(id, crt_list)



    def store_film(self, film):
        '''
        Adauga un film in lista
        :param film: filmul care se adauga
        :type film: Film
        :return: lista de filme se modifica prin adaugarea filmului dat
        :raises: RepositoryException daca filmul exista deja
        '''

        toate_filmele = self.get_toate_filmele()
        #print(toate_filmele)
        for fi in range(len(toate_filmele)):
            if film.getID() == toate_filmele[fi].getID():
                raise RepositoryException

        toate_filmele.append(film)
        self.__save_to_file_film(toate_filmele)

    def get_all_filme(self):
        '''
        Returneaza o lista cu toate filmele existente
        :return: list of objects de tip Film
        '''
        return self.get_toate_filmele()

    def delete_by_id_film(self, id):
        '''
        Sterge filmul dupa id
        :param id:id-ul dat
        :type id: str
        :return: filmul sters
        :raises: ValueError daca id-ul filmului nu se gaseste in lista
        '''

        film = self.find_film(id)
        toate_filmele = self.get_toate_filmele()
        if film is None:
            raise ValueError('Nu exista film cu acest id. ')

        toate_filmele.remove(film)
        self.__save_to_file_film(toate_filmele)
        return film

    def update_film(self, id, modified_film):
        '''
        Modifica datele filmului cu id dat
        :param id: id dat
        :type id: str
        :param modified_film: filmul cu datele noi
        :type modified_film: Film
        :return: filmul modificat
        :rtype: Film
        '''

        film = self.find_film(id)
        toate_filmele = self.get_toate_filmele()
        for i in range(len(toate_filmele)):
            if toate_filmele[i].getID() == id:
                index = i
        if film is None:
            raise ValueError('Nu exista film cu acest id.')

        film.setTitlu(modified_film.getTitlu())
        film.setDescriere(modified_film.getDescriere())
        film.setGen(modified_film.getGen())
        toate_filmele[index] = film
        self.__save_to_file_film(toate_filmele)
        return film

    def find_film_by_id(self, id):
        '''
        Gaseste filmul cu id-ul dat
        :param id: id-ul dat
        :type id: str
        :return: filmul cautat
        :rtype: Film
        :raises:ValueError daca nu exista film cu acest id
        '''

        film = self.find_film(id)
        if film is None:
            raise ValueError('Nu exista film cu acest id ')

        return film

    #clienti
class ClientiFileRepo:
    def __init__(self, filename):
        self.__filename = filename

    def get_toti_clientii(self):
        '''
        Incarca datele din fisier
        :return: lista de clienti din fisier
        :rtype: list of Client Objects
        '''
        try:
            f = open(self.__filename, 'r')
        except IOError:
            return
        lines = f.readlines()
        toti_clientii = []
        for line in lines:
            id, nume, cnp = [token.strip() for token in line.split(';')]

            client = Client(id, nume, cnp)
            toti_clientii.append(client)
        f.close()
        return toti_clientii

    def __save_to_file_client(self, toti_clientii):
        '''
        Salveaza clientii in fisier
        :return:
        '''
        with open(self.__filename, 'w') as f:
            for client in toti_clientii:
                client_string = str(client.getID() + ';' + str(client.getNume()) + ';' + str(client.getCNP()) + '\n')
                f.write(client_string)

    def find_client(self, id):
        '''
        Cauta clientul cu id-ul dat
        :param id: id dat
        :type id: str
        :return: Clientul cu id-ul dat, None daca nu exista clientul cu id-ul dat
        :rtype: Client
        '''


        all_clienti = self.get_toti_clientii()
        for client in all_clienti:
            if str(client.getID()) == str(id):
                return client
        return None

    def find_client_recursiv(self, id, crt_list):
        '''
        Gaseste filmul cu id dat, dar recursiv
        :param id: id dat
        :rtype id: str
        :return: id-ul filmului dat, None daca nu exista
        :rtype: int (>=0, <repo.size())
        '''
        if len(crt_list) == 0:
            return None
        if crt_list[0].getID() == id:
            return crt_list[0]
        crt_list = crt_list[1:]
        return self.find_client_recursiv(id, crt_list)

    def store_client(self, client):
        '''
        Adauga un client in lista
        :param film: clientul care se adauga
        :type film: Client
        :return: lista de clienti se modifica prin adaugarea clientului dat
        :raises: RepositoryException daca clientul exista deja
        '''

        all_clienti = self.get_toti_clientii()
        for cl in range(len(all_clienti)):
            if client.getID() == all_clienti[cl].getID():
                raise RepositoryException

        all_clienti.append(client)
        self.__save_to_file_client(all_clienti)

    def get_all_clienti(self):
        '''
        Returneaza o lista cu toti clientii existenti
        :return: list of objects de tip Client
        '''
        return self.get_toti_clientii()

    def delete_by_id_client(self, id):
        '''
        Sterge clientul dupa id
        :param id: id-ul dat
        :type id: str
        :return: clientul sters
        :raises: ValueError daca id-ul clientului nu se gaseste in lista
        '''

        client = self.find_client(id)
        toti_clientii = self.get_toti_clientii()
        if client is None:
            raise ValueError('Nu exista client cu acest id.')

        toti_clientii.remove(client)
        self.__save_to_file_client(toti_clientii)
        return client

    def update_client(self, id, modified_client):
        '''
        Modifica datele clientului cu id dat
        :param id: id-dat
        :type id: str
        :param modified_client: clientul cu datele noi
        :type modified_client: client
        :return: clientul modificat
        :rtype: Client
        '''

        client = self.find_client(id)
        toti_clientii = self.get_toti_clientii()
        for i in range(len(toti_clientii)):
            if toti_clientii[i].getID() == id:
                index = i

        if client is None:
            raise ValueError("Nu exista client cu acest id. ")

        client.setCNP(modified_client.getCNP())
        client.setNume(modified_client.getNume())
        toti_clientii[index] = client
        self.__save_to_file_client(toti_clientii)
        return client

    def find_client_by_id(self, id):
        '''
        Gaseste clientul cu id dat
        :param id: id-ul dat
        :type id: str
        :return: clientul cautat
        :rtype: Client
        :raises: ValueError daca nu exista client cu acest id
        '''

        client = self.find_client(id)
        if client is None:
            raise ValueError('Nu exista client cu acest id. ')
        return client


class InchiriereFileRepo:
    def __init__(self, filename):
        self.__filename = filename

    def get_all_inchirieri(self):
        '''
        Incarca datele din fisier
        :return: lista de inchirieri din fisier
        :rtype: list of Inchiriere Objects
        '''
        try:
            f = open(self.__filename, 'r')
        except IOError:
            return
        film_repo = FilmFileRepo('data/film.txt')
        client_repo = ClientiFileRepo('data/client.txt')
        lines = f.readlines()
        toate_inchirierile = []
        for line in lines:
            if line == "":
                return
            id_film, id_client, data = [token.strip() for token in line.split(';')]
            #print(id_film, id_client, data)
            film = film_repo.find_film(id_film)
            client = client_repo.find_client(id_client)
            inch = Inchiriere(film, client, data)
            toate_inchirierile.append(inch)

        f.close()
        return toate_inchirierile

    def find_inchiriere(self, inch):
        '''
        Cauta inchirierea in lista de inchirieri
        :param inch: inchirierea cautata
        :type inch: Inchiriere
        :return: inchirierea cautata daca exista in lista, None altfel
        :rtype: Inchiriere
        '''

        toate_inchirierile = self.get_all_inchirieri()
        for i in toate_inchirierile:
            if i == inch:
                return inch
        return None

    def __save_to_file_inchiriere(self, toate_inchirierile):
        '''
        Salveaza clientii in fisier
        :return:
        '''
        with open(self.__filename, 'w') as f:
            for inch in toate_inchirierile:
                inch_string = str(inch.getFilm().getID()) + ';' + str(inch.getClient().getID()) + ';' + str(inch.getData()) + '\n'
                f.write(inch_string)

    def store_inchiriere(self, inch):
        '''
        Adauga o inchiriere
        :param inch: inchirierea de adaugat
        :type inch: Inchiriere
        :return: se adauga inchirierea la lista de inchirieri
        :raises: InchiriereaDejaExista daca deja exista inchierere pentru filmul si clientul dat
        '''

        i = self.find_inchiriere(inch)
        toate_inchirierile = self.get_all_inchirieri()
        if i is not None:
            raise InchiriereaDejaExista()
        toate_inchirierile.append(inch)
        self.__save_to_file_inchiriere(toate_inchirierile)

    def find_inchiriere_by_ids(self, id_film, id_client):
        '''
        Gaseste inchirierea filmului dat facuta de clientul dat
        :param id_film: id film
        :type id_film: str
        :param id_client: id client
        :type id_client: str
        :return; inchirierea efectuata, None daca nu exista
        :rtype: Inchiriere
        '''
        toate_inchirierile = self.get_all_inchirieri()
        for inch in toate_inchirierile:
            if inch.getFilm().getID() == id_film and inch.getClient().getID() == id_client:
                return inch
        return None

    def delete_inchiriere(self, id_film, id_client):
        '''
        Sterge inchirierea care are filmul dat si este efectuata de clientul dat
        :param id_film: id film
        :type id_film: str
        :param id_client: id client
        :type id_client: str
        :return: inchirierea stearsa, ValueError daca nu s-a gasit inchirierea
        '''
        all_inchirieri = self.get_all_inchirieri()
        found_inchiriere = self.find_inchiriere_by_ids(id_film, id_client)

        if found_inchiriere is None:
            raise ValueError("Nu avem aceasta inchiriere")
        all_inchirieri.remove(found_inchiriere)
        self.__save_to_file_inchiriere(all_inchirieri)
        return found_inchiriere

    def get_all_for_client(self, client_id):
        '''
        Returneaza numar de inchirieri facute de un anumit client
        :param client_id: id client
        :type client_id: str
        :return: numarul de inchirieri facute de client
        :rtype: int
        '''
        no_inchirieri = 0
        all_inchirieri = self.get_all_inchirieri()

        for inch in all_inchirieri:
            if inch.getClient().getID() == client_id:
                no_inchirieri += no_inchirieri + 1

        return no_inchirieri

    def get_all_id_clienti_for_inchirieri(self):
        '''
        Returneaza toate id-urile clientilor care au efectuat vreodata inchirieri
        :return: id-urile clientilor care au efectuat inchirieri
        :rtype: list of strings(ids)
        '''
        all_id_clienti_for_inchirieri = []
        all_inchirieri = self.get_all_inchirieri()

        for inch in all_inchirieri:
            all_id_clienti_for_inchirieri.append(inch.getClient().getNume())

        return all_id_clienti_for_inchirieri

    def get_all_filme_for_inchirieri(self):
        '''
        Returneaza toate id-urile filmelor care au fost inchiriate vreodata
        :return: id-urile filmelor care au fost inchiriate
        :rtype: list of strings(ids)
        '''
        all_filme_for_inchirieri = []
        all_inchirieri = self.get_all_inchirieri()

        for inch in all_inchirieri:
            all_filme_for_inchirieri.append(inch.getFilm().getTitlu())

        return all_filme_for_inchirieri

    def get_all_for_a_client(self, id_client):
        '''
        Gaseste toate inchirierile aferente unui client dat
        :param id_client: id-ul clientului
        :type id_client: str
        :return: lista cu obiecte Inchiriere care contin informatiile necesare(id_film, id_client, data)
        :rtype: list of Inchiriere objects
        '''

        all_inchirieri = self.get_all_inchirieri()
        client_filme = []

        for inch in all_inchirieri:
            if inch.getClient().getID() == id_client:
                client_film = Inchiriere(inch.getFilm().getTitlu(), inch.getClient().getID(), inch.getData())
            client_filme.append(client_film)

        return client_filme



class InMemoryRepository:
    '''
    Clasa creata cu responsabilitatea de a gestiona multimea de filme si multimea de clienti
    '''

    def __init__(self):
        '''
        Multimea de filme pe care o gestionam
        Stocare intr-o lista in care ID-ul este unic
        film = [ID, titlu, descriere, gen]
        '''
        self.__filme = []
        self.__clienti = []
        self.__inchirieri = []

    def store_film(self, film):
        '''
        Adauga un film la lista de filme
        :param film: Filmul care se adauga
        :return: lista de filme se modifica prin adaugarea filmului dat
        return daca avem doua filme cu acelasi ID
        '''
        for f in range(len(self.__filme)):
            if film.getID() == self.__filme[f].getID():
                raise RepositoryException

        self.__filme.append(film)


    def store_client(self, client):
        '''
        Adauga un client la lista de clienti
        :param client: Clientul care se adauga
        :return: Listaa de clienti care se modifica prin adaugarea clientului dat
        '''

        for c in range(len(self.__clienti)):
            if client.getID() == self.__clienti[c].getID() or client.getCNP() == self.__clienti[c].getCNP() :
                raise RepositoryException

        self.__clienti.append(client)

    def get_toate_filmele(self):
        '''
        Returneaza o lista cu toate filmele existente
        :return:
        :rtype: list of objects de tip Film
        '''

        return list(self.__filme)

    def get_toti_clientii(self):
        '''
        Returneaza o lista cu toti clientii existentii
        :return:
        :rtype: list of objects de tip Client
        '''

        return self.__clienti

    def find_film(self, id):
        '''
        Gaseste filmul cu id dat
        :param id: id dat
        :rtype id: str
        :return: id-ul filmului dat, None daca nu exista
        :rtype: int (>=0, <repo.size())
        '''
        for film in self.__filme:
            if film.getID() == id:
                return film
        return None


    def delete_by_id_film(self, id):
        '''
        Sterge filmul dupa id
        :param id:id-ul dat
        :type id: str
        :return: filmul sters
        :raises: ValueError daca id-ul filmului nu se gaseste in lista
        '''
        film = self.find_film(id)
        if film is None:
            raise ValueError('Nu exista film cu acest id. ')

        self.__filme.remove(film)
        return film

    def find_client(self, id):
        '''
        Gaseste clientul cu id dat
        :param id: id dat
        :rtype id: str
        :return: id-ul in lista a clientului dat, None daca nu exista
        :rtype: int (>=0, <repo.size())
        '''
        for client in self.__clienti:
            if client.getID() == id:
                return client
        return None

    def delete_by_id_client(self, id):
        '''
        Sterge clientul dupa id
        :param id: id-ul clientului de sters
        :tyoe id: str
        :return: clientul sters
        :rtype: Client
        :raises: ValueError daca id-ul clientului nu se gaseste in lista
        '''

        client = self.find_client(id)
        if client is None:
            raise ValueError('Nu exista client cu acest id. ')
        self.__clienti.remove(client)
        return client

    def update_film(self, id, modified_film):
        '''
        Modifica datele filmului cu id dat
        :param id: id dat
        :type id: str
        :param modified_film: filmul cu datele noi
        :type modified_film: Film
        :return: filmul modificat
        :rtype: Film
        '''

        film = self.find_film(id)
        if film is None:
            raise ValueError('Nu exista film cu acest id.')

        film.setTitlu(modified_film.getTitlu())
        film.setDescriere(modified_film.getDescriere())
        film.setGen(modified_film.getGen())
        return film

    def update_client(self, id, modified_client):
        '''
        Modifica datele clientului cu id dat
        :param id: id dat
        :type id: str
        :param modified_client: clientul cu datele noi
        :type modified_client: Client
        :return: clientul modificat
        :rtype: Client
        '''

        client = self.find_client(id)
        if client is None:
            raise ValueError('Nu exista client cu acest id. ')

        client.setNume(modified_client.getNume())
        client.setCNP(modified_client.getCNP())
        return client

    def find_film_by_id(self, id):
        '''
        Gaseste filmul cu id-ul dat
        :param id: id-ul dat
        :type id: str
        :return: filmul cautat
        :rtype: Film
        :raises:ValueError daca nu exista film cu acest id
        '''

        film = self.find_film(id)
        if film is None:
            raise ValueError('Nu exista film cu acest id ')

        return film

    def find_client_by_id(self, id):
        '''
        Gaseste clietul cu id-ul dat
        :param id: id-ul dat
        :type id: str
        :return: clientul cautat
        :rtype: Client
        :raises: ValueError daca nu exista client cu acest id
        '''

        client = self.find_client(id)
        if client is None:
            raise ValueError('Nu exista client cu acest id ')

        return client

    def find_inchiriere(self, inch):
        '''
        Cauta inchirierea in lista de inchirieri
        :param inch: inchirierea cautata
        :type inch: Inchiriere
        :return: inchirierea cautata daca exista in lista, None altfel
        :rtype: Inchiriere
        '''

        for i in self.__inchirieri:
            if i == inch:
                return inch
        return None

    def store_inchiriere(self, inch):
        '''
        Adauga o inchiriere
        :param inch: inchirierea de adaugat
        :type inch: Inchiriere
        :return: se adauga inchirierea la lista de inchirieri
        :raises: InchiriereaDejaExista daca deja exista inchierere pentru filmul si clientul dat
        '''

        i = self.find_inchiriere(inch)
        if i is not None:
            raise InchiriereaDejaExista()
        self.__inchirieri.append(inch)

    def get_all_inchirieri(self):
        '''
        Returneaza o lista cu toate inchirierile facute
        :return: lista cu inchirierile facute
        :rtype: list of Inchiriere objects
        '''

        return self.__inchirieri

    def get_all_for_client(self, client_id):
        '''
        Returneaza numar de inchirieri facute de un anumit client
        :param client_id: id client
        :type client_id: str
        :return: numarul de inchirieri facute de client
        :rtype: int
        '''
        no_inchirieri = 0
        all_inchirieri = self.get_all_inchirieri()

        for inch in all_inchirieri:
            if inch.getClient().getID() == client_id:
                no_inchirieri += no_inchirieri + 1

        return no_inchirieri

    def get_all_id_clienti_for_inchirieri(self):
        '''
        Returneaza toate id-urile clientilor care au efectuat vreodata inchirieri
        :return: id-urile clientilor care au efectuat inchirieri
        :rtype: list of strings(ids)
        '''
        all_id_clienti_for_inchirieri = []
        all_inchirieri = self.get_all_inchirieri()

        for inch in all_inchirieri:
            all_id_clienti_for_inchirieri.append(inch.getClient().getNume())

        return all_id_clienti_for_inchirieri

    def get_all_filme_for_inchirieri(self):
        '''
        Returneaza toate id-urile filmelor care au fost inchiriate vreodata
        :return: id-urile filmelor care au fost inchiriate
        :rtype: list of strings(ids)
        '''
        all_filme_for_inchirieri = []
        all_inchirieri = self.get_all_inchirieri()

        for inch in all_inchirieri:
            all_filme_for_inchirieri.append(inch.getFilm().getTitlu())

        return all_filme_for_inchirieri

    def find_inchiriere_by_ids(self, id_film, id_client):
        '''
        Gaseste inchirierea filmului dat facuta de clientul dat
        :param id_film: id film
        :type id_film: str
        :param id_client: id client
        :type id_client: str
        :return; inchirierea efectuata, None daca nu exista
        :rtype: Inchiriere
        '''

        for inch in self.__inchirieri:
            if inch.getFilm().getID() == id_film and inch.getClient().getID() == id_client:
                return inch
        return None


    def delete_inchiriere(self, id_film, id_client):
        '''
        Sterge inchirierea care are filmul dat si este efectuata de clientul dat
        :param id_film: id film
        :type id_film: str
        :param id_client: id client
        :type id_client: str
        :return: inchirierea stearsa, ValueError daca nu s-a gasit inchirierea
        '''
        all_inchirieri = self.get_all_inchirieri()
        found_inchiriere = self.find_inchiriere_by_ids(id_film, id_client)

        if found_inchiriere is None:
            raise ValueError("Nu avem aceasta inchiriere")
        self.__inchirieri.remove(found_inchiriere)
        return found_inchiriere

    def get_all_for_a_client(self, id_client):
        '''
        Gaseste toate inchirierile aferente unui client dat
        :param id_client: id-ul clientului
        :type id_client: str
        :return: lista cu obiecte Inchiriere care contin informatiile necesare(id_film, id_client, data)
        :rtype: list of Inchiriere objects
        '''

        all_inchirieri = self.get_all_inchirieri()
        client_filme = []

        for inch in all_inchirieri:
            if inch.getClient().getID() == id_client:
                client_film = Inchiriere(inch.getFilm().getTitlu(), inch.getClient().getID(), inch.getData())
            client_filme.append(client_film)

        return client_filme

def test_get_all_for_a_client():
    film = Film('103', 'Modern Family', 'este un film', 'SF')
    client = Client('905', 'Marian', '4994930304045')

    inchiriere = Inchiriere(film, client, 20)

    test_repo = InMemoryRepository()
    test_repo.store_inchiriere(inchiriere)

    client_film = test_repo.get_all_for_a_client('103')
    assert (len(client_film) == 1)


def test_store_inchiriere():
    film = Film('103', 'Modern Family', 'este un film', 'SF')
    client = Client('905', 'Marian', '4994930304045')

    inchiriere = Inchiriere(film, client, 20)

    test_repo = InMemoryRepository()
    test_repo.store_inchiriere(inchiriere)

    assert (len(test_repo.get_all_inchirieri()) == 1)
    try:
        test_repo.store_inchiriere(inchiriere)
        assert False
    except InchiriereaDejaExista:
        assert True

test_store_inchiriere()

def setup_test_filme_repo():
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

    test_repo = InMemoryRepository()
    test_repo.store_film(film1)
    test_repo.store_film(film2)
    test_repo.store_film(film3)
    test_repo.store_film(film4)
    test_repo.store_film(film5)
    test_repo.store_film(film6)
    test_repo.store_film(film7)
    test_repo.store_film(film8)
    test_repo.store_film(film9)
    test_repo.store_film(film10)

    return test_repo

def setup_test_clienti_repo():
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

    test_repo = InMemoryRepository()
    test_repo.store_client(client1)
    test_repo.store_client(client2)
    test_repo.store_client(client3)
    test_repo.store_client(client4)
    test_repo.store_client(client5)
    test_repo.store_client(client6)
    test_repo.store_client(client7)
    test_repo.store_client(client8)
    test_repo.store_client(client9)
    test_repo.store_client(client10)


    return test_repo

def test_find_film():
    test_repo = setup_test_filme_repo()

    p = test_repo.find_film('105')
    assert(p.getTitlu() == 'See')
    assert(p.getDescriere() == 'este un film')
    assert(p.getGen() == 'mister')

    p1 = test_repo.find_film('1234')
    assert(p1 is None)

test_find_film()

def test_find_client():
    test_repo = setup_test_clienti_repo()

    p = test_repo.find_client('907')
    assert(p.getNume() == 'Vlad')
    assert(p.getCNP() == '3499239299245')

    p1 = test_repo.find_client('207')
    assert(p1 is None)

test_find_client()

def test_get_toate_filmele():
    test_repo = setup_test_filme_repo()
    filme = test_repo.get_toate_filmele()
    assert(type(filme) == list)
    assert(len(filme) == 10)

    test_repo.delete_by_id_film('107')
    test_repo.delete_by_id_film('101')

    filme = test_repo.get_toate_filmele()
    assert(len(filme) == 8)
    try:
        test_repo.delete_by_id_film('100')
        assert False
    except ValueError:
        assert True
    film = Film('111', 'The Crown', 'este un film despre o dinastie', 'actiune')
    test_repo.store_film(film)
    assert(test_repo.get_toate_filmele()[-1].getTitlu() == 'The Crown')
    assert(test_repo.get_toate_filmele()[-1].getGen() == 'actiune')


test_get_toate_filmele()

def test_get_toti_clientii():
    test_repo = setup_test_clienti_repo()
    clienti = test_repo.get_toti_clientii()

    assert(type(clienti) == list)
    assert(len(clienti) == 10)

    test_repo.delete_by_id_client('906')
    assert(len(test_repo.get_toti_clientii()) == 9)
    try:
        test_repo.delete_by_id_client('304')
        assert False
    except ValueError:
        assert True
    client = Client('912', 'Marius', '2378459076542')
    test_repo.store_client(client)
    assert(test_repo.get_toti_clientii()[-1].getNume() == 'Marius')
    assert(test_repo.get_toti_clientii()[-1].getCNP() == '2378459076542')
    assert(len(test_repo.get_toti_clientii()) == 10)

test_get_toti_clientii()

def test_store_film():
    test_repo = InMemoryRepository()
    film1 = Film('111', 'The Crown', 'este un film despre o dinastie', 'actiune')
    test_repo.store_film(film1)
    filme = test_repo.get_toate_filmele()
    assert (len(filme) == 1)
    film2 = Film('123', 'The X-Files', 'este un film de actiune', 'actiune')
    test_repo.store_film(film2)
    filme = test_repo.get_toate_filmele()
    assert (len(filme) == 2)



test_store_film()

def test_store_client():
    test_repo = InMemoryRepository()
    #client2 = Client('902', 'Luiza', '2344565567888')
    #client3 = Client('903', 'Maria', '2394833929044')
    #client4 = Client('904', 'Alina', '3330204934842')
    client1 = Client('902', 'Luiza', '2344565567888')
    test_repo.store_client(client1)
    clienti = test_repo.get_toti_clientii()
    assert(len(clienti) == 1)
    client2 = Client('904', 'Alina', '3330204934842')
    test_repo.store_client(client2)
    clienti = test_repo.get_toti_clientii()
    assert(len(clienti) == 2)
    try:
        client3 = Client('904', 'Cosmin', '3330204934842')
        test_repo.store_client(client3)
        assert False
    except RepositoryException:
        assert True

test_store_client()

def test_delete_by_id_film():
    test_repo = InMemoryRepository()
    film1 = Film('111', 'The Crown', 'este un film despre o dinastie', 'actiune')
    test_repo.store_film(film1)
    film2 = Film('123', 'The X-Files', 'este un film de actiune', 'actiune')
    test_repo.store_film(film2)

    deleted_film = test_repo.delete_by_id_film('123')
    assert (deleted_film.getTitlu() == 'The X-Files')
    assert (deleted_film.getDescriere() == 'este un film de actiune')
    assert (deleted_film.getGen() == 'actiune')

    try:
        test_repo.delete_by_id_film('234ff')
        assert False
    except ValueError:
        assert True

test_delete_by_id_film()

def test_delete_by_id_client():
    test_repo = setup_test_clienti_repo()
    deleted_client = test_repo.delete_by_id_client('905')
    #client5 = Client('905', 'Marian', '4994930304045')
    assert (deleted_client.getCNP() == '4994930304045')
    assert (deleted_client.getNume() == 'Marian')

    try:
        test_repo.delete_by_id_client('34fhw')
        assert False
    except ValueError:
        assert True

    try:
        test_repo.delete_by_id_client('123')
        assert False
    except ValueError:
        assert True

test_delete_by_id_client()

def test_update_film():
    test_repo = setup_test_filme_repo()
    film1 = Film('108', 'Kim', 'este un film cu mister', 'drama')
    modified_film = test_repo.update_film('108', film1)
    assert (modified_film.getTitlu() == 'Kim')
    assert (modified_film.getDescriere() == 'este un film cu mister')
    assert (modified_film.getGen() == 'drama')

    try:
        test_repo.update_film('2346', film1)
        assert False
    except ValueError:
        assert True

test_update_film()

def test_update_client():
    test_repo = setup_test_clienti_repo()
    client1 = Client('908', 'Carmen', '4579246578001')
    #client8 = Client('908', 'Monalisa', '3949293994300')
    modified_client = test_repo.update_client('908', client1)
    assert (modified_client.getNume() == 'Carmen')
    assert (modified_client.getCNP() == '4579246578001')

test_update_client()

def test_store_inchiriere():
    test_repo = setup_test_clienti_repo()
    deleted_client = test_repo.delete_by_id_client('905')
    # client5 = Client('905', 'Marian', '4994930304045')
    assert (deleted_client.getCNP() == '4994930304045')
    assert (deleted_client.getNume() == 'Marian')

    try:
        test_repo.delete_by_id_client('34fhw')
        assert False
    except ValueError:
        assert True

    try:
        test_repo.delete_by_id_client('123')
        assert False
    except ValueError:
        assert True

test_store_inchiriere()

import random
from domain.entities import Film, Client
from domain.validators import FilmValidator
from repository.film_repo import InMemoryRepository, RepositoryException
from service.film_service import Service
class Generari:
    #film1 = Film('101', 'Superstore', 'este un film', 'comedie')
    #film2 = Film('102', 'Arrow', 'este un film ', 'aciune')
    #film3 = Film('103', 'Modern Family', 'este un film', 'SF')
    #film4 = Film('104', 'Squid Game', 'este un film', 'aventura')
    #film5 = Film('105', 'See', 'este un film', 'mister')
    #film6 = Film('106', 'Atypical', 'este un film', 'drama')
    #film7 = Film('107', 'The X-Files', 'este un film', 'mister')
    #film8 = Film('108', 'The Star', 'este un film', 'romantic')
    #film9 = Film('109', 'Now you see me', 'este un film', 'mister')
    #film10 = Film('110', 'The Friend', 'este un film', 'comedie')
    def __init__(self, srv, repo):


        self.__id_list = ['101', '102', '103', '104', '105', '106', '107', '109', '110']
        self.__film_list = ['Superstore', 'Arrow', 'Modern Family', 'Squid Game', 'See', 'Atypical', 'The X-Files', 'The Star', 'Now you see me', 'The Friend']
        self.__descriere_list = ['este un film', 'este un film', 'este un film', 'este un film', 'este un film', 'este un film', 'este un film', 'este un film', 'este un film', 'este un film' ]
        self.__gen_list = ['comedie', 'actiune', 'SF', 'aventura', 'mister', 'drama', 'mister', 'romantic', 'mister', 'comedie']
        self.__srv = srv
        self.__repo = repo
        self.__id_list_client = ['902', '903', '904', '905', '906']
        self.__id_nume = ['Ana', 'George', 'Mihai', 'Sabina','Maria']
        self.__id_cnp = ['2345678901234', '2344565567888', '2394833929044', '3330204934842', '1234567890123']

    def get_id_list(self):
        return random.choice(self.__id_list)

    def get_film_list(self):
        return random.choice(self.__film_list)

    def get_descriere_list(self):
        return random.choice(self.__descriere_list)

    def get_gen_list(self):
        return random.choice(self.__gen_list)

    def generate_film(self):
        return Film(generare.get_id_list(), generare.get_film_list(), generare.get_descriere_list(), generare.get_gen_list() )

    def get_id(self):
        return random.choice(self.__id_list_client)

    def get_nume(self):
        return random.choice(self.__id_nume)
    def get_cnp(self):
        return random.choice(self.__id_cnp)
    def generate_client(self):
        return Client(self.get_id(), self.get_nume(), self.get_cnp())

    def generate_filme(self):
        optiune = int(input('Dati nr:'))
        for i in range (0, optiune):
            added_film = self.generate_film()
            print('Tiltul: ' + self.get_film_list() + ';  Gen: ' + self.get_gen_list())

    def generate_clienti(self):
        optiune = int(input('Dati nr:'))
        for i in range (0, optiune):
            added_client = self.generate_client()
            print('Nume: ' + self.get_nume() + '; CNP: ' + self.get_cnp())

#repo = InMemoryRepository()
#val =FilmValidator()

#srv = Service(repo, val)
#generare = Generari(srv, repo)
#print(generare.get_id_list(repo))

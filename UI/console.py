from domain.entities import Film, Client
from domain.validators import FilmValidator
from repository.film_repo import InMemoryRepository, RepositoryException, FilmFileRepo, ClientiFileRepo, InchiriereFileRepo
from service.film_service import Service





class Console:

    def __init__(self, srv, filename):
        '''
        Initializeaza consola
        :type srv: FilmeService
        :type filename: fisier
        '''

        self.__srv = srv
        self.__filename = filename

    def __showallClienti(self):
        '''
        Printeaza toti clientii din lista de clienti
        :return:
        '''

        clients = self.__srv.get_toti_clientii()
        if len(clients) == 0:
            print('Nu sunt clienti')
        else:
            print('Lista de clienti: ')
            for client in clients:
                print('ID: ', client.getID(),'; Nume client: ', client.getNume(),'; CNP client: ', client.getCNP())


    def __showallFilme(self):
        '''
        Printeaza toate filmele din lista de filme
        :return:
        '''

        films = self.__srv.get_toate_filmele()
        if len(films) == 0:
            print('Nu sunt filme')
        else:
            print("Lista de filme este: ")
            for film in films:
                print('ID: ', film.getID(),'; Titlu film: ', film.getTitlu(),'; Gen film: ', film.getGen())



    def __add_film(self):
        '''
        Adauga un film cu datele citite de la tastatura

        :return:
        '''
        try:
            id = input('Id-ul filmului: ')
            titlu = input('Titlul filmului: ')
            descriere = input('Descrierea filmului: ')
            gen = input('Genul fimului: ')
        except ValueError:
            print('Introduceti date valide!')
        try:
            added_film = self.__srv.add_film(id, titlu, descriere, gen)
            print(added_film.GetDisplay())
            print('Filmul ' + added_film.getTitlu() + ' (' + str(
                added_film.getGen()) + ') a fost adaugat cu succes.')
        except RepositoryException:
            print('Filme duplicate! ')
        except ValueError as ve:
            print(str(ve))

    def __add_client(self):
        '''
        Adauga clientul cu datele citite de la tastatura
        :return:
        '''
        try:
            id = input('Id-ul clientului: ')
            nume = input('Numele clientului: ')
            cnp = input('CNP-ul clientului: ')
        except ValueError:
            print('Introduceti date valide! ')

        try:
            added_client = self.__srv.add_client(id, nume, cnp)
            print('Clientul a fost adaugat cu succes')
        except RepositoryException as re:
            print('Clienti duplicati!')
        except ValueError as ve:
            print(str(ve))

    def __delete_by_id_film(self):
        id = input('ID-ul filmului de sters: ')
        try:
            deleted_film = self.__srv.delete_by_id_film(id)
            print('Filmul ' + deleted_film.getTitlu() + '(' + deleted_film.getGen() + ') a fost sters cu succes!')
        except ValueError as ve:
            print(ve)

    def __delete_by_id_client(self):
        id = input('ID-ul clientului de sters: ')
        try:
            deleted_client = self.__srv.delete_by_id_client(id)
            print('Clientul ' + deleted_client.getNume() + '(' + deleted_client.getID() + ') a fost sters cu succes!')
        except ValueError as ve:
            print(ve)


    def __update_film(self):
        try:
            id = input('Id-ul filmului: ')
            titlu = input('Titlul filmului: ')
            descriere = input('Descrierea filmului: ')
            gen = input('Genul fimului: ')
        except ValueError:
            print('Introduceti date valide!')
            return

        try:
            modified_film = self.__srv.update_film(id, titlu, descriere, gen)
            print('Filmul ' + modified_film.getTitlu() + '(' + modified_film.getGen() + ') a fost modificat cu succes!')
        except ValueError as ve:
            print(ve)

    def __update_client(self):
        try:
            id = input('Id-ul clientului: ')
            nume = input('Numele clientului: ')
            cnp = input('CNP-u; clientului: ')
        except ValueError:
            print('Introduceti date valide! ')
            return

        try:
            modified_client = self.__srv.update_client(id, nume, cnp)
            print('Clientul ' + modified_client.getNume() + '(' + modified_client.getID() + ') a fost modificat cu succes!' )
        except ValueError as ve:
            print(ve)

    def __find_film(self):
        try:
            id = input('Id-ul filmului ')
        except ValueError:
            print('Introduceti date valide! ')
            return

        try:
            found_film = self.__srv.find_film_by_id(id)
            print('Filmul ' + found_film.getTitlu() + '(' + found_film.getGen() + ') este filmul cautat. ')
        except ValueError as ve:
            print(ve)

    def __find_client(self):
        try:
            id = input('Id-ul filmului ')
        except ValueError:
            print('Introduceti date valide! ')
            return

        try:
            found_client = self.__srv.find_client_by_id(id)
            print('Clientul ' + found_client.getNume() + '(' + found_client.getID() + ') este clientul cautat. ')
        except ValueError as ve:
            print(ve)

    def __add_inchiriere(self):
        id_film = input('ID film: ')
        id_client = input('ID client: ')
        try:
            data = int(input('Data inchirierii: '))
            inchiriere = self.__srv.create_inchiriere(id_film, id_client, data)
            print('Inchirierea' , inchiriere, 'a fost facuta cu succes. ')
        except ValueError as ve:
            print(ve)

    def __get_sorted_by_name_inchirieri(self):
        sorted_inchirieri = self.__srv.get_sorted_by_name_inchirieri()
        for inchiriere in sorted_inchirieri:
            print('Nume client: ' + str(inchiriere.getClient().getNume()) + '; Titlu film: ' + str(inchiriere.getFilm().getTitlu()))

    def __get_sorted_by_number_inchirieri(self):
        sorted_by_number_inchirieri = self.__srv.get_sorted_by_number_inchirieri()
        for inch in sorted_by_number_inchirieri:
            print('Clientul ', inch, 'are ', sorted_by_number_inchirieri[inch], 'inchirieri. ')
        if len(sorted_by_number_inchirieri) == 0:
            print('Nu exista inchirieri.')

    def __get_sorted_by_inchirieri_filme(self):
        sorted_by_inchirieri_filme = self.__srv.get_sorted_by_inchirieri_filme()
        for inch in sorted_by_inchirieri_filme:
            print('Filmul ', inch, 'are ' , sorted_by_inchirieri_filme[inch], 'inchirieri')
        if len(sorted_by_inchirieri_filme) == 0:
            print('Nu exista inchirieri.')

        with open(self.__filename, 'w') as f:
            for inch in sorted_by_inchirieri_filme:
                inch_string = str('Filmul ') + str(inch) + str(' are ') + str(sorted_by_inchirieri_filme[inch]) + str(' inchirieri ') + '\n'
                f.write(inch_string)

    def __get_primii_30_clienti(self):
        sorted_by_primii = self.__srv.get_sorted_by_number_inchirieri()
        no_inch = 0
        n = int((len(sorted_by_primii)) * 0.3)
        for inch in sorted_by_primii:
            no_inch += 1
            print('Clientul', inch)
            if no_inch > n:
                break
        if n == 0:
            print('Nu putem afla primii 30% clienti. ')

    def __delete_inchiriere(self):
        id_film = input('Dati id-ul filmului inchiriat')
        try:
            id_client = input('Dati id-ul clientului care a inchiriat')
            deleted_inchiriere = self.__srv.delete_inchiriere(id_film, id_client)
            print('Nume client: ' + str(deleted_inchiriere.getClient().getNume()) + '; Titlu film: ' + str(deleted_inchiriere.getFilm().getTitlu()) + 'a returnata cu succes. ')
        except ValueError as ve:
            print(ve)

    def __get_filme_inchiriate_by_client(self):
        try:
            id_client = input('Dati id-ul clientului')
            filme_client = self.__srv.get_filme_inchiriate_by_client(id_client)
            for film in filme_client:
                print('Titlu film inchiriat: ', film.getFilm())
        except ValueError as ve:
            print (ve)
    def film_ui(self):

        while True:
            print('Comenzi disponibile: adaugare, vizualizare, sterge dupa id, modificare dupa id, cautare dupa id, generare, inchiriere, returnare, ordonare clienti dupa nume')
            print('ordonare clienti dupa filme, cele mai inchiriate filme, primii 30% clienti, primele 3 filme inchiriate de client')
            cmd = input('Comanda este: ')
            cmd = cmd.lower().strip()
            if cmd == 'adaugare':
                print('Adaugare film sau client: ')
                opt = input('Comanda este: ')
                opt = opt.lower().strip()
                if opt == 'film':
                    self.__add_film()
                elif opt == 'client':
                    self.__add_client()
                else:
                    print('Comanda invalida.')
            elif cmd == 'vizualizare':
                print('Vizualizare filme sau clienti: ')
                opt = input('Comanda este: ')
                opt = opt.lower().strip()
                if opt == 'filme':
                    self.__showallFilme()
                elif opt == 'clienti':
                    self.__showallClienti()
            elif cmd == 'sterge':
                print('Stergere film sau client dupa id: ')
                opt = input('Comanda este: ')
                opt = opt.lower().strip()
                if opt == 'film':
                    self.__delete_by_id_film()
                elif opt =='client':
                    self.__delete_by_id_client()
                else:
                    print('Comanda invalida. ')
            elif cmd == 'modificare':
                print('Modificare film sau client: ')
                opt = input('Comanda este: ')
                opt = opt.lower().strip()
                if opt == 'film':
                    self.__update_film()
                elif opt == 'client':
                    self.__update_client()
            elif cmd == 'cautare':
                print('Cautare film sau client: ')
                opt = input('Comanda este: ')
                opt = opt.lower().strip()
                if opt == 'film':
                    self.__find_film()
                elif opt == 'client':
                    self.__find_client()
            elif cmd == 'generare':
                generare.generate_filme()
                generare.generate_clienti()
            elif cmd == 'inchiriere':
                self.__add_inchiriere()
            elif cmd == 'returnare':
                self.__delete_inchiriere()
            elif cmd == 'ordonare clienti dupa nume':
                self.__get_sorted_by_name_inchirieri()
            elif cmd == 'ordonare clienti dupa filme':
                self.__get_sorted_by_number_inchirieri()
            elif cmd == 'cele mai inchiriate filme':
                self.__get_sorted_by_inchirieri_filme()
            elif cmd == 'primii 30% clienti':
                self.__get_primii_30_clienti()
            elif cmd == 'primele 3 filme inchiriate de client':
                self.__get_filme_inchiriate_by_client()

            else:
                print('Comanda invalida.')


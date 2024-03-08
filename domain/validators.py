from domain.entities import Film, Client, Inchiriere

class FilmValidator:
    def validateFilm(self, film):
        errors = []
        '''
        Ne dorim ca ID-urile filmelor sa contina doar cifre
        '''
        if len(film.getID()) < 1:
            errors.append('ID-ul filmului trebuie sa aiba cel putin o cifra')
        if film.isdigit() == False:
            errors.append('ID-ul filmului trebuie sa contina doar cifre')
        if len (film.getTitlu()) < 1:
            errors.append('Titlul filmului trebuie sa aiba cel putin 1 caracter')
        if len(film.getDescriere()) < 10:
            errors.append('Descrierea filmului trebuie sa aiba cel putin 10 caractere')

        '''
        Ne dorim ca genul filmului sa contina doar un cuvant format doar din litere alfabetice
        '''
        if len(film.getGen()) < 1:
            errors.append('Genul filmului trebuie sa aiba cel putin un caracter')
        if film.isalpha() == False:
            errors.append('Genul filmului trebuie sa contina doar litere')

        if len(errors) > 0:
            errors_string = '\n'.join(errors)
            raise ValueError(errors_string)

    def validateClient(self, client):
        errors = []

        if len(client.getID()) < 1:
            errors.append('ID-ul clientului trebuie sa aiba cel putin o cifra')
        if client.isdigitID() == False:
            errors.append('ID-ul clientului trebuie sa contina doar cifre')
        if len(client.getNume()) < 1:
            errors.append('Numele clientului trebuie sa contina cel putin un caracter')
        if client.isalphaNume() == False:
            errors.append('Numele clientului trebuie sa contina doar litere si/sau spatii')
        if client.isdigitCNP() == False:
            errors.append('CNP-ul clientului trebuie sa contina doar cifre')
        if len(client.getCNP()) != 13:
            errors.append('CNP-ul nu este valid. El trebuie sa contina 13 cifre')

        if len(errors) > 0:
            errors_string = '\n'.join(errors)
            raise ValueError(errors_string)

    def validateInchiriere(self, inchiriere):
        errors = []
        if inchiriere.getData() < 0 or inchiriere.getData() > 31:
            errors.append('Data inchirierii poate fi intre 1 si 31. ')

        if len(errors) > 0:
            raise ValueError(errors)




def test_validateFilm():
    validator = FilmValidator()
    f = Film("", "", "","")
    try:
        validator.validateFilm(f)
        assert False
    except  ValueError as ve:
        assert True

    f = Film('3', 'Midnight', 'este o actiune plina de suspans', 'actiune')
    try:
        validator.validateFilm(f)
        assert True
    except ValueError as ve:
        assert True

test_validateFilm()

def test_validateClient():
    validator = FilmValidator()
    c = Client("", "", "")
    try:
        validator.validateClient(c)
        assert False
    except ValueError as ve:
        assert True

    c = Client('2', 'Mihai', '1234567890123')
    try:
        validator.validateClient(c)
        assert True
    except ValueError:
        assert False

test_validateClient()

def test_validateInchiriere():
    validator = FilmValidator()
    film = Film(200, 'The Rain', 'este un film cu mister', 'SF')
    client = ('2', 'Stefan', '1234567890123')

    inchiriere = Inchiriere(film, client, 20)
    validator.validateInchiriere(inchiriere)

    inchiriere1 = Inchiriere(film, client, -2)
    try:
        validator.validateInchiriere(inchiriere1)
        assert False
    except ValueError:
        assert True

test_validateInchiriere()
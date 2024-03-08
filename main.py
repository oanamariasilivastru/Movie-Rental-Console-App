from domain.entities import Film, Client, Inchiriere
from domain.validators import FilmValidator
from repository.film_repo import InMemoryRepository, RepositoryException, FilmFileRepo, ClientiFileRepo, InchiriereFileRepo
from service.film_service import Service
from UI.console import Console
from UI.Nou_ui import  Generari

repo_film = FilmFileRepo('data/film.txt')
repo_client = ClientiFileRepo('data/client.txt')
repo_inch = InchiriereFileRepo('data/inchiriere.txt')
val = FilmValidator()
print('Pentru fisiere tastati fisiere. ')
print('\nPentru citire de la tastatura tastati orice. ')
cmd = input('Doriti cu fisiere sau citire de la tastatura? ')

if cmd == 'fisiere':
    srv = Service(repo_film, repo_client, repo_inch, val)

else:
    repo_film = InMemoryRepository()
    repo_client = InMemoryRepository()
    repo_inch = InMemoryRepository()
    srv = Service(repo_film, repo_client, repo_inch, val)
ui = Console(srv, 'data/raport.txt')
ui.film_ui()

class Exception(Exception):
    pass

class Validation(Exception):
    def __init__(self, msg):
        self.__msg = msg

    def getMessage(self):
        return self.__msg

class InchiriereaDejaExista(Exception):
    def __init__(self):
        Exception.__init__(self, "Inchiriere existenta pentru filmul si clientul dat.")

class FilmNotFoundException(Exception):
    def __init__(self):
        Exception.__init__(self, 'Filmul nu a fost gasit. ')

class ClientNotFoundException(Exception):
    def __init__(self):
       Exception.__init__(self, 'Clientul nu a fost gasit. ')

class InchiriereNotFoundException(Exception):
    def __init__(self):
        Exception.__init__(self, 'Inchirierea  nu a fost gasita. ')


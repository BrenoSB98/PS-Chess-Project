from model.peca import Peca

class Cavaleiro(Peca):

    def __init__(self, cor):
        super().__init__('cavaleiro', cor, 3.0)
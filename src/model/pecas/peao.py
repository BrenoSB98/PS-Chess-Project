
from model.peca import Peca

class Peao(Peca):

    def __init__(self, cor):
        self.dir = -1 if cor == 'white' else 1
        self.en_passant = False
        super().__init__('peao', cor, 1.0)
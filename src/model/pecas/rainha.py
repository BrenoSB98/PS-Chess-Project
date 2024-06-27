from model.peca import Peca

class Rainha(Peca):

    def __init__(self, cor):
        super().__init__('rainha', cor, 9.0)
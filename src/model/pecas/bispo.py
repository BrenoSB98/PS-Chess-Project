from model.peca import Peca

class Bispo(Peca):

    def __init__(self, cor):
        super().__init__('bispo', cor, 3.001)
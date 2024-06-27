from model.peca import Peca

class Rei(Peca):

    def __init__(self, cor):
        self.torre_esquerda = None
        self.torre_direita = None
        super().__init__('rei', cor, 10000.0)
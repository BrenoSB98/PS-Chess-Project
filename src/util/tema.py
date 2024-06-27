from util.cor import Cor

class Tema:

    def __init__(self, bg_claro, bg_escuro, traco_claro, traco_escuro,
                       movimentos_claro, movimentos_escuro):
        
        self.bg = Cor(bg_claro, bg_escuro)
        self.traco = Cor(traco_claro  , traco_escuro)
        self.movimentos = Cor(movimentos_claro, movimentos_escuro)
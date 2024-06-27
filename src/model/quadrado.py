
class Quadrado:

    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, linha, coluna, peca=None):
        self.linha = linha
        self.coluna = coluna
        self.peca = peca
        self.alphacol = self.ALPHACOLS[coluna]

    def __eq__(self, other):
        return self.linha == other.linha and self.coluna == other.coluna

    def tem_peca(self):
        return self.peca != None

    def esta_livre(self):
        return not self.tem_peca()

    def tem_peca_amiga(self, cor):
        return self.tem_peca() and self.peca.cor == cor

    def tem_peca_inimiga(self, cor):
        return self.tem_peca() and self.peca.cor != cor

    def esta_livre_ou_tem_inimigo(self, cor):
        return self.esta_livre() or self.tem_peca_inimiga(cor)

    @staticmethod
    def no_alcance(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    @staticmethod
    def get_alphacol(coluna):
        ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return ALPHACOLS[coluna]
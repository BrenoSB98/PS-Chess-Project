import os

class Peca:

    def __init__(self, nome, cor, valor, textura=None, textura_rect=None):
        self.nome = nome
        self.cor = cor
        valor_sign = 1 if cor == 'white' else -1
        self.valor = valor * valor_sign
        self.movimentos = []
        self.movido = False
        self.textura = textura
        self.set_textura()
        self.textura_rect = textura_rect

    def set_textura(self):
        self.textura = os.path.join(
            f'D:\\temp\\chess_project\\src\\assets\\imgs\\{self.cor}_{self.nome}.png')

    def adiciona_movimento(self, movimento):
        self.movimentos.append(movimento)

    def limpa_movimento(self):
        self.movimentos = []

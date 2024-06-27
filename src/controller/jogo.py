import pygame

from config.const import *
from model.tabuleiro import Tabuleiro
from controller.dragger import Dragger
from config.config import Config
from model.quadrado import Quadrado

class Jogo:

    def __init__(self):
        self.proximo_jogador = 'white'
        self.flutuar_sqr = None
        self.tabuleiro = Tabuleiro()
        self.dragger = Dragger()
        self.config = Config()

    def mostra_background(self, superficie):
        tema = self.config.temas
        
        for linha in range(ROWS):
            for coluna in range(COLS):
                cor = tema.bg.claro if (linha + coluna) % 2 == 0 else tema.bg.escuro
                
                rect = (coluna * SQSIZE, linha * SQSIZE, SQSIZE, SQSIZE)
                
                pygame.draw.rect(superficie, cor, rect)

                if coluna == 0:
                    cor = tema.bg.escuro if linha % 2 == 0 else tema.bg.claro
                    lbl = self.config.font.render(str(ROWS-linha), 1, cor)
                    lbl_pos = (5, 5 + linha * SQSIZE)
                    superficie.blit(lbl, lbl_pos)

                if linha == 7:
                    cor = tema.bg.escuro if (linha + coluna) % 2 == 0 else tema.bg.claro
                    lbl = self.config.font.render(Quadrado.get_alphacol(coluna), 1, cor)
                    lbl_pos = (coluna * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    superficie.blit(lbl, lbl_pos)

    def mostra_pecas(self, superficie):
        for linha in range(ROWS):
            for coluna in range(COLS):
                if self.tabuleiro.quadrados[linha][coluna].tem_peca():
                    peca = self.tabuleiro.quadrados[linha][coluna].peca
                    
                    if peca is not self.dragger.peca:
                        peca.set_textura()
                        img = pygame.image.load(peca.textura)
                        img_center = coluna * SQSIZE + SQSIZE // 2, linha * SQSIZE + SQSIZE // 2
                        peca.textura_rect = img.get_rect(center=img_center)
                        superficie.blit(img, peca.textura_rect)

    def mostra_movimentos(self, superficie):
        tema = self.config.temas

        if self.dragger.dragging:
            peca = self.dragger.peca

            for movimento in peca.movimentos:
                cor = tema.movimentos.claro if (movimento.final.linha + movimento.final.coluna) % 2 == 0 else tema.movimentos.escuro
                rect = (movimento.final.coluna * SQSIZE, movimento.final.linha * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(superficie, cor, rect)

    def mostra_ultimos_movimentos(self, superficie):
        tema = self.config.temas

        if self.tabuleiro.ultimo_movimento:
            initial = self.tabuleiro.ultimo_movimento.inicial
            final = self.tabuleiro.ultimo_movimento.final

            for posicao in [initial, final]:
                cor = tema.traco.claro if (posicao.linha + posicao.coluna) % 2 == 0 else tema.traco.escuro
                rect = (posicao.coluna * SQSIZE, posicao.linha * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(superficie, cor, rect)

    def mostra_passagem(self, superficie):
        if self.flutuar_sqr:
            cor = (180, 180, 180)
            rect = (self.flutuar_sqr.coluna * SQSIZE, self.flutuar_sqr.linha * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(superficie, cor, rect, width=3)

    def proximo_turno(self):
        self.proximo_jogador = 'white' if self.proximo_jogador == 'black' else 'black'

    def set_passagem(self, linha, coluna):
        self.flutuar_sqr = self.tabuleiro.quadrados[linha][coluna]

    def mostra_tema(self):
        self.config.temas

    def reset(self):
        self.__init__()
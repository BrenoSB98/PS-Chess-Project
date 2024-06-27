import pygame

from config.const import *

class Dragger:

    def __init__(self):
        self.peca = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.linha_inicial = 0
        self.coluna_inicial = 0

    def altera_blit(self, superficie):
        self.peca.set_textura()
        textura = self.peca.textura
        img = pygame.image.load(textura)
        img_center = (self.mouseX, self.mouseY)
        self.peca.textura_rect = img.get_rect(center=img_center)
        superficie.blit(img, self.peca.textura_rect)

    def altera_mouse(self, posicao):
        self.mouseX, self.mouseY = posicao

    def salva_inicio(self, posicao):
        self.linha_inicial = posicao[1] // SQSIZE
        self.coluna_inicial = posicao[0] // SQSIZE

    def mover_peca(self, peca):
        self.peca = peca
        self.dragging = True

    def desmover_peca(self):
        self.peca = None
        self.dragging = False

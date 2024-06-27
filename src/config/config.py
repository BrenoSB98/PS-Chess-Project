import pygame
import os

from util.tema import Tema

class Config:

    def __init__(self):
        self.temas = Tema((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 102, 128), '#C86464', '#C84646')
        self.font = pygame.font.SysFont('arial', 18, bold=True)

    def escolhe_tema(self):
        self.tema = self.temas
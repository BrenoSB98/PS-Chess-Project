import pygame
import sys
import os

from config.const import *
from controller.jogo import Jogo
from model.quadrado import Quadrado
from model.movimento import Movimento

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Xadrez')
        self.jogo = Jogo()

    def laco_principal(self):
        screen = self.screen
        jogo = self.jogo
        tabuleiro = self.jogo.tabuleiro
        dragger = self.jogo.dragger

        while True:
            jogo.mostra_background(screen)
            jogo.mostra_ultimos_movimentos(screen)
            jogo.mostra_movimentos(screen)
            jogo.mostra_pecas(screen)
            jogo.mostra_passagem(screen)

            if dragger.dragging:
                dragger.altera_blit(screen)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.altera_mouse(event.pos)
                    click_linha = dragger.mouseY // SQSIZE
                    click_coluna = dragger.mouseX // SQSIZE

                    if tabuleiro.quadrados[click_linha][click_coluna].tem_peca():
                        peca = tabuleiro.quadrados[click_linha][click_coluna].peca
                        if peca.cor == jogo.proximo_jogador:
                            tabuleiro.conta_movimentos(peca, click_linha, click_coluna, bool=True)
                            dragger.salva_inicio(event.pos)
                            dragger.mover_peca(peca)
                            
                            jogo.mostra_background(screen)
                            jogo.mostra_ultimos_movimentos(screen)
                            jogo.mostra_movimentos(screen)
                            jogo.mostra_pecas(screen)
            
                elif event.type == pygame.MOUSEMOTION:
                    linha_proposta = event.pos[1] // SQSIZE
                    coluna_proposta = event.pos[0] // SQSIZE

                    jogo.set_passagem(linha_proposta, coluna_proposta)

                    if dragger.dragging:
                        dragger.altera_mouse(event.pos)
                        
                        jogo.mostra_background(screen)
                        jogo.mostra_ultimos_movimentos(screen)
                        jogo.mostra_movimentos(screen)
                        jogo.mostra_pecas(screen)
                        jogo.mostra_passagem(screen)
                        dragger.altera_blit(screen)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.altera_mouse(event.pos)

                        linha_liberada = dragger.mouseY // SQSIZE
                        coluna_liberada = dragger.mouseX // SQSIZE

                        initial = Quadrado(dragger.linha_inicial, dragger.coluna_inicial)
                        final = Quadrado(linha_liberada, coluna_liberada)
                        movimento = Movimento(initial, final)

                        if tabuleiro.valida_movimento(dragger.peca, movimento):
                            capturada = tabuleiro.quadrados[linha_liberada][coluna_liberada].tem_peca()
                            tabuleiro.movimento(dragger.peca, movimento)
                            tabuleiro.set_verdadeiro_en_passant(dragger.peca)                            

                            jogo.mostra_background(screen)
                            jogo.mostra_ultimos_movimentos(screen)
                            jogo.mostra_pecas(screen)
                            jogo.proximo_turno()
                    
                    dragger.desmover_peca()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        jogo.mostra_tema()

                    if event.key == pygame.K_r:
                        jogo.reset()
                        jogo = self.jogo
                        tabuleiro = self.jogo.tabuleiro
                        dragger = self.jogo.dragger

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

main = Main()
main.laco_principal()
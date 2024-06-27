from config.const import *
from model.pecas.bispo import Bispo
from model.pecas.cavaleiro import Cavaleiro
from model.pecas.peao import Peao
from model.pecas.rainha import Rainha
from model.pecas.rei import Rei
from model.pecas.torre import Torre
from model.quadrado import Quadrado
from model.movimento import Movimento
import copy
import os

class Tabuleiro:

    def __init__(self):
        self.quadrados = [[0, 0, 0, 0, 0, 0, 0, 0] for coluna in range(COLS)]
        self.ultimo_movimento = None
        self._criar()
        self._adiciona_pecas('white')
        self._adiciona_pecas('black')

    def movimento(self, peca, movimento, test=False):
        inicial = movimento.inicial
        final = movimento.final

        en_passant_vulnerable_vazio = self.quadrados[final.linha][final.coluna].esta_livre()

        self.quadrados[inicial.linha][inicial.coluna].peca = None
        self.quadrados[final.linha][final.coluna].peca = peca

        if isinstance(peca, Peao):
            diff = final.coluna - inicial.coluna
            if diff != 0 and en_passant_vulnerable_vazio:
                self.quadrados[inicial.linha][inicial.coluna + diff].peca = None
                self.quadrados[final.linha][final.coluna].peca = peca
            else:
                self.verifica_promocao(peca, final)

        if isinstance(peca, Rei):
            if self.roque(inicial, final) and not test:
                diff = final.coluna - inicial.coluna
                torre = peca.torre_esquerda if (diff < 0) else peca.torre_direita
                self.movimento(torre, torre.movimentos[-1])

        peca.movido = True

        peca.limpa_movimento()

        self.ultimo_movimento = movimento

    def valida_movimento(self, peca, movimento):
        return movimento in peca.movimentos

    def verifica_promocao(self, peca, final):
        if final.linha == 0 or final.linha == 7:
            self.quadrados[final.linha][final.coluna].peca = Rainha(peca.cor)

    def roque(self, inicial, final):
        return abs(inicial.coluna - final.coluna) == 2

    def set_verdadeiro_en_passant(self, peca):
        
        if not isinstance(peca, Peao):
            return

        for linha in range(ROWS):
            for coluna in range(COLS):
                if isinstance(self.quadrados[linha][coluna].peca, Peao):
                    self.quadrados[linha][coluna].peca.en_passant = False
        
        peca.en_passant = True

    def em_xeque(self, peca, movimento):
        peca_temporaria = copy.deepcopy(peca)
        tabuleiro_temporario = copy.deepcopy(self)
        tabuleiro_temporario.movimento(peca_temporaria, movimento, test=True)
        
        for linha in range(ROWS):
            for coluna in range(COLS):
                if tabuleiro_temporario.quadrados[linha][coluna].tem_peca_inimiga(peca.cor):
                    p = tabuleiro_temporario.quadrados[linha][coluna].peca
                    tabuleiro_temporario.conta_movimentos(p, linha, coluna, bool=False)
                    for m in p.movimentos:
                        if isinstance(m.final.peca, Rei):
                            return True
        
        return False

    def conta_movimentos(self, peca, linha, coluna, bool=True):
        
        def movimentos_peao():
            steps = 1 if peca.movido else 2

            # vertical moves
            inicio = linha + peca.dir
            fim = linha + (peca.dir * (1 + steps))
            for possivel_linha_movimentos in range(inicio, fim, peca.dir):
                if Quadrado.no_alcance(possivel_linha_movimentos):
                    if self.quadrados[possivel_linha_movimentos][coluna].esta_livre():
                        inicial = Quadrado(linha, coluna)
                        final = Quadrado(possivel_linha_movimentos, coluna)
                        movimento = Movimento(inicial, final)

                        if bool:
                            if not self.em_xeque(peca, movimento):
                                peca.adiciona_movimento(movimento)
                        else:
                            peca.adiciona_movimento(movimento)
                    else: break
                else: break

            possivel_linha_movimentos = linha + peca.dir
            possivel_coluna_movimentos = [coluna-1, coluna+1]
            for possivel_coluna_movimento in possivel_coluna_movimentos:
                if Quadrado.no_alcance(possivel_linha_movimentos, possivel_coluna_movimento):
                    if self.quadrados[possivel_linha_movimentos][possivel_coluna_movimento].tem_peca_inimiga(peca.cor):
                        inicial = Quadrado(linha, coluna)
                        peca_final = self.quadrados[possivel_linha_movimentos][possivel_coluna_movimento].peca
                        final = Quadrado(possivel_linha_movimentos, possivel_coluna_movimento, peca_final)
                        movimento = Movimento(inicial, final)
                        
                        if bool:
                            if not self.em_xeque(peca, movimento):
                                peca.adiciona_movimento(movimento)
                        else:
                            peca.adiciona_movimento(movimento)

            r = 3 if peca.cor == 'white' else 4
            fr = 2 if peca.cor == 'white' else 5
            
            if Quadrado.no_alcance(coluna-1) and linha == r:
                if self.quadrados[linha][coluna-1].tem_peca_inimiga(peca.cor):
                    p = self.quadrados[linha][coluna-1].peca
                    if isinstance(p, Peao):
                        if p.en_passant:
                            inicial = Quadrado(linha, coluna)
                            final = Quadrado(fr, coluna-1, p)
                            
                            movimento = Movimento(inicial, final)
                            
                            if bool:
                                if not self.em_xeque(peca, movimento):
                                    peca.adiciona_movimento(movimento)
                            else:
                                peca.adiciona_movimento(movimento)
            
            if Quadrado.no_alcance(coluna+1) and linha == r:
                if self.quadrados[linha][coluna+1].tem_peca_inimiga(peca.cor):
                    p = self.quadrados[linha][coluna+1].peca
                    if isinstance(p, Peao):
                        if p.en_passant:
                            inicial = Quadrado(linha, coluna)
                            final = Quadrado(fr, coluna+1, p)
                            movimento = Movimento(inicial, final)
                            
                            if bool:
                                if not self.em_xeque(peca, movimento):
                                    peca.adiciona_movimento(movimento)
                            else:
                                peca.adiciona_movimento(movimento)

        def cavaleiro_movimentos():
            possiveis_movimentos = [
                (linha-2, coluna+1),
                (linha-1, coluna+2),
                (linha+1, coluna+2),
                (linha+2, coluna+1),
                (linha+2, coluna-1),
                (linha+1, coluna-2),
                (linha-1, coluna-2),
                (linha-2, coluna-1),
            ]

            for possiveis_movimento in possiveis_movimentos:
                possivel_linha_movimentos, possivel_coluna_movimento = possiveis_movimento

                if Quadrado.no_alcance(possivel_linha_movimentos, possivel_coluna_movimento):
                    if self.quadrados[possivel_linha_movimentos][possivel_coluna_movimento].esta_livre_ou_tem_inimigo(peca.cor):
                        # create quadrados of the new movimento
                        inicial = Quadrado(linha, coluna)
                        peca_final = self.quadrados[possivel_linha_movimentos][possivel_coluna_movimento].peca
                        final = Quadrado(possivel_linha_movimentos, possivel_coluna_movimento, peca_final)
                        movimento = Movimento(inicial, final)
                        
                        if bool:
                            if not self.em_xeque(peca, movimento):
                                peca.adiciona_movimento(movimento)
                            else: break
                        else:
                            peca.adiciona_movimento(movimento)

        def movimentos_em_linha_reta(incrs):
            for incr in incrs:
                linha_incr, coluna_incr = incr
                possivel_linha_movimentos = linha + linha_incr
                possivel_coluna_movimento = coluna + coluna_incr

                while True:
                    if Quadrado.no_alcance(possivel_linha_movimentos, possivel_coluna_movimento):
                        inicial = Quadrado(linha, coluna)
                        peca_final = self.quadrados[possivel_linha_movimentos][possivel_coluna_movimento].peca
                        final = Quadrado(possivel_linha_movimentos, possivel_coluna_movimento, peca_final)
                        movimento = Movimento(inicial, final)

                        if self.quadrados[possivel_linha_movimentos][possivel_coluna_movimento].esta_livre():
                            if bool:
                                if not self.em_xeque(peca, movimento):
                                    peca.adiciona_movimento(movimento)
                            else:
                                peca.adiciona_movimento(movimento)

                        elif self.quadrados[possivel_linha_movimentos][possivel_coluna_movimento].tem_peca_inimiga(peca.cor):
                            if bool:
                                if not self.em_xeque(peca, movimento):
                                    peca.adiciona_movimento(movimento)
                            else:
                                peca.adiciona_movimento(movimento)
                            break

                        elif self.quadrados[possivel_linha_movimentos][possivel_coluna_movimento].tem_peca_amiga(peca.cor):
                            break
                    
                    else: break

                    possivel_linha_movimentos = possivel_linha_movimentos + linha_incr
                    possivel_coluna_movimento = possivel_coluna_movimento + coluna_incr

        def movimentos_rei():
            adjs = [
                (linha-1, coluna+0), # up
                (linha-1, coluna+1), # up-right
                (linha+0, coluna+1), # right
                (linha+1, coluna+1), # down-right
                (linha+1, coluna+0), # down
                (linha+1, coluna-1), # down-left
                (linha+0, coluna-1), # left
                (linha-1, coluna-1), # up-left
            ]

            for possiveis_movimento in adjs:
                possivel_linha_movimentos, possivel_coluna_movimento = possiveis_movimento

                if Quadrado.no_alcance(possivel_linha_movimentos, possivel_coluna_movimento):
                    if self.quadrados[possivel_linha_movimentos][possivel_coluna_movimento].esta_livre_ou_tem_inimigo(peca.cor):
                        inicial = Quadrado(linha, coluna)
                        final = Quadrado(possivel_linha_movimentos, possivel_coluna_movimento)
                        movimento = Movimento(inicial, final)
                        if bool:
                            if not self.em_xeque(peca, movimento):
                                peca.adiciona_movimento(movimento)
                            else: break
                        else:
                            peca.adiciona_movimento(movimento)

            if not peca.movido:
                torre_esquerda = self.quadrados[linha][0].peca
                if isinstance(torre_esquerda, Torre):
                    if not torre_esquerda.movido:
                        for c in range(1, 4):
                            if self.quadrados[linha][c].tem_peca():
                                break

                            if c == 3:
                                peca.torre_esquerda = torre_esquerda

                                inicial = Quadrado(linha, 0)
                                final = Quadrado(linha, 3)
                                movimentoT = Movimento(inicial, final)

                                inicial = Quadrado(linha, coluna)
                                final = Quadrado(linha, 2)
                                movimentoR = Movimento(inicial, final)

                                if bool:
                                    if not self.em_xeque(peca, movimentoR) and not self.em_xeque(torre_esquerda, movimentoT):
                                        torre_esquerda.adiciona_movimento(movimentoT)
                                        peca.adiciona_movimento(movimentoR)
                                else:
                                    torre_esquerda.adiciona_movimento(movimentoT)
                                    peca.adiciona_movimento(movimentoR)

                torre_direita = self.quadrados[linha][7].peca
                if isinstance(torre_direita, Torre):
                    if not torre_direita.movido:
                        for c in range(5, 7):
                            if self.quadrados[linha][c].tem_peca():
                                break

                            if c == 6:
                                peca.torre_direita = torre_direita

                                inicial = Quadrado(linha, 7)
                                final = Quadrado(linha, 5)
                                movimentoT = Movimento(inicial, final)

                                inicial = Quadrado(linha, coluna)
                                final = Quadrado(linha, 6)
                                movimentoR = Movimento(inicial, final)

                                if bool:
                                    if not self.em_xeque(peca, movimentoR) and not self.em_xeque(torre_direita, movimentoT):
                                        torre_direita.adiciona_movimento(movimentoT)
                                        peca.adiciona_movimento(movimentoR)
                                else:
                                    torre_direita.adiciona_movimento(movimentoT)
                                    peca.adiciona_movimento(movimentoR)

        if isinstance(peca, Peao): 
            movimentos_peao()

        elif isinstance(peca, Cavaleiro): 
            cavaleiro_movimentos()

        elif isinstance(peca, Bispo): 
            movimentos_em_linha_reta([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left
            ])

        elif isinstance(peca, Torre): 
            movimentos_em_linha_reta([
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1), # left
            ])

        elif isinstance(peca, Rainha): 
            movimentos_em_linha_reta([
                (-1, 1), # up-right
                (-1, -1), # up-left
                (1, 1), # down-right
                (1, -1), # down-left
                (-1, 0), # up
                (0, 1), # right
                (1, 0), # down
                (0, -1) # left
            ])

        elif isinstance(peca, Rei): 
            movimentos_rei()

    def _criar(self):
        for linha in range(ROWS):
            for coluna in range(COLS):
                self.quadrados[linha][coluna] = Quadrado(linha, coluna)

    def _adiciona_pecas(self, cor):
        linha_peao, outra_linha = (6, 7) if cor == 'white' else (1, 0)

        for coluna in range(COLS):
            self.quadrados[linha_peao][coluna] = Quadrado(linha_peao, coluna, Peao(cor))

        self.quadrados[outra_linha][1] = Quadrado(outra_linha, 1, Cavaleiro(cor))
        self.quadrados[outra_linha][6] = Quadrado(outra_linha, 6, Cavaleiro(cor))

        self.quadrados[outra_linha][2] = Quadrado(outra_linha, 2, Bispo(cor))
        self.quadrados[outra_linha][5] = Quadrado(outra_linha, 5, Bispo(cor))

        self.quadrados[outra_linha][0] = Quadrado(outra_linha, 0, Torre(cor))
        self.quadrados[outra_linha][7] = Quadrado(outra_linha, 7, Torre(cor))

        self.quadrados[outra_linha][3] = Quadrado(outra_linha, 3, Rainha(cor))

        self.quadrados[outra_linha][4] = Quadrado(outra_linha, 4, Rei(cor))
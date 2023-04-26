import pygame
from pygame.locals import *
from vetor import Vetor2
from constantes import *
from random import randint

class Andarilhos(object):
    def __init__(self, no):
        self.name = None
        self.direcoes = {CIMA: Vetor2(0, -1), BAIXO: Vetor2(0, 1),
                         ESQUERDA: Vetor2(-1, 0), DIREITA: Vetor2(1, 0), PARADO: Vetor2()}
        self.direcao = PARADO
        self.defineVelocidade(100)
        self.raio = 10
        self.raio_colisao = 5
        self.cor = BRANCO
        self.no = no
        self.definePosicao()
        self.alvo = no
        self.visivel = True

    def definePosicao(self):
        self.posicao = self.no.posicao.copia()

    def direcaoValida(self, direcao):
        if direcao is not PARADO:
            if self.no.vizinhos[direcao] is not None:
                return True
        return False

    def pegaNovoAlvo(self, direcao):
        if self.direcaoValida(direcao):
            return self.no.vizinhos[direcao]
        return self.no

    def ultrapassouAlvo(self):
        if self.alvo is not None:
            vec1 = self.alvo.posicao - self.no.posicao
            vec2 = self.posicao - self.no.posicao
            no2alvo = vec1.distanciaQuadrado()
            no2self = vec2.distanciaQuadrado()
            return no2self >= no2alvo
        return False

    def direcaoReversa(self):
        self.direcao *= -1
        temp = self.no
        self.no = self.alvo
        self.alvo = temp

    def direcaoOposta(self, direcao):
        if direcao is not PARADO:
            if direcao == self.direcao * -1:
                return True
        return False

    def defineVelocidade(self, velocidade):
        self.velocidade = velocidade * LARGURA_NO / 16

    def desenha(self, tela):
        if self.visivel:
            p = self.posicao.intTupla()
            pygame.draw.circle(tela, self.cor, p, self.raio)

    def direcoesValidas(self):
        direcoes = []
        for chave in [CIMA, BAIXO, ESQUERDA, DIREITA]:
            if self.direcaoValida(chave):
                if chave != self.direcao * -1:
                    direcoes.append(chave)
        if len(direcoes) == 0:
            direcoes.append(self.direcao * -1)
        return direcoes

    def direcaoAleatoria(self, direcoes):
        return direcoes[randint(0, len(direcoes) - 1)]

    def update(self, dt):
        self.posicao += self.direcoes[self.direcao] * self.velocidade * dt

        if self.ultrapassouAlvo():
            self.node = self.alvo
            direcoes = self.direcoesValidas()
            direcao = self.direcaoAleatoria(direcoes)
            self.target = self.pegaNovoAlvo(direcao)
            if self.target is not self.node:
                self.direcao = direcao
            else:
                self.alvo = self.pegaNovoAlvo(self.direcao)

            self.definePosicao()
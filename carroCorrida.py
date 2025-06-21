import pygame
import random
import sys

# Inicializa o pygame
pygame.init()

# Constantes da tela
LARGURA = 400
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Corrida Sinuosa")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (100, 100, 100)
VERDE = (0, 200, 0)
VERMELHO = (200, 0, 0)

# Relógio
clock = pygame.time.Clock()
FPS = 60

# Variáveis do jogo
carro_largura = 40
carro_altura = 60
faixa_largura = 200
velocidade = 5


def tela_inicio():
    fonte = pygame.font.SysFont(None, 40)
    rodando = True
    while rodando:
        TELA.fill(BRANCO)
        texto = fonte.render("Aperte qualquer tecla para começar", True, PRETO)
        TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                rodando = False


def tela_fim():
    fonte = pygame.font.SysFont(None, 50)
    texto = fonte.render("Você bateu! Fim de jogo!", True, VERMELHO)
    TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def jogo():
    carro_x = LARGURA // 2 - carro_largura // 2
    carro_y = ALTURA - carro_altura - 20
    pista_curva = 0
    rodando = True

    while rodando:
        clock.tick(FPS)
        TELA.fill(BRANCO)

        # Curva da pista
        pista_curva += random.choice([-1, 0, 1])
        pista_curva = max(-40, min(40, pista_curva))
        pista_x = LARGURA // 2 - faixa_largura // 2 + pista_curva

        # Evento
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimento do carro
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            carro_x -= velocidade
        if teclas[pygame.K_RIGHT]:
            carro_x += velocidade

        # Desenha pista
        pygame.draw.rect(TELA, CINZA, (pista_x, 0, faixa_largura, ALTURA))
        pygame.draw.rect(TELA, VERDE, (0, 0, pista_x, ALTURA))
        pygame.draw.rect(TELA, VERDE, (pista_x + faixa_largura, 0, LARGURA - pista_x - faixa_largura, ALTURA))

        # Desenha carro
        carro = pygame.Rect(carro_x, carro_y, carro_largura, carro_altura)
        pygame.draw.rect(TELA, PRETO, carro)

        # Colisão
        if carro_x < pista_x or carro_x + carro_largura > pista_x + faixa_largura:
            tela_fim()
            rodando = False

        pygame.display.update()


# Executa o jogo
tela_inicio()
jogo()


      
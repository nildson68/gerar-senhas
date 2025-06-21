import pygame
import sys

# Inicializar pygame
pygame.init()

# Constantes
LARGURA, ALTURA = 800, 600
FPS = 60

# Cores
COR_FUNDO = (255, 255, 255)  # branco puro
COR_TEXTO = (107, 114, 128)  # cinza neutro
COR_TITULO = (31, 41, 55)    # cinza escuro quase preto
COR_CARD_BG = (249, 250, 251)  # fundo claro para as áreas das peças
COR_BORDA = (229, 231, 235)    # borda clara
COR_SOMBRA = (200, 200, 200)

# Fontes
FONT_TITULO = pygame.font.SysFont("Poppins", 48, bold=True)
FONT_TEXTO = pygame.font.SysFont("Poppins", 24)
FONT_PEQUENO = pygame.font.SysFont("Poppins", 18)

# Setup tela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Encaixe de Figuras Geométricas - Jogo Infantil")
clock = pygame.time.Clock()

# Classe para figura geométrica
class Figura:
    def __init__(self, forma, cor, pos, tamanho, encaixe_pos):
        """
        forma: 'circulo', 'quadrado', 'triangulo'
        cor: tupla RGB
        pos: posição inicial (x,y) da figura (onde o usuário pode arrastar)
        tamanho: tamanho da figura (raio para círculo, lado para quadrado/triângulo)
        encaixe_pos: posição (x,y) onde a figura deve ser encaixada
        """
        self.forma = forma
        self.cor = cor
        self.pos = list(pos)
        self.tamanho = tamanho
        self.encaixe_pos = encaixe_pos
        self.arrastando = False
        self.offset_x = 0
        self.offset_y = 0
        self.encaixada = False

    def draw(self, superficie):
        if self.encaixada:
            draw_cor = (100, 200, 100)  # Verde para encaixada
        else:
            draw_cor = self.cor

        x, y = self.pos
        t = self.tamanho

        if self.forma == "circulo":
            pygame.draw.circle(superficie, draw_cor, (int(x), int(y)), t)
            pygame.draw.circle(superficie, COR_BORDA, (int(x), int(y)), t, 2)

        elif self.forma == "quadrado":
            rect = pygame.Rect(x - t//2, y - t//2, t, t)
            pygame.draw.rect(superficie, draw_cor, rect)
            pygame.draw.rect(superficie, COR_BORDA, rect, 2)

        elif self.forma == "triangulo":
            ponto1 = (x, y - t//2)
            ponto2 = (x - t//2, y + t//2)
            ponto3 = (x + t//2, y + t//2)
            pygame.draw.polygon(superficie, draw_cor, [ponto1, ponto2, ponto3])
            pygame.draw.polygon(superficie, COR_BORDA, [ponto1, ponto2, ponto3], 2)

    def desenha_encaixe(self, superficie):
        """
        Desenha a forma no local correto com borda pontilhada para indicar o encaixe
        """
        x, y = self.encaixe_pos
        t = self.tamanho
        borda_cor = (156, 163, 175)  # cinza claro

        # desenha forma vazia para encaixe
        if self.forma == "circulo":
            pygame.draw.circle(superficie, COR_CARD_BG, (int(x), int(y)), t)
            self.draw_circulo_pontilhado(superficie, (int(x), int(y)), t, borda_cor)

        elif self.forma == "quadrado":
            rect = pygame.Rect(x - t//2, y - t//2, t, t)
            superficie.fill(COR_CARD_BG, rect)
            self.draw_retangulo_pontilhado(superficie, rect, borda_cor)

        elif self.forma == "triangulo":
            ponto1 = (x, y - t//2)
            ponto2 = (x - t//2, y + t//2)
            ponto3 = (x + t//2, y + t//2)
            polygon_points = [ponto1, ponto2, ponto3]
            self.draw_poligono_pontilhado(superficie, polygon_points, borda_cor)

    @staticmethod
    def draw_circulo_pontilhado(surf, center, radius, color, dash_length=5, space_length=5):
        circunferencia = 2 * 3.14159 * radius
        num_dashes = int(circunferencia / (dash_length + space_length))
        for i in range(num_dashes):
            start_angle = (i * (dash_length + space_length)) / radius
            end_angle = start_angle + dash_length / radius
            pygame.draw.arc(surf, color, (center[0]-radius, center[1]-radius, radius*2, radius*2), start_angle, end_angle, 2)

    @staticmethod
    def draw_retangulo_pontilhado(surf, rect, color, dash_length=10, space_length=10):
        x, y, w, h = rect
        # linha superior
        Figura.draw_linha_pontilhada(surf, color, (x, y), (x+w, y), dash_length, space_length)
        # linha inferior
        Figura.draw_linha_pontilhada(surf, color, (x, y+h), (x+w, y+h), dash_length, space_length)
        # linha esquerda
        Figura.draw_linha_pontilhada(surf, color, (x, y), (x, y+h), dash_length, space_length)
        # linha direita
        Figura.draw_linha_pontilhada(surf, color, (x+w, y), (x+w, y+h), dash_length, space_length)

    @staticmethod
    def draw_poligono_pontilhado(surf, pontos, color, dash_length=10, space_length=10):
        n = len(pontos)
        for i in range(n):
            p1 = pontos[i]
            p2 = pontos[(i+1) % n]
            Figura.draw_linha_pontilhada(surf, color, p1, p2, dash_length, space_length)

    @staticmethod
    def draw_linha_pontilhada(surf, color, start_pos, end_pos, dash_length=10, space_length=10):
        from math import sqrt
        x1, y1 = start_pos
        x2, y2 = end_pos
        length = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        dash_space = dash_length + space_length
        num_dashes = int(length // dash_space)
        for i in range(num_dashes + 1):
            start_x = x1 + (i * dash_space) * (x2 - x1) / length
            start_y = y1 + (i * dash_space) * (y2 - y1) / length
            end_x = start_x + dash_length * (x2 - x1) / length
            end_y = start_y + dash_length * (y2 - y1) / length
            if (x2 - x1) >= 0:
                if end_x > x2: end_x = x2
            else:
                if end_x < x2: end_x = x2
            if (y2 - y1) >= 0:
                if end_y > y2: end_y = y2
            else:
                if end_y < y2: end_y = y2
            pygame.draw.line(surf, color, (start_x, start_y), (end_x, end_y), 2)

def esta_encaixada(figura):
    px, py = figura.pos
    ex, ey = figura.encaixe_pos
    distancia = ((px - ex)**2 + (py - ey)**2)**0.5
    return distancia < figura.tamanho * 0.5

def main():
    figuras = [
        Figura('circulo', (255, 99, 132), (150, 500), 60, (150, 150)),
        Figura('quadrado', (54, 162, 235), (350, 500), 80, (350, 150)),
        Figura('triangulo', (255, 206, 86), (550, 500), 90, (550, 150))
    ]

    selecionada = None
    offset_x = 0
    offset_y = 0

    rodando = True
    while rodando:
        clock.tick(FPS)
        tela.fill(COR_FUNDO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mx, my = evento.pos
                for figura in reversed(figuras):  # checar da cima para baixo
                    px, py = figura.pos
                    t = figura.tamanho
                    dentro = False
                    if figura.forma == 'circulo':
                        dx = mx - px
                        dy = my - py
                        dentro = (dx*dx + dy*dy) <= t*t
                    elif figura.forma == 'quadrado':
                        dentro = (px - t//2 <= mx <= px + t//2) and (py - t//2 <= my <= py + t//2)
                    elif figura.forma == 'triangulo':
                        # para simplificar caixa retangular
                        dentro = (px - t//2 <= mx <= px + t//2) and (py - t//2 <= my <= py + t//2)
                    if dentro and not figura.encaixada:
                        selecionada = figura
                        offset_x = px - mx
                        offset_y = py - my
                        break

            elif evento.type == pygame.MOUSEBUTTONUP:
                if selecionada:
                    if esta_encaixada(selecionada):
                        selecionada.pos = list(selecionada.encaixe_pos)
                        selecionada.encaixada = True
                    selecionada = None

            elif evento.type == pygame.MOUSEMOTION:
                if selecionada and not selecionada.encaixada:
                    mx, my = evento.pos
                    selecionada.pos = [mx + offset_x, my + offset_y]

        # Desenha local de encaixe
        for figura in figuras:
            figura.desenha_encaixe(tela)

        # Desenha figuras
        for figura in figuras:
            figura.draw(tela)

        # Texto título
        titulo_surf = FONT_TITULO.render("Encaixe de Figuras Geométricas", True, COR_TITULO)
        tela.blit(titulo_surf, (LARGURA//2 - titulo_surf.get_width() // 2, 20))

        # Texto instruções
        instrucao_surf = FONT_TEXTO.render("Arraste as figuras para os encaixes correspondentes.", True, COR_TEXTO)
        tela.blit(instrucao_surf, (LARGURA//2 - instrucao_surf.get_width() // 2, ALTURA - 50))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


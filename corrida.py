import pygame
import sys
import math

# Inicialização Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Pista Sinuosa")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
YELLOW = (255, 215, 0)
BLUE = (70, 130, 180)

# Frame rate
FPS = 60
clock = pygame.time.Clock()

# Configurações da pista
TRACK_WIDTH = 200  # largura total da pista
TRACK_COLOR = DARK_GRAY
GUARDRAIL_COLOR = RED
GUARDRAIL_WIDTH = 20  # espessura dos guard rails

# Configurações do carro
CAR_WIDTH, CAR_HEIGHT = 50, 30
CAR_COLOR = BLUE
CAR_SPEED = 5
CAR_TURN_SPEED = 5  # graus por frame

# Fonte para textos
font = pygame.font.SysFont('Arial', 24)

# Função para desenhar a pista com efeito sinuoso
def draw_track(surface, scroll):
    # Vamos desenhar o centro da pista como uma linha senoidal vertical que anda para cima
    points_center = []
    amplitude = 120  # amplitude das curvas
    wavelength = 400  # distância entre as curvas (pixels)
    # Mostra pontos da pista no eixo Y (varrendo toda tela + buffer)
    for y in range(-100, HEIGHT + 100, 5):
        # O eixo y deslocado por scroll (deslocamento vertical)
        y_pos = y
        # O eixo x é função senoidal do y+scroll para "mover" a pista pra cima
        x_offset = amplitude * math.sin(2 * math.pi * (y + scroll) / wavelength)
        x_pos = WIDTH // 2 + x_offset
        points_center.append((x_pos, y_pos))

    # Gerar as bordas da pista offset a esquerda e direita do centro
    points_left = []
    points_right = []
    # Para cada ponto central, deslocar nas normais para as bordas
    for i in range(len(points_center)):
        # Calcular direção aproximada da pista (vetor tangente)
        if i < len(points_center) - 1:
            dx = points_center[i+1][0] - points_center[i][0]
            dy = points_center[i+1][1] - points_center[i][1]
        else:
            dx = points_center[i][0] - points_center[i-1][0]
            dy = points_center[i][1] - points_center[i-1][1]

        length = math.hypot(dx, dy)
        if length == 0:
            length = 1
        # Normal ao vetor tangente
        nx = -dy / length
        ny = dx / length
        # Ponto esquerdo e direito da pista
        left_point = (points_center[i][0] + nx * TRACK_WIDTH // 2, points_center[i][1] + ny * TRACK_WIDTH // 2)
        right_point = (points_center[i][0] - nx * TRACK_WIDTH // 2, points_center[i][1] - ny * TRACK_WIDTH // 2)
        points_left.append(left_point)
        points_right.append(right_point)

    # Desenhar pista preenchida entre esquerda e direita
    polygon_points = points_left + points_right[::-1]  # esquerda descendo e direita subindo invertido
    pygame.draw.polygon(surface, TRACK_COLOR, polygon_points)

    # Desenhar guard rails (barras vermelhas nas bordas)
    # As bordas internas da pista são guard rails: um pouco deslocados para dentro
    inner_offset = TRACK_WIDTH//2 - GUARDRAIL_WIDTH/2
    guard_left = []
    guard_right = []
    for i in range(len(points_center)):
        if i < len(points_center) - 1:
            dx = points_center[i+1][0] - points_center[i][0]
            dy = points_center[i+1][1] - points_center[i][1]
        else:
            dx = points_center[i][0] - points_center[i-1][0]
            dy = points_center[i][1] - points_center[i-1][1]
        length = math.hypot(dx, dy)
        if length == 0:
            length = 1
        nx = -dy / length
        ny = dx / length
        # guard rail left (mais pro centro)
        gl = (points_center[i][0] + nx * inner_offset, points_center[i][1] + ny * inner_offset)
        # guard rail right
        gr = (points_center[i][0] - nx * inner_offset, points_center[i][1] - ny * inner_offset)
        guard_left.append(gl)
        guard_right.append(gr)

    pygame.draw.lines(surface, GUARDRAIL_COLOR, False, guard_left, int(GUARDRAIL_WIDTH))
    pygame.draw.lines(surface, GUARDRAIL_COLOR, False, guard_right, int(GUARDRAIL_WIDTH))

    # Para efeitos de colisão, retornamos o centro e bordas da pista para referência
    return points_center, points_left, points_right

# Classe Carro
class Car:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.angle = 0  # em graus, 0 para cima
        self.speed = 0
        self.max_speed = 8
        self.min_speed = -3
        self.acceleration = 0.2
        self.deceleration = 0.1
        self.turn_speed = CAR_TURN_SPEED
        self.image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
        # Desenhar um carro simples (retângulo azul com cabine branca)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, CAR_COLOR, (0, 0, CAR_WIDTH, CAR_HEIGHT), border_radius=6)
        pygame.draw.rect(self.image, WHITE, (10, 5, CAR_WIDTH-20, CAR_HEIGHT-10), border_radius=4)

    def update(self, keys_pressed):
        # Acelerar e desacelerar
        if keys_pressed[pygame.K_UP]:
            self.speed += self.acceleration
        elif keys_pressed[pygame.K_DOWN]:
            self.speed -= self.acceleration
        else:
            # desacelera naturalmente
            if self.speed > 0:
                self.speed -= self.deceleration
            elif self.speed < 0:
                self.speed += self.deceleration

        # Clamp speed
        self.speed = max(min(self.speed, self.max_speed), self.min_speed)

        # Virar o carro
        if keys_pressed[pygame.K_LEFT]:
            self.angle += self.turn_speed * (self.speed / self.max_speed if self.speed > 0 else 0)
        if keys_pressed[pygame.K_RIGHT]:
            self.angle -= self.turn_speed * (self.speed / self.max_speed if self.speed > 0 else 0)

        # Atualizar posição
        rad = math.radians(self.angle)
        self.x += -self.speed * math.sin(rad)
        self.y += -self.speed * math.cos(rad)

        # Ficar dentro da tela verticalmente (o carro anda na pista pra cima)
        if self.y < HEIGHT//2:
            self.y = HEIGHT//2
        elif self.y > HEIGHT - CAR_HEIGHT//2:
            self.y = HEIGHT - CAR_HEIGHT//2

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        surface.blit(rotated_image, rect.topleft)

    def get_position(self):
        return self.x, self.y

# Função para colisão do carro com os guard rails (simples)
def check_collision(car_x, car_y, points_left, points_right):
    # Como pista está no eixo Y, encontre ponto mais próximo na vertical
    # Como pista está desenhada de -100 a HEIGHT+100 com passos de 5px,
    # Calcula índice aproximado de y
    y_idx = int(car_y) // 5
    y_idx = max(0, min(y_idx, len(points_left)-1))
    left_x, left_y = points_left[y_idx]
    right_x, right_y = points_right[y_idx]

    # Checar se carro está dentro da pista (entre bordas)
    if car_x < left_x + GUARDRAIL_WIDTH/2 or car_x > right_x - GUARDRAIL_WIDTH/2:
        return True
    return False

def main():
    car = Car()
    scroll = 0  # controla o deslocamento vertical da pista (quanto avançamos)

    running = True
    collision = False
    collision_timer = 0

    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not collision:
            car.update(keys)
            scroll += car.speed  # mover a pista para baixo para dar a sensação do carro andando para cima

        # Desenhar fundo
        SCREEN.fill(GREEN)

        # Desenhar pista e obter bordas para colisão
        points_center, points_left, points_right = draw_track(SCREEN, scroll)

        # Checar colisão
        if check_collision(car.x, car.y, points_left, points_right):
            collision = True
            collision_timer = pygame.time.get_ticks()

        # Desenhar carro
        car.draw(SCREEN)

        # Mensagem
        if collision:
            text = font.render("Você bateu! Reinicie o jogo para tentar de novo.", True, YELLOW)
            SCREEN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()



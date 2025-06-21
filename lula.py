import pygame
import sys
import random
import math

# Inicializa pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
FPS = 60

# Cores seguindo diretrizes
COLOR_BG = (255, 255, 255)
COLOR_TEXT_PRIMARY = (31, 41, 55)
COLOR_TEXT_SECONDARY = (107, 114, 128)
COLOR_PLAYER = (0, 128, 255)
COLOR_ROCK = (139, 69, 19)
COLOR_TARGET = (255, 0, 0)
COLOR_EXPLOSION = (255, 100, 0)

# Fontes
FONT_TITLE = pygame.font.SysFont("Poppins", 54, bold=True)
FONT_BODY = pygame.font.SysFont("Poppins", 22)

# Configura tela e relógio
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atire pedras no Lula")
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 10
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, dx):
        self.x += dx * self.speed
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.rect.x = self.x

    def draw(self, surf):
        pygame.draw.rect(surf, COLOR_PLAYER, self.rect)

class Rock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.speed = -10  # vai para cima
        self.alive = True

    def update(self):
        self.y += self.speed
        if self.y < 0:
            self.alive = False

    def draw(self, surf):
        pygame.draw.circle(surf, COLOR_ROCK, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

class Target:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = random.randint(0, WIDTH - self.width)
        self.y = random.randint(50, 150)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.x += random.choice([-1, 1]) * 2
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.rect.x = self.x

    def draw(self, surf):
        pygame.draw.rect(surf, COLOR_TARGET, self.rect)

class Explosion:
    def __init__(self, pos):
        self.pos = pos
        self.radius = 10
        self.max_radius = 40
        self.life = 30  # frames da explosão
        self.current_frame = 0

    def update(self):
        self.current_frame += 1
        self.radius = int(10 + (self.max_radius - 10) * (self.current_frame / self.life))

    def draw(self, surf):
        alpha = max(255 - int(255 * (self.current_frame / self.life)), 0)
        if alpha > 0:
            exploded_surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(exploded_surf, (*COLOR_EXPLOSION, alpha), (self.radius, self.radius), self.radius)
            surf.blit(exploded_surf, (self.pos[0] - self.radius, self.pos[1] - self.radius))

    def is_finished(self):
        return self.current_frame >= self.life

def draw_text_center(surf, text, font, color, y):
    txt_surf = font.render(text, True, color)
    rect = txt_surf.get_rect(center=(WIDTH // 2, y))
    surf.blit(txt_surf, rect)

def main():
    player = Player()
    rocks = []
    target = Target()
    explosions = []
    running = True
    move_dir = 0
    score = 0
    game_over = False

    while running:
        clock.tick(FPS)
        screen.fill(COLOR_BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key in (pygame.K_LEFT, pygame.K_a):
                        move_dir = -1
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        move_dir = 1
                    elif event.key == pygame.K_SPACE:
                        rocks.append(Rock(player.x + player.width//2, player.y))
                else:
                    if event.key == pygame.K_RETURN:
                        # reiniciar jogo
                        rocks.clear()
                        explosions.clear()
                        target = Target()
                        player.x = WIDTH // 2 - player.width // 2
                        player.rect.x = player.x
                        score = 0
                        game_over = False
                        move_dir = 0

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_a) and move_dir == -1:
                    move_dir = 0
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and move_dir == 1:
                    move_dir = 0

        if not game_over:
            player.move(move_dir)
            target.move()

            for rock in rocks[:]:
                rock.update()
                if not rock.alive:
                    rocks.remove(rock)
                    score += 1
                elif rock.get_rect().colliderect(target.rect):
                    rocks.remove(rock)
                    explosions.append(Explosion((target.rect.centerx, target.rect.centery)))
                    target = Target()
                    score += 5

            for explosion in explosions[:]:
                explosion.update()
                if explosion.is_finished():
                    explosions.remove(explosion)

            # colisão asteroide x jogador (não tem asteroide, não usada)

        # desenha elementos
        target.draw(screen)
        player.draw(screen)
        for rock in rocks:
            rock.draw(screen)
        for explosion in explosions:
            explosion.draw(screen)

        draw_text_center(screen, f"Pontuação: {score}", FONT_BODY, COLOR_TEXT_SECONDARY, 30)

        if game_over:
            draw_text_center(screen, "FIM DE JOGO! Pressione ENTER para reiniciar", FONT_TITLE, COLOR_TEXT_PRIMARY, HEIGHT//2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


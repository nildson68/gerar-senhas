import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors following guidelines
COLOR_BG = (255, 255, 255)  # white background
COLOR_TEXT_PRIMARY = (31, 41, 55)  # #1f2937 dark gray
COLOR_TEXT_SECONDARY = (107, 114, 128)  # #6b7280 neutral gray

# Fonts
FONT_TITLE = pygame.font.SysFont("Poppins", 54, bold=True)
FONT_BODY = pygame.font.SysFont("Poppins", 22)

# Setup screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge - Desvie dos asteroides")
clock = pygame.time.Clock()

# Load spaceship image or draw a simple ship shape
# Since no images allowed, we'll draw a minimalistic ship with polygons and circles


class Spaceship:
    def __init__(self):
        self.width = 50
        self.height = 70
        self.x = WIDTH // 2
        self.y = HEIGHT - self.height - 10
        self.speed = 6
        self.color = (20, 20, 40)  # dark navy blue
        # Used for collision rectangle
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                                self.width, self.height)

    def move(self, dx):
        self.x += dx * self.speed
        # Boundaries
        self.x = max(self.width // 2 + 10, min(WIDTH - self.width // 2 -10, self.x))
        self.rect.x = self.x - self.width // 2

    def draw(self, surf):
        # Draw ship body - rounded polygon shape
        # Base rectangle with rounded edges (simulate with polygons and circle caps)
        body_rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2,
                                self.width, self.height)
        # Body
        pygame.draw.rect(surf, self.color, body_rect, border_radius=20)

        # Cockpit - ellipse on top
        cockpit_rect = pygame.Rect(self.x - 15, self.y - self.height // 2 - 10, 30, 20)
        pygame.draw.ellipse(surf, (80, 120, 200), cockpit_rect)

        # Flame behind the ship - flickering triangles
        flame_color = (255, 150, 50)
        points = [(self.x - 15, self.y + self.height // 2),
                  (self.x, self.y + self.height // 2 + 25),
                  (self.x + 15, self.y + self.height // 2)]
        pygame.draw.polygon(surf, flame_color, points)

class Asteroid:
    def __init__(self):
        self.radius = random.randint(15, 30)
        self.x = random.randint(self.radius + 10, WIDTH - self.radius - 10)
        self.y = -self.radius
        self.speed = random.uniform(2.5, 5.5)
        self.color = (120, 120, 120)  # greyish asteroid

    def update(self):
        self.y += self.speed

    def off_screen(self):
        return self.y - self.radius > HEIGHT

    def draw(self, surf):
        # Draw as a circle with subtle shading
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), self.radius)

        # Add a little lighter highlight on top-left
        highlight_color = (200, 200, 200)
        highlight_pos = (int(self.x - self.radius / 3), int(self.y - self.radius / 3))
        pygame.draw.circle(surf, highlight_color, highlight_pos, self.radius // 3)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           2 * self.radius, 2 * self.radius)

def draw_text_center(surf, text, font, color, y):
    text_surf = font.render(text, True, color)
    rect = text_surf.get_rect(center=(WIDTH // 2, y))
    surf.blit(text_surf, rect)

def main():
    spaceship = Spaceship()
    asteroids = []
    asteroid_spawn_delay = 20  # frames between spawns
    asteroid_timer = 0

    running = True
    move_dir = 0  # -1 left, 1 right, 0 none
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
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        move_dir = -1
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        move_dir = 1
                if game_over:
                    if event.key == pygame.K_RETURN:
                        # restart the game
                        asteroids.clear()
                        spaceship.x = WIDTH // 2
                        spaceship.rect.x = spaceship.x - spaceship.width // 2
                        score = 0
                        game_over = False
                        asteroid_timer = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and move_dir == -1:
                    move_dir = 0
                elif event.key == pygame.K_RIGHT and move_dir == 1:
                    move_dir = 0

        if not game_over:
            spaceship.move(move_dir)

            # Spawn asteroids
            asteroid_timer += 1
            if asteroid_timer >= asteroid_spawn_delay:
                asteroid_timer = 0
                asteroids.append(Asteroid())

            # Update asteroids
            for asteroid in asteroids[:]:
                asteroid.update()
                if asteroid.off_screen():
                    asteroids.remove(asteroid)
                    score += 1  # Survive scores
                elif asteroid.get_rect().colliderect(spaceship.rect):
                    game_over = True

        # Draw spaceship
        spaceship.draw(screen)

        # Draw asteroids
        for asteroid in asteroids:
            asteroid.draw(screen)

        # Score display
        draw_text_center(screen, f"Score: {score}", FONT_BODY, COLOR_TEXT_SECONDARY, 30)

        if game_over:
            draw_text_center(screen, "GAME OVER", FONT_TITLE, COLOR_TEXT_PRIMARY, HEIGHT // 2 - 30)
            draw_text_center(screen, "Pressione ENTER para jogar novamente", FONT_BODY, COLOR_TEXT_SECONDARY, HEIGHT // 2 + 20)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


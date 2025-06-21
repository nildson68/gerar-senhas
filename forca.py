import pygame
import sys
import random

pygame.init()
pygame.display.set_caption("Jogo da Forca")

# Constantes
WIDTH, HEIGHT = 800, 600
FPS = 60
MAX_WRONG_GUESSES = 6
CONTAINER_WIDTH = 480  # Reduzi a largura para dar mais espaço à direita para a forca

# Cores
COLOR_BG = (255, 255, 255)
COLOR_TEXT = (107, 114, 128)  # #6b7280 cinza neutro
COLOR_TITLE = (31, 41, 55)  # cinza escuro quase preto
COLOR_SHADOW = (220, 220, 220)
COLOR_INPUT_BG = (245, 245, 245)
COLOR_BORDER = (203, 213, 225)
COLOR_BORDER_FOCUS = (147, 197, 253)
COLOR_CORRECT = (34, 197, 94)  # verde
COLOR_WRONG = (220, 38, 38)  # vermelho
COLOR_BUTTON_BG = (31, 41, 55)
COLOR_BUTTON_TEXT = (255, 255, 255)

# Fontes
FONT_TITLE = pygame.font.SysFont("Segoe UI", 56, bold=True)
FONT_SUBTITLE = pygame.font.SysFont("Segoe UI", 24)
FONT_TEXT = pygame.font.SysFont("Segoe UI", 20)
FONT_LETTER = pygame.font.SysFont("Segoe UI", 40, bold=True)
FONT_SMALL = pygame.font.SysFont("Segoe UI", 16)

# Lista de palavras
WORDS = [
    "python", "programacao", "jogo", "computador", "desenvolvedor",
    "teclado", "monitor", "mouse", "janela", "sistema", "desafio",
    "codigo", "linguagem", "variavel", "funcao", "interface"
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def draw_rounded_rect(surf, rect, color, radius=12):
    x, y, w, h = rect
    pygame.draw.rect(surf, color, (x + radius, y, w - 2*radius, h))
    pygame.draw.rect(surf, color, (x, y + radius, w, h - 2*radius))
    pygame.draw.circle(surf, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surf, color, (x + w - radius, y + radius), radius)
    pygame.draw.circle(surf, color, (x + radius, y + h - radius), radius)
    pygame.draw.circle(surf, color, (x + w - radius, y + h - radius), radius)

def draw_hangman(surf, center_x, center_y, wrong_guesses):
    # Base da forca
    base_y = center_y + 150
    pygame.draw.line(surf, COLOR_TEXT, (center_x - 100, base_y), (center_x + 100, base_y), 6)
    pygame.draw.line(surf, COLOR_TEXT, (center_x - 60, base_y), (center_x - 60, center_y - 150), 6)
    pygame.draw.line(surf, COLOR_TEXT, (center_x - 60, center_y - 150), (center_x + 20, center_y - 150), 6)
    pygame.draw.line(surf, COLOR_TEXT, (center_x + 20, center_y - 150), (center_x + 20, center_y - 120), 4)

    if wrong_guesses > 0:
        pygame.draw.circle(surf, COLOR_TEXT, (center_x + 20, center_y - 90), 30, 4)
    if wrong_guesses > 1:
        pygame.draw.line(surf, COLOR_TEXT, (center_x + 20, center_y - 60), (center_x + 20, center_y + 40), 4)
    if wrong_guesses > 2:
        pygame.draw.line(surf, COLOR_TEXT, (center_x + 20, center_y - 40), (center_x - 30, center_y - 10), 4)
    if wrong_guesses > 3:
        pygame.draw.line(surf, COLOR_TEXT, (center_x + 20, center_y - 40), (center_x + 70, center_y - 10), 4)
    if wrong_guesses > 4:
        pygame.draw.line(surf, COLOR_TEXT, (center_x + 20, center_y + 40), (center_x - 30, center_y + 100), 4)
    if wrong_guesses > 5:
        pygame.draw.line(surf, COLOR_TEXT, (center_x + 20, center_y + 40), (center_x + 70, center_y + 100), 4)

def main():
    running = True

    word = random.choice(WORDS)
    word_letters = set(word)
    guessed_letters = set()
    wrong_guesses = 0
    score = 0
    game_over = False
    message = "Digite uma letra e pressione ENTER"

    container_x = 40  # margem esquerda razoável

    while running:
        screen.fill(COLOR_BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pass  # não faz nada aqui, o input é por letra
                elif event.key == pygame.K_BACKSPACE:
                    pass  # backspace não faz sentido aqui (input único)
                else:
                    letra = event.unicode.lower()
                    if letra.isalpha() and len(letra) == 1:
                        if letra in guessed_letters:
                            message = f"A letra '{letra.upper()}' já foi tentada"
                        else:
                            guessed_letters.add(letra)
                            if letra in word_letters:
                                message = f"Boa! A letra '{letra.upper()}' está na palavra"
                                if word_letters.issubset(guessed_letters):
                                    score += 1
                                    message = f"Você acertou a palavra '{word.upper()}'! Pressione ENTER para continuar"
                                    game_over = True
                            else:
                                wrong_guesses += 1
                                if wrong_guesses >= MAX_WRONG_GUESSES:
                                    message = f"Fim de jogo! A palavra era '{word.upper()}'. Pressione ENTER para jogar novamente"
                                    game_over = True
                                else:
                                    message = f"Letra '{letra.upper()}' não está na palavra. Tentativas restantes: {MAX_WRONG_GUESSES - wrong_guesses}"

            elif game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    word = random.choice(WORDS)
                    word_letters = set(word)
                    guessed_letters = set()
                    wrong_guesses = 0
                    game_over = False
                    message = "Digite uma letra e pressione ENTER"

        # --- Desenho UI ---

        # Título
        title_surf = FONT_TITLE.render("Jogo da Forca", True, COLOR_TITLE)
        screen.blit(title_surf, (container_x, 40))

        # Pontuação
        score_surf = FONT_SUBTITLE.render(f"Pontuação: {score}", True, COLOR_TITLE)
        screen.blit(score_surf, (container_x, 110))

        # Caixa de mensagem
        msg_rect = pygame.Rect(container_x, 520, CONTAINER_WIDTH, 50)
        shadow_rect = msg_rect.move(4, 4)
        draw_rounded_rect(screen, shadow_rect, COLOR_SHADOW)
        draw_rounded_rect(screen, msg_rect, COLOR_INPUT_BG)
        pygame.draw.rect(screen, COLOR_BORDER, msg_rect, 1, border_radius=12)

        msg_surf = FONT_TEXT.render(message, True, COLOR_TEXT)
        msg_rect_inner = msg_surf.get_rect(center=msg_rect.center)
        screen.blit(msg_surf, msg_rect_inner)

        # Palavras com underlines e letras reveladas
        display_word = ""
        for letter in word:
            if letter in guessed_letters:
                display_word += letter.upper() + " "
            else:
                display_word += "_ "
        display_word = display_word.strip()

        word_rect = pygame.Rect(container_x, 180, CONTAINER_WIDTH, 80)
        draw_rounded_rect(screen, word_rect.move(4, 4), COLOR_SHADOW)
        draw_rounded_rect(screen, word_rect, COLOR_INPUT_BG)
        pygame.draw.rect(screen, COLOR_BORDER, word_rect, 1, border_radius=12)

        word_surf = FONT_LETTER.render(display_word, True, COLOR_TITLE)
        word_rect_inner = word_surf.get_rect(center=word_rect.center)
        screen.blit(word_surf, word_rect_inner)

        # Letras usadas
        guessed_rect = pygame.Rect(container_x, 280, CONTAINER_WIDTH, 60)
        draw_rounded_rect(screen, guessed_rect.move(4, 4), COLOR_SHADOW)
        draw_rounded_rect(screen, guessed_rect, COLOR_INPUT_BG)
        pygame.draw.rect(screen, COLOR_BORDER, guessed_rect, 1, border_radius=12)

        guessed_text = "Letras usadas: " + ", ".join(sorted(guessed_letters)).upper() if guessed_letters else "Letras usadas: -"
        guessed_surf = FONT_TEXT.render(guessed_text, True, COLOR_TEXT)
        guessed_rect_inner = guessed_surf.get_rect(midleft=(guessed_rect.left + 15, guessed_rect.centery))
        screen.blit(guessed_surf, guessed_rect_inner)

        # Desenhar a forca mais para a direita
        hangman_x = container_x + CONTAINER_WIDTH + 120  # 120px afastado da área do texto
        hangman_y = 350
        draw_hangman(screen, hangman_x, hangman_y, wrong_guesses)

        # Instruções
        instr_surf = FONT_SMALL.render("Digite uma letra no teclado. Pressione ENTER para confirmar.", True, COLOR_TEXT)
        screen.blit(instr_surf, (container_x, 370))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()


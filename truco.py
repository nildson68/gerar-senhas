import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Truco - Pygame")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 215, 0)

# Fontes
FONT_SMALL = pygame.font.SysFont('arial', 18)
FONT_MEDIUM = pygame.font.SysFont('arial', 24)
FONT_LARGE = pygame.font.SysFont('arial', 36)

# Cartas do Truco (modalidade comum com 40 cartas: 1 a 7 e 10 a 12)
SUITS = ['Espadas', 'Copas', 'Paus', 'Ouros']
RANKS = [1, 2, 3, 4, 5, 6, 7, 10, 11, 12]

# Valores do truco para as cartas (modo paulista/truco paulista - exemplo)
# Nota: Pode variar conforme regional, esse valor é usado para comparação na rodada
# As cartas são ordenadas por força decrescente
CARD_STRENGTH = {
    (1, 'Espadas'): 14,  # Espadão
    (1, 'Bastos'): 13,   # Manilha ex: "Bastos" é "Paus" na lógica, se precisar troco
    (7, 'Ouros'): 12,
    (7, 'Espadas'): 11,
    # resto das cartas com seus valores
}

# Função auxiliar: força da carta com fallback para ranking normal if not in special
def card_strength(rank, suit):
    # Ajuste para manilhas do truco paulista tradicional
    # Aqui consideramos só valores estáticos para simplicidade
    # Exemplo simplificado: 3 > 2 > A > K > Q ... para baralho reduzido
    # Implementação simplificada: força = rank (com alguns ajustes)
    # Para Truco, normalmente (3 > 2 > A > K > Q > J > 7 > 6 > 5 > 4)
    # Usar um mapeamento para rank real no truco:
    # Valores truco: 3(10), 2(9), A(8), K(7), Q(6), J(5), 7(4), 6(3), 5(2), 4(1)
    # Como as cartas no baralho são 1-7 e 10-12, associar:
    # 1 = A, 10 = J, 11 = Q, 12 = K
    rank_map = {
        3: 10,
        2: 9,
        1: 8,  # Ás
        12: 7, # Rei (K)
        11: 6, # Dama (Q)
        10: 5, # Valete (J)
        7: 4,
        6: 3,
        5: 2,
        4: 1
    }
    return rank_map.get(rank, 0)

# Classe Carta
class Card:
    WIDTH = 70
    HEIGHT = 100

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.rect = pygame.Rect(0, 0, Card.WIDTH, Card.HEIGHT)
        self.selected = False  # para seleção e interação

    def draw(self, surface, pos, face_up=True):
        self.rect.topleft = pos
        # Carta virada para o jogador ou costas para o oponente
        if face_up:
            pygame.draw.rect(surface, WHITE, self.rect, border_radius=12)
            pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=12)
            # texto rank e naipe
            text_rank = FONT_MEDIUM.render(str(self.rank), True, BLACK)
            text_suit = FONT_SMALL.render(self.suit, True, BLACK)
            surface.blit(text_rank, (self.rect.x + 8, self.rect.y + 8))
            surface.blit(text_suit, (self.rect.x + 5, self.rect.y + 40))

            # Destaque se selecionada
            if self.selected:
                pygame.draw.rect(surface, YELLOW, self.rect, 4, border_radius=12)
        else:
            # costas da carta
            pygame.draw.rect(surface, DARK_GRAY, self.rect, border_radius=12)
            pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=12)
            # desenho de padrão simples
            center = self.rect.center
            pygame.draw.circle(surface, YELLOW, center, 15, 3)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Classe Baralho
class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def deal(self, num_cards):
        dealt_cards = []
        for _ in range(num_cards):
            if self.cards:
                dealt_cards.append(self.cards.pop())
        return dealt_cards

# Classe Jogador
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.points = 0
        self.played_card = None

    def play_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            self.played_card = card
            return True
        return False

    def receive_cards(self, cards):
        self.hand.extend(cards)
        # Organizar a mão por rank para melhor visualização
        self.hand.sort(key=lambda c: card_strength(c.rank, c.suit), reverse=True)

# Classe jogo principal
class TrucoGame:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.deck = Deck()
        self.player = Player("Você")
        self.opponent = Player("Oponente")
        self.table_cards = []  # cartas jogadas na mesa neste turno
        self.turn = 0  # 0 = jogador, 1 = oponente
        self.font = FONT_MEDIUM
        self.round = 1
        self.max_rounds = 3
        self.message = "Jogue sua carta."
        self.winner = None

        # Distribuir cartas para cada jogador (3 cartas)
        self.player.receive_cards(self.deck.deal(3))
        self.opponent.receive_cards(self.deck.deal(3))

    def draw(self):
        SCREEN.fill(GREEN)

        # Mostrar Informações de pontos
        text_score = self.font.render(f"Pontos - Você: {self.player.points}  Oponente: {self.opponent.points}", True, WHITE)
        SCREEN.blit(text_score, (20, 20))

        text_round = self.font.render(f"Rodada {self.round} de {self.max_rounds}", True, WHITE)
        SCREEN.blit(text_round, (WIDTH // 2 - text_round.get_width()//2, 20))

        # Mensagem
        msg_text = FONT_SMALL.render(self.message, True, WHITE)
        SCREEN.blit(msg_text, (20, HEIGHT - 30))

        # Mostrar cartas do jogador (viradas para cima)
        hand_y = HEIGHT - Card.HEIGHT - 40
        gap = 20
        start_x = (WIDTH - (len(self.player.hand)*(Card.WIDTH + gap) - gap))//2
        for idx, card in enumerate(self.player.hand):
            pos = (start_x + idx*(Card.WIDTH + gap), hand_y)
            card.draw(SCREEN, pos, face_up=True)

        # Mostrar cartas do oponente (viradas para baixo)
        opp_y = 40
        start_x = (WIDTH - (len(self.opponent.hand)*(Card.WIDTH + gap) - gap))//2
        for idx, card in enumerate(self.opponent.hand):
            pos = (start_x + idx*(Card.WIDTH + gap), opp_y)
            card.draw(SCREEN, pos, face_up=False)

        # Mostrar cartas na mesa
        table_y = HEIGHT//2 - Card.HEIGHT//2
        # Carta do jogador esquerda
        if self.player.played_card:
            pos_player = (WIDTH//4 - Card.WIDTH//2, table_y)
            self.player.played_card.draw(SCREEN, pos_player, face_up=True)
        # Carta do oponente direita
        if self.opponent.played_card:
            pos_opp = (3*WIDTH//4 - Card.WIDTH//2, table_y)
            self.opponent.played_card.draw(SCREEN, pos_opp, face_up=True)

        # Indicador de vez
        turn_text = self.font.render("Sua vez" if self.turn == 0 else "Vez do oponente", True, YELLOW)
        SCREEN.blit(turn_text, (WIDTH - turn_text.get_width() - 20, 20))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.turn == 0 and self.winner is None:
                    pos = pygame.mouse.get_pos()
                    for card in self.player.hand:
                        if card.is_clicked(pos):
                            # Jogar a carta selecionada
                            self.player.play_card(card)
                            self.message = f"Você jogou {card.rank} de {card.suit}."
                            self.turn = 1  # vez do oponente
                            # Aguardar jogada do oponente
                            pygame.time.set_timer(pygame.USEREVENT, 1000)  # evento usuário para jogada do oponente
                            break

            elif event.type == pygame.USEREVENT:
                # Jogada do oponente automática (joga a carta mais forte)
                if self.turn == 1 and self.opponent.hand:
                    best_card = max(self.opponent.hand, key=lambda c: card_strength(c.rank, c.suit))
                    self.opponent.play_card(best_card)
                    self.message = f"Oponente jogou {best_card.rank} de {best_card.suit}."
                    self.turn = 0  # volta para jogador
                    pygame.time.set_timer(pygame.USEREVENT, 0)  # parar timer
                    # Conferir ganhador dessa rodada
                    self.check_round_winner()

    def check_round_winner(self):
        # Só conferir se os dois jogaram
        if self.player.played_card and self.opponent.played_card:
            p_card = self.player.played_card
            o_card = self.opponent.played_card
            p_value = card_strength(p_card.rank, p_card.suit)
            o_value = card_strength(o_card.rank, o_card.suit)

            if p_value > o_value:
                self.player.points += 1
                self.message = "Você venceu a rodada!"
            elif p_value < o_value:
                self.opponent.points += 1
                self.message = "O oponente venceu a rodada!"
            else:
                self.message = "Rodada empatada!"

            # Resetar cartas jogadas para próxima rodada
            self.player.played_card = None
            self.opponent.played_card = None

            self.round += 1

            # Distribuir novas cartas se houverem na mesa (simplificado)
            if self.round <= self.max_rounds:
                self.message += " Jogue sua carta."
                # Quando as cartas acabarem, o jogo termina
                if not self.player.hand:
                    # Reposição simples de cartas se o deck tiver
                    if len(self.deck.cards) >= 6:
                        self.player.receive_cards(self.deck.deal(3))
                        self.opponent.receive_cards(self.deck.deal(3))
                # continua o jogo normal
            else:
                self.end_game()

    def end_game(self):
        self.winner = None
        if self.player.points > self.opponent.points:
            self.message = "Parabéns! Você ganhou o jogo!"
            self.winner = self.player.name
        elif self.player.points < self.opponent.points:
            self.message = "O oponente ganhou o jogo. Tente novamente!"
            self.winner = self.opponent.name
        else:
            self.message = "O jogo terminou empatado!"
            self.winner = "Empate"

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TrucoGame()
    game.run()



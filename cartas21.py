import pygame
import sys
import random

pygame.init()

# Configurações principais
WIDTH, HEIGHT = 800, 600
FPS = 60
MAX_BET = 10_000

# Cores - paleta neutra, elegante
COLOR_BG = (255, 255, 255)
COLOR_TEXT_PRIMARY = (31, 41, 55)      # #1f2937, título escuro
COLOR_TEXT_SECONDARY = (107, 114, 128) # #6b7280, texto neutro
COLOR_CARD_BG = (249, 250, 251)         # #f9fafb, branco lavado
COLOR_CARD_SHADOW = (0, 0, 0, 25)       # sombra sutil
COLOR_BTN_BG = (0, 0, 0)
COLOR_BTN_HOVER = (30, 30, 30)
COLOR_BTN_TEXT = (255, 255, 255)
COLOR_SUCCESS = (22, 163, 74)  # verde limão #16a34a
COLOR_ERROR = (220, 38, 38)    # vermelho #dc2626
COLOR_DISABLED = (156, 163, 175) # cinza claro

RADIUS = 12
PADDING = 24
MAX_CONTAINER_W = 720

# Fontes: Poppins para título e texto, monospace para cartas
FONT_TITLE = pygame.font.SysFont("Poppins", 48, bold=True)
FONT_SUBTITLE = pygame.font.SysFont("Poppins", 22)
FONT_SMALL = pygame.font.SysFont("Poppins", 18)
FONT_CARD = pygame.font.SysFont("monospace", 40, bold=True)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de 21 - Blackjack com Apostas")
clock = pygame.time.Clock()

def draw_rounded_rect_with_shadow(surface, rect, bg_color, radius=RADIUS, shadow_offset=6):
    # Desenha sombra sutil e retângulo arredondado
    shadow_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, COLOR_CARD_SHADOW, shadow_surf.get_rect(), border_radius=radius)
    surface.blit(shadow_surf, (rect.x + shadow_offset, rect.y + shadow_offset))
    pygame.draw.rect(surface, bg_color, rect, border_radius=radius)

class Button:
    def __init__(self, rect, text, font, fg_color, bg_color, hover_color=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.hover_color = hover_color or bg_color
        self.hover = False
        self.enabled = True
        self.render_text()

    def render_text(self):
        color = self.fg_color if self.enabled else COLOR_DISABLED
        self.text_surf = self.font.render(self.text, True, color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        bg = self.hover_color if self.hover and self.enabled else self.bg_color
        if not self.enabled:
            bg = COLOR_DISABLED
        pygame.draw.rect(surface, bg, self.rect, border_radius=RADIUS)
        surface.blit(self.text_surf, self.text_rect)

    def update(self, mouse_pos):
        self.hover = self.enabled and self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if not self.enabled:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def set_enabled(self, enabled):
        self.enabled = enabled
        self.render_text()

class Card:
    SUITS_SYMBOLS = {'S':'♠', 'H':'♥', 'D':'♦', 'C':'♣'}
    RED_SUITS = ('H','D')

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def value(self):
        if self.rank in ['J','Q','K']:
            return 10
        if self.rank == 'A':
            return 11
        return int(self.rank)

    def draw(self, surface, pos):
        x,y = pos
        w,h = 60, 90
        rect = pygame.Rect(x,y,w,h)

        # sombra leve com blur fake
        shadow = pygame.Surface((w,h), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0,0,0,30),(5,5,w,h), border_radius=RADIUS)
        surface.blit(shadow,(x,y))

        # card bg branco com borda arredondada
        pygame.draw.rect(surface, COLOR_BG, rect, border_radius=RADIUS)
        pygame.draw.rect(surface, COLOR_TEXT_PRIMARY, rect, 2, border_radius=RADIUS)

        # cores do texto (vermelho para red suits)
        color = COLOR_ERROR if self.suit in Card.RED_SUITS else COLOR_TEXT_PRIMARY

        # Rank nos cantos
        rank_surf = FONT_CARD.render(self.rank, True, color)
        surface.blit(rank_surf, (x + 8, y + 5))
        surface.blit(rank_surf, (x + w - rank_surf.get_width() - 8, y + h - rank_surf.get_height() - 8))

        # Simbolo central
        symbol = Card.SUITS_SYMBOLS.get(self.suit, '?')
        symbol_surf = FONT_CARD.render(symbol, True, color)
        symbol_rect = symbol_surf.get_rect(center=(x + w//2, y + h//2 + 8))
        surface.blit(symbol_surf, symbol_rect)

class BlackjackGame:
    def __init__(self):
        self.balance = 1000
        self.bet = 0
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.state = 'betting'  # betting, playing, round_end
        self.message = "Faça sua aposta para começar"
        self.message_color = COLOR_TEXT_SECONDARY

        self.bet_input_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 140, 200, 40)
        self.bet_input_active = False
        self.bet_input_text = ''
        self.error_msg = ''

        # Botões elegantes
        self.btn_bet = Button((WIDTH//2 - 103, HEIGHT - 90, 206, 45), "Fazer Aposta", FONT_SUBTITLE, COLOR_BTN_TEXT, COLOR_BTN_BG, COLOR_BTN_HOVER)
        self.btn_hit = Button((WIDTH//4 - 75, HEIGHT - 130, 140, 50), "Pedir Carta", FONT_SUBTITLE, COLOR_BTN_TEXT, COLOR_BTN_BG, COLOR_BTN_HOVER)
        self.btn_stand = Button((WIDTH*3//4 - 75, HEIGHT - 130, 140, 50), "Parar", FONT_SUBTITLE, COLOR_BTN_TEXT, COLOR_BTN_BG, COLOR_BTN_HOVER)
        self.btn_restart = Button((WIDTH//2 - 100, HEIGHT - 70, 200, 50), "Jogar Novamente", FONT_SUBTITLE, COLOR_BTN_TEXT, COLOR_BTN_BG, COLOR_BTN_HOVER)

        self.btn_hit.set_enabled(False)
        self.btn_stand.set_enabled(False)
        self.btn_restart.set_enabled(False)

    def create_deck(self):
        suits = ['S','H','D','C']
        ranks = ['A'] + [str(i) for i in range(2,11)] + ['J','Q','K']
        deck = [Card(r,s) for s in suits for r in ranks]
        random.shuffle(deck)
        return deck

    def start_round(self):
        self.deck = self.create_deck()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.state = 'playing'
        self.message = "Sua vez: peça carta ou pare"
        self.message_color = COLOR_TEXT_SECONDARY
        self.btn_hit.set_enabled(True)
        self.btn_stand.set_enabled(True)
        self.btn_restart.set_enabled(False)

    def hand_value(self, hand):
        val=0
        aces=0
        for c in hand:
            val += c.value()
            if c.rank=='A': aces+=1
        while val>21 and aces>0:
            val -= 10
            aces -= 1
        return val

    def player_hit(self):
        if self.state != 'playing': return
        self.player_hand.append(self.deck.pop())
        val = self.hand_value(self.player_hand)
        if val > 21:
            self.end_round(False, "Você estourou! Perdeu a rodada.")
        elif val == 21:
            self.player_stand()

    def player_stand(self):
        if self.state != 'playing': return
        while self.hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
        self.compare_hands()

    def compare_hands(self):
        p = self.hand_value(self.player_hand)
        d = self.hand_value(self.dealer_hand)
        if d > 21:
            self.end_round(True, "Dealer estourou! Você ganhou!")
        elif d > p:
            self.end_round(False, "Dealer venceu. Você perdeu.")
        elif d < p:
            self.end_round(True, "Você venceu a rodada!")
        else:
            self.end_round(None, "Empate! Sua aposta foi devolvida.")

    def end_round(self, won, msg):
        self.state = 'round_end'
        self.message = msg
        if won is True:
            self.balance += self.bet
            self.message_color = COLOR_SUCCESS
        elif won is False:
            self.balance -= self.bet
            self.message_color = COLOR_ERROR
        else:
            self.message_color = COLOR_TEXT_SECONDARY
        self.bet = 0
        self.btn_hit.set_enabled(False)
        self.btn_stand.set_enabled(False)
        self.btn_restart.set_enabled(True)

    def reset(self):
        self.state = 'betting'
        self.message = "Faça sua aposta para começar"
        self.message_color = COLOR_TEXT_SECONDARY
        self.bet_input_text = ''
        self.error_msg = ''
        self.btn_hit.set_enabled(False)
        self.btn_stand.set_enabled(False)
        self.btn_restart.set_enabled(False)
        self.bet = 0

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.btn_bet.update(mouse_pos)
        self.btn_hit.update(mouse_pos)
        self.btn_stand.update(mouse_pos)
        self.btn_restart.update(mouse_pos)

        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == 'betting':
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.bet_input_active = self.bet_input_rect.collidepoint(e.pos)
                if e.type == pygame.KEYDOWN and self.bet_input_active:
                    if e.key == pygame.K_BACKSPACE:
                        self.bet_input_text = self.bet_input_text[:-1]
                    elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if self.btn_bet.enabled:
                            self.place_bet()
                    else:
                        if e.unicode.isdigit() and len(self.bet_input_text) < 7:
                            self.bet_input_text += e.unicode

            if self.btn_bet.handle_event(e):
                if self.btn_bet.enabled:
                    self.place_bet()
            if self.btn_hit.handle_event(e):
                self.player_hit()
            if self.btn_stand.handle_event(e):
                self.player_stand()
            if self.btn_restart.handle_event(e):
                self.reset()

        if self.state == 'betting':
            try:
                val = int(self.bet_input_text) if self.bet_input_text else 0
            except:
                val = 0
            valid = 0 < val <= self.balance and val <= MAX_BET
            self.btn_bet.set_enabled(valid)
            self.error_msg = '' if valid or self.bet_input_text == '' else "Aposta inválida ou maior que saldo"
        else:
            self.btn_bet.set_enabled(False)

    def place_bet(self):
        try:
            val = int(self.bet_input_text)
        except:
            self.error_msg = "Digite um valor válido"
            return
        if val < 1 or val > self.balance or val > MAX_BET:
            self.error_msg = "Aposta inválida ou maior que saldo"
            return
        self.bet = val
        self.bet_input_text = ''
        self.error_msg = ''
        self.start_round()

    def draw_center_text(self, surf, text, font, color, y):
        surf_text = font.render(text, True, color)
        rect = surf_text.get_rect(center=(WIDTH//2, y))
        surf.blit(surf_text, rect)

    def draw(self, surf):
        surf.fill(COLOR_BG)
        container_x = (WIDTH - MAX_CONTAINER_W) // 2

        # Título grande e ousado no topo
        self.draw_center_text(surf, 'Jogo 21 - Blackjack com Apostas', FONT_TITLE, COLOR_TEXT_PRIMARY, 70)

        # Container para aposta
        box_rect = pygame.Rect(container_x, 120, MAX_CONTAINER_W, 120)
        draw_rounded_rect_with_shadow(surf, box_rect, COLOR_CARD_BG)
        pygame.draw.rect(surf, COLOR_TEXT_SECONDARY, box_rect, 1, border_radius=RADIUS)

        # Texto saldo
        balance_text = f"Saldo: R$ {self.balance:.2f}"
        balance_surf = FONT_SUBTITLE.render(balance_text, True, COLOR_TEXT_PRIMARY)
        surf.blit(balance_surf, (box_rect.left + PADDING, box_rect.top + PADDING))

        # Caixa input aposta
        input_rect = self.bet_input_rect
        pygame.draw.rect(surf, COLOR_BG, input_rect, border_radius=RADIUS)
        border_color = COLOR_TEXT_SECONDARY if self.bet_input_active else (200, 200, 200)
        pygame.draw.rect(surf, border_color, input_rect, 2, border_radius=RADIUS)
        bet_text = self.bet_input_text if self.bet_input_text else "R$ 0"
        bet_surf = FONT_SUBTITLE.render(bet_text, True, COLOR_TEXT_PRIMARY)
        surf.blit(bet_surf, (input_rect.left + 12, input_rect.top + (input_rect.height - bet_surf.get_height()) // 2))

        # Mensagem de erro aposta
        if self.error_msg:
            err_surf = FONT_SMALL.render(self.error_msg, True, COLOR_ERROR)
            surf.blit(err_surf, (box_rect.left + PADDING, input_rect.bottom + 5))

        # Botão de apostar
        self.btn_bet.draw(surf)

        if self.state in ('playing', 'round_end'):
            cards_top = box_rect.bottom + 80

            # Área jogador
            label_jog = FONT_SUBTITLE.render("Suas cartas:", True, COLOR_TEXT_PRIMARY)
            surf.blit(label_jog, (container_x + PADDING, cards_top))

            # Desenha cartas do jogador
            start_x = container_x + PADDING
            y = cards_top + 35
            for i, card in enumerate(self.player_hand):
                card.draw(surf, (start_x + i * 70, y))

            player_total = self.hand_value(self.player_hand)
            total_surf = FONT_SUBTITLE.render(f"Total: {player_total}", True, COLOR_TEXT_PRIMARY)
            surf.blit(total_surf, (start_x, y + 95))

            # Área dealer
            label_dealer = FONT_SUBTITLE.render("Cartas da máquina:", True, COLOR_TEXT_PRIMARY)
            surf.blit(label_dealer, (container_x + MAX_CONTAINER_W // 2 + PADDING, cards_top))

            start_x_dealer = container_x + MAX_CONTAINER_W // 2 + PADDING
            y_dealer = y

            for i, card in enumerate(self.dealer_hand):
                card_pos = (start_x_dealer + i * 70, y_dealer)

                # Oculta a segunda carta do dealer enquanto jogando
                if self.state == 'playing' and i == 1:
                    oculto_rect = pygame.Rect(card_pos[0], card_pos[1], 60, 90)
                    pygame.draw.rect(surf, (230, 230, 230), oculto_rect, border_radius=RADIUS)
                    pygame.draw.rect(surf, (180, 180, 180), oculto_rect, 2, border_radius=RADIUS)
                else:
                    card.draw(surf, card_pos)

            dealer_text = f"Total: {self.hand_value(self.dealer_hand)}" if self.state == 'round_end' else "Total: ?"
            dealer_total_surf = FONT_SUBTITLE.render(dealer_text, True, COLOR_TEXT_SECONDARY)
            surf.blit(dealer_total_surf, (start_x_dealer, y_dealer + 95))

            # Mensagem status rodada
            msg_surf = FONT_SUBTITLE.render(self.message, True, self.message_color)
            msg_rect = msg_surf.get_rect(center=(WIDTH//2, y + 140))
            surf.blit(msg_surf, msg_rect)

            # Botões HIT e STAND
            self.btn_hit.draw(surf)
            self.btn_stand.draw(surf)

            if self.state == 'round_end':
                self.btn_restart.draw(surf)

    def run(self):
        while True:
            events = pygame.event.get()
            self.update(events)
            self.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    blackjack_game = BlackjackGame()
    blackjack_game.run()



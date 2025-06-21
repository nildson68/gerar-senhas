from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import random

KV = '''
<BlackjackWidget>:
    orientation: 'vertical'
    padding: dp(24)
    spacing: dp(24)
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # Fundo branco puro
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: self.minimum_height
        Label:
            text: "Jogo 21 - Blackjack com Apostas"
            font_size: '48sp'
            bold: True
            color: root.color_title
            halign: "left"
            valign: "middle"
            text_size: self.size
        Label:
            text: root.score_text
            font_size: '24sp'
            bold: True
            color: root.color_title
            halign: "right"
            valign: "middle"
            text_size: self.size

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: dp(140)
        padding: dp(20)
        spacing: dp(12)
        canvas.before:
            Color:
                rgba: 0.96, 0.96, 0.96, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [16,]

        Label:
            id: word_display
            text: root.current_message
            font_size: '22sp'
            color: root.current_message_color
            halign: 'center'
            valign: 'middle'
            text_size: self.size
            bold: True

    BoxLayout:
        size_hint_y: None
        height: dp(40)
        spacing: dp(16)

        TextInput:
            id: bet_input
            size_hint_x: 0.4
            multiline: False
            font_size: '22sp'
            halign: 'center'
            bold: True
            hint_text: "Valor da aposta"
            input_filter: 'int'
            disabled: root.game_active
            on_text: root.on_bet_text(self.text)

        Button:
            text: "Apostar"
            size_hint_x: 0.3
            font_size: '20sp'
            bold: True
            background_color: (0, 0, 0, 1) if root.can_place_bet else (0.7, 0.7, 0.7, 1)
            color: (1, 1, 1, 1)
            disabled: not root.can_place_bet
            on_release: root.place_bet()

        Button:
            text: "Reiniciar"
            size_hint_x: 0.3
            font_size: '20sp'
            bold: True
            background_color: (0, 0, 0, 1)
            color: (1, 1, 1, 1)
            on_release: root.restart()
            disabled: not root.round_over

    BoxLayout:
        spacing: dp(24)
        padding: dp(8), 0
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(8)
            Label:
                text: "Suas cartas:"
                font_size: '20sp'
                bold: True
                color: root.color_text_primary
            GridLayout:
                id: player_cards_layout
                cols: 6
                size_hint_y: None
                height: dp(100)
                spacing: dp(8)
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(8)
            Label:
                text: "Cartas da máquina:"
                font_size: '20sp'
                bold: True
                color: root.color_text_primary
            GridLayout:
                id: dealer_cards_layout
                cols: 6
                size_hint_y: None
                height: dp(100)
                spacing: dp(8)

    BoxLayout:
        size_hint_y: None
        height: dp(60)
        spacing: dp(24)
        Button:
            text: "Pedir Carta"
            font_size: '20sp'
            bold: True
            background_color: (0, 0, 0, 1) if root.can_hit else (0.7, 0.7, 0.7, 1)
            color: (1, 1, 1, 1)
            disabled: not root.can_hit
            on_release: root.hit()
        Button:
            text: "Parar"
            font_size: '20sp'
            bold: True
            background_color: (0, 0, 0, 1) if root.can_stand else (0.7, 0.7, 0.7, 1)
            color: (1, 1, 1, 1)
            disabled: not root.can_stand
            on_release: root.stand()

    BoxLayout:
        size_hint_y: None
        height: dp(30)
        Label:
            text: root.balance_text
            font_size: '18sp'
            bold: True
            color: root.color_text_secondary
            halign: "center"
            valign: "middle"
            text_size: self.size
'''

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

class CardWidget(Label):
    def __init__(self, rank, suit, **kwargs):
        super().__init__(**kwargs)
        self.rank = rank
        self.suit = suit
        self.size_hint = (None, None)
        self.size = (60, 90)
        self.font_size = '36sp'
        self.bold = True
        self.halign = 'center'
        self.valign = 'middle'
        self.color = (0.86, 0.08, 0.24, 1) if suit in ('♥', '♦') else (0, 0, 0, 1)
        self.text = f"{rank}\n{suit}"
        self.text_size = self.size
        self.markup = False

class BlackjackWidget(BoxLayout):
    current_message = StringProperty("Faça sua aposta para começar")
    current_message_color = ColorProperty((0.42, 0.44, 0.5, 1))
    score_text = StringProperty("Saldo: R$ 1000")
    color_title = ColorProperty((0.12, 0.16, 0.22, 1))
    color_text_primary = ColorProperty((0.12, 0.16, 0.22, 1))
    color_text_secondary = ColorProperty((0.42, 0.44, 0.5, 1))
    game_active = BooleanProperty(False)
    can_place_bet = BooleanProperty(False)
    can_hit = BooleanProperty(False)
    can_stand = BooleanProperty(False)
    round_over = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.balance = 1000
        self.bet = 0
        self.deck = []
        self.player_hand = []
        self.dealer_hand = []
        self.ids.bet_input.bind(text=self.on_text_change)
        self._reset()

    def _reset(self):
        self.can_place_bet = False
        self.can_hit = False
        self.can_stand = False
        self.round_over = False
        self.bet = 0
        self.game_active = False
        self.current_message = "Faça sua aposta para começar"
        self.current_message_color = (0.42, 0.44, 0.5, 1)
        self.update_balance()
        self._clear_cards()

    def _clear_cards(self):
        self.ids.player_cards_layout.clear_widgets()
        self.ids.dealer_cards_layout.clear_widgets()

    def update_balance(self):
        self.score_text = f"Saldo: R$ {self.balance:.2f}"

    def on_text_change(self, instance, value):
        try:
            bet_value = int(value)
            self.can_place_bet = (bet_value > 0 and bet_value <= self.balance)
        except:
            self.can_place_bet = False

    def place_bet(self):
        try:
            bet_value = int(self.ids.bet_input.text)
            if bet_value > 0 and bet_value <= self.balance:
                self.bet = bet_value
                self.ids.bet_input.text = ''
                self.start_round()
            else:
                self.current_message = "Aposta inválida"
                self.current_message_color = (1, 0, 0, 1)
        except:
            self.current_message = "Aposta inválida"
            self.current_message_color = (1, 0, 0, 1)

    def create_deck(self):
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['A'] + [str(i) for i in range(2, 11)] + ['J', 'Q', 'K']
        deck = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(deck)
        return deck

    def start_round(self):
        self.deck = self.create_deck()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.game_active = True
        self.can_place_bet = False
        self.can_hit = True
        self.can_stand = True
        self.round_over = False
        self.current_message = "Sua vez: peça carta ou pare"
        self.current_message_color = self.color_text_secondary
        self._show_hands(hide_dealer_second=True)

    def _show_hands(self, hide_dealer_second=False):
        self._clear_cards()
        for rank, suit in self.player_hand:
            self.ids.player_cards_layout.add_widget(CardWidget(rank, suit))
        for i, (rank, suit) in enumerate(self.dealer_hand):
            if i == 1 and hide_dealer_second:
                card = CardWidget("?", "?")
                card.color = (0.7, 0.7, 0.7, 1)
                self.ids.dealer_cards_layout.add_widget(card)
            else:
                self.ids.dealer_cards_layout.add_widget(CardWidget(rank, suit))

    def hand_value(self, hand):
        value = 0
        aces = 0
        for rank, suit in hand:
            if rank in ['J','Q','K']:
                value += 10
            elif rank == 'A':
                value += 11
                aces += 1
            else:
                try:
                    value += int(rank)
                except:
                    value += 0
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        return value

    def hit(self):
        if not self.game_active:
            return
        self.player_hand.append(self.deck.pop())
        self._show_hands(hide_dealer_second=True)
        val = self.hand_value(self.player_hand)
        if val > 21:
            self.end_round(False, "Você estourou! Perdeu a rodada.")
        elif val == 21:
            self.stand()

    def stand(self):
        if not self.game_active:
            return
        while self.hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
        self._show_hands(hide_dealer_second=False)
        self.compare_hands()

    def compare_hands(self):
        p_val = self.hand_value(self.player_hand)
        d_val = self.hand_value(self.dealer_hand)
        if d_val > 21:
            self.end_round(True, "Dealer estourou! Você ganhou!")
        elif d_val > p_val:
            self.end_round(False, "Dealer venceu. Você perdeu.")
        elif d_val < p_val:
            self.end_round(True, "Você venceu a rodada!")
        else:
            self.end_round(None, "Empate! Sua aposta foi devolvida.")

    def end_round(self, player_win, message):
        self.game_active = False
        self.can_hit = False
        self.can_stand = False
        self.round_over = True
        self.current_message = message
        if player_win is True:
            self.balance += self.bet
            self.current_message_color = (0.09, 0.62, 0.15, 1) # verde
        elif player_win is False:
            self.balance -= self.bet
            self.current_message_color = (0.86, 0.15, 0.15, 1) # vermelho
        else:
            self.current_message_color = self.color_text_secondary
        self.update_balance()

    def restart(self):
        self._reset()
        self._clear_cards()

class BlackjackApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return Builder.load_string(KV, filename="blackjack.kv").instantiate(rootclass=BlackjackWidget)

if __name__ == "__main__":
    BlackjackApp().run()


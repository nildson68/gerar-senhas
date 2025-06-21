from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
import random

KV = '''
<ForcaWidget>:
    orientation: 'vertical'
    padding: dp(24)
    spacing: dp(24)
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1  # fundo branco
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: self.minimum_height
        Label:
            text: "Jogo da Forca"
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
            text: root.display_word
            font_size: '40sp'
            bold: True
            color: root.color_text
            halign: 'center'
            valign: 'middle'
            text_size: self.size

        Label:
            id: message_label
            text: root.message
            font_size: '18sp'
            color: root.message_color
            halign: 'center'
            valign: 'middle'
            text_size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(60)
        spacing: dp(16)

        TextInput:
            id: input_letter
            size_hint_x: 0.4
            multiline: False
            font_size: '28sp'
            halign: 'center'
            bold: True
            hint_text: "Digite uma letra"
            max_text_length: 1
            write_tab: False
            on_text_validate: root.process_guess()
            on_text:
                if len(self.text) > 1: self.text = self.text[:1]
            input_filter: 'str'
            disabled: root.game_over

        Button:
            text: "Enviar"
            size_hint_x: 0.3
            font_size: '20sp'
            bold: True
            background_color: (0.1, 0.1, 0.1, 1)
            color: (1, 1, 1, 1)
            disabled: root.game_over or not input_letter.text
            on_release: root.process_guess()

        Button:
            text: "Reiniciar"
            size_hint_x: 0.3
            font_size: '20sp'
            bold: True
            background_color: (0.9, 0.9, 0.9, 1)
            color: (0.1, 0.1, 0.1, 1)
            on_release: root.restart_game()

    BoxLayout:
        size_hint_y: None
        height: dp(60)
        padding: dp(12)
        spacing: dp(20)
        canvas.before:
            Color:
                rgba: 0.96, 0.96, 0.96, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [16,]

        Label:
            text: "[b]Letras usadas:[/b] " + root.guessed_letters_text
            markup: True
            font_size: '18sp'
            color: root.color_secondary
            halign: 'left'
            valign: 'middle'
            text_size: self.size

        Label:
            text: "[b]Tentativas restantes:[/b] " + str(root.tries_left)
            markup: True
            font_size: '18sp'
            color: root.color_secondary
            halign: 'right'
            valign: 'middle'
            text_size: self.size
'''

class ForcaWidget(BoxLayout):
    word_list = [
        "python", "programacao", "jogo", "computador", "desenvolvedor",
        "teclado", "monitor", "mouse", "janela", "sistema", "desafio",
        "codigo", "linguagem", "variavel", "funcao", "interface"
    ]

    current_word = StringProperty("")
    display_word = StringProperty("")
    guessed_letters = ListProperty([])
    guessed_letters_text = StringProperty("-")
    tries_left = NumericProperty(6)
    max_tries = 6
    score = NumericProperty(0)
    score_text = StringProperty("Pontuação: 0")
    message = StringProperty("Digite uma letra e pressione Enter")
    message_color = ColorProperty([0.4, 0.4, 0.5, 1])  # cinza neutro
    game_over = BooleanProperty(False)

    color_title = ColorProperty([31/255, 41/255, 55/255, 1])
    color_text = ColorProperty([31/255, 41/255, 55/255, 1])
    color_secondary = ColorProperty([107/255, 114/255, 128/255, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._start_game()

    def _start_game(self):
        self.current_word = random.choice(self.word_list).lower()
        self.guessed_letters = []
        self.tries_left = self.max_tries
        self.score = 0
        self.score_text = f"Pontuação: {self.score}"
        self.game_over = False
        self.message = "Digite uma letra e pressione Enter"
        self.message_color = [0.4, 0.4, 0.5, 1]
        self._update_display_word()
        self._update_guessed_letters_text()

    def restart_game(self):
        self.current_word = random.choice(self.word_list).lower()
        self.guessed_letters = []
        self.tries_left = self.max_tries
        self.game_over = False
        self.message = "Jogo reiniciado! Digite uma letra e pressione Enter"
        self.message_color = [0.4, 0.4, 0.5, 1]
        self.score = 0
        self.score_text = f"Pontuação: {self.score}"
        self.ids.input_letter.text = ""
        self._update_display_word()
        self._update_guessed_letters_text()

    def _update_display_word(self):
        revealed = [l.upper() if l in self.guessed_letters else "_" for l in self.current_word]
        self.display_word = " ".join(revealed)

    def _update_guessed_letters_text(self):
        if self.guessed_letters:
            self.guessed_letters_text = ", ".join(letter.upper() for letter in sorted(self.guessed_letters))
        else:
            self.guessed_letters_text = "-"

    def process_guess(self):
        if self.game_over:
            return
        guess = self.ids.input_letter.text.lower().strip()
        self.ids.input_letter.text = ""
        if not guess or len(guess) != 1 or not guess.isalpha():
            self.message = "[color=#dc2626][b]Digite apenas uma letra válida![/b][/color]"
            self.message_color = [0.86, 0.15, 0.15, 1]
            return
        if guess in self.guessed_letters:
            self.message = f"[color=#dc2626]Letra '{guess.upper()}' já foi tentada![/color]"
            self.message_color = [0.86, 0.15, 0.15, 1]
            return

        self.guessed_letters.append(guess)
        self._update_guessed_letters_text()

        if guess in self.current_word:
            self.message = f"[color=#22c55e]Boa! A letra '{guess.upper()}' está na palavra.[/color]"
            self.message_color = [0.13, 0.77, 0.37, 1]
            self._update_display_word()
            if all(l in self.guessed_letters for l in self.current_word):
                self.score += 1
                self.score_text = f"Pontuação: {self.score}"
                self.message = f"[color=#22c55e]Parabéns! Você acertou a palavra '{self.current_word.upper()}'. Pressione Reiniciar para jogar novamente.[/color]"
                self.message_color = [0.13, 0.77, 0.37, 1]
                self.game_over = True
        else:
            self.tries_left -= 1
            if self.tries_left <= 0:
                self.message = f"[color=#dc2626]Fim de jogo! A palavra era: '{self.current_word.upper()}'. Pressione Reiniciar para tentar outra vez.[/color]"
                self.message_color = [0.86, 0.15, 0.15, 1]
                self.game_over = True
            else:
                self.message = f"[color=#dc2626]Letra '{guess.upper()}' não está na palavra. Tentativas restantes: {self.tries_left}[/color]"
                self.message_color = [0.86, 0.15, 0.15, 1]

class ForcaApp(App):
    def build(self):
        return Builder.load_string(KV, filename="forca.kv").instantiate(rootclass=ForcaWidget)

if __name__ == "__main__":
    ForcaApp().run()



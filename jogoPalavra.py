import pygame
import random
import sys

pygame.init()

# Constantes
LARGURA_JANELA, ALTURA_JANELA = 800, 600
FPS = 60
MAX_TENTATIVAS = 5
MAX_WIDTH_CONTAINER = 600  # Limitar largura do conteúdo para efeito de container central

# Cores seguindo as guidelines
COR_FUNDO = (255, 255, 255)  # Branco puro
COR_TITULO = (31, 41, 55)  # #1f2937 - cinza escuro para título (quase preto)
COR_TEXTO = (107, 114, 128)  # #6b7280 cinza neutro para textos
COR_SOMBRA_SUAVE = (220, 220, 220)
COR_BG_INPUT = (245, 245, 245)
COR_BORDA_INPUT = (203, 213, 225)  # cinza claro para borda input
COR_BORDA_INPUT_FOCUS = (147, 197, 253)  # azul claro para foco
COR_TEXTO_INPUT = (31, 41, 55)
COR_ACERTO = (34, 197, 94)  # verde
COR_ERRO = (220, 38, 38)  # vermelho intenso
COR_MENSAGEM = (75, 85, 99)  # cinza médio

# Fontes
# Pygame não tem Poppins embutido, usa system font sans serif para simular moderna e limpa
FONTE_TITULO = pygame.font.SysFont("Segoe UI", 56, bold=True)
FONTE_SUBTITULO = pygame.font.SysFont("Segoe UI", 24)
FONTE_TEXTO = pygame.font.SysFont("Segoe UI", 20)
FONTE_INPUT = pygame.font.SysFont("Segoe UI", 26)
FONTE_MENOR = pygame.font.SysFont("Segoe UI", 16)

# Lista de palavras
PALAVRAS = [
    "python", "pygame", "desktop", "jogo", "adivinhar", "desafio", "pontuacao",
    "jogador", "entrada", "aleatorio", "teclado", "tela", "janela", "adivinhacao",
    "palavras", "logica", "codigo", "desenvolvedor", "computador"
]

# Dicionário de dicas: palavra -> dica curta
DICAS = {
    "python": "Uma linguagem de programação muito popular.",
    "pygame": "Biblioteca para jogos em Python.",
    "desktop": "Tipo de computador com monitor e teclado.",
    "jogo": "Atividade para diversão e desafio.",
    "adivinhar": "Tentar descobrir algo sem saber.",
    "desafio": "Algo difícil que exige esforço.",
    "pontuacao": "Total de pontos conquistados.",
    "jogador": "Quem participa do jogo.",
    "entrada": "Lugar onde você digita ou insere dados.",
    "aleatorio": "Algo feito sem padrão definido.",
    "teclado": "Dispositivo para digitar letras.",
    "tela": "Mostrador de imagens e vídeos.",
    "janela": "Área da interface que mostra conteúdo.",
    "adivinhacao": "Ato de tentar descobrir algo oculto.",
    "palavras": "Conjunto de letras formando sentido.",
    "logica": "Raciocínio coerente e estruturado.",
    "codigo": "Conjunto de instruções para computadores.",
    "desenvolvedor": "Quem cria software e apps.",
    "computador": "Máquina para processar dados e informação."
}

tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption("Jogo de Adivinhação de Palavras")

clock = pygame.time.Clock()

def desenhar_retangulo_arredondado(superficie, retangulo, cor, raio=12):
    """Desenha retângulo com cantos arredondados."""
    x, y, largura, altura = retangulo
    pygame.draw.rect(superficie, cor, (x + raio, y, largura - 2 * raio, altura))
    pygame.draw.rect(superficie, cor, (x, y + raio, largura, altura - 2 * raio))
    pygame.draw.circle(superficie, cor, (x + raio, y + raio), raio)
    pygame.draw.circle(superficie, cor, (x + largura - raio, y + raio), raio)
    pygame.draw.circle(superficie, cor, (x + raio, y + altura - raio), raio)
    pygame.draw.circle(superficie, cor, (x + largura - raio, y + altura - raio), raio)

def main():
    pontuacao = 0
    tentativas_restantes = MAX_TENTATIVAS
    palavra_atual = random.choice(PALAVRAS)
    palpite = ""
    jogo_finalizado = False
    mensagem_info = "Digite seu palpite e pressione Enter"
    foco_input = True  # sempre focado para digitar

    while True:
        tela.fill(COR_FUNDO)

        # Container centralizado para o conteúdo
        container_x = (LARGURA_JANELA - MAX_WIDTH_CONTAINER) // 2

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not jogo_finalizado:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_BACKSPACE:
                        palpite = palpite[:-1]
                    elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        # Enviar palpite
                        if palpite.lower() == palavra_atual:
                            pontuacao += 1
                            mensagem_info = "✔ Acertou! Uma nova palavra foi escolhida."
                            palavra_atual = random.choice(PALAVRAS)
                            tentativas_restantes = MAX_TENTATIVAS
                            palpite = ""
                        else:
                            tentativas_restantes -= 1
                            if tentativas_restantes == 0:
                                jogo_finalizado = True
                                mensagem_info = f"✘ Fim de jogo! Sua pontuação final foi: {pontuacao}"
                            else:
                                mensagem_info = f"✘ Errou! Tente novamente. Tentativas restantes: {tentativas_restantes}"
                            palpite = ""
                    else:
                        # Aceitar apenas letras
                        if evento.unicode.isalpha() and len(palpite) < 20:
                            palpite += evento.unicode.lower()
            else:
                # Fim de jogo - reiniciar ou sair
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        pontuacao = 0
                        tentativas_restantes = MAX_TENTATIVAS
                        palavra_atual = random.choice(PALAVRAS)
                        palpite = ""
                        jogo_finalizado = False
                        mensagem_info = "Jogo reiniciado! Digite seu palpite e pressione Enter"
                    elif evento.key in (pygame.K_q, pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()

        # Título principal - fonte bold e tamanho grande
        titulo_surf = FONTE_TITULO.render("Jogo de Adivinhação", True, COR_TITULO)
        tela.blit(titulo_surf, (container_x, 40))

        subtitulo_surf = FONTE_SUBTITULO.render("Tente adivinhar a palavra. Você tem 5 tentativas para cada palavra.", True, COR_TEXTO)
        tela.blit(subtitulo_surf, (container_x, 110))

        # Áreas de pontuação e tentativas lado a lado
        pontuacao_surf = FONTE_TEXTO.render(f"Pontuação: {pontuacao}", True, COR_TITULO)
        tentativa_surf = FONTE_TEXTO.render(f"Tentativas restantes: {tentativas_restantes}", True, COR_TITULO)

        tela.blit(pontuacao_surf, (container_x, 160))
        tela.blit(tentativa_surf, (container_x + 350, 160))

        # Caixa de entrada do palpite com sombra sutil e cantos arredondados
        input_rect = pygame.Rect(container_x, 220, MAX_WIDTH_CONTAINER, 60)
        sombra_rect = input_rect.move(4, 4)
        desenhar_retangulo_arredondado(tela, sombra_rect, COR_SOMBRA_SUAVE)
        desenhar_retangulo_arredondado(tela, input_rect, COR_BG_INPUT)

        # Borda do input muda se focado (simples, consideramos sempre focado)
        pygame.draw.rect(tela, COR_BORDA_INPUT_FOCUS, input_rect, 2, border_radius=12)

        texto_palpite = palpite if palpite else "Digite seu palpite..."
        palpite_surf = FONTE_INPUT.render(texto_palpite, True, COR_TEXTO_INPUT if palpite else COR_TEXTO)
        palpite_rect = palpite_surf.get_rect(midleft=(input_rect.left + 15, input_rect.centery))
        tela.blit(palpite_surf, palpite_rect)

        # Card da dica abaixo do input
        dica_card_rect = pygame.Rect(container_x, input_rect.bottom + 20, MAX_WIDTH_CONTAINER, 100)
        desenhar_retangulo_arredondado(tela, dica_card_rect, COR_BG_INPUT)
        pygame.draw.rect(tela, COR_BORDA_INPUT, dica_card_rect, 1, border_radius=12)

        dica_titulo_surf = FONTE_TEXTO.render("Dica:", True, COR_TITULO)
        tela.blit(dica_titulo_surf, (dica_card_rect.left + 15, dica_card_rect.top + 15))

        dica_texto = DICAS.get(palavra_atual, "Sem dica disponível.")
        dica_texto_surf = FONTE_TEXTO.render(dica_texto, True, COR_TEXTO)
        tela.blit(dica_texto_surf, (dica_card_rect.left + 15, dica_card_rect.top + 50))

        # Mensagem informativa abaixo da dica
        cor_mensagem = COR_ACERTO if "✔" in mensagem_info else (COR_ERRO if "✘" in mensagem_info else COR_MENSAGEM)
        mensagem_surf = FONTE_TEXTO.render(mensagem_info, True, cor_mensagem)
        tela.blit(mensagem_surf, (container_x, dica_card_rect.bottom + 20))

        # Instruções e fim de jogo
        if jogo_finalizado:
            instr_final_surf = FONTE_MENOR.render("Pressione 'R' para reiniciar ou 'Q' / ESC para sair", True, COR_ERRO)
            tela.blit(instr_final_surf, (container_x, dica_card_rect.bottom + 60))
        else:
            instr_surf = FONTE_MENOR.render("Use o teclado para digitar. Enter para enviar. Backspace para deletar.", True, COR_TEXTO)
            tela.blit(instr_surf, (container_x, dica_card_rect.bottom + 60))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()






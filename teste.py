import pygame
import time
import random

# Inicializa o Pygame
pygame.init()

# Define as cores
branco = (255, 255, 255)
preto = (0, 0, 0)
verde = (0, 255, 0)
vermelho = (213, 50, 80)
azul = (50, 153, 213)
rosa = (213, 50, 190)  # Cor da moldura

# Define o tamanho da tela
largura_tela = 800
altura_tela = 800

# Cria a tela
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Jogo da Cobrinha')

# Define o clock para controlar a taxa de quadros
clock = pygame.time.Clock()
velocidade_cobrinha = 38

# Fonte para o texto
fonte = pygame.font.SysFont(None, 35)
fonte_fps = pygame.font.SysFont(None, 25)  # Fonte para o contador de FPS

def nossa_cobrinha(tamanho_cobra, lista_cobra):
    for x in lista_cobra:
        pygame.draw.rect(tela, verde, [x[0], x[1], tamanho_cobra, tamanho_cobra])

def mensagem(msg, cor_texto, cor_fundo):
    linhas = msg.split('\n')  # Divide a mensagem em linhas
    y_offset = 0  # Offset inicial para desenhar a primeira linha

    # Calcula a largura e altura do retângulo de fundo
    largura_maxima = max(fonte.size(linha)[0] for linha in linhas)  # Largura da maior linha
    altura_total = len(linhas) * fonte.get_height()  # Altura total do retângulo

    # Define a posição do retângulo
    x_fundo = largura_tela / 6 - 10  # Adiciona uma margem de 10 pixels
    y_fundo = altura_tela / 3 - 10  # Adiciona uma margem de 10 pixels

    # Desenha o retângulo de fundo
    pygame.draw.rect(tela, cor_fundo, [x_fundo, y_fundo, largura_maxima + 20, altura_total + 20])  # Margens adicionais

    # Desenha o texto sobre o retângulo
    for linha in linhas:
        texto = fonte.render(linha, True, cor_texto)
        tela.blit(texto, [x_fundo + 10, y_fundo + y_offset + 10])  # Adiciona margens internas
        y_offset += fonte.get_height()  # Atualiza o offset para a próxima linha

def desenhar_moldura():
    espessura_moldura = 10
    pygame.draw.rect(tela, rosa, [0, 0, largura_tela, altura_tela], espessura_moldura)

def mostrar_fps(fps):
    texto_fps = fonte_fps.render(f"FPS: {int(fps)}", True, branco)
    tela.blit(texto_fps, [10, 10])  # Exibe o FPS no canto superior esquerdo

def jogo():
    game_over = False
    game_close = False

    x1 = largura_tela / 2
    y1 = altura_tela / 2

    x1_mudanca = 0
    y1_mudanca = 0

    tamanho_cobra = 10
    lista_cobra = []
    comprimento_cobra = 1

    comida_x = round(random.randrange(0, largura_tela - tamanho_cobra) / 10.0) * 10.0
    comida_y = round(random.randrange(0, altura_tela - tamanho_cobra) / 10.0) * 10.0

    while not game_over:
        while game_close:
            tela.fill(azul)  # Limpa a tela com a cor de fundo
            mensagem("Você perdeu!\nPressione Q para Sair\nou C para Jogar Novamente", vermelho, preto)
            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if evento.key == pygame.K_c:
                        jogo()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                game_over = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    x1_mudanca = -tamanho_cobra
                    y1_mudanca = 0
                elif evento.key == pygame.K_RIGHT:
                    x1_mudanca = tamanho_cobra
                    y1_mudanca = 0
                elif evento.key == pygame.K_UP:
                    y1_mudanca = -tamanho_cobra
                    x1_mudanca = 0
                elif evento.key == pygame.K_DOWN:
                    y1_mudanca = tamanho_cobra
                    x1_mudanca = 0

        if x1 >= largura_tela or x1 < 0 or y1 >= altura_tela or y1 < 0:
            game_close = True
        x1 += x1_mudanca
        y1 += y1_mudanca
        tela.fill(azul)
        desenhar_moldura()  # Desenha a moldura

        pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho_cobra, tamanho_cobra])
        lista_cobra.append([x1, y1])
        if len(lista_cobra) > comprimento_cobra:
            del lista_cobra[0]

        for x in lista_cobra[:-1]:
            if x == [x1, y1]:
                game_close = True

        nossa_cobrinha(tamanho_cobra, lista_cobra)

        # Mostrar FPS
        fps = clock.get_fps()
        mostrar_fps(fps)

        pygame.display.update()

        if x1 == comida_x and y1 == comida_y:
            comida_x = round(random.randrange(0, largura_tela - tamanho_cobra) / 10.0) * 10.0
            comida_y = round(random.randrange(0, altura_tela - tamanho_cobra) / 10.0) * 10.0
            comprimento_cobra += 1

        clock.tick(velocidade_cobrinha)

    pygame.quit()
    quit()

# Inicia o jogo
jogo()

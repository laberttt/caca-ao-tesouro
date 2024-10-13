import pygame
import random
import cores

# Inicialização do Pygame e cores
pygame.init()
preto = (0, 0, 0)
branco = (255, 255, 255)
fonte = pygame.font.SysFont("Comic Sans MS", 30)

# Definições da tela e das células
largura_tela = 800
altura_tela = 600
lado_celula = 50
altura_indicador = 50
altura_score = 50
num_linhas = 4
num_colunas = 4
lado_celula_largura = largura_tela // num_colunas
altura_tabuleiro = altura_tela - altura_indicador - altura_score
lado_celula_altura = altura_tabuleiro // num_linhas # espaço para o score

# Resolução da tela
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Caça ao Tesouro")

# Carrega a imagem de fundo
imagem_de_fundo = pygame.image.load("images/background_jogo.jpg")
imagem_de_fundo = pygame.transform.scale(imagem_de_fundo, (largura_tela, altura_tela)) # Ajusta o tamanho conforme necessário

# Carrega a imagem do tesouro
imagem_tesouro = pygame.image.load("images/tesouro.png")
imagem_tesouro = pygame.transform.scale(imagem_tesouro, (lado_celula - 2, lado_celula - 2))  # Ajusta o tamanho conforme necessário

# Carrega a imagem do tesouro
imagem_buraco = pygame.image.load("images/buraco.png")
imagem_buraco = pygame.transform.scale(imagem_buraco, (lado_celula - 2, lado_celula - 2))  # Ajusta o tamanho conforme necessário

# Tela inicial
tela.blit(imagem_de_fundo, (0, 0))

# Tabuleiro de 16 células (4 x 4)
matriz = [[None]*4 for _ in range(4)]
for i in range(num_linhas):
    for j in range(num_colunas):
        matriz[i][j] = pygame.draw.rect(tela, branco, (i * lado_celula_largura, j * lado_celula_altura, lado_celula_largura, lado_celula_altura), 1)
pygame.display.update()

# Criando o tabuleiro virtual cujos elementos correspondem a um tesouro ('T')
conteudo_celula = [[None for _ in range(num_linhas)] for _ in range(num_colunas)]

# Marca com 'T' exatamente 6 células
num_tesouros = 0
max_tesouros = 6  # Número desejado de tesouros
while num_tesouros < max_tesouros:
    i = random.randint(0, num_linhas - 1)
    j = random.randint(0, num_colunas - 1)
    if conteudo_celula[i][j] is None:
        conteudo_celula[i][j] = "T"
        num_tesouros += 1
        
# Marca com 'B' exatamente 3 células
num_buracos = 0
max_buracos = 3
while num_buracos < max_buracos:
    i = random.randint(0, num_linhas - 1)
    j = random.randint(0, num_colunas - 1)
    if conteudo_celula[i][j] is None:
        conteudo_celula[i][j] = "B"
        num_buracos += 1

# Calcula o número de tesouros ao redor das células
for i in range(num_linhas):
    for j in range(num_colunas):
        if conteudo_celula[i][j] not in ["T", "B"]:
            tesouros_redor = 0

            # Verifica a célula acima
            if i > 0 and conteudo_celula[i-1][j] == "T":
                tesouros_redor += 1

            # Verifica a célula abaixo
            if i < num_linhas - 1 and conteudo_celula[i+1][j] == "T":
                tesouros_redor += 1

            # Verifica a célula à esquerda
            if j > 0 and conteudo_celula[i][j-1] == "T":
                tesouros_redor += 1

            # Verifica a célula à direita
            if j < num_colunas - 1 and conteudo_celula[i][j+1] == "T":
                tesouros_redor += 1

            conteudo_celula[i][j] = tesouros_redor



# Cria uma matriz para controlar a visualização do conteúdo das células
celula_revelada = [[False for _ in range(num_linhas)] for _ in range(num_colunas)]
jogo_cancelado = False

# Variaveis para os jogadores
score_jogador1 = 0
score_jogador2 = 0
turno_jogador1 = True # Se caso for False significa que é o segundo jogador

# Dsenha o score e o indicador de turno inicialmente
tela.blit(imagem_de_fundo, (0, 0))

# Desenha o tabuleiro
for i in range(num_linhas):
    for j in range(num_colunas):
        pygame.draw.rect(tela, branco, (i * lado_celula_largura, j * lado_celula_altura, lado_celula_largura, lado_celula_altura), 1)

# Mostra o score na parte inferior da tela
texto_score_jogador1 = fonte.render(f"Jogador 1: {score_jogador1}", True, branco)
texto_score_jogador2 = fonte.render(f"Jogador 2: {score_jogador2}", True, branco)
tela.blit(texto_score_jogador1, (0, altura_tela - altura_score - altura_indicador))
tela.blit(texto_score_jogador2, (largura_tela // 2, altura_tela - altura_score - altura_indicador))

# Desenha o indicador de turno
if turno_jogador1:
    texto_turno = fonte.render("Vez do Jogador 1", True, branco)
else:
    texto_turno = fonte.render("Vez do Jogador 2", True, branco)
tela.blit(texto_turno, (largura_tela // 2 - texto_turno.get_width() // 2, altura_tela - altura_indicador))

pygame.display.update()

# Laço do jogo
while not jogo_cancelado:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_cancelado = True
            break

        # Tela só será atualizada quando tela_mudou for igual a True
        tela_mudou = False
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            # Pega as coordenadas do ponto de clique e calcula a célula
            mouse_x, mouse_y = evento.pos
            celula_x = mouse_x // lado_celula_largura
            celula_y = mouse_y // lado_celula_altura

            # Clicou fora do tabuleiro
            if celula_y > num_linhas - 1:
                continue  # segue para o próximo evento

            # Entra no if se a célula foi clicada pela primeira vez
            if not celula_revelada[celula_x][celula_y]:
                tela_mudou = True
                celula_revelada[celula_x][celula_y] = True
                # Atualiza o score se encontrar um tesouro
                if conteudo_celula[celula_x][celula_y] == "T":
                    if turno_jogador1:
                        score_jogador1 += 100
                    else:
                        score_jogador2 += 100
                elif conteudo_celula[celula_x][celula_y] == "B":
                    if turno_jogador1:
                        score_jogador1 -= 50
                    else:
                        score_jogador2 -= 50
                        
                turno_jogador1 = not turno_jogador1

        if tela_mudou:
            # Desenha a imagem de fundo a cada atualização
            tela.blit(imagem_de_fundo, (0, 0))

            # Desenha o tabuleiro
            for i in range(num_linhas):
                for j in range(num_colunas):
                    if celula_revelada[i][j]:
                        if conteudo_celula[i][j] == "T":
                            # Mostrar tesouro
                            tela.blit(imagem_tesouro, (i * lado_celula_largura + 1, j * lado_celula_altura + 1))
                        elif conteudo_celula[i][j] == "B":
                            # Mostrar tesouro
                            tela.blit(imagem_buraco, (i * lado_celula_largura + 1, j * lado_celula_altura + 1))
                        else:
                            # Mostrar número de tesouros ao redor
                            texto_numero = fonte.render(str(conteudo_celula[i][j]), True, cores.WHITE)
                            tela.blit(texto_numero, (i * lado_celula_largura + 0.4 * lado_celula_largura, j * lado_celula_altura + 0.4 * lado_celula_altura))
                    # Desenha o retângulo da célula
                    pygame.draw.rect(tela, branco, (i * lado_celula_largura, j * lado_celula_altura, lado_celula_largura, lado_celula_altura), 1)

            # Mostra o score na parte inferior da tela
            texto_score_jogador1 = fonte.render(f"Jogador 1: {score_jogador1}", True, cores.WHITE)
            texto_score_jogador2 = fonte.render(f"Jogador 2: {score_jogador2}", True, cores.WHITE)
            tela.blit(texto_score_jogador1, (0, altura_tela - altura_score - altura_indicador))
            tela.blit(texto_score_jogador2, (largura_tela // 2, altura_tela - altura_score - altura_indicador))
            
            # Desenha indicador de turno
            if turno_jogador1:
                texto_turno = fonte.render("Vez do Jogador 1", True, cores.WHITE)
            else:
                texto_turno = fonte.render("Vez do Jogador 2", True, cores.WHITE)
                
            tela.blit(texto_turno, (largura_tela // 2 - texto_turno.get_width() // 2, altura_tela - altura_indicador))
            
            pygame.display.update()

pygame.quit()
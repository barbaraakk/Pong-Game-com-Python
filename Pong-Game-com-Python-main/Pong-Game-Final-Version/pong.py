import pygame
import sys
from pygame.locals import *
from backend.geral.config import *
from backend.modelo.jogador import Jogador
from backend.modelo.jogadorE import JogadorE


pygame.init()

#carrega o jogador
app.app_context().push()
jogador = db.session.query(Jogador).first()
jogadorE = db.session.query(JogadorE).first()

#Define o tamanho da janela.
WIDTH, HEIGHT = 700, 500
JANELA = pygame.display.set_mode((WIDTH, HEIGHT))

#Coloca um nome a janela.
pygame.display.set_caption("Pong")

def get_font(size):
    return pygame.font.Font("comicsans", size)
 
#Define o FPS
FPS = 60
clock = pygame.time.Clock()

#Define as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FIGURA_WIDTH, FIGURA_HEIGHT= 20, 100
BOLA_RADIUS = 7
 
SCORE_FONT = pygame.font.SysFont("comicsans", 40)

SCORE_VENCEDOR = 5

imagem = {}


#background image
background = pygame.image.load('Pong-Game-Final-Version/back.png')
background = pygame.transform.scale(background, (700, 500))
'''backgroundWidth = background.get_width()
backgroundHeight = background.get_height()
count = 1
while backgroundWidth < WIDTH and backgroundHeight < HEIGHT:
        backgroundWidth = background.get_width()*count
        backgroundHeight = background.get_height()*count
        count+=0.1
while backgroundWidth > WIDTH and backgroundHeight > HEIGHT:
        backgroundWidth = background.get_width()/count
        backgroundHeight = background.get_height()/count
        count+=0.1
background = pygame.transform.scale(background, (backgroundWidth, backgroundHeight))'''

class Figura:
    COLOR = WHITE
    VEL = 5

    #especifica a posição e o tamanho da figura
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y =  self.original_y = y
        self.width = width
        self.height = height

    #Cria a figura
    def draw(self, JANELA):
        pygame.draw.rect(JANELA, self.COLOR, (self.x, self.y, self.width, self.height))

    #Escolhe a direção que a figura vai se mover
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL
            
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        
class Bola:
    COLOR = WHITE
    MAX_VEL = 6
    
    #especifica a posição e o tamanho da bola
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
  
    #Cria a bola
    def draw(self, JANELA):
        pygame.draw.circle(JANELA, self.COLOR, (self.x, self.y), self.radius)
        
    #Escolhe a direção que a bola vai se mover
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel  *= -1
  
#Desenha na janela do jogo
def draw(JANELA, figuras, bola, score_direito, score_esquerdo):
    

    #Desenha o score
    score_esquerdo_text = SCORE_FONT.render(str(score_esquerdo), 1, WHITE)
    score_direito_text = SCORE_FONT.render(str(score_direito), 1, WHITE)
    JANELA.blit(score_esquerdo_text, (WIDTH//4 - score_esquerdo_text.get_width()//2, 20))
    JANELA.blit(score_direito_text, (WIDTH//4 * 3 - score_direito_text.get_width()//2, 20))

    for figura in figuras:
        figura.draw(JANELA)
        
    #Desenha as linhas no meio da tela
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(JANELA, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))


    bola.draw(JANELA)
    pygame.display.update()

#Verifica se a bola colidiu com a figura
def figura_colisao(bola, left_figura, figura_direita):
    if bola.y + bola.radius >= HEIGHT:
        bola.y_vel *= -1
    elif bola.y - bola.radius <= 0:
        bola.y_vel *= -1
    
    #quando a bola colide com a figura, ela muda de direção
    if bola.x_vel < 0:
        if bola.y >= left_figura.y and bola.y <= left_figura.y + left_figura.height:
            if bola.x - bola.radius <= left_figura.x + left_figura.width: 
                bola.x_vel *= -1
                
                meio_y = left_figura.y + left_figura.height / 2 
                diferenca_no_y = meio_y - bola.y
                fator_reducao = (left_figura.height / 2) / bola.MAX_VEL
                y_vel = diferenca_no_y / fator_reducao
                bola.y_vel = -1 * y_vel
                
    #se não colidir com a figura, o jogo acaba         
    else:
        if bola.y >= figura_direita.y and bola.y <= figura_direita.y + figura_direita.height:
            if bola.x + bola.radius >= figura_direita.x: 
                bola.x_vel *= -1
                
                
                meio_y = figura_direita.y + figura_direita.height / 2
                diferenca_no_y = meio_y - bola.y
                fator_reducao = (figura_direita.height / 2) / bola.MAX_VEL
                y_vel = diferenca_no_y / fator_reducao
                bola.y_vel = -1 * y_vel

#Movimenta a figura de acordo com a tecla pressionada
def figura_movimento(teclas, left_figura, figura_direita):
    if teclas[pygame.K_w] and left_figura.y - left_figura.VEL >= 0:
        left_figura.move(up=True)
    if teclas[pygame.K_s] and left_figura.y + left_figura.VEL + left_figura.height <= HEIGHT:
        left_figura.move(up=False)
        
    if teclas[pygame.K_UP]and figura_direita.y - figura_direita.VEL >= 0:
        figura_direita.move(up=True)
    if teclas[pygame.K_DOWN]and figura_direita.y + figura_direita.VEL + figura_direita.height <= HEIGHT:
        figura_direita.move(up=False)




def main():
    
    rodando = True

    #especifica a posição e o tamanho da figura
    left_figura = Figura(10, HEIGHT//2 - FIGURA_HEIGHT//2, FIGURA_WIDTH, FIGURA_HEIGHT)
    figura_direita = Figura(WIDTH - 10 - FIGURA_WIDTH, HEIGHT//2 - FIGURA_HEIGHT//2, FIGURA_WIDTH, FIGURA_HEIGHT)
    
    
    bola = Bola(WIDTH//2, HEIGHT//2, BOLA_RADIUS)
   
    
    global score_direito
    score_direito = 0
    record = jogador.pontos

    global score_esquerdo
    score_esquerdo = 0
    recordE = jogadorE.pontos

    #imagem['back'] = pygame.image.load(background).convert_alpha()
    imagem['back'] = background

    #Loop principal
    while rodando:
        
        
        
        draw(JANELA, [left_figura, figura_direita], bola, score_direito, score_esquerdo)

        JANELA.blit(imagem['back'], (0, 0))

        #Verifica se o usuário quer sair do jogo
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            

        #Verifica se o usuário apertou alguma tecla
        teclas = pygame.key.get_pressed()
        figura_movimento(teclas, left_figura, figura_direita)
        
        #Atualiza a posição da bola
        bola.move()
        figura_colisao(bola, left_figura, figura_direita)
        
        
        if bola.x < 0:
            score_direito += 1

            if score_direito > record:
                jogador.pontos = score_direito
                db.session.commit()
            print(f"Score jogador direita: {score_direito}")

            bola.reset()
            figura_direita.reset()
            left_figura.reset()

        elif bola.x > WIDTH:
            score_esquerdo += 1
            if score_esquerdo > recordE:
                jogadorE.pontos = score_esquerdo
                db.session.commit()
            print(f"Score jogador esquerda: {score_esquerdo}")
            bola.reset()
            figura_direita.reset()
            left_figura.reset()
            

        

        
        #Exibe o vencedor
        venceu = False
        if score_esquerdo >= SCORE_VENCEDOR:
            venceu = True
            texto_vencedor = "Jogador da esquerda venceu!"
        elif score_direito >= SCORE_VENCEDOR:
            venceu = True
            texto_vencedor = "Jogador da direita venceu!"
        
        #Se alguém venceu, o jogo reinicia
        if venceu:
            texto = SCORE_FONT.render(texto_vencedor, 1, WHITE)
            JANELA.blit(texto, (WIDTH//2 - texto.get_width()//2, HEIGHT//2 - texto.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            bola.reset()
            figura_direita.reset()
            left_figura.reset()
            score_direito = 0
            score_esquerdo = 0
            
        #Atualiza o FPS
        clock.tick(FPS)
    
    pygame.quit()

#executa o jogo
if __name__ == '__main__':
    main()
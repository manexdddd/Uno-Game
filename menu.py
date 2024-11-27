import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 1050
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("UNO - Seleccionar Dificultad")
pygame.mixer.music.load("music/intro.mp3")

# Colores
WHITE = (255, 255, 255)
GREEN = (14, 209, 46)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
FAC = (170,255,170)
NEGRO = (0,0,0)
NAR = (255, 213, 128)
ORANGE = (255, 165, 0)
ROJ = (254,	69	,91)
BUTTON_BORDER_COLOR = (0, 0, 0)  # Color del borde de los botones

# Fuentes
font = pygame.font.SysFont(None, 25)
title_font = pygame.font.SysFont(None, 75)
button_font = pygame.font.SysFont(None, 30)  # Fuente para el texto de los botones

# Tamaño de las imágenes y botones
CARD_SIZE = (250, 320)
BUTTON_SIZE = (180, 40)  # Tamaño de los botones
BUTTON_RADIUS = 20      # Radio de los bordes redondeados
BUTTON_BORDER_WIDTH = 2 # Grosor del borde del botón

# Cargar imágenes y escalarlas
logo = pygame.image.load('images/fondos/logo0791.png').convert_alpha()
background = pygame.image.load('images/fondos/fondo3.jpg').convert()
uno_card_1 = pygame.image.load('images/fondos/easi.png').convert_alpha()
uno_card_2 = pygame.image.load('images/fondos/inter.png').convert_alpha()
uno_card_3 = pygame.image.load('images/fondos/hard.png').convert_alpha()

scaled_logo = pygame.transform.scale(logo, (3922/16, 3342/16))
scaled_uno= pygame.transform.scale(uno_card_1, (295/2, 465/2))
scaled_dos= pygame.transform.scale(uno_card_2, (295/2, 465/2))
scaled_tres= pygame.transform.scale(uno_card_3, (295/2, 465/2))
# Función para dibujar texto
def draw_text(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

# Función para dibujar cartas
def draw_card(surface, card_image, x, y):
    surface.blit(card_image, (x, y))

# Función para dibujar botones normales con texto y bordes redondeados
def draw_button_with_text(text, color, x, y):
    # Crear un rectángulo con bordes redondeados
    button_rect = pygame.Rect(x, y, BUTTON_SIZE[0], BUTTON_SIZE[1])
    pygame.draw.rect(screen, color, button_rect, border_radius=BUTTON_RADIUS)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, button_rect, BUTTON_BORDER_WIDTH, border_radius=BUTTON_RADIUS)
    draw_text(text, button_font,NEGRO, screen, x + BUTTON_SIZE[0] // 2, y + BUTTON_SIZE[1] // 2)


def start_easy():
    pygame.quit()
    os.system('python easy.py')

def start_intermediate():
    pygame.quit()
    os.system('python medio.py')

def start_hard():
    pygame.quit()
    os.system('python hard.py')


# Función principal
def main():
    selected_difficulty = None
    pygame.mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 100 < mouse_x < 380 and 600 < mouse_y < 650:
                    selected_difficulty = 'Easy'
                elif 450 < mouse_x < 605 and 600 < mouse_y < 650:
                    selected_difficulty = 'Intermediate'
                elif 780 < mouse_x < 960 and 600 < mouse_y < 650:
                    selected_difficulty = 'Hard'

        screen.blit(background, (0, 0))

      # Dibujar título (ahora es el logo escalado)
        logo_rect = scaled_logo.get_rect(center=(screen_width // 2, 200))
        screen.blit(scaled_logo, logo_rect)
        uno_rect = scaled_uno.get_rect(center=(190, 450))
        screen.blit(scaled_uno, uno_rect)

        dos_rect = scaled_dos.get_rect(center=(540, 450))
        screen.blit(scaled_dos, dos_rect)
    
        tres_rect = scaled_tres.get_rect(center=(870, 450))
        screen.blit(scaled_tres, tres_rect)

        # Dibujar cartas con botones normales
    #draw_card(screen, uno_card_1, 30, 200)
        draw_button_with_text('Easy', FAC, 100, 600)

       # draw_card(screen, uno_card_2, 400, 200)
        draw_button_with_text('Intermediate', NAR, 450, 600)

        #draw_card(screen, uno_card_3, 750, 200)
        draw_button_with_text('Hard', ROJ, 780, 600)

        
        if selected_difficulty:
            if selected_difficulty == 'Easy':
                start_easy()
            elif selected_difficulty == 'Intermediate':
                start_intermediate()
            elif selected_difficulty == 'Hard':
                start_hard()

            # Reiniciar el ciclo principal
            selected_difficulty = None
        
        pygame.display.update()

if __name__ == "__main__":
    main()

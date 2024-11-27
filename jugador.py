import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 1050
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("UNO - Ganador Jugador")
pygame.mixer.music.load("music/victory.mp3")

# Colores
WHITE = (255, 255, 255)
GREEN = (14, 209, 46)
ORANGE = (255, 165, 0)
RED = (254,69,91)
BLUE = (37, 150, 190)
BUTTON_BORDER_COLOR = (0, 0, 0)  # Color del borde de los botones

# Fuentes
font = pygame.font.SysFont(None, 25)
title_font = pygame.font.SysFont(None, 65)
button_font = pygame.font.SysFont(None, 30)  # Fuente para el texto de los botones



# Tamaño de las imágenes y botones
CARD_SIZE = (250, 320)
BUTTON_SIZE = (180, 40)  # Tamaño de los botones
BUTTON_RADIUS = 20      # Radio de los bordes redondeados
BUTTON_BORDER_WIDTH = 2 # Grosor del borde del botón



# Cargar imágenes y escalarlas
logo = pygame.image.load('images/fondos/logo0791.png').convert_alpha()
background = pygame.image.load('images/fondos/win2.jpg').convert()
uno_card_1 = pygame.image.load('images/fondos/exit.png').convert_alpha()
uno_card_2 = pygame.image.load('images/fondos/menu.png').convert_alpha()
win = pygame.image.load('images/fondos/win.png').convert_alpha()

scaled_logo = pygame.transform.scale(logo, (3922/16, 3342/16))
scaled_uno= pygame.transform.scale(uno_card_1, (295/2, 465/2))
scaled_dos= pygame.transform.scale(uno_card_2, (295/2, 465/2))
wins= pygame.transform.scale(win, (1024/2, 174/2))
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
    draw_text(text, button_font, WHITE, screen, x + BUTTON_SIZE[0] // 2, y + BUTTON_SIZE[1] // 2)
    

def start_salir():
    pygame.quit()

def start_menu():
    pygame.quit()
    os.system('python menu.py')



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
                if 215 < mouse_x < 395 and 600 < mouse_y < 650:
                    selected_difficulty = 'Salir'
                elif 630 < mouse_x < 810 and 600 < mouse_y < 650:
                    selected_difficulty = 'Menu'

        screen.blit(background, (0, 0))


      # Dibujar título (ahora es el logo escalado)
        logo_rect = scaled_logo.get_rect(center=(screen_width // 2, 130))
        screen.blit(scaled_logo, logo_rect)
        uno_rect = scaled_uno.get_rect(center=(300, 450))
        screen.blit(scaled_uno, uno_rect)

        dos_rect = scaled_dos.get_rect(center=(720, 450))
        screen.blit(scaled_dos, dos_rect)
    
        win_rect = wins.get_rect(center=(screen_width // 2, 270))
        screen.blit(wins, win_rect)

        # Dibujar cartas con botones normales
    #draw_card(screen, uno_card_1, 30, 200)
        draw_button_with_text('SALIR',RED, 215, 600)

       # draw_card(screen, uno_card_2, 400, 200)
        draw_button_with_text('MENU',BLUE, 630, 600)


        
        if selected_difficulty:
            if selected_difficulty == 'Salir':
                start_salir()
            elif selected_difficulty == 'Menu':
                start_menu()

            # Reiniciar el ciclo principal
        
        selected_difficulty = None
        
        pygame.display.update()

if __name__ == "__main__":
    main()

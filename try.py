import pygame
import random
import sys
import os

# Inicializar Pygame
pygame.init()

# Configurar la ventana del juego
ANCHO, ALTO = 1050, 650
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('UNO')

# Dimensiones y posiciones
PILA_X, PILA_Y = ANCHO // 2 - 50, ALTO // 2 - 55
MAZO_X, MAZO_Y = ANCHO // 2 - 150, ALTO // 2 - 55
ANCHO_CARTA, ALTO_CARTA = 50, 75
POS_X_COMPUTADORA, POS_Y_COMPUTADORA = 50, 20
ESPACIADO_CARTAS = 110
pygame.mixer.music.load("music/nena.mp3")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)

# Botones
TEXTO_BOTON = "Menú"
TEXTO_COLOR = BLANCO
BOTON_WIDTH = 100
BOTON_HEIGHT = 40
BOTON_X = ANCHO - BOTON_WIDTH - 10
BOTON_Y = ALTO - BOTON_HEIGHT - 10
BOTON_COLOR = AZUL

SALIR_WIDTH = 100
SALIR_HEIGHT = 40
SALIR_X = ANCHO - BOTON_WIDTH - 10
SALIR_Y = ALTO - SALIR_HEIGHT - 70
SALIR_COLOR = ROJO
TEXTO_SALIR = "Salir"
TEXTO_SALIR_COLOR = BLANCO

# Variables globales para acumular efectos de +2 y +4
acumulado_plus2 = 0
acumulado_plus4 = 0

# Configurar reloj
reloj = pygame.time.Clock()
FPS = 30
IMAGENES_CARTAS = {}
colores = ['Rojo', 'Verde', 'Azul', 'Amarillo']
valores = list(range(0, 10))


def cargar_imagenes_cartas():
    imagenes = {}
    colores = ['Rojo', 'Verde', 'Azul', 'Amarillo']
    valores = list(range(0, 10))
    ancho_deseado = 50
    alto_deseado = 75

    for color in colores:
        for valor in valores:
            nombre_imagen = f'images/cartas/{color}_{valor}.png'
            try:
                imagen = pygame.image.load(nombre_imagen).convert_alpha()
                imagen = pygame.transform.scale(imagen, (ancho_deseado, alto_deseado))
                imagenes[(color, str(valor))] = imagen
            except pygame.error as e:
                print(f"Error al cargar la imagen {nombre_imagen}: {e}")

    return imagenes

# Cargar las imágenes al inicio
IMAGENES_CARTAS = cargar_imagenes_cartas()



def obtener_nombre_color(color):
    if color == ROJO:
        return 'Rojo'
    elif color == VERDE:
        return 'Verde'
    elif color == AZUL:
        return 'Azul'
    elif color == AMARILLO:
        return 'Amarillo'
    else:
        return 'Desconocido'

def dibujar_carta(carta, x, y):
    # Obtener el nombre del color
    nombre_color = obtener_nombre_color(carta.color)
    
    # Asegúrate de que las imágenes estén en el diccionario IMAGENES_CARTAS
    imagen = IMAGENES_CARTAS.get((nombre_color, str(carta.valor)), None)
    
    if imagen:
        ventana.blit(imagen, (x, y))
    else:
        # Dibuja un rectángulo como respaldo si no se encuentra la imagen
        pygame.draw.rect(ventana, BLANCO, (x, y, ANCHO_CARTA, ALTO_CARTA))
        pygame.draw.rect(ventana, carta.color, (x + 5, y + 10, 45, 70))
        fuente = pygame.font.SysFont(None, 20)
        texto = fuente.render(str(carta.valor), True, NEGRO)
        ventana.blit(texto, (x + 5, y + 30))

class Carta:
    def __init__(self, color, valor):
        self.color = color
        self.valor = valor

    def __str__(self):
        return f"{self.color} {self.valor}"

def dibujar_botón():
    pygame.draw.rect(ventana, BOTON_COLOR, (BOTON_X, BOTON_Y, BOTON_WIDTH, BOTON_HEIGHT))
    fuente = pygame.font.SysFont(None, 32)
    texto = fuente.render(TEXTO_BOTON, True, TEXTO_COLOR)
    text_rect = texto.get_rect(center=(BOTON_X + BOTON_WIDTH / 2, BOTON_Y + BOTON_HEIGHT / 2))
    ventana.blit(texto, text_rect)

def dibujar_boton_salir():
    pygame.draw.rect(ventana, SALIR_COLOR, (SALIR_X, SALIR_Y, SALIR_WIDTH, SALIR_HEIGHT))
    fuente = pygame.font.SysFont(None, 24)
    texto = fuente.render(TEXTO_SALIR, True, TEXTO_SALIR_COLOR)
    text_rect = texto.get_rect(center=(SALIR_X + SALIR_WIDTH / 2, SALIR_Y + SALIR_HEIGHT / 2))
    ventana.blit(texto, text_rect)

def obtener_color_rgb(color):
    if color == 'Rojo':
        return ROJO
    elif color == 'Verde':
        return VERDE
    elif color == 'Azul':
        return AZUL
    elif color == 'Amarillo':
        return AMARILLO
    else:
        return (0, 0, 0)  # Color predeterminado en caso de error

def crear_mazo():
    colores = ['Rojo', 'Verde', 'Azul', 'Amarillo']
    valores = list(range(0, 10))
    mazo = [Carta(obtener_color_rgb(color), valor) for color in colores for valor in valores]
    random.shuffle(mazo)
    return mazo

def dibujar_cartas_jugador(cartas, x_inicial, y_inicial, max_cartas_por_fila=8):
    x = x_inicial
    y = y_inicial
    espacio_entre_cartas = 110
    espacio_entre_filas = 90
    cartas_por_fila = 0

    for carta in cartas:
        dibujar_carta(carta, x, y)
        x += espacio_entre_cartas
        cartas_por_fila += 1

        if cartas_por_fila == max_cartas_por_fila:
            cartas_por_fila = 0
            x = x_inicial
            y += espacio_entre_filas


def carta_valida(carta, pila):
    if not pila:
        return True
    ultima_carta = pila[-1]
    return carta.color == ultima_carta.color or carta.valor == ultima_carta.valor

def aplicar_efecto_carta(carta, mazo, oponente_cartas):
    global acumulado_plus2, acumulado_plus4

    if carta.valor == '+Two':
        acumulado_plus2 += 2
        return True

    elif carta.valor == '+Four':
        acumulado_plus4 += 4
        return True

    if acumulado_plus2 > 0:
        for _ in range(acumulado_plus2):
            tomar_carta(mazo, oponente_cartas)
        acumulado_plus2 = 0

    if acumulado_plus4 > 0:
        for _ in range(acumulado_plus4):
            tomar_carta(mazo, oponente_cartas)
        acumulado_plus4 = 0

    if carta.valor == 'Skip' or carta.valor == 'Reverse':
        return True

    return False

def tiene_carta_valida(cartas, pila):
    for carta in cartas:
        if carta_valida(carta, pila):
            return True
    return False

def jugada_computadora(cartas_computadora, pila):
    for i, carta in enumerate(cartas_computadora):
        if carta_valida(carta, pila):
            return cartas_computadora.pop(i)
    return None

def dibujar_pila(pila):
    if pila:
        carta = pila[-1]
        dibujar_carta(carta, PILA_X, PILA_Y)
    else:
        pygame.draw.rect(ventana, BLANCO, (PILA_X, PILA_Y, ANCHO_CARTA, ALTO_CARTA))
        fuente = pygame.font.SysFont(None, 22)
        texto = fuente.render('Vacia', True, NEGRO)
        ventana.blit(texto, (PILA_X + 5, PILA_Y + 30))

def cargar_imagen_mazo():
    nombre_imagen_mazo = 'images/fondos/unoBack.png'
    ancho_deseado = 50
    alto_deseado = 75
    try:
        imagen_mazo = pygame.image.load(nombre_imagen_mazo).convert_alpha()
        imagen_mazo = pygame.transform.scale(imagen_mazo, (ancho_deseado, alto_deseado))
        return imagen_mazo
    except pygame.error as e:
        print(f"Error al cargar la imagen {nombre_imagen_mazo}: {e}")
        return None

def dibujar_mazo(mazo):
    # Obtener la imagen del mazo
    imagen_mazo = cargar_imagen_mazo()
    
    if imagen_mazo:
        ventana.blit(imagen_mazo, (MAZO_X, MAZO_Y))
    else:
        pygame.draw.rect(ventana, NEGRO, (MAZO_X, MAZO_Y, ANCHO_CARTA, ALTO_CARTA))
        pygame.draw.rect(ventana, BLANCO, (MAZO_X, MAZO_Y, ANCHO_CARTA, ALTO_CARTA), 2)
        fuente = pygame.font.SysFont(None, 22)
        texto = fuente.render('UNO', True, AMARILLO)
        ventana.blit(texto, (MAZO_X + 7, MAZO_Y + 30))


def dibujar_cartas_computadora(cartas_computadora, x, y, max_cartas_por_fila=8):
    espacio_entre_cartas = 110
    espacio_entre_filas = 90
    cartas_por_fila = 0

    for carta in cartas_computadora:
        dibujar_carta(carta, x, y)
        x += espacio_entre_cartas
        cartas_por_fila += 1

        if cartas_por_fila == max_cartas_por_fila:
            cartas_por_fila = 0
            x = POS_X_COMPUTADORA
            y += espacio_entre_filas

def tomar_carta(mazo, mano):
    if len(mazo) > 0:
        carta = mazo.pop()
        mano.append(carta)
        return carta
    return None

def carta_seleccionada(cartas_jugador, pos_mouse, max_cartas_por_fila=8):
    fila_actual = 0
    x_inicial, y_inicial = 50, 450
    espacio_entre_filas = 90
    espacio_entre_cartas = 110

    for i, carta in enumerate(cartas_jugador):
        fila_actual = i // max_cartas_por_fila
        x = x_inicial + (i % max_cartas_por_fila) * espacio_entre_cartas
        y = y_inicial + fila_actual * espacio_entre_filas

        rect = pygame.Rect(x, y, ANCHO_CARTA, ALTO_CARTA)
        if rect.collidepoint(pos_mouse):
            return i
    return None

def dibujar_acumulado():
    fuente = pygame.font.SysFont(None, 24)
    texto = "Nivel FACIL"
    superficie_texto = fuente.render(texto, True, BLANCO)
    texto2 = "Limite C:16"
    superficie_texto2 = fuente.render(texto2, True, BLANCO)
    ventana.blit(superficie_texto2, (ANCHO - 110, ALTO - SALIR_HEIGHT - 170))
    ventana.blit(superficie_texto, (ANCHO - 110, ALTO - SALIR_HEIGHT - 120))
    dibujar_botón()
    dibujar_boton_salir()

def start_jugador():
    pygame.quit()
    os.system('python jugador.py')

def start_pc():
    pygame.quit()
    os.system('python computadora.py')

def main():
    pygame.mixer.music.play(-1)
    mazo = crear_mazo()
    pila = []
    cartas_jugador = [mazo.pop() for _ in range(7)]
    cartas_computadora = [mazo.pop() for _ in range(7)]
    turno_jugador = True
    carta_valida_tomada = None
    carta_tomada = False

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Verificar si alguno ha ganado
        if len(cartas_jugador) == 0:
            start_jugador()
            corriendo = False
            break
        elif len(cartas_computadora) == 0:
            start_pc()
            corriendo = False
            break

        # Verificar si el jugador tiene más de 15 cartas (final del juego)
        if len(cartas_jugador) >= 16:
            start_jugador()
            corriendo = False
            break
        elif len(cartas_computadora) >= 16:
            start_pc()
            corriendo = False
            break

        # Imprimir de quién es el turno
        if turno_jugador:
            print("Turno del jugador")
        else:
            print("Turno de la computadora")

        # Eventos del juego
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos_mouse = pygame.mouse.get_pos()

            if pygame.Rect(BOTON_X, BOTON_Y, BOTON_WIDTH, BOTON_HEIGHT).collidepoint(pos_mouse):
                pygame.quit()
                os.system('python menu.py')

            if pygame.Rect(SALIR_X, SALIR_Y, SALIR_WIDTH, SALIR_HEIGHT).collidepoint(pos_mouse):
                pygame.quit()
                sys.exit()

            # Turno del jugador
            if turno_jugador:


                if tiene_carta_valida(cartas_jugador, pila):
                    carta_idx = carta_seleccionada(cartas_jugador, pos_mouse)
                    if carta_idx is not None and carta_valida(cartas_jugador[carta_idx], pila):
                        carta_jugada = cartas_jugador.pop(carta_idx)
                        pila.append(carta_jugada)
                        turno_jugador_sigue = aplicar_efecto_carta(carta_jugada, mazo, cartas_computadora)
                        if turno_jugador_sigue:
                            carta_valida_tomada = None
                        else:
                            turno_jugador = False
                            carta_tomada = False
                else:
                    if pygame.Rect(MAZO_X, MAZO_Y, ANCHO_CARTA, ALTO_CARTA).collidepoint(pos_mouse) and not carta_tomada:
                        carta_nueva = tomar_carta(mazo, cartas_jugador)
                        if carta_nueva:
                            if carta_valida(carta_nueva, pila):
                                turno_jugador = True
                            else:
                                turno_jugador = False
                        

            # Turno de la computadora
            else:
                if tiene_carta_valida(cartas_computadora, pila):
                    pygame.time.wait(1000)
                    carta_computadora = jugada_computadora(cartas_computadora, pila)
                    if carta_computadora:
                        pila.append(carta_computadora)
                        turno_computadora_sigue = aplicar_efecto_carta(carta_computadora, mazo, cartas_jugador)
                        if not turno_computadora_sigue:
                            turno_jugador = True
                else:
                    pygame.time.wait(1000)
                    carta_nueva = tomar_carta(mazo, cartas_computadora)
                    if carta_nueva and carta_valida(carta_nueva, pila):
                        pila.append(carta_nueva)
                        cartas_computadora.remove(carta_nueva)
                    turno_jugador = True

        ventana.fill(NEGRO)
        dibujar_cartas_jugador(cartas_jugador, 50, 450)
        dibujar_cartas_computadora(cartas_computadora, POS_X_COMPUTADORA, POS_Y_COMPUTADORA)
        dibujar_pila(pila)
        dibujar_acumulado()
        dibujar_mazo(mazo)
        pygame.display.flip()
        reloj.tick(FPS)

if __name__ == "__main__":
    main()

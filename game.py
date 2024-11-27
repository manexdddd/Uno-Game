import pygame
import random
import sys

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
# Posición inicial y espaciado para las cartas de la computadora
POS_X_COMPUTADORA, POS_Y_COMPUTADORA = 50, 20
ESPACIADO_CARTAS = 110


BLANCO= (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)


# Variables globales para acumular efectos de +2 y +4
acumulado_plus2 = 0
acumulado_plus4 = 0

# Configurar reloj
reloj = pygame.time.Clock()
FPS = 30
class Carta:
    def __init__(self, color, valor):
        self.color = color  # color debe ser una tupla RGB
        self.valor = valor

    def __str__(self):
        return f"{self.color} {self.valor}"


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
    valores = list(range(0, 10)) + ['Skip', 'Reverse', '+Two', '+Four']
    mazo = [Carta(obtener_color_rgb(color), valor) for color in colores for valor in valores]
    random.shuffle(mazo)
    return mazo


def dibujar_cartas_jugador(cartas, x_inicial, y_inicial, max_cartas_por_fila=8):
    # Configuramos las posiciones iniciales para las cartas
    x = x_inicial
    y = y_inicial
    espacio_entre_cartas = 110  # Distancia entre las cartas en horizontal
    espacio_entre_filas = 90   # Distancia entre las filas de cartas en vertical
    cartas_por_fila = 0  # Contador de cartas en la fila actual

    for carta in cartas:
        dibujar_carta(carta, x, y)
        x += espacio_entre_cartas
        cartas_por_fila += 1

        # Si alcanzamos el número máximo de cartas por fila, cambiamos de fila
        if cartas_por_fila == max_cartas_por_fila:
            cartas_por_fila = 0
            x = x_inicial  # Reiniciar la posición X para la nueva fila
            y += espacio_entre_filas  # Moverse a la siguiente fila

def dibujar_carta(carta, x, y):
    pygame.draw.rect(ventana, BLANCO, (x, y, ANCHO_CARTA, ALTO_CARTA))
    pygame.draw.rect(ventana, carta.color, (x + 5, y + 10, 45, 70))  # Ajusta el tamaño y la posición si es necesario
    fuente = pygame.font.SysFont(None, 20)
    texto = fuente.render(str(carta.valor), True, NEGRO)
    ventana.blit(texto, (x + 5, y + 30))  # Ajusta la posición del texto si es necesario


def carta_valida(carta, pila):
    if not pila:
        return True
    ultima_carta = pila[-1]
    
    # Las cartas +Two y +Four solo pueden jugarse si coinciden en color
    if carta.valor in ['+Two', '+Four']:
        return carta.color == ultima_carta.color
    
    # La carta es válida si tiene el mismo color o el mismo número
    return carta.color == ultima_carta.color or carta.valor == ultima_carta.valor


def aplicar_efecto_carta(carta, mazo, oponente_cartas):
    global acumulado_plus2, acumulado_plus4
     # Acumulación de +Two
    if carta.valor == '+Two':
        acumulado_plus2 += 2
        return True  # El turno del oponente se salta
    
    # Acumulación de +Four
    elif carta.valor == '+Four':
        acumulado_plus4 += 4
        return True  # El turno del oponente se salta
    
    # Aplicar acumulaciones al oponente
    if acumulado_plus2 > 0:
        for _ in range(acumulado_plus2):
            tomar_carta(mazo, oponente_cartas)
        acumulado_plus2 = 0  # Resetear acumulado
    
    if acumulado_plus4 > 0:
        for _ in range(acumulado_plus4):
            tomar_carta(mazo, oponente_cartas)
        acumulado_plus4 = 0  # Resetear acumulado

    # Si la carta es un Skip, el oponente pierde su turno y el jugador vuelve a tirar
    elif carta.valor == 'Skip':
        return True  # El jugador puede volver a tirar

    # Si la carta es Reverse, en un juego de dos jugadores actúa como un Skip
    elif carta.valor == 'Reverse':
        return True  # El jugador puede volver a tirar

    return False  # Si no es una carta especial, el turno cambia



def tiene_carta_valida(cartas, pila):
    # Verifica si alguna de las cartas en la mano es válida para jugar
    for carta in cartas:
        if carta_valida(carta, pila):
            return True
    return False


def jugada_computadora(cartas_computadora, pila):
    for i, carta in enumerate(cartas_computadora):
        if carta_valida(carta, pila):
            return cartas_computadora.pop(i)  # La computadora juega la primera carta válida
    return None  # Si no tiene cartas válidas


def dibujar_pila(pila):
    # Dibujar la última carta jugada en la pila
    if pila:
        carta = pila[-1]  # Última carta de la pila (la que está visible)
        dibujar_carta(carta, PILA_X, PILA_Y)  # Dibujar la carta visible en la pila
    else:
        # Si la pila está vacía, dibujar un rectángulo vacío
        pygame.draw.rect(ventana, BLANCO, (PILA_X, PILA_Y, ANCHO_CARTA, ALTO_CARTA))
        fuente = pygame.font.SysFont(None, 22)
        texto = fuente.render('Vacia', True, NEGRO)
        ventana.blit(texto, (PILA_X + 5, PILA_Y + 30))  # Ajusta la posición si es necesario


def dibujar_mazo(mazo):
    # Dibujar un rectángulo que representa el mazo oculto
    pygame.draw.rect(ventana, NEGRO, (MAZO_X, MAZO_Y, ANCHO_CARTA, ALTO_CARTA))  # Fondo negro (carta cubierta)
    
    # Opcional: agregar un borde o diseño para sugerir que es un mazo cubierto
    pygame.draw.rect(ventana, BLANCO, (MAZO_X, MAZO_Y, ANCHO_CARTA, ALTO_CARTA), 2)  # Borde blanco
    
    # Dibujar un texto o ícono para indicar que es el mazo
    fuente = pygame.font.SysFont(None, 22)
    texto = fuente.render('UNO', True, AMARILLO)
    ventana.blit(texto, (MAZO_X + 7, MAZO_Y + 30))  # Ajusta la posición según sea necesario

def dibujar_cartas_computadora(cartas_computadora, POS_X_COMPUTADORA, POS_Y_COMPUTADORA, max_cartas_por_fila=8):
    # Configuramos las posiciones iniciales para las cartas
    x =POS_X_COMPUTADORA
    y = POS_Y_COMPUTADORA
    espacio_entre_cartas = 110  # Distancia entre las cartas en horizontal
    espacio_entre_filas = 90   # Distancia entre las filas de cartas en vertical
    cartas_por_fila = 0  # Contador de cartas en la fila actual

    for carta in cartas_computadora:
        dibujar_carta(carta, x, y)
        x += espacio_entre_cartas
        cartas_por_fila += 1

        # Si alcanzamos el número máximo de cartas por fila, cambiamos de fila
        if cartas_por_fila == max_cartas_por_fila:
            cartas_por_fila = 0
            x = POS_X_COMPUTADORA  # Reiniciar la posición X para la nueva fila
            y += espacio_entre_filas  # Moverse a la siguiente fila

def tomar_carta(mazo, cartas):
    if mazo:
        carta_nueva = mazo.pop()
        cartas.append(carta_nueva)
        return carta_nueva
    return None


def carta_seleccionada(cartas_jugador, pos_mouse, max_cartas_por_fila=8):
    fila_actual = 0
    x_inicial, y_inicial = 50, 450  # Coordenadas iniciales para la primera fila
    espacio_entre_filas = 90       # Espaciado entre las filas de cartas
    espacio_entre_cartas = 110      # Espacio entre cartas en una fila
    
    # Recorrer todas las cartas, verificando fila por fila
    for i, carta in enumerate(cartas_jugador):
        # Calcular la fila actual basándonos en el índice y el máximo de cartas por fila
        fila_actual = i // max_cartas_por_fila
        x = x_inicial + (i % max_cartas_por_fila) * espacio_entre_cartas
        y = y_inicial + fila_actual * espacio_entre_filas

        # Definir el área (rectángulo) de cada carta
        rect = pygame.Rect(x, y, ANCHO_CARTA, ALTO_CARTA)
        
        # Verificar si la posición del mouse está dentro de la carta
        if rect.collidepoint(pos_mouse):
            return i  # Retorna el índice de la carta seleccionada

    return None  # Si no se selecciona ninguna carta


def mostrar_ganador(ganador):
    # Cerrar la ventana actual
    pygame.quit()
    
    # Reiniciar Pygame
    pygame.init()
    
    # Crear una ventana emergente
    ventana_emergente = pygame.display.set_mode((400, 200))
    
    # Establecer el título de la ventana emergente
    pygame.display.set_caption("Resultado del Juego")
    
    # Color de fondo
    color_fondo = (5, 5, 5)
    color_texto = (255, 255, 255)
    
    # Fuente para el texto
    fuente = pygame.font.SysFont("Arial", 24)
    
    # Texto del resultado
    texto_resultado = fuente.render(f"{ganador} ha ganado el juego!", True, color_texto)
    
    # Bucle principal de la ventana emergente
    en_ciclo = True
    while en_ciclo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                en_ciclo = False
        
        # Dibujar el fondo y el texto
        ventana_emergente.fill(color_fondo)
        ventana_emergente.blit(texto_resultado, (20, 40))
        
        # Actualizar la pantalla
        pygame.display.flip()
    
    # Cerrar la ventana emergente
    pygame.quit()

def main():
    mazo = crear_mazo()
    pila = []
    cartas_jugador = [mazo.pop() for _ in range(7)]
    cartas_computadora = [mazo.pop() for _ in range(7)]
    turno_jugador = True
    jugador_tomo_carta = False
    computadora_tomo_carta = False
    carta_tomada = None
    jugador_repite_turno = False

    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Verificar si alguno ha ganado
            if len(cartas_jugador) >=16:
                mostrar_ganador("Computadora")
                corriendo = False
                break
            elif len(cartas_computadora) >=16:
                mostrar_ganador("Jugador")
                corriendo = False
                break



            # Verificar si alguno ha ganado
            if len(cartas_jugador) ==0:
                mostrar_ganador("Jugador")
                corriendo = False
                break
            elif len(cartas_computadora) ==0:
                mostrar_ganador("Computadora")
                corriendo = False
                break


            if turno_jugador:
                if tiene_carta_valida(cartas_jugador, pila):
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        pos_mouse = pygame.mouse.get_pos()
                        carta_idx = carta_seleccionada(cartas_jugador, pos_mouse)
                        if carta_idx is not None and carta_valida(cartas_jugador[carta_idx], pila):
                            carta_jugada = cartas_jugador.pop(carta_idx)
                            pila.append(carta_jugada)
                            # Aplicar los efectos de la carta especial
                            turno_jugador_sigue = aplicar_efecto_carta(carta_jugada, mazo, cartas_computadora)
                            jugador_tomo_carta = False
                            # Si es una carta especial, el jugador puede repetir el turno
                            if turno_jugador_sigue:
                                jugador_repite_turno = True
                            else:
                                turno_jugador = False
                else:
                    # Permitir al jugador tomar cartas
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        pos_mouse = pygame.mouse.get_pos()
                        if pygame.Rect(MAZO_X, MAZO_Y, ANCHO_CARTA, ALTO_CARTA).collidepoint(pos_mouse):
                            carta_nueva = tomar_carta(mazo, cartas_jugador)
                            if carta_nueva:
                                jugador_tomo_carta = True
                                carta_tomada = carta_nueva
                if jugador_tomo_carta and evento.type == pygame.MOUSEBUTTONDOWN:
                    pos_mouse = pygame.mouse.get_pos()
                    carta_idx = carta_seleccionada([carta_tomada], pos_mouse)
                    if carta_idx is not None and carta_valida(carta_tomada, pila):
                        pila.append(carta_tomada)
                        cartas_jugador.remove(carta_tomada)
                        turno_jugador = False
                        jugador_tomo_carta = False
                        carta_tomada = None

            else:
                if not computadora_tomo_carta:
                    pygame.time.wait(1000)
                    # Si la computadora no tiene carta válida, toma una nueva
                    while not tiene_carta_valida(cartas_computadora, pila) and mazo:
                        carta_nueva = tomar_carta(mazo, cartas_computadora)
                        if carta_nueva:
                            pygame.time.wait(500)
                    carta_computadora = jugada_computadora(cartas_computadora, pila)
                    if carta_computadora:
                        pila.append(carta_computadora)
                        turno_computadora_sigue = aplicar_efecto_carta(carta_computadora, mazo, cartas_jugador)
                        computadora_tomo_carta = True
                        if turno_computadora_sigue:
                            jugador_repite_turno = True
                        else:
                            turno_jugador = True
                else:
                    turno_jugador = True
                computadora_tomo_carta = False

            # Verificar si el jugador debe repetir el turno
            if jugador_repite_turno:
                jugador_repite_turno = False  # El jugador vuelve a jugar
                turno_jugador = True  # El jugador sigue

        ventana.fill(NEGRO)
        dibujar_cartas_jugador(cartas_jugador, 50, 450)
        dibujar_cartas_computadora(cartas_computadora, POS_X_COMPUTADORA, POS_Y_COMPUTADORA)
        dibujar_pila(pila)
        dibujar_mazo(mazo)
        pygame.display.flip()
        reloj.tick(FPS)

if __name__ == "__main__":
    main()
import pygame
import sys
import math
import time

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Triángulo al estilo Asteroids")

# Colores
black = (0, 0, 0)
turquoise = (64, 224, 208)  # Color turquesa

# Triángulo
triangle_color = turquoise
triangle_width = 50
triangle_height = 50
triangle_x = screen_width // 2
triangle_y = screen_height // 2
triangle_angle = 0

# Velocidades
max_speed = 1  # Reducir la velocidad máxima a 1
acceleration = 0.5  # Ajustar la aceleración a 0.5
deceleration = 0.1
brake = 1.0  # Factor de frenado al presionar la tecla "down"
rotation_speed = 0.1
current_speed = 0
last_acceleration_time = time.time()

def draw_triangle(x, y, angle):
    triangle_points = [
        (x, y - triangle_height / 2),
        (x + triangle_width / 2, y + triangle_height / 2),
        (x - triangle_width / 2, y + triangle_height / 2)
    ]

    rotated_points = []
    for point in triangle_points:
        dx = point[0] - x
        dy = point[1] - y
        new_x = dx * math.cos(math.radians(angle)) - dy * math.sin(math.radians(angle)) + x
        new_y = dx * math.sin(math.radians(angle)) + dy * math.cos(math.radians(angle)) + y
        rotated_points.append((new_x, new_y))

    pygame.draw.polygon(screen, triangle_color, rotated_points)

# Bucle principal del juego
running = True
accelerating = False
braking = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        triangle_angle -= rotation_speed  # Cambiar dirección de rotación
    if keys[pygame.K_RIGHT]:
        triangle_angle += rotation_speed  # Cambiar dirección de rotación
    if keys[pygame.K_UP]:
        current_speed += acceleration
        last_acceleration_time = time.time()
        accelerating = True
    else:
        # Aplicar fuerza de frenado
        if current_speed > 0:
            current_speed -= deceleration
        elif current_speed < 0:
            current_speed += deceleration

        # Detener la aceleración después de 1.5 segundos de inactividad
        if time.time() - last_acceleration_time >= 1.5:
            accelerating = False

    if keys[pygame.K_DOWN]:
        current_speed -= deceleration * brake  # Frenado más rápido
        braking = True
    else:
        braking = False

    # Limitar la velocidad máxima
    current_speed = max(-max_speed, min(max_speed, current_speed))

    # Calcular el vector de movimiento en función del ángulo
    dx = current_speed * math.sin(math.radians(triangle_angle))
    dy = -current_speed * math.cos(math.radians(triangle_angle))

    triangle_x += dx
    triangle_y += dy

    # Teletransporte cuando el triángulo atraviesa los bordes
    if triangle_x < 0:
        triangle_x = screen_width
    elif triangle_x > screen_width:
        triangle_x = 0
    if triangle_y < 0:
        triangle_y = screen_height
    elif triangle_y > screen_height:
        triangle_y = 0

    screen.fill(black)

    # Dibuja el triángulo dentro de la ventana
    draw_triangle(triangle_x, triangle_y, triangle_angle)

    pygame.display.update()

# Salir del juego
pygame.quit()
sys.exit()

import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Игра мостики")

# Шрифт
myfont = pygame.font.SysFont('fonts/bitoc.ttf', 36)

# Цвета
POINT_COLOR = (50, 50, 50)
BACKGROUND_COLOR = pygame.image.load('images/sky.jpg')
RED = (220, 50, 50)
BLUE = (50, 50, 220)
WHITE = (255, 255, 255)

# Создаём точки для игры 
def create_points_grid():
    points = []
    col_size = 342  # Расстояние между точками колонки
    row_size = 176  # Расстояние между точками строки
    for row in range(6):
        for col in range(6):
            x = 100 + col * col_size
            y = 100 + row * row_size
            points.append({
                'x': x, 
                'y': y, 
                'color': POINT_COLOR, 
                'connections': []
            })
    return points

# Функция отрисовки всех точек
def draw_points():
    for point in POINTS:
        pygame.draw.circle(screen, point['color'], (point['x'], point['y']), 8)
        pygame.draw.circle(screen, WHITE, (point['x'], point['y']), 8, 2)

# Основной игровой цикл
POINTS = create_points_grid()

running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            # Проверяем, кликнули ли по точке
            for point in POINTS:
                distance = ((point['x'] - mouse_x) ** 2 + (point['y'] - mouse_y) ** 2) ** 0.5
                if distance <= 8:
                    print(f"Клик по точке на позиции ({point['x']}, {point['y']})")
    
    # Отрисовка
    screen.blit(BACKGROUND_COLOR, (0, 0))
    draw_points()
    
    # Обновление экрана
    pygame.display.flip()

pygame.quit()
sys.exit()
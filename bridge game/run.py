import pygame

pygame.init()
screen = pygame.display.set_mode((800, 350))  # Размер как кортеж
pygame.display.set_caption("Игра мостики") 

# Создаем иконку программно (так как у нас нет файла 'images/bridge-icon.png')
icon_surface = pygame.Surface((32, 32))
icon_surface.fill((70, 130, 180))  # Цвет иконки (стальной синий)
pygame.draw.rect(icon_surface, (139, 69, 19), (5, 12, 22, 8))  # Рисуем мостик
pygame.display.set_icon(icon_surface)

# Создаем квадрат (правильно передаем размер как кортеж)
square = pygame.Surface((10, 200))
square.fill('Red')

# Цвета
BACKGROUND_COLOR = (240, 240, 200)
RED = (220, 50, 50)
BLUE = (50, 50, 220)
BLACK = (20, 20, 20)
GREEN = (50, 150, 50)
YELLOW = (240, 200, 50)

# Параметры игрового поля
GRID_SIZE = 40
GRID_OFFSET_X = 100
GRID_OFFSET_Y = 100
GRID_WIDTH = 15
GRID_HEIGHT = 10

myfont = pygame.font.Font('fonts/')

running = True
while running:
    # Заполняем экран цветом по умолчанию
    screen.fill((135, 206, 235))  # Голубой цвет неба
    
    
    # Обновляем дисплей
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                # Правильный синтаксис для изменения цвета фона
                screen.fill((63, 94, 117))
                pygame.display.update()  # Обновляем экран после изменения цвета

pygame.quit()
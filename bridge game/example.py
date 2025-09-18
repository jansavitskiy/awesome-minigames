import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра Мостики")

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

# Создаем точки для игры
points = []
for row in range(GRID_HEIGHT):
    for col in range(GRID_WIDTH):
        x = GRID_OFFSET_X + col * GRID_SIZE
        y = GRID_OFFSET_Y + row * GRID_SIZE
        # Чередуем цвета точек в шахматном порядке
        color = RED if (row + col) % 2 == 0 else BLUE
        points.append({"x": x, "y": y, "color": color, "connections": []})

# Определяем берега
shores = [
    {"color": RED, "points": [i for i in range(GRID_HEIGHT * GRID_WIDTH) 
                             if points[i]["color"] == RED and i % GRID_WIDTH == 0]},
    {"color": RED, "points": [i for i in range(GRID_HEIGHT * GRID_WIDTH) 
                             if points[i]["color"] == RED and i % GRID_WIDTH == GRID_WIDTH - 1]},
    {"color": BLUE, "points": [i for i in range(GRID_HEIGHT * GRID_WIDTH) 
                              if points[i]["color"] == BLUE and i < GRID_WIDTH]},
    {"color": BLUE, "points": [i for i in range(GRID_HEIGHT * GRID_WIDTH) 
                              if points[i]["color"] == BLUE and i >= (GRID_HEIGHT - 1) * GRID_WIDTH]}
]

# Игроки
players = [RED, BLUE]
current_player = 0

# История ходов для возможности отмены
history = []

# Функция проверки соединения берегов
def check_win(color):
    # Находим все точки на одном берегу этого цвета
    start_points = []
    for shore in shores:
        if shore["color"] == color:
            start_points.extend(shore["points"])
    
    # Используем поиск в ширину для проверки соединения
    visited = set()
    queue = []
    
    for point in start_points:
        queue.append(point)
        visited.add(point)
    
    while queue:
        current = queue.pop(0)
        
        # Проверяем, достигли ли мы противоположного берега
        for shore in shores:
            if shore["color"] == color and current in shore["points"] and current not in start_points:
                return True
        
        # Добавляем все соединенные точки
        for neighbor in points[current]["connections"]:
            if neighbor not in visited and points[neighbor]["color"] == color:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return False

# Функция отрисовки игрового поля
def draw_game():
    # Фон
    screen.fill(BACKGROUND_COLOR)
    
    # Рисуем берега
    for shore in shores:
        for point_index in shore["points"]:
            point = points[point_index]
            pygame.draw.circle(screen, shore["color"], (point["x"], point["y"]), 10)
    
    # Рисуем соединения
    for i, point in enumerate(points):
        for connection in point["connections"]:
            if connection > i:  # Чтобы не рисовать дважды одно соединение
                other_point = points[connection]
                pygame.draw.line(screen, point["color"], 
                                (point["x"], point["y"]), 
                                (other_point["x"], other_point["y"]), 3)
    
    # Рисуем точки
    for point in points:
        pygame.draw.circle(screen, point["color"], (point["x"], point["y"]), 5)
        pygame.draw.circle(screen, BLACK, (point["x"], point["y"]), 5, 1)
    
    # Рисуем информационную панель
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Ход игрока: {'Красный' if players[current_player] == RED else 'Синий'}", 
                      True, players[current_player])
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 30))
    
    # Инструкция
    instruction_font = pygame.font.SysFont(None, 24)
    instruction = instruction_font.render("Соединяйте точки своего цвета, чтобы построить мост между вашими берегами", 
                                         True, BLACK)
    screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT - 40))

# Основной игровой цикл
running = True
game_over = False
winner = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                x, y = event.pos
                
                # Ищем ближайшую точку
                min_dist = float('inf')
                selected_point = None
                
                for i, point in enumerate(points):
                    dist = ((point["x"] - x) ** 2 + (point["y"] - y) ** 2) ** 0.5
                    if dist < min_dist and dist < 20:  # 20 - радиус клика
                        min_dist = dist
                        selected_point = i
                
                if selected_point is not None and points[selected_point]["color"] == players[current_player]:
                    # Ищем вторую точку для соединения
                    for i, point in enumerate(points):
                        if i != selected_point and points[i]["color"] == players[current_player]:
                            # Проверяем, являются ли точки соседями
                            dx = abs(points[selected_point]["x"] - point["x"])
                            dy = abs(points[selected_point]["y"] - point["y"])
                            
                            # Точки должны быть соседями по горизонтали, вертикали или диагонали
                            if (dx < GRID_SIZE * 1.5 and dy < GRID_SIZE * 1.5 and 
                                (dx > 0 or dy > 0) and i not in points[selected_point]["connections"]):
                                
                                # Сохраняем ход в истории
                                history.append((selected_point, i, current_player))
                                
                                # Создаем соединение
                                points[selected_point]["connections"].append(i)
                                points[i]["connections"].append(selected_point)
                                
                                # Проверяем победу
                                if check_win(players[current_player]):
                                    game_over = True
                                    winner = players[current_player]
                                else:
                                    # Передаем ход другому игроку
                                    current_player = (current_player + 1) % len(players)
                                break
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Перезапуск игры
                # Сбрасываем соединения
                for point in points:
                    point["connections"] = []
                current_player = 0
                game_over = False
                winner = None
                history = []
            
            if event.key == pygame.K_z and not game_over and history:  # Отмена хода
                last_move = history.pop()
                point1, point2, player = last_move
                points[point1]["connections"].remove(point2)
                points[point2]["connections"].remove(point1)
                current_player = player
    
    # Отрисовка игры
    draw_game()
    
    # Если игра окончена, показываем победителя
    if game_over:
        font = pygame.font.SysFont(None, 72)
        text = font.render(f"{'Красный' if winner == RED else 'Синий'} игрок победил!", 
                          True, winner)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 36))
        
        restart_font = pygame.font.SysFont(None, 36)
        restart_text = restart_font.render("Нажмите R для новой игры", True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 36))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
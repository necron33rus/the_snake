from random import randint

import pygame as pg

pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)
# Цвет яблока
APPLE_COLOR = (255, 0, 0)
# Цвет змейки
SNAKE_COLOR = (0, 255, 0)
# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

screen.fill(BOARD_BACKGROUND_COLOR)


# Тут опишите все классы игры.
class GameObject:
    """Экран объекта."""

    def __init__(self, body_color=None):
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для отрисовки объекта на экране."""
        pass

    def draw_cell(self, grid_position):
        """Отрисовка ячейки на экране."""
        rect = pg.Rect(grid_position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Отрисовка яблока"""

    def __init__(self, occupied=None):
        """Инициация яблока на игровом поле."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied)

    def randomize_position(self, occupied):
        """Установка случайного положения яблока на игровом поле."""
        occupied = [] if occupied is None else occupied
        self.position = get_random_position()
        while self.position in occupied:
            self.position = get_random_position()

    def draw(self):
        """Отрисовка яблока на экране."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Змейка."""

    def __init__(self):
        """Инициация начального состояния змейки"""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction

    def move(self):
        """Обновляется позиция змейки."""
        current_head_x, current_head_y = self.get_head_position()
        x_direction, y_direction = self.direction
        new_head_x = current_head_x + x_direction * GRID_SIZE
        new_head_y = current_head_y + y_direction * GRID_SIZE
        new_position = [new_head_x % SCREEN_WIDTH,
                        new_head_y % SCREEN_HEIGHT]

        self.positions.insert(0, new_position)
        if len(self.positions) > self.length:
            self.last_position = self.positions.pop()
        else:
            self.last_position = None

    def draw(self):
        """Отрисовка движения змейки на экране."""
        for position in self.positions:
            self.draw_cell(position)
        self.draw_cell(self.get_head_position())
        if self.last_position:
            last_rect = pg.Rect(self.last_position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> list[int]:
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.positions = [SCREEN_CENTER]
        self.length = 1
        self.direction = RIGHT
        self.last_position = None
        self.next_direction = None


def handle_keys(game_object) -> None:
    """Обрабатывает клавиши для движения змейки."""
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.K_ESCAPE:
            pg.quit()
            raise SystemExit(0)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT:
                game_object.next_direction = RIGHT


def get_random_position():
    """Генерация новой рандомной позиции."""
    return [randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE]


def main():
    """Основная функция."""
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if apple.position in snake.positions:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()

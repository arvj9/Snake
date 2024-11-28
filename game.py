import pygame, random, time
from pygame import Vector2, Rect


pygame.init()

CELL_WIDTH = 20
CELL_GRID_SIZE = 40
SCREEN = pygame.display.set_mode((CELL_WIDTH * CELL_GRID_SIZE, CELL_WIDTH * CELL_GRID_SIZE))
CLOCK = pygame.time.Clock()
FPS = 60
game_running = True


UP: Vector2 = Vector2(0, -1)
DOWN: Vector2 = Vector2(0, 1)
LEFT: Vector2 = Vector2(-1, 0)
RIGHT: Vector2 = Vector2(1, 0)


FONT = "courier new"

score: int = 0

def show_score(font, size, color) -> None:
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(f"Score: {score}", True, color)
    score_rect = score_surface.get_rect()
    SCREEN.blit(score_surface, score_rect)

def game_over(font, size, color) -> None:
    game_over_font = pygame.font.SysFont(font, size)
    game_over_surface = game_over_font.render(f"Your Score is: {score}", True, color)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (SCREEN.get_width() / 2, SCREEN.get_height() / 2)
    SCREEN.blit(game_over_surface, game_over_rect)
    pygame.display.flip()


class Entity:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.color = "white"
        self.position = Vector2(self.x, self.y)

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, Rect(*(CELL_WIDTH * self.position), CELL_WIDTH, CELL_WIDTH))


class Fruit(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.exists = False
        self.color = "red"

    def spawn(self):
        self.x = random.randint(0, CELL_GRID_SIZE - 1)
        self.y = random.randint(0, CELL_GRID_SIZE - 1)
        self.position = Vector2(self.x, self.y)
        self.exists = True


class SnakeComponent(Entity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.direction = RIGHT

    def move(self):
        self.position += self.direction


class Snake:
    def __init__(self):
        self.direction = RIGHT
        
        # initial position of the snake
        # last item in the list is the head
        self.body = [
            SnakeComponent(x=0, y=0),
        ]

    def draw(self):
        for block in self.body:
            block.draw()

    def move(self):
        for i in range(len(self.body)):
            if i == len(self.body) - 1:
                self.body[i].direction = self.direction
                self.body[i].move()
            else:
                self.body[i].direction = self.body[i + 1].direction
                self.body[i].move()

    def extend_snake(self):
        new_block = SnakeComponent()
        new_block.position = self.body[0].position - self.body[0].direction
        self.body.insert(0, new_block)


fruit = Fruit()
snake = Snake()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_running = False
            if event.key == pygame.K_SPACE:
                fruit.exists = False
            if event.key == pygame.K_UP:
                snake.direction = UP
            if event.key == pygame.K_DOWN:
                snake.direction = DOWN
            if event.key == pygame.K_LEFT:
                snake.direction = LEFT
            if event.key == pygame.K_RIGHT:
                snake.direction = RIGHT

        if event.type == SCREEN_UPDATE:
            snake.move()

    SCREEN.fill("black")

    if not fruit.exists:
        fruit.spawn()

    # add to the snake body when head touches fruit
    if snake.body[-1].position == fruit.position:
        score += 1
        fruit.spawn()
        snake.extend_snake()

    for i, block in enumerate(snake.body):
        if block.position == fruit.position:
            fruit.spawn()

        if block.position == snake.body[-1].position and i < len(snake.body) - 1:
            game_running = False

    fruit.draw()
    snake.draw()

    show_score(FONT, 20, "white")
    pygame.display.update()
    CLOCK.tick(FPS)

print(f"Your score was: {score}")
pygame.quit()
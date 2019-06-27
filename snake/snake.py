import pygame
import random
import sys


class Snake:
    def __init__(self):
        self.head = [10, 10]
        self.body = []
        self.direction = 'R'

    def get_head(self):
        return self.head

    def is_alive(self):
        if self.head in self.body:
            return False
        x, y = self.head
        if x < 0 or x > WIDTH / UNIT_SIZE or y < 0 or y > HEIGHT / UNIT_SIZE:
            return False
        return True

    def set_direction(self, direction):
        if direction == 'L' and self.direction != 'R':
            self.direction = 'L'
        elif direction == 'R' and self.direction != 'L':
            self.direction = 'R'
        elif direction == 'U' and self.direction != 'D':
            self.direction = 'U'
        elif direction == 'D' and self.direction != 'U':
            self.direction = 'D'

    def set_body(self, pos):
        self.body.insert(0, pos)

    def eat_food(self, new_head, food_pos):
        """
            can eat, insert food pos in pos_list; otherwise, return false.
        """
        self.body.insert(0, self.head)
        if new_head == food_pos:
            return True
        else:
            self.body = self.body[: -1]
            return False

    def move_head(self):
        x, y = self.head
        if self.direction == 'U':
            y -= 1
        elif self.direction == 'D':
            y += 1
        elif self.direction == 'L':
            x -= 1
        elif self.direction == 'R':
            x += 1
        else:
            pass
        return [x, y]

    def draw(self):
        rect_head = (self.head[0] * UNIT_SIZE, self.head[1] * UNIT_SIZE, UNIT_SIZE, UNIT_SIZE)
        pygame.draw.rect(screen, BLACK, rect_head, 0)

        for body_node in self.body:
            rect_node = (body_node[0] * UNIT_SIZE, body_node[1] * UNIT_SIZE, UNIT_SIZE, UNIT_SIZE)
            pygame.draw.rect(screen, BLACK, rect_node, 0)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.set_direction(direction='U')
                elif event.key == pygame.K_DOWN:
                    self.set_direction(direction='D')
                elif event.key == pygame.K_LEFT:
                    self.set_direction(direction='L')
                elif event.key == pygame.K_RIGHT:
                    self.set_direction(direction='R')
                elif event.key == pygame.K_KP_ENTER:
                    pass


class Food:
    def __init__(self):
        self.x = random.randint(0, WIDTH / UNIT_SIZE - 1)
        self.y = random.randint(0, HEIGHT / UNIT_SIZE - 1)

    def update(self, head, body):
        """
            head is a tuple, body is a list.
        """
        i = 0
        # new pos should avoid appearing in the Snake.
        while i < 100:
            # judge until meeting the condition.
            self.x = random.randint(0, WIDTH / UNIT_SIZE - 1)
            self.y = random.randint(0, HEIGHT / UNIT_SIZE - 1)
            break
        return self.get_pos()

    def get_pos(self):
        return [self.x, self.y]

    def draw(self):
        rect = (self.x * UNIT_SIZE, self.y * UNIT_SIZE, UNIT_SIZE, UNIT_SIZE)
        pygame.draw.rect(screen, GREEN, rect, 0)


WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREEN = [0, 255, 0]


def run():
    restart = True
    while restart:
        screen.fill(WHITE)
        running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    running = True
                elif event.key == pygame.K_BACKSPACE:
                    restart = False
        pygame.display.flip()
        snake = Snake()
        food = Food()
        # snake.go_direction('R')
        while running:
            screen.fill(WHITE)
            print(food.get_pos(), snake.head, snake.body)
            snake.draw()
            food.draw()
            snake.update()
            new_head = snake.move_head()
            if snake.eat_food(new_head, food.get_pos()):
                food.update(snake.head, snake.body)
                print(1)
            else:
                print(2)
                pass
            snake.head = new_head
            if not snake.is_alive():
                print(1, food.get_pos(), snake.head, snake.body)
                running = False
            pygame.display.flip()
            clock.tick(5)


if __name__ == "__main__":
    UP, DOWN, LEFT, RIGHT = False, False, False, True
    pygame.init()
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = 400, 400
    UNIT_SIZE = 20
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    run()

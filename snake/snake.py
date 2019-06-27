import pygame
import random
import sys


class Snake:
    def __init__(self):
        self.head = [10, 10]
        self.body = []
        self.life = True
        self.__new_head = self.head.copy()
        self.__direction = 'R'

    def update_head(self):
        """
            only when __new_head is correct, can we update head.
        """
        self.head = self.__new_head.copy()

    def reset(self):
        self.__init__()

    def is_alive(self):
        """
            check whether the __new_head is correct.
        :return:
        """
        if self.__new_head in self.body:
            return False
        x, y = self.__new_head
        if x < 0 or x >= WIDTH / UNIT_SIZE or y < 0 or y >= HEIGHT / UNIT_SIZE:
            self.life = False
            return False
        return True

    def eat_food(self, food_pos):
        """
            update body:
            1.insert old head in body.
            2.can eat, food pos will be new head, return true;
              otherwise, delete the last body node, return false.
        """
        self.body.insert(0, self.head)
        if self.__new_head == food_pos:
            return True
        else:
            self.body = self.body[: -1]
            return False

    def move_head(self):
        """
            according __direction, just update __new_head.
        """
        x, y = self.head
        if self.__direction == 'U':
            y -= 1
        elif self.__direction == 'D':
            y += 1
        elif self.__direction == 'L':
            x -= 1
        elif self.__direction == 'R':
            x += 1
        else:
            pass
        self.__new_head = [x, y]

    def draw(self):
        """
            draw head and body.
        """

        rect_head = (self.head[0] * UNIT_SIZE, self.head[1] * UNIT_SIZE, UNIT_SIZE - 0.5, UNIT_SIZE - 0.5)
        pygame.draw.rect(screen, GREY + ALPHA, rect_head, 0)
        # I want to add two eyes!
        if self.__direction == 'U':
            ball_eye1 = (self.head[0] * UNIT_SIZE, self.head[1] * UNIT_SIZE)
            ball_eye2 = ((self.head[0] + 1) * UNIT_SIZE, self.head[1] * UNIT_SIZE)
        elif self.__direction == 'D':
            ball_eye1 = (self.head[0] * UNIT_SIZE, (self.head[1] + 1) * UNIT_SIZE)
            ball_eye2 = ((self.head[0] + 1) * UNIT_SIZE, (self.head[1] + 1) * UNIT_SIZE)
        elif self.__direction == 'L':
            ball_eye1 = (self.head[0] * UNIT_SIZE, self.head[1] * UNIT_SIZE)
            ball_eye2 = (self.head[0] * UNIT_SIZE, (self.head[1] + 1) * UNIT_SIZE)
        elif self.__direction == 'R':
            ball_eye1 = ((self.head[0] + 1) * UNIT_SIZE, self.head[1] * UNIT_SIZE)
            ball_eye2 = ((self.head[0] + 1) * UNIT_SIZE, (self.head[1] + 1) * UNIT_SIZE)
        pygame.draw.circle(screen, WHITE + ALPHA, ball_eye1, 5)
        pygame.draw.circle(screen, WHITE + ALPHA, ball_eye2, 5)
        for body_node in self.body:
            rect_node = (body_node[0] * UNIT_SIZE, body_node[1] * UNIT_SIZE, UNIT_SIZE - 0.5, UNIT_SIZE - 0.5)
            pygame.draw.rect(screen, GREY + ALPHA, rect_node, 0)

    def update_direction(self):
        """
            according key event, update __direction.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.__set_direction(direction='U')
                elif event.key == pygame.K_DOWN:
                    self.__set_direction(direction='D')
                elif event.key == pygame.K_LEFT:
                    self.__set_direction(direction='L')
                elif event.key == pygame.K_RIGHT:
                    self.__set_direction(direction='R')
                elif event.key == pygame.K_KP_ENTER:
                    pass

    def __set_direction(self, direction):
        if direction == 'L' and self.__direction != 'R':
            self.__direction = 'L'
        elif direction == 'R' and self.__direction != 'L':
            self.__direction = 'R'
        elif direction == 'U' and self.__direction != 'D':
            self.__direction = 'U'
        elif direction == 'D' and self.__direction != 'U':
            self.__direction = 'D'


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
        # continue to be done.
        while i < 100:
            # judge until meeting the condition.
            # self.x = random.randint(0, WIDTH / UNIT_SIZE - 1)
            # self.y = random.randint(0, HEIGHT / UNIT_SIZE - 1)
            self.x = WIDTH / UNIT_SIZE - 2
            self.y = 0
            break
        return self.get_pos()

    def get_pos(self):
        return [self.x, self.y]

    def draw(self):
        rect = (self.x * UNIT_SIZE, self.y * UNIT_SIZE, UNIT_SIZE, UNIT_SIZE)
        pygame.draw.rect(screen, GREEN + ALPHA, rect, 0)


class Message:
    def __init__(self, game_screen):
        self.screen = game_screen

    def show_score(self, score):
        msg_score = pygame.font.SysFont('Comic Sans MS', 20)
        text_surface_score = msg_score.render(str(score), False, BLACK)
        self.screen.blit(text_surface_score, (WIDTH - UNIT_SIZE * 2, 0))


WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREY = [190, 190, 190]
GREEN = [0, 255, 0]
ALPHA = [0]

def run():
    restart = True
    snake = Snake()
    food = Food()
    message = Message(screen)
    while restart:
        running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    running = True
                elif event.key == pygame.K_BACKSPACE:
                    restart = False
        screen.fill(WHITE)

        if not snake.is_alive():
            if not running:
                # print(snake.head, snake.body)
                snake.draw()
                message.show_score(len(snake.body))
            else:
                snake.reset()
        pygame.display.flip()
        while running:
            screen.fill(WHITE)
            # show score.
            message.show_score(len(snake.body))
            # print(food.get_pos(), snake.head, snake.body)
            snake.draw()
            food.draw()
            snake.update_direction()
            snake.move_head()
            if not snake.is_alive():
                # print(1, food.get_pos(), snake.head, snake.body)
                running = False
            else:
                if snake.eat_food(food.get_pos()):
                    food.update(snake.head, snake.body)
                else:
                    pass
                snake.update_head()

            pygame.display.flip()
            clock.tick(5)


if __name__ == "__main__":
    # UP, DOWN, LEFT, RIGHT = False, False, False, True
    pygame.init()
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = 300, 300
    UNIT_SIZE = 20
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    run()

import pygame
import random
import sys


class Snake:
    def __init__(self):
        # start in the screen center.
        self.head = [int(WIDTH / UNIT_SIZE // 2), int(HEIGHT / UNIT_SIZE // 2)]
        self.body = []
        self.life = True
        self.__new_head = self.head.copy()
        self.__direction = 'R'
        # __is_valid_key is designed to avoid head-to-neck collision.
        # Used in update_head() and update_direction() -> __set_direction().
        self.__is_valid_key = True

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Snake, "_instance"):
            Snake._instance = Snake(*args, **kwargs)
        return Snake._instance

    def update_head(self):
        """
            only when __new_head is correct, can we update head.
        """
        if not self.__is_valid_key:
            self.__is_valid_key = True
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
        # rect_head = (self.head[0] * UNIT_SIZE, self.head[1] * UNIT_SIZE, UNIT_SIZE - 0.5, UNIT_SIZE - 0.5)
        # pygame.draw.rect(screen, GREY + ALPHA, rect_head, 0)
        # I want to add two eyes! OR, use FACE and NECK!
        ball_face = (int((self.head[0] + 0.5) * UNIT_SIZE), int((self.head[1] + 0.5) * UNIT_SIZE))
        pygame.draw.circle(screen, GREY + ALPHA, ball_face, int(UNIT_SIZE / 2) - 1)
        if self.__direction == 'U':
            rect_neck = (self.head[0] * UNIT_SIZE, int((self.head[1] + 0.5) * UNIT_SIZE),
                         UNIT_SIZE - 0.5, UNIT_SIZE / 2 - 0.5)
            # ball_eye1 = (self.head[0] * UNIT_SIZE, self.head[1] * UNIT_SIZE)
            # ball_eye2 = ((self.head[0] + 1) * UNIT_SIZE, self.head[1] * UNIT_SIZE)
        elif self.__direction == 'D':
            rect_neck = (self.head[0] * UNIT_SIZE, self.head[1] * UNIT_SIZE,
                         UNIT_SIZE - 0.5, UNIT_SIZE / 2 - 0.5)
        elif self.__direction == 'L':
            rect_neck = (int((self.head[0] + 0.5) * UNIT_SIZE), self.head[1] * UNIT_SIZE,
                         UNIT_SIZE / 2 - 0.5, UNIT_SIZE - 0.5)
        elif self.__direction == 'R':
            rect_neck = (self.head[0] * UNIT_SIZE, self.head[1] * UNIT_SIZE,
                         UNIT_SIZE / 2 - 0.5, UNIT_SIZE - 0.5)
        pygame.draw.rect(screen, GREY + ALPHA, rect_neck, 0)
        # pygame.draw.circle(screen, WHITE + ALPHA, ball_eye1, 5)
        # pygame.draw.circle(screen, WHITE + ALPHA, ball_eye2, 5)
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
        """
            Only when __is_valid_key is True, can we update __direction.
                After update __direction, __is_valid_key become False.
            And in function update_head(), if __is_valid_key is False, set __is_valid_key True,
                then we can get new __direction.
        """
        if not self.__is_valid_key:
            pass
        else:
            self.__is_valid_key = False
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
        self.__width = WIDTH // UNIT_SIZE
        self.__height = HEIGHT // UNIT_SIZE
        self.__units_num = self.__width * self.__height
        self.__units = set([i * self.__width + j for i in range(self.__width) for j in range(self.__height)])
        self.__x = random.randint(0, self.__width - 1)
        self.__y = random.randint(0, self.__height - 1)

    def update(self, head, body):
        """
            head is a tuple, body is a list.
        """
        units_left_num = self.__units_num - 1 - len(body)
        # new pos should avoid appearing in the Snake.
        if units_left_num > 0:
            # judge until meeting the condition.
            units_snake = [head[0] * self.__width + head[1]] + \
                          [node[0] * self.__width + node[1] for node in body]
            units_left = list(self.__units ^ set(units_snake))
            unit_food = random.choice(units_left)
            self.__x = unit_food // self.__width
            self.__y = unit_food - self.__x * self.__width
        return self.get_pos()

    def get_pos(self):
        return [self.__x, self.__y]

    def draw(self):
        # ball or rect?
        ball = (int((self.__x + 0.5) * UNIT_SIZE), int((self.__y + 0.5) * UNIT_SIZE))
        pygame.draw.circle(screen, GREEN + ALPHA, ball, int(UNIT_SIZE / 2))
        '''
        rect = (self.x * UNIT_SIZE, self.y * UNIT_SIZE, UNIT_SIZE, UNIT_SIZE)
        pygame.draw.rect(screen, GREEN + ALPHA, rect, 0)
        '''


class Message:
    def __init__(self, game_screen):
        self.screen = game_screen

    # then execute __init__, different from Snake.instance()
    def __new__(cls, *args, **kwargs):
        if not hasattr(Message, "_instance"):
            Message._instance = object.__new__(cls)
        return Message._instance

    def show_score(self, score):
        msg_font = pygame.font.SysFont('Comic Sans MS', 20)
        text_surface_score = msg_font.render(str(score), False, BLACK)
        self.screen.blit(text_surface_score, (WIDTH - UNIT_SIZE * 2, 0))

    def show_start(self):
        msg_font = pygame.font.SysFont('Comic Sans MS', 30)
        msg_start = ["ENTER", "for start", "BACKSPACE", "for end"]
        text_surface_start = msg_font.render(msg_start[0], False, YELLOW_GREEN)
        self.screen.blit(text_surface_start, (WIDTH / 6, HEIGHT / 4))
        text_surface_start = msg_font.render(msg_start[1], False, BLACK)
        self.screen.blit(text_surface_start, (WIDTH / 2, HEIGHT / 4 + 30))
        text_surface_start = msg_font.render(msg_start[2], False, ORANGE3)
        self.screen.blit(text_surface_start, (WIDTH / 6, HEIGHT / 2))
        text_surface_start = msg_font.render(msg_start[3], False, BLACK)
        self.screen.blit(text_surface_start, (WIDTH / 1.8, HEIGHT / 2 + 30))


WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREY = [190, 190, 190]
GREEN = [0, 255, 0]
YELLOW_GREEN = [154, 205, 50]
ORANGE3 = [205, 133, 0]
ALPHA = [0]


def run():
    restart = True
    snake = Snake.instance()
    food = Food()
    message = Message(screen)
    fps = 30
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
                snake.draw()
                message.show_score(len(snake.body))
            else:
                snake.reset()
        # MESSAGE should be draw after SNAKE.
        message.show_start()
        pygame.display.flip()
        clock.tick(fps)
        # min time_delay = 2
        time_delay = 10
        time_delay_increment = 0
        time = 0
        while running:
            screen.fill(WHITE)
            snake.draw()
            food.draw()
            # show score.
            '''
                SCORE should be draw after SNAKE and FOOD, otherwise, it will be interrupted.
                Beside, color ALPHA need to be set.
                Draw order: SNAKE, FOOD -> MESSAGE(SCORE and START...)
            '''
            message.show_score(len(snake.body))
            snake.update_direction()
            # control speed according length of snake.
            if time >= time_delay + time_delay_increment:
                time = 0
                snake.move_head()
                # print(snake.head, snake._Snake__new_head, snake.body)
                if not snake.is_alive():
                    running = False
                else:
                    '''
                    Here may be strange. eat_food() -> use old head to update body.
                    But updating food should use new head!
                    '''
                    if snake.eat_food(food.get_pos()):
                        snake.update_head()
                        food.update(snake.head, snake.body)
                    else:
                        snake.update_head()

                temp = - len(snake.body) // 4
                time_delay_increment = temp if temp >= -8 else -8
            else:
                time += 1
            pygame.display.flip()
            clock.tick(fps)
            # clock.tick_busy_loop(speed)


if __name__ == "__main__":
    # UP, DOWN, LEFT, RIGHT = False, False, False, True
    pygame.init()
    clock = pygame.time.Clock()
    WIDTH, HEIGHT = 300, 240
    UNIT_SIZE = 20
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    run()

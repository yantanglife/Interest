import pygame
import random
import string

# Define Four Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


pygame.init()

# Setting the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

"""
    This is a simple Ball class for respresenting a ball 
    in the game. 
"""


class Ball(object):
    def __init__(self, screen, radius, x, y):
        self.__screen = screen
        self._radius = radius
        self._xLoc = x
        self._yLoc = y
        self.__xVel = 7
        self.__yVel = 2
        w, h = pygame.display.get_surface().get_size()
        self.__width = w
        self.__height = h

    def getXVel(self):
        return self.__xVel

    def getYVel(self):
        return self.__yVel

    def draw(self):
        """
            draws the ball onto screen.
        """
        pygame.draw.circle(screen, (255, 0, 0), (self._xLoc, self._yLoc), self._radius)

    def update(self, paddle, brickwall):
        """
            moves the ball at the screen.
            contains some collision detection.
        """
        self._xLoc += self.__xVel
        self._yLoc += self.__yVel
        # left screen wall bounce
        if self._xLoc <= self._radius:
            self.__xVel *= -1
        # right screen wall bounce
        elif self._xLoc >= self.__width - self._radius:
            self.__xVel *= -1
        # top wall bounce
        if self._yLoc <= self._radius:
            self.__yVel *= -1
        # bottom drop out
        # elif self._yLoc >= self.__height - self._radius:
        # instead of comparing ball and surface's bottom, it's better to choose paddle.
        elif self._yLoc - self._radius >= paddle._yLoc:
            return True

        # for bouncing off the bricks.
        if brickwall.collide(self):
            self.__yVel *= -1

        # collision detection between ball and paddle
        paddleX = paddle._xLoc
        paddleY = paddle._yLoc
        paddleW = paddle._width
        paddleH = paddle._height

        ballX = self._xLoc
        ballY = self._yLoc
        # collision detection on the top of paddle.
        if ((ballX + self._radius) >= paddleX and ballX <= (paddleX + paddleW)) \
                and (ballY + self._radius) >= paddleY:
            ''''((ballY + self._radius) >= paddleY and ballY <= (paddleY + paddleH))'''
            self.__yVel *= -1

        return False


"""
    Simple class for representing a paddle
"""


class Paddle(object):
    def __init__(self, screen, width, height, x, y):
        self.__screen = screen
        self._width = width
        self._height = height
        self._xLoc = x
        self._yLoc = y
        w, h = pygame.display.get_surface().get_size()
        self.__W = w
        self.__H = h

    def draw(self):
        """
            draws the paddle onto screen.
        """
        pygame.draw.rect(screen, (0, 0, 0), (self._xLoc, self._yLoc, self._width, self._height), 0)

    def update(self):
        """
            moves the paddle at the screen via mouse or KEY(LEFT and RIGHT)
        """
        # x, y = pygame.mouse.get_pos()
        x = self._xLoc
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            x -= self._width / 5
        elif key[pygame.K_RIGHT]:
            x += self._width / 5
        # no key has been pressed. detect the mouse.
        elif not any(key):
            x, y = pygame.mouse.get_pos()
        if 0 <= x <= (self.__W - self._width):
            self._xLoc = x
        # else paddle could not move.


"""
    This class represents a simple Brick class.
    For representing bricks onto screen.
"""


class Brick(pygame.sprite.Sprite):
    def __init__(self, screen, width, height, x, y):
        self.__screen = screen
        self._width = width
        self._height = height
        self._xLoc = x
        self._yLoc = y
        w, h = pygame.display.get_surface().get_size()
        self.__W = w
        self.__H = h
        self.__isInGroup = False

    def draw(self):
        """
            draws the brick onto screen.
            color: rgb(56, 177, 237)
        """
        pygame.draw.rect(screen, (56, 177, 237), (self._xLoc, self._yLoc, self._width, self._height), 0)

    def add(self, group):
        """
            adds this brick to a given group.
        """
        group.add(self)
        self.__isInGroup = True

    def remove(self, group):
        """
            removes this brick from the given group.
        """
        group.remove(self)
        self.__isInGroup = False

    def alive(self):
        """
            returns true when this brick belongs to the brick wall.
            otherwise false
        """
        return self.__isInGroup

    def collide(self, ball):
        """
            collision detection between ball and this brick
        """
        brickX = self._xLoc
        brickY = self._yLoc
        brickW = self._width
        brickH = self._height
        ballX = ball._xLoc
        ballY = ball._yLoc
        ballXVel = ball.getXVel()
        ballYVel = ball.getYVel()

        if ((ballX + ball._radius) >= brickX and (ballX + ball._radius) <= (brickX + brickW)) \
                and ((ballY - ball._radius) >= brickY and (ballY - ball._radius) \
                     <= (brickY + brickH)):
            return True
        else:
            return False


"""
    This is a simple class for representing a 
    brick wall.
"""


class BrickWall(pygame.sprite.Group):
    def __init__(self, screen, x, y, width, height):
        self.__screen = screen
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._bricks = []

        X = x
        Y = y
        row, col = 3, 10
        for i in range(row):
            for j in range(col):
                self._bricks.append(Brick(screen, width, height, X, Y))
                X += width + (width / 7.0)
            Y += height + (height / 7.0)
            X = x

    def add(self, brick):
        """
            adds a brick to this BrickWall (group)
        """
        self._bricks.append(brick)

    def remove(self, brick):
        """
            removes a brick from this BrickWall (group)
        """
        self._bricks.remove(brick)

    def draw(self):
        """
            draws all bricks onto screen.
        """
        for brick in self._bricks:
            if brick != None:
                brick.draw()

    def update(self, ball):
        """
            checks collision between ball and bricks.
        """
        for i in range(len(self._bricks)):
            if ((self._bricks[i] != None) and self._bricks[i].collide(ball)):
                self._bricks[i] = None

        # removes the None-elements from the brick list.
        for brick in self._bricks:
            if brick == None:
                self._bricks.remove(brick)

    def hasWin(self):
        """
            Has player win the game?
        """
        return len(self._bricks) == 0

    def collide(self, ball):
        """
            check collisions between the ball and
            any of the bricks.
        """
        for brick in self._bricks:
            if brick.collide(ball):
                return True
        return False


class Button(object):
    def __init__(self, up_image, down_image, position):
        """
        self.imageUp = pygame.image.load(up_image).convert_alpha()
        self.imageDown = pygame.image.load(down_image).convert_alpha()
        """
        self.position = position

    def is_over(self):
        point_x, point_y = pygame.mouse.get_pos()
        x, y = self.position
        w, h = self.imageUp.get_size()
        in_x = x - w / 2 < point_x < x + w / 2
        in_y = y - h / 2 < point_y < y + h / 2
        return in_x and in_y

    def render(self):
        w, h = self.imageUp.get_size()
        x, y = self.position
        if self.is_over():
            screen.blit(self.imageDown, (x - w / 2, y - h / 2))
        else:
            screen.blit(self.imageUp, (x - w / 2, y - h / 2))


'''   
def button (msg, x, y, w, h, ic, ac):
  mouse =pygame.mouse.get_pos()
  if x + w > mouse[0] > x and y + h > mouse[1] > y:
   pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
  else:
   pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
  smallText = pygame.font.Font("freesansbold.ttf", 20)
  textSurf, textRect = text_objects(msg, smallText)
  textRect.center = ( (x+(w/2)), (y+(h/2)))
  gameDisplay.blit(textSurf, textRect)
'''


class Button2(object):
    def __init__(self, msg, position, w, h, ic, ac):
        """
        :param msg:
        :param position: left and top.
        :param w:
        :param h:
        :param ic: color before press.
        :param ac:
        """
        self.msg = msg
        self.position = position
        self.weight = w
        self.height = h
        self.ac = ac
        self.ic = ic

    def is_over(self):
        point_x, point_y = pygame.mouse.get_pos()
        x, y = self.position
        in_x = x < point_x < x + self.weight
        in_y = y < point_y < y + self.height
        return in_x and in_y

    def render(self, surface):
        x, y = self.position
        if self.is_over():
            pygame.draw.rect(screen, self.ac, (x, y, self.weight, self.height))
        else:
            pygame.draw.rect(screen, self.ic, (x, y, self.weight, self.height))
        text = pygame.font.Font('freesansbold.ttf', 20)
        text_surface, text_rect = text_objects(self.msg, text)
        text_rect.center = (x + self.weight / 2, y + self.height / 2)
        surface.blit(text_surface, text_rect)


def text_objects(text, font):
    text_surface = font.render(text, True, (0, 0, 0))
    return text_surface, text_surface.get_rect()


def show_welcome(gameStart, gameOver):
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.KEYDOWN):
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if gameStart.is_over():
                return False
            elif gameOver.is_over():
                pygame.quit()
                exit()
    #screen.blit(background, (0,0))
    #screen.blit(logo, ((SCREEN_SIZE[0]-logo.get_width())/2,100))
    gameStart.render(screen)
    gameOver.render(screen)
    return True


def main():
    ball = Ball(screen, 25, random.randint(1, 700), 250)
    paddle = Paddle(screen, 100, 10, 250, 450)
    brickWall = BrickWall(screen, 25, 25, 150, 50)

    isGameOver = False  # determines whether game is lose
    gameStatus = True  # game is still running
    score = 0  # score for the game.
    # Loop until the user clicks the close button.
    done = False
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # message for game over
    mgGameOver = pygame.font.SysFont('Comic Sans MS', 40)

    # message for winning the game.
    mgWin = pygame.font.SysFont('Comic Sans MS', 40)

    # message for score
    mgScore = pygame.font.SysFont('Comic Sans MS', 40)

    textsurfaceGameOver = mgGameOver.render('Game Over!', False, (0, 0, 0))
    textsurfaceWin = mgWin.render("You win!", False, (0, 0, 0))
    textsurfaceScore = mgScore.render("score: " + str(score), False, (0, 0, 0))

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # --- Game logic should go here

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(WHITE)

        # --- Drawing code should go here

        """
            Because I use OOP in the game logic and the drawing code,
            are both in the same section.
        """
        if gameStatus:

            # first draws ball for appropriate displaying the score.
            brickWall.draw()

            # for counting and displaying the score
            if brickWall.collide(ball):
                score += 10
            textsurfaceScore = mgScore.render("score: " + str(score), False, (0, 0, 0))
            screen.blit(textsurfaceScore, (300, 0))

            # after scoring. because hit bricks are removed in the update-method
            brickWall.update(ball)

            paddle.draw()
            paddle.update()

            if ball.update(paddle, brickWall):
                isGameOver = True
                gameStatus = False

            if brickWall.hasWin():
                gameStatus = False

            ball.draw()

        else:  # game isn't running.
            if isGameOver:  # player lose
                screen.blit(textsurfaceGameOver, (0, 0))
                textsurfaceScore = mgScore.render("score: " + str(score), False, (0, 0, 0))
                screen.blit(textsurfaceScore, (300, 0))
            elif brickWall.hasWin():  # player win
                screen.blit(textsurfaceWin, (0, 0))
                textsurfaceScore = mgScore.render("score: " + str(score), False, (0, 0, 0))
                screen.blit(textsurfaceScore, (300, 0))
            # whatever player lose or win, end event loop.
            done = True
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        # --- Limit to 60 frames per second
        clock.tick(60)
    return {"done": done, "score": score}
    # Close the window and quit.
    # pygame.quit()


def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            return event.key
        else:
            pass


def display_box(screen, message):
    "Print a message in a box in the middle of the screen"
    fontobject = pygame.font.Font(None, 18)
    pygame.draw.rect(screen, (0, 0, 0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
    pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
        # pygame.time.Clock().tick(60)
    pygame.display.flip()


def ask(screen, question):
    "ask(screen, question) -> answer"
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": " + ''.join(current_string))
    while 1:
        inkey = get_key()
        print(inkey)
        if inkey == pygame.K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == pygame.K_RETURN:
            break
        elif inkey == pygame.K_MINUS:
            current_string.append("_")
        elif inkey <= 127:
            current_string.append(chr(inkey))
        display_box(screen, question + ": " + ''.join(current_string) + '_')
        display_box(screen, question + ": " + ''.join(current_string))
    return ''.join(current_string)


if __name__ == "__main__":
    pygame.display.set_caption("Brickout-game")
    # The game objects ball, paddle and brick wall
    # for displaying text in the game
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    screen.fill(WHITE)
    screen_size = screen.get_size()
    screen_center = (screen_size[0] / 2, screen_size[1] / 2)
    button_size = (120, 60)
    pos1 = (screen_center[0]- button_size[0] / 2, screen_center[1]- button_size[1] / 2)
    gameStart = Button2("Start", pos1, button_size[0], button_size[1], (255, 0, 0), (255, 255, 0))
    gameOver = Button2("Over", (pos1[0], pos1[1] + 80), button_size[0], button_size[1], (255, 0, 0), (255, 255, 0))
    done = False
    while not done:
        while show_welcome(gameStart, gameOver):
            pygame.display.update()
        res_dic = main()
        if res_dic.get("done", False):
            records = [50, 30, 0]
            score = res_dic.get("score", 0)
            # here, display the records.
            index = 0
            for record in records:
                if score < record:
                    index += 1
            if index < 3:
                # should input player's name.
                name = ask(screen, "Name")
                if name:
                    records = records.insert(index, score)
                screen.fill(WHITE)
                pygame.display.flip()


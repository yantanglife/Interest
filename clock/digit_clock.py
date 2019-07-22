import turtle
from datetime import datetime


class DigitalTube:
    def __init__(self, pos, digit=0):
        self.__digit = digit
        self.__pos = pos
        self.__changed = True
        self._line_len = 30
        self._pen_size = 5
        self.ttl = turtle.Turtle()
        self.ttl.penup()
        # self.ttl.setpos(pos)
        self.ttl.pensize(self._pen_size)
        self.ttl.hideturtle()

    def set_value(self, digit):
        if self.__digit != digit:
            self.__changed = True
            self.__digit = digit

    def draw(self):
        if self.__changed:
            self.__changed = False
            self.ttl.clear()
            self.ttl.setpos(self.__pos)
            '''digit width is line length + pensize * 2;
                height is line length * 2 + pensize * 3.'''
            self.__draw_line(True) if self.__digit in [2, 3, 4, 5, 6, 8, 9] else self.__draw_line(False)
            self.__draw_line(True) if self.__digit in [0, 1, 3, 4, 5, 6, 7, 8, 9] else self.__draw_line(False)
            self.__draw_line(True) if self.__digit in [0, 2, 3, 5, 6, 8, 9] else self.__draw_line(False)
            self.__draw_line(True) if self.__digit in [0, 2, 6, 8] else self.__draw_line(False)
            self.ttl.left(90)
            self.__draw_line(True) if self.__digit in [0, 4, 5, 6, 8, 9] else self.__draw_line(False)
            self.__draw_line(True) if self.__digit in [0, 2, 3, 5, 6, 7, 8, 9] else self.__draw_line(False)
            self.__draw_line(True) if self.__digit in [0, 1, 2, 3, 4, 7, 8, 9] else self.__draw_line(False)
            self.ttl.left(180)

    def __draw_line(self, is_draw):
        self.__draw_gap()
        # self.ttl.pendown() if is_draw else self.ttl.penup()
        self.ttl.pendown()
        if not is_draw:
            self.ttl.pencolor('#EEE9E9')
        else:
            self.ttl.pencolor("black")
        # line length.
        self.ttl.fd(self._line_len)
        self.__draw_gap()
        self.ttl.right(90)

    def __draw_gap(self):
        self.ttl.penup()
        # pensize
        self.ttl.fd(self._pen_size)


def main():
    now_time = datetime.now()
    now_time = now_time.strftime('%H:%M:%S')
    '''00:00 00  -> d1d2:d3d4 d5d6'''
    d1.set_value(int(now_time[0]))
    d2.set_value(int(now_time[1]))
    d3.set_value(int(now_time[3]))
    d4.set_value(int(now_time[4]))
    d5.set_value(int(now_time[6]))
    d6.set_value(int(now_time[7]))
    t.screen.tracer(False)
    d1.draw()
    d2.draw()
    d3.draw()
    d4.draw()
    d5.draw()
    d6.draw()
    t.screen.tracer(True)
    double_dot()
    '''Considering the time of calculate and paint, we put time delay 950ms.
        (Unless this value is appropriate on my computer.)
        If we put 1000ms, there will be a two-second jump sometimes;
        and if the time is less than 900ms, it seems that there will be a brief pause.'''
    t.screen.ontimer(main, 950)


def double_dot():
    """
    Show double_dot between HOUR and MINUTE.
    """
    dd.clear()
    dd.hideturtle()
    dd.screen.tracer(False)
    dd.penup()
    '''Center of the dot dots is in the middle of the window.'''
    dd.setpos(0, 0)
    dd.left(90)
    dd.penup()
    # dot pos
    dd.fd(20)
    dd.pendown()
    # dot size
    dd.dot(7)
    dd.left(180)
    dd.penup()
    dd.fd(40)
    dd.pendown()
    dd.dot(7)
    dd.left(90)


t = turtle.Turtle()
dd = turtle.Turtle()
if __name__ == "__main__":
    # window size, and the pos where window show.
    t.screen.tracer(False)
    t.screen.setup(500, 400, 200, 200)
    # circle
    t.penup()
    t.setpos(0, -150)
    t.pendown()
    t.pensize(2)
    t.circle(150)
    t.hideturtle()
    # life
    t.penup()
    t.setpos(0, 80)
    t.write("life", align="center",
            font=("Times", 14, "bold"))

    d1 = DigitalTube((-130, 0))
    d2 = DigitalTube((-70, 0))
    d3 = DigitalTube((30, 0))
    d4 = DigitalTube((90, 0))

    d5 = DigitalTube((-25, -90))
    d6 = DigitalTube((5, -90))
    d5._pen_size = 4
    d5._line_len = 12
    d6._pen_size = 4
    d6._line_len = 12

    main()
    t.screen.mainloop()

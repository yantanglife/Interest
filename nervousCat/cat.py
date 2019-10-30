import tkinter as tk
import tkinter.messagebox
import random

# m for start point , k for space between circles.
m = 20
k = 4

values = [100 for x in range(81)]
# border pos.
ups = list(range(1, 10))
lefts = [1 + i * 9 for i in range(9)]
rights = [9 + i * 9 for i in range(9)]
downs = list(range(72, 82))

cat_pos = 41 * 2 - 1

top = tk.Tk()
cvs = tk.Canvas(top, width=600, height=500)
cvs.pack()


def click(event, c):
    global cat_pos
    global values
    # disable the pos clicked.
    cvs.itemconfig(c, fill='yellow')
    values[c//2] = 100
    # update cat's pos
    cat_pos = update(cat_pos)
    print(c, event.x, event.y)
    a = neighbors_index(c // 2 + 1)
    '''
    for i in a:
        cvs.itemconfig(trans_pos(i), fill='red')
    '''


def neighbors(all_index):
    """
    :param all_index:  [1, 81]
    :return:
    """
    ans = []
    for index in all_index:
        if index == -1:
            continue
        ans.append(values[index - 1])
    return ans


def min_neighbor_index(all_index):
    """
    :param all_index: in [1, 81]
    :return: index in [1, 81]
    """
    ans = neighbors(all_index)
    min_neighbor = min(ans)
    if min_neighbor == 100:
        tk.messagebox.showinfo('Success', '成功围住')
        exit()
    for i in all_index:
        if values[i - 1] == min_neighbor:
            return i
    # return -1


def update(pos):
    # k = trans_pos(pos)
    cvs.itemconfig(pos, fill='white')

    # update. border pos = 0, disable pos = 100, cat pos = 200.
    for i in range(81):
        if values[i] in (0, 100):
            continue
        a = neighbors_index(i + 1)
        values[i] = min(neighbors(a)) + 1
    # cat pos to
    pos = pos // 2 + 1
    a = neighbors_index(pos)
    next_pos = min_neighbor_index(a)
    if values[next_pos - 1] == 0:
        tk.messagebox.showinfo('失败', 'Game Over.')
        exit()
    values[next_pos - 1] = 200
    show()
    cvs.itemconfig(trans_pos(next_pos), fill='blue')
    return trans_pos(next_pos)


def handler_adaptor(func, **kwargs):
    return lambda event, func=func, kwargs=kwargs: func(event, **kwargs)


def trans_pos(pos):
    """[1, 81] to show"""
    return 2 * pos - 1


def init():
    global values
    # Init border's value.
    for i in ups:
        values[i - 1] = 0
    for i in lefts:
        values[i - 1] = 0
    for i in rights:
        values[i - 1] = 0
    for i in downs:
        values[i - 1] = 0
    for i in range(81):
        if values[i] == 0:
            continue
        a = neighbors_index(i)
        values[i] = min(neighbors(a)) + 1
    points = random.sample(list(range(1, 41)) + list(range(42, 82)), 8)
    for pos in points:
        values[pos - 1] = 100
        cvs.itemconfig(trans_pos(pos), fill='yellow')
    cvs.itemconfig(cat_pos, fill='blue')
    values[cat_pos // 2 + 1] = 200
    return points


def neighbors_index(pos):
    """pos in [1, 81], 81 = m * n"""
    '''
          up_left    up_right
    left                        right
          down_left  down_right 
    '''
    flag = ((pos - 1) // 9) % 2
    left = pos - 1
    right = pos + 1
    if flag:
        cre = [0, 1, 0, 1]
    else:
        cre = [-1, 0, -1, 0]
    up_left = pos - 9 + cre[0]
    up_right = pos - 9 + cre[1]
    down_left = pos + 9 + cre[2]
    down_right = pos + 9 + cre[3]

    # make true these values around this pos.
    if pos in ups:
        up_left = -1
        up_right = -1
    if pos in downs:
        down_left = -1
        down_right = -1
    if pos in lefts:
        left = -1
        if not flag:
            up_left = -1
            down_left = -1
    if pos in rights:
        right = -1
        if flag:
            up_right = -1
            down_right = -1
    # print(pos, left, up_left, up_right, right, down_right, down_left)
    return left, up_left, up_right, right, down_right, down_left


def p(canvas, diameter):
    for j in range(9):
        for i in range(9):
            w = diameter / 2 if j % 2 else 0
            c = canvas.create_oval(w + m + i * (diameter + k), m + j * diameter,
                                   w + m + i * (diameter + k) + diameter, m + (j + 1) * diameter,
                                   fill='white')
            canvas.create_text(w + m + i * (diameter + k) + diameter / 2,
                               m + j * diameter + diameter / 2, text=values[c//2])
            canvas.tag_bind(c, '<Button -1>', func=handler_adaptor(click, c=c),)


def show():
    for j in range(9):
        for i in range(9):
            c = j * 9 + i
            cvs.itemconfig((c+1)*2, text=values[c])


p(cvs, 50)
init_points = init()


top.mainloop()

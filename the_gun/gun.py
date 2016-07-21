from tkinter import *
from random import choice, randint
from math import *

screen_width = 400
screen_height = 300
timer_delay = 100


class Ball:
    initial_number = 20
    minimal_radius = 15
    maximal_radius = 40
    available_colors = ['green', 'blue', 'red']
    max_offset_Vx = 9
    max_offset_Vy = 4

    def __init__(self):
        """
        Cоздаёт шарик в случайном месте игрового холста canvas,
        при этом шарик не выходит за границы холста!
        """
        R = randint(Ball.minimal_radius, Ball.maximal_radius)
        x = randint(0, screen_width-1-2*R)
        y = randint(0, screen_height-1-2*R)
        self._R = R
        self._x = x
        self._y = y
        fillcolor = choice(Ball.available_colors)
        self._avatar = canvas.create_oval(x, y, x+2*R, y+2*R,
                                          width=1, fill=fillcolor,
                                          outline=fillcolor)

        self._Vx = randint(0-Ball.max_offset_Vx, Ball.max_offset_Vx)
        self._Vy = randint(0-Ball.max_offset_Vy, Ball.max_offset_Vy)
        while self._Vx==0 and self._Vy==0:
            self._Vx = randint(0-Ball.max_offset_Vx, Ball.max_offset_Vx)
            self._Vy = randint(0-Ball.max_offset_Vy, Ball.max_offset_Vy)

    def fly(self):
        self._x += self._Vx
        self._y += self._Vy
        # отбивается от горизонтальных стенок
        if self._x < 0:
            self._x = 0
            self._Vx = -self._Vx
        elif self._x + 2*self._R >= screen_width:
            self._x = screen_width - 2*self._R -1
            self._Vx = -self._Vx
        # отбивается от вертикальных стенок
        if self._y < 0:
            self._y = 0
            self._Vy = -self._Vy
        elif self._y + 2*self._R >= screen_height:
            self._y = screen_height - 2*self._R  - 1
            self._Vy = -self._Vy

        canvas.coords(self._avatar, self._x, self._y,
                      self._x + 2*self._R, self._y + 2*self._R)


class Gun:
    def __init__(self, length=60, angle=45):
        self._x = 1
        self._y = screen_height-1
        self._lx = +cos(angle/180*pi)*length
        self._ly = -sin(angle/180*pi)*length
        self._length = length
        self._angle = angle
        self._avatar = canvas.create_line(self._x, self._y,
                                          self._x+self._lx,
                                          self._y+self._ly,
                                          width=5)

    def shoot(self):
        """
        :return возвращает объект снаряда (класса Ball)
        """
        shell = Ball()
        shell._x = self._x + self._lx
        shell._y = self._y + self._ly
        shell._Vx = self._lx/10 #...
        shell._Vy = self._ly/10 #...
        shell._R = 5
        shell.fly()
        return shell


def init_game():
    """
    Создаём необходимое для игры количество объектов-шариков,
    а также объект - пушку.
    """
    global balls, gun, shells_on_fly
    balls = [Ball() for i in range(Ball.initial_number)]
    gun = Gun()
    shells_on_fly = []


def init_main_window():
    global root, canvas, scores_text, scores_value
    root = Tk()
    root.title("Пушка")
    scores_value = IntVar()
    canvas = Canvas(root, width=screen_width, height=screen_height,
                    bg="white")
    scores_text = Entry(root, textvariable=scores_value)
    canvas.grid(row=1, column=0, columnspan=3)
    scores_text.grid(row=0, column=2)
    canvas.bind('<Button-1>', click_event_handler)
    canvas.bind('<Motion>', move_event_handler)


def timer_event():
    # все периодические рассчёты, которые я хочу, делаю здесь
    for ball in balls:
        ball.fly()

    for shell in shells_on_fly:
        shell.fly()

    for ball in balls:
        xi1, yi1, xi2, yi2 = canvas.coords(ball._avatar)
        for shell in shells_on_fly:
            xj1, yj1, xj2, yj2 = canvas.coords(shell._avatar)
            if (xi1 < xj1+5 < xi2) and \
                (yi1 < yj1+5 < yi2):
                    canvas.delete(ball._avatar)
                    canvas.delete(shell._avatar)
                    balls.remove(ball)
                    shells_on_fly.remove(shell)

    canvas.after(timer_delay, timer_event)


def click_event_handler(event):
    global shells_on_fly
    shell = gun.shoot()
    shells_on_fly.append(shell)


def angle(x, y):
    """
    Вычисляет угол наклона прямой в зависимости от текущих коорлинат мышки
    с учетом размеров (высоты screen_height) игрового холста canvas
    :param x: текущая коорлината мышки по X
    :param y: текущая коорлината мышки по Y
    :return: угол в градусах
    """
    return atan2(screen_height - y, x)/pi*180


def move_event_handler(event):
    global gun
    canvas.delete(gun._avatar)
    ug_v_grad = angle(event.x, event.y)
    gun = Gun(angle=ug_v_grad)
    #print('x = ', event.x, 'y = ', event.y, 'angle = ', angle)




if __name__ == "__main__":
    init_main_window()
    init_game()
    timer_event()
    root.mainloop()
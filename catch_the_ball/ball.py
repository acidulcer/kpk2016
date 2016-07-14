import tkinter
from random import choice, randint

ball_initial_number = 20
ball_minimal_radius = 15
ball_maximal_radius = 40
ball_available_colors = ['green', 'blue', 'red', 'lightgray', '#FF00FF', '#FFFF00']
ball_max_offset_x = 10
ball_max_offset_y = 5
score_change_up = 1
score_change_down = 2


def start_command():
    """
    настройки игры сбрасываются по умолчанию для начала новой игры
    :return:
    """
    global score, label_lkm_color, label_pkm_color

    score.set(0)

    canvas.delete("all")

    cvet_fona_lkm = random_color()
    label_lkm_color['bg'] = cvet_fona_lkm
    label_lkm_color['text'] = str(cvet_fona_lkm)

    cvet_fona_pkm = random_color()
    while cvet_fona_pkm == cvet_fona_lkm:
        cvet_fona_pkm = random_color()
    label_pkm_color['bg'] = cvet_fona_pkm
    label_pkm_color['text'] = str(cvet_fona_pkm)

    init_ball_catch_game()


def score_up():
    """
    увеличивает число набранных очков на score_change_up
    текущее значение очков берет из глобпльной переменной score
    :return:
    """
    global score
    score.set(score.get()+score_change_up)


def score_down():
    """
    уменьшает число набранных очков на score_change_down
    текущее значение очков берет из глобальной переменной score
    :return:
    """
    global score
    score.set(score.get()-score_change_down)


def click_ball(event):
    """ Обработчик событий мышки для игрового холста canvas
    :param event: событие с координатами клика
    По клику мышки определяет цвет кликнутого объетка, и:
        1) если нажата ЛКМ и цвет объекта равен "цвету для ЛКМ",
           то увеличиваем количество очков на 1, иначе уменьшаем на 1
        2) если нажата СКМ и цвет объетка на совпадает с "цветом для ЛКМ" и не совпадает с "цветом для ПКМ",
           то увеличиваем количество очков на 1, иначе уменьшаем на 1
        3) если нажата ПКМ и цвет объекта равен "цвету для ПКМ",
           то увеличиваем количество очков на 1, иначе уменьшаем на 1
    По клику мышки удаляется тот объект, на который мышка указывает.
    """
    global score, label_lkm_color, label_pkm_color
    obj = canvas.find_closest(event.x, event.y)
    x1, y1, x2, y2 = canvas.coords(obj)

    if x1 <= event.x <= x2 and y1 <= event.y <= y2:
        if event.num == 1:
            if canvas.itemconfig(obj)['fill'][4] == label_lkm_color['bg']:
                score_up()
            else:
                score_down()
        elif event.num == 2:
            if (canvas.itemconfig(obj)['fill'][4] != label_lkm_color['bg']) \
                    and (canvas.itemconfig(obj)['fill'][4] != label_pkm_color['bg']):
                score_up()
            else:
                score_down()
        else:
            if canvas.itemconfig(obj)['fill'][4] == label_pkm_color['bg']:
                score_up()
            else:
                score_down()

        canvas.delete(obj)

        create_random_ball()


def move_all_balls(event):
    """ передвигает все шарики при движении мышкой
    """
    #for obj in canvas.find_all():
    #    dx = randint(-1, 1)
    #    dy = randint(-1, 1)
    #    canvas.move(obj, dx, dy)
    k = 0
    for obj in canvas.find_all():
        h = int(canvas['height'])
        w = int(canvas['width'])
        x1, y1, x2, y2 = canvas.coords(obj)
        if x1<3 or x2>w-3:
            v[k][0]=-v[k][0]
        if y1 < 3 or y2>h-3:
            v[k][1] = -v[k][1]
        canvas.move(obj, v[k][0],v[k][1])
        k+=1


def create_random_ball():
    """
    создаёт шарик в случайном месте игрового холста canvas,
     при этом шарик не выходит за границы холста!
    """
    R = randint(ball_minimal_radius, ball_maximal_radius)
    x = randint(0, int(canvas['width'])-1-2*R)
    y = randint(0, int(canvas['height'])-1-2*R)
    canvas.create_oval(x, y, x+2*R, y+2*R, width=1, fill=random_color())


def random_color():
    """
    :return: Случайный цвет из некоторого набора цветов
    """
    return choice(ball_available_colors)


def init_ball_catch_game():
    """
    Создаём необходимое для игры количество шариков, по которым нужно будет кликать

    для каждого шарика запоминаем смещение, учитывая параметры ball_max_offset_x и ball_max_offset_y.
    """
    global v
    v=[]

    for i in range(ball_initial_number):
        vx = randint(0-ball_max_offset_x, ball_max_offset_x)
        vy = randint(0-ball_max_offset_y, ball_max_offset_y)
        while vx==0 and vy==0:
            vx = randint(0-ball_max_offset_x, ball_max_offset_x)
            vy = randint(0-ball_max_offset_y, ball_max_offset_y)
        v.append([vx, vy])
        create_random_ball()


def init_main_window():
    global root, canvas, label, score, label_lkm_color, label_pkm_color, v

    root = tkinter.Tk()

    v=[]

    label_lkm_text = tkinter.Label(root,  text="Цвет для ЛКМ")
    #label_lkm_text.pack()
    cvet_fona_lkm = random_color()
    label_lkm_color = tkinter.Label(root,  text=str(cvet_fona_lkm), bg=cvet_fona_lkm)
    #label_lkm_color.pack()

    label_score_text = tkinter.Label(root,  text="Набранные очки")
    #label_score_text.pack()
    score = tkinter.IntVar(0)
    label = tkinter.Label(root,  text="Очки: ", textvariable=score)
    #label.pack()

    label_pkm_text = tkinter.Label(root,  text="Цвет для ПКМ")
    #label_pkm_text.pack()
    cvet_fona_pkm = random_color()
    while cvet_fona_pkm == cvet_fona_lkm:
        cvet_fona_pkm = random_color()
    label_pkm_color = tkinter.Label(root,  text=str(cvet_fona_pkm), bg=cvet_fona_pkm)
    #label_pkm_color.pack()

    canvas = tkinter.Canvas(root, background='white', width=400, height=400)
    canvas.bind("<Button>", click_ball)
    canvas.bind("<Motion>", move_all_balls)
    #canvas.pack()

    button1 = tkinter.Button(root, text="Новая игра", command=start_command)

    #расположение элементов
    label_lkm_text.grid(row=0, column=0)
    label_lkm_color.grid(row=1, column=0)
    label_pkm_text.grid(row=0, column=1)
    label_pkm_color.grid(row=1, column=1)
    label_score_text.grid(row=0, column=2)
    label.grid(row=1, column=2)
    button1.grid(row=0, column=3, rowspan=2)
    canvas.grid(row=2, column=0, columnspan=4)



if __name__ == "__main__":
    init_main_window()
    init_ball_catch_game()
    root.mainloop()
print("Приходите поиграть ещё!")
import tkinter
import random
from tkinter import messagebox


flag_new_figure = False  # флаг выбора новой фигуры для следующего хода
flag_fall = True  # флаг того что фигура ещё может падать
y_step = 0  # шаг падения фигуры. увеличивается от 0 в момент появления до утыкания фигуры в другую и конца поля
x_shift = 4  # сдвиг фигуры по горизонтали
next_figure = ''  # следующая падающая фигура
current_figure = ''  # текущая падающая фигура
who_figure = 0  # переменная которая хранит подтип падающей фигуры (нужна для вращения фигуры)
y_last = [0, 0, 0, 0]  # переменные которые хранят координаты поля где находиласть текущая фигуры и по ним
x_last = [0, 0, 0, 0]  # поле перекрашивается обратно в светлый цвет
speed = 1
const_fall_time = (11 - speed) * 50
last_count_change_speed = 0
temp_param = 0
figure = {'figure_kv': [[[0, 0], [1, 0], [0, 1], [1, 1]], 1],  # типы фигур, координаты точек, сколько есть вариантов

          'figure_I': [[[0, 0], [1, 0], [2, 0], [3, 0]],
                       [[0, 0], [0, 1], [0, 2], [0, 3]], 2],

          'figure_L_right': [[[0, 0], [1, 0], [2, 0], [2, 1]],
                            [[1, 0], [1, 1], [0, 2], [1, 2]],
                            [[0, 0], [0, 1], [1, 1], [2, 1]],
                            [[1, 0], [0, 0], [0, 1], [0, 2]], 4],

          'figure_L_left': [[[0, 1], [1, 1], [2, 0], [2, 1]],
                            [[0, 0], [1, 0], [1, 1], [1, 2]],
                            [[0, 0], [1, 0], [2, 0], [0, 1]],
                            [[0, 0], [0, 1], [0, 2], [1, 2]], 4],

          'figure_s_left': [[[0, 0], [1, 0], [1, 1], [2, 1]],
                            [[1, 0], [1, 1], [0, 1], [0, 2]], 2],

          'figure_s_right': [[[0, 1], [2, 0], [1, 0], [1, 1]],
                             [[0, 0], [0, 1], [1, 1], [1, 2]], 2],

          'figure_T': [[[1, 0], [1, 1], [0, 1], [1, 2]],
                       [[0, 0], [1, 0], [2, 0], [1, 1]],
                       [[0, 0], [0, 1], [1, 1], [0, 2]],
                       [[1, 0], [0, 1], [1, 1], [2, 1]], 4]
          }


def shift_right(event):  # функция сдвига фигуры вправо
    global x_shift
    if x_shift + figure[current_figure][who_figure][-1][-1] < 9:  # если сдвиг по х + самая правая часть фигуры не
        x_shift += 1  # выходят за границу поля, то увеличим сдвиг вправо на 1
    else:
        x_shift = 9 - figure[current_figure][who_figure][-1][-1]  # если нет, то выставим сдвиг такой чтобы самая
        # правая часть фигуры была на краю поля
        # figure[current_figure][who_figure][-1][-1] - есть самая правая координата фигуры
    otrisovka(y_step, x_shift, current_figure, who_figure, 0, True)


def shift_left(event): # функция сдвига фигуры влево
    global x_shift
    if x_shift > 0:  # т.к. отсчёт координат всех фигур начинается с 0, то если сдвиг будет меньше нуля, сдвиг дальше
        x_shift -= 1  # не уменьшаем
    else:
        x_shift = 0
    otrisovka(y_step, x_shift, current_figure, who_figure, 0, True)


def move_fall_fast(event):
    global const_fall_time, flag_after_cancel
    pole_game.after_cancel(flag_after_cancel)  # надо отменить предыдущий перезапуск, ибо если это не сделать то фигурка
    const_fall_time = 20  # ускориться только через следующий ход. Как бы будет задержка ускорения падения
    flag_after_cancel = pole_game.after_idle(fall_figure)  # снова запустим падение, но уже ускорено


def move_fall_low(event):
    global const_fall_time
    const_fall_time = (11 - speed) * 50


def rotate_figure(event):  # функция вращения фигуры. тут поочерёдно выбираются подтипы падающей фигуры
    global current_figure, who_figure, x_shift, y_step
    if who_figure+1 < figure[current_figure][-1]:
        who_figure += 1
        while x_shift + figure[current_figure][who_figure][-1][-1] >= 10:
            x_shift -= 1
    else:
        who_figure = 0
    otrisovka(y_step, x_shift, current_figure, who_figure, 0, True)


def del_line():
    global speed, last_count_change_speed
    count = 0
    count_segment_line = 0
    i = 29
    while i > -1:  # идём снизу вверх до тех пор пока не достогнем верхней части поля. если встречаем законченную линию
        for j in range(10):  # то её зачищаем опускаем всё что выше неё и начинаем проход заново с нижней части поля
            if globals()['label{}*{}'.format(i, j)]['bg'] == 'gray3':  # для поиска ещё законченных строк
                count_segment_line += 1
        if count_segment_line == 10:  # если в строке десять чёрных клеток то...
            count += 1
            for j in range(10):  # перекрашиваем строку
                globals()['label{}*{}'.format(i, j)]['bg'] = 'linen'
            for k in range(i-1, -1, -1):  # перекрашиваем все клетки, которые выше удаляемой линии, на одну клетку вниз
                for o in range(10):
                    if globals()['label{}*{}'.format(k, o)]['bg'] == 'gray3':
                        globals()['label{}*{}'.format(k+1, o)]['bg'] = 'gray3'
                        globals()['label{}*{}'.format(k, o)]['bg'] = 'linen'
            i = 30
        count_segment_line = 0  # обнуляем счётчик
        i -= 1
    if count == 1:  # накинем очков
        text_count['text'] += 2
    elif count == 2:
        text_count['text'] += 4
    elif count == 3:
        text_count['text'] += 6
    elif count == 4:
        text_count['text'] += 8
    if text_count['text'] - last_count_change_speed > 20 and speed < 9:  # ускорим игру через каждые 50 набранных очков
        speed += 1
        last_count_change_speed = text_count['text']
        text_speed['text'] = speed


def fall_figure():  # основная функция. функция падения фигур. запускается каждые speed*50 мс
    global next_figure, x_shift, y_step, flag_fall, current_figure, who_figure, const_fall_time, flag_after_cancel
    global temp_param
    flag_after_cancel = pole_game.after(const_fall_time, fall_figure)  # повторный запуск функции
    for i in figure[current_figure][who_figure]:
        if i[0] + y_step + 1 > 29 or globals()['label{}*{}'.format(i[0] + y_step + 1, i[1] + x_shift)]['bg'] == 'gray3':
            flag_fall = False
    if flag_fall is True:
        otrisovka(y_step, x_shift, current_figure, who_figure, 0, True)
        y_step += 1
    else:
        otrisovka(y_step, x_shift, current_figure, who_figure, 0, False)
        del_line()
        const_fall_time = (11 - speed) * 50
        flag_fall = True
        y_step = 0
        x_shift = 4
        current_figure = next_figure
        next_figure = random.choice(list(figure.keys()))
        who_figure = 0
        otrisovka(0, 0, next_figure, who_figure, 1, True)


def otrisovka(y, x, figure_type, who_figure2, pole, flag):  # функция отрисовки фигуры на полях
    # у, х - координаты с которых надо отрисовать новую фигуру (к ним прибавляются координаты самой фигуры)
    # figure_type - тип той фигуры из словаря фигур который надо отрисовывать ("figure_kv или figure_s_right и пр.")
    # who_figure2 - подтип фигуры из словаря фигур (тот самый массив координат который надо отрисовать)
    # pole - если 1 - то фигуру надо отрисовать в маленьком поле. 2 в большом
    # flag - местная переменная. если она True, то это значит фигура падает и нам надо затирать старое положение и
    # падающая фигура красится в цвет black. Если False, то фигура не падает и последнее её положение красим в gray3
    global x_last, y_last, y_step
    if pole == 1:  # рисуем фигуру на маленьком поле
        for i in range(4):
            for j in range(3):
                globals()['label{}**{}'.format(i, j)]['bg'] = 'linen'
        for i in figure[figure_type][who_figure2]:
            globals()['label{}**{}'.format(i[0] + y, i[1] + x)]['bg'] = 'black'
    else:  # рисуем фигуру на большом поле
        if flag is False:  # фигура перестала падать
            for i in range(4):  # затираем предыдущее положение фигуры
                if globals()['label{}*{}'.format(y_last[i], x_last[i])]['bg'] == 'black':
                    globals()['label{}*{}'.format(y_last[i], x_last[i])]['bg'] = 'linen'
            y_last = []  # сбрасываем координаты предыдущего положения
            x_last = []
            for i in figure[figure_type][who_figure2]:
                globals()['label{}*{}'.format(i[0] + y, i[1] + x)]['bg'] = 'gray3'
        else:  # фигура падает
            if y_last != [] and x_last != []:  # т.к. после падения предыдущей фигуры координаты были сброшены
                for i in range(4):  # затираем предыдущее положение фигуры
                    if globals()['label{}*{}'.format(y_last[i], x_last[i])]['bg'] == 'black':
                        globals()['label{}*{}'.format(y_last[i], x_last[i])]['bg'] = 'linen'
                y_last = []  # сбрасываем координаты предыдущего положения
                x_last = []
            for i in figure[figure_type][who_figure2]:  # рисуем новое положение и запоминаем её координаты для
                globals()['label{}*{}'.format(i[0] + y, i[1] + x)]['bg'] = 'black' # следующей отрисовки
                y_last += [i[0] + y]
                x_last += [i[1] + x]


def fall_start():
    global flag_after_cancel
    flag_after_cancel = pole_game.after_idle(fall_figure)


def fall_pause():
    pole_game.after_cancel(flag_after_cancel)


def change_speed_plus():
    global speed
    if speed < 9:
        speed += 1
    text_speed['text'] = speed


def change_speed_minus():
    global speed
    if speed > 1:
        speed -= 1
    text_speed['text'] = speed


# ----------------создание окна---------------------
pole_game = tkinter.Tk()
pole_game.title('Тетрис от Alex_chel_man')
pole_game.geometry('500x700')
frame = tkinter.Frame(pole_game, bg='gold', height=100, width=100)
frame.place(x=250, y=200)
# ------------создадим поле и надписи----------------
for i in range(4):
    for j in range(3):
        globals()['label{}**{}'.format(i, j)] = tkinter.Label(frame, text='     ', bg='linen', relief='groove')
        globals()['label{}**{}'.format(i, j)].grid(row=i, column=j)

for i in range(30):
    for j in range(10):
        globals()['label{}*{}'.format(i, j)] = tkinter.Label(text='     ', bg='linen', relief='groove')
        globals()['label{}*{}'.format(i, j)].grid(row=i, column=j)

label_name = tkinter.Label(text='Тетрис', font='Arial 14')
label_name.place(x=250, y=20)

button_start = tkinter.Button(text='Старт', font='Arial 20', command=fall_start)
button_start.place(x=250, y=400)
button_pause = tkinter.Button(text='Пауза', font='Arial 20', command=fall_pause)
button_pause.place(x=350, y=400)

button_speed_plus = tkinter.Button(text='+', command=change_speed_plus)
button_speed_plus.place(x=370, y=250)
button_speed_minus = tkinter.Button(text='- ', command=change_speed_minus)
button_speed_minus.place(x=370, y=280)

text_motivation = tkinter.Label(text='следующая фигура', font='Arial 15')
text_motivation.place(x=250, y=150)
label_speed = tkinter.Label(text='Скорость', font='Arial 14')
label_speed.place(x=370, y=220)
text_speed = tkinter.Label(text=speed, font='Arial 14')
text_speed.place(x=400, y=265)
label_count = tkinter.Label(text='Счёт:', font='Arial 14')
label_count.place(x=250, y=75)
text_count = tkinter.Label(text=0, font='Arial 14')
text_count.place(x=310, y=75)

info = tkinter.Label(text='Вращение - пробел\n\nУправление движением -\na s d (англ)', font='Arial 15')
info.place(x=250, y=500)
# ----------------------запуск-----------------------
next_figure = random.choice(list(figure.keys()))
current_figure = random.choice(list(figure.keys()))
otrisovka(0, 0, next_figure, who_figure, 1, True)
pole_game.bind('<space>', rotate_figure)
pole_game.bind('a', shift_left)
pole_game.bind('d', shift_right)
pole_game.bind('<KeyPress-s>', move_fall_fast)  # нажали s - падаем быстрее
pole_game.bind('<KeyRelease-s>', move_fall_low)  # отпустили s - падаем медленее

pole_game.mainloop()

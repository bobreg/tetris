# tetris
# python
# tkinter
Тетрис на Python и Tkinter
Тетрис реализован при помощи библиотеки tkinter. С помощью этой библиотеки нарисовано поле и перерисовываются падающие фигурки.

Падение фигурок происходит цикличным перезапуском главной функции fall_figure. С каждым вызовом функции координата перерисовки 
увеличивается на 1 (верх поля это 0 строка, низ это 29 строка).
Перед перерисовкой фигуры происходит проверка на две вещи: фигура достигла дна и фигура коснулась уже лежащей фигуры.
Если внизу на один шаг ничего нет, то можно перерисовывать фигуру.

Для понимания того что фигура коснулась другой фигуры используется следующий способ: 
  - падающая фигура отрисовывается в цвете black;
  - уже упавшая фигура отрисовывается в цвете gray3;
  - свободное поле имеет цвет linen;
  - при падении фигуры для каждой клетки самой фигуры проверяется что поле внизу имеет цвет linen или gray3;
  - если внизу под любой клеткой падающей фигуры есть клетка в цвете gray3, то фигура останавливается и также перерисовывается в gray3.
  
В момент когда фигура закончила падение происходит цикличная проверка на полностью заполненые строки.
Проверка на заполненые строки начинается с 29 строки и идёт до 0 строки. Если заполненая строка найдена, то она перерисовывается в цвет
linen и все клетки над ней в цвете gray3 опускаются на одну клетку вниз. Цикл проверки начинаем снова с 29 строки, чтобы удалить еще 
существующие заполненые строки. 

Также в игре реализован подсчёт очков. За одну собранную строку за ход даётся 2 очка, за 4 даётся 8 очков

В игре можно менять скорость падения фигурок. И скорость падения фигурок увеличивается с ростом количества очков.

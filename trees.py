import turtle
import re
import random

# Добавляем параметры 

# список функций для управления параметаризированными командами
# у всех функций будет префикс cmd_ и первый параметр t - черепашка
def cmd_turtle_fd(t, length, *args):
    t.pensize(args[1])
    t.fd(length*args[0])

def cmd_turtle_left(t, angle, *args): # поварачивает черепашку влево
    t.left(args[0]) 

def cmd_turtle_right(t, angle, *args): # поварачивает вправо
    t.right(args[0])

class LSystem:
    def __init__(self, t, axiom, width, length, angle):
        self.axiom = axiom # инициатр
        self.state = axiom # строка с набором команд для фрактала
        self.width = width # толщина линии рисованияя
        self.length = length # длина одного лнейного сигмента кривой
        self.angle = angle # фиксированный угол поворота
        self.t = t  # черепашка
        self.rules = {} # словарь для хранения правил формирования кревых
        self.t.pensize(self.width) # ширина линии рисования
        self.key_re_list = [] # шаблон команд
        self.cmd_functions = {}  # словарь связей параметаризованных команд и функций
        self.function_key = None

    def add_rules(self, *rules):
        for key, value in rules:
            key_re = ""  
            if not isinstance(value, str): # ключ с параметрами
                key_re = key.replace("(", r"\(")
                key_re = key_re.replace(")", r"\)")
                key_re = key_re.replace("+", r"\+")
                key_re = key_re.replace("-", r"\-")
                key_re = re.sub(r"([a-z]+)([, ]*)", lambda m: r"([-+]?\b\d+(?:\.\d+)?\b)" + m.group(2), key_re)
                self.key_re_list.append(key_re)

            self.rules[key] = (value, key_re)


    def update_param_cmd(self, m):
        if not self.function_key: # ссылается на lambda функцию
            return ""

        args = list(map(float, m.groups()))
        return self.function_key(*args).lower()


    def generate_path(self, n_iter):
        for n in range(n_iter):
            for key, value in self.rules.items():
                if isinstance(value[0], str):
                    self.state = self.state.replace(key, value[0].lower())
                else:   # команда с параметром
                    self.function_key = value[0]   # ссылка на лямбда-функцию
                    self.state = re.sub(value[1], self.update_param_cmd, self.state)
                    self.function_key = None

            self.state = self.state.upper()

    def set_turtle(self, my_tuple):
        self.t.up()
        self.t.goto(my_tuple[0], my_tuple[1]) # переносит черепашку в нужные координаты
        self.t.seth(my_tuple[2]) # угол поварота
        self.t.down()

    def add_rules_move(self, *moves):
        for key, func in moves:
            self.cmd_functions[key] = func


    def drow_turtle(self, start_pos, start_angle):
        turtle.tracer(1, 0) # скорость черепашки
        self.t.up() # черепашка поднимается на верх
        self.t.setpos(start_pos) # начальная стартовая позиция
        self.t.seth(start_angle) # начальный угол поворота 
        self.t.down() # черепашка опускается вниз
        turtle_stack = []# хранит данные для ветвления
        key_list_re = "|".join(self.key_re_list)

        for value in re.finditer(r"(" + key_list_re + r"|.)", self.state):
            cmd = value.group(0)
            args = [float(x) for x in value.groups()[1:] if x]
            if 'F' in cmd:
                if len(args) > 0 and self.cmd_functions.get('F'):
                    self.cmd_functions['F'](t, self.length, *args)
                else:
                    self.t.fd(self.length)
            elif 'S' in cmd:
                if len(args) > 0 and self.cmd_functions.get('S'):
                    self.cmd_functions['S'](t, self.length, *args)
                else:
                    self.t.up()
                    self.t.forward(self.length)
                    self.t.down()
            elif '+' in cmd:
                if len(args) > 0 and self.cmd_functions.get('+'):
                    self.cmd_functions['+'](t, self.angle, *args)
                else:
                    self.t.left(self.angle)
            elif '-' in cmd:
                if len(args) > 0 and self.cmd_functions.get('-'):
                    self.cmd_functions['-'](t, self.angle, *args)
                else:
                    self.t.right(self.angle)
            elif "[" in cmd:
                turtle_stack.append((self.t.xcor(), self.t.ycor(), self.t.heading(), self.t.pensize()))
            elif "]" in cmd:
                xcor, ycor, head, w = turtle_stack.pop()
                self.set_turtle((xcor, ycor, head))
                self.width = w
                self.t.pensize(self.width)
        turtle.done() # используем что бы окно не закрывалось после отрисовки изображения 

#  прописываем что бы окно появилось, с размерами 1200х600
width = 1100
height = 600
screen = turtle.Screen()
screen.setup(width, height, 0, 0)

t = turtle.Turtle()
t.ht() #  прописываем что бы черепашка не была видна

pen_width = 2 # толщина линни рисования 
f_len = 20 # длина одного сегмента прямой (в пикселах)
angle = 33 # фиксированный угол поворота 
axiom = "A"

l_sys = LSystem(t, axiom, pen_width, f_len, angle)
l_sys.add_rules(("A", f"F(1, 1)[+({angle}))A][-({angle})A]"),
                ("F(x, y)", lambda x, y: f"F({(1.2+random.triangular(-0.5, 0.5, random.gauss(0, 1)))*x}, {1.4*y})"), # талщина дерева
                ("+(x)", lambda x: f"+({x + random.triangular(-10, 10, random.gauss(0,2))})"), # длина элементов дерева
                ("-(x)", lambda x: f"-({x + random.triangular(-10, 10, random.gauss(0,2))})"), # углы поварота
                )
l_sys.add_rules_move(("F", cmd_turtle_fd), ("+", cmd_turtle_left), ("-", cmd_turtle_right))
l_sys.generate_path(5) # колличество итерации
l_sys.drow_turtle((0, -200), 90)


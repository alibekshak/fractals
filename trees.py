import turtle
import re

# Добавляем параметры 

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

        
    def add_rules(self, *rules):
        for key, value in rules:
            key_re = ""  
            if not isinstance(value, str): # ключ с параметрами
                key_re = key.replace("(", r"\(")
                key_re = key_re.replace(")", r"\)")
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

    def drow_turtle(self, start_pos, start_angle):
        turtle.tracer(1, 0) # скорость черепашки
        self.t.up() # черепашка поднимается на верх
        self.t.setpos(start_pos) # начальная стартовая позиция
        self.t.seth(start_angle) # начальный угол поворота 
        self.t.down() # черепашка опускается вниз
        turtle_stack = []# хранит данные для ветвления
        for move in self.state:
            if move == "F":
                self.t.forward(self.length)
            elif move == "S": # для формирования более сложных фракталов
                self.t.up()
                self.t.forward(self.length)
                self.t.down()
            elif move == "+":
                self.t.left(self.angle)
            elif move == "-":
                self.t.right(self.angle)
            elif move == "[":
                turtle_stack.append((self.t.xcor(), self.t.ycor(), self.t.heading(), self.t.pensize()))
            elif move == "]":
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
f_len = 8# длина одного сегмента прямой (в пикселах)
angle = 33 # фиксированный угол поворота 
axiom = "F(1)+A(1)"

l_sys = LSystem(t, axiom, pen_width, f_len, angle)
l_sys.add_rules(("A(x)", lambda x: f"F({x+1})+A({x+1})"))
l_sys.generate_path(6) # колличество итерации
l_sys.drow_turtle((0, -200), 90)


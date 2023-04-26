import turtle

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

    def add_rules(self, *rules):
        for key, value in rules:
            self.rules[key] = value

    def generate_path(self, n_iter):
        for n in range(n_iter):
            for key, value in self.rules.items():
                self.state = self.state.replace(key, value.lower())

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
axiom = "А" 

l_sys = LSystem(t, axiom, pen_width, f_len, angle)
l_sys.add_rules(("F", "FF"), ("А", "F[+А][-А]"))
l_sys.generate_path(6) # колличество итерации
l_sys.drow_turtle((0, -200), 90)


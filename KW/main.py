from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math as m


# параметры
k = 100 # масштабировние
mul = 10 # коэффициент массштабирования
w = 3 * mul
h = 2 * mul
levels = 3 * mul
k_round = mul // 2

r = lambda x, y:  m.sqrt(x ** 2 + y ** 2)



class Vertex:
	def __init__(self, x = 0., y = 0., z = 0.):
		self.x = x
		self.y = y
		self.z = z

class Triangle:
	def __init__(self, vertex_1, vertex_2, vertex_3):
		self.vertex_1 = vertex_1
		self.vertex_2 = vertex_2
		self.vertex_3 = vertex_3

class Figure:
	def __init__(self, color):
		self.pointdata = []
		self.color = color

	def add_pointdata(self, pointdata):
		self.pointdata.append(pointdata)

	def add_half(self, kx, ky, kz):
		size = len(self.pointdata)
		for i in range(size):
			vertex_1 = Vertex(kx*self.pointdata[i].vertex_1.x, ky*self.pointdata[i].vertex_1.y, kz*self.pointdata[i].vertex_1.z)
			vertex_2 = Vertex(kx*self.pointdata[i].vertex_2.x, ky*self.pointdata[i].vertex_2.y, kz*self.pointdata[i].vertex_2.z)
			vertex_3 = Vertex(kx*self.pointdata[i].vertex_3.x, ky*self.pointdata[i].vertex_3.y, kz*self.pointdata[i].vertex_3.z)
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			self.pointdata.append(triangle)

	def add_half_x(self):
		self.add_half(-1, 1, 1)

	def add_half_y(self):
		self.add_half(1, -1, 1)

	def add_half_z(self):
		self.add_half(1, 1, -1)

	def copy(self, pill_box_part):
		for i in range(len(self.pointdata)):
			vertex_1 = Vertex(self.pointdata[i].vertex_1.x, self.pointdata[i].vertex_1.y, self.pointdata[i].vertex_1.z)
			vertex_2 = Vertex(self.pointdata[i].vertex_2.x, self.pointdata[i].vertex_2.y, self.pointdata[i].vertex_2.z)
			vertex_3 = Vertex(self.pointdata[i].vertex_3.x, self.pointdata[i].vertex_3.y, self.pointdata[i].vertex_3.z)
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			pill_box_part.add_pointdata(triangle)

class PillBox:
	def __init__(self, color):
		self.base = Figure(color)
		self.cap = Figure(color)
		self.lock = Figure(color)

class Pill:
	def __init__(self, color_cover, color_cross_section):
		self.cover = Figure(color_cover)
		self.cross_section = Figure(color_cross_section)

blue_pill_box = PillBox([0., 0., 1., 1.])
white_pill_box = PillBox([1., 1., 1., 1.])
pills = []

# функии
def create__pill_box():
	round = lambda y: (y ** 2) / k_round
	anti_round = lambda y: m.sqrt(y * k_round)

	# генерация прямоугольной части
	for x in range(w):
		for y in range(h // 2):
			# правый нижний треугольник
			vertex_1 = Vertex(x, y, 0.)
			vertex_2 = Vertex(x+1, y, 0.)
			vertex_3 = Vertex(x+1, y + 1, 0.)
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.base.add_pointdata(triangle)

			# левый верхний треугольник
			vertex_2 = Vertex(x, y + 1, 0.)
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.base.add_pointdata(triangle)

	# генерация скруглений по бокам
	delta = h // 2
	delta_y = k_round / levels

	for x in range(w):
		for y in range(levels):
			# правый нижний треугольник
			vertex_1 = Vertex(x, y * delta_y + delta, round(y * delta_y))
			vertex_2 = Vertex(x + 1, y * delta_y + delta, round(y * delta_y))
			vertex_3 = Vertex(x + 1,  (y + 1) * delta_y + delta, round((y + 1) * delta_y))
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.base.add_pointdata(triangle)

			# левый верхний треугольник
			vertex_2 = Vertex(x, (y + 1) * delta_y + delta, round((y + 1) * delta_y))
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.base.add_pointdata(triangle)

	# стенки
	highest_z = k_round
	highest_y = k_round + delta

	for x in range(w):
		for z in range(mul):
			# правый нижний треугольник
			vertex_1 = Vertex(x, highest_y, highest_z + z)
			vertex_2 = Vertex(x + 1, highest_y, highest_z + z)
			vertex_3 = Vertex(x + 1, highest_y, highest_z + (z + 1))
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.base.add_pointdata(triangle)

			# левый верхний треугольник
			vertex_2 = Vertex(x, highest_y, highest_z + (z + 1))
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.base.add_pointdata(triangle)

	# перегородки
	border_x_left = w // 10
	border_x_right = w * 9 // 10
	delta_z = (highest_z + mul) / (2 * levels)

	for i in range(2 * levels): # уровни
		if(delta_z * i <= highest_z):
			delta_y_low = (2 * anti_round(delta_z * i) + h) / h
		else:
			delta_y_low = 2 * highest_y / h
		if(delta_z * (i + 1) <= highest_z):
			delta_y_high = (2 * anti_round(delta_z * (i + 1)) + h) / h
		else:
			delta_y_high = 2 * highest_y / h

		for j in range(h // 2):
			# левая перегородка

			# правый нижний треугольник
			vertex_1 = Vertex(border_x_left, j * delta_y_low, i * delta_z)
			vertex_2 = Vertex(border_x_left, (j + 1) * delta_y_low, i * delta_z)
			vertex_3 = Vertex(border_x_left, (j + 1) * delta_y_high, (i + 1) * delta_z)
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.base.add_pointdata(triangle)

			# левый верхний треугольник
			vertex_2 = Vertex(border_x_left, j * delta_y_high, (i + 1) * delta_z)
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.base.add_pointdata(triangle)

			# правая перегородка

			# правый нижний треугольник
			vertex_1 = Vertex(border_x_right, j * delta_y_low, i * delta_z)
			vertex_2 = Vertex(border_x_right, (j + 1) * delta_y_low, i * delta_z)
			vertex_3 = Vertex(border_x_right, (j + 1) * delta_y_high, (i + 1) * delta_z)
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.base.add_pointdata(triangle)

			# левый верхний треугольник
			vertex_2 = Vertex(border_x_right, j * delta_y_high, (i + 1) * delta_z)
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.base.add_pointdata(triangle)

	# полуокружность co скруглением
	radius = h // 2 + k_round
	delta_r = radius / (2 * levels)
	round_circle = lambda r: max(0., np.sign(r - delta) * round((r - delta)))

	for i in range(2 * levels):
		delta_y_low = 2 * m.sqrt(radius ** 2 - (delta_r * i) ** 2) / h
		delta_y_high = 2 * m.sqrt(radius ** 2 - (delta_r * (i + 1)) ** 2) / h

		for j in range(h // 2):
			# правый нижний треугольник
			vertex_1 = Vertex(-delta_r * i, delta_y_low * j, round_circle(r(delta_r * i, delta_y_low * j)))
			vertex_2 = Vertex(-delta_r * i, delta_y_low * (j + 1), round_circle(r(delta_r * i, delta_y_low * (j + 1))))
			vertex_3 = Vertex(-delta_r * (i + 1), delta_y_high * (j + 1), round_circle(r(delta_r * (i + 1), delta_y_high * (j + 1))))
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.base.add_pointdata(triangle)

			# левый верхний треугольник
			vertex_2 = Vertex(-delta_r * (i + 1), delta_y_high * j, round_circle(r(delta_r * (i + 1), delta_y_high * j)))
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.base.add_pointdata(triangle)

	# стенки полуокружности
	coord = lambda x: m.sqrt(radius ** 2 - x ** 2)

	for x in range(radius):
		for z in range(mul):
			# правый нижний треугольник
			vertex_1 = Vertex(-x, coord(x), highest_z + z)
			vertex_2 = Vertex(-(x + 1), coord(x + 1), highest_z + z)
			vertex_3 = Vertex(-(x + 1), coord(x + 1), highest_z + (z + 1))
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.base.add_pointdata(triangle)

			# левый верхний треугольник
			vertex_2 = Vertex(-x, coord(x), highest_z + (z + 1))
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.base.add_pointdata(triangle)

	blue_pill_box.base.add_half_y() # дорисовывает вторую половину
	blue_pill_box.base.copy(blue_pill_box.cap) # копируем в крышку

	# создание крепежа
	radius = mul
	length = h // 2 + k_round
	a = (radius * 1.5) / 2
	b = (mul + k_round + 2 * radius) / 2

	z = lambda x: m.sqrt(radius ** 2 - x ** 2)

	# цилиндр
	for x in range(radius):
		for y in range(length):
			# правый нижний треугольник
			vertex_1 = Vertex(x, y, z(x))
			vertex_2 = Vertex(x + 1, y, z(x + 1))
			vertex_3 = Vertex(x + 1, y + 1, z(x + 1))
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.lock.add_pointdata(triangle)

			# левый верхний треугольник
			vertex_2 = Vertex(x, y + 1, z(x))
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.lock.add_pointdata(triangle)

	# овал
	delta_r = b / levels
	for i in range(levels):
		delta_y_low = a * m.sqrt(1 - (delta_r * i / b) ** 2) / levels
		delta_y_high = a * m.sqrt(radius ** 2 - (delta_r * (i + 1) / b) ** 2) / levels

		# поверхность
		for j in range(levels):
			# правый нижний треугольник
			vertex_1 = Vertex(j * delta_y_low, length, delta_r * i)
			vertex_2 = Vertex((j + 1) * delta_y_low, length, delta_r * i)
			vertex_3 = Vertex((j + 1) * delta_y_high, length, delta_r * (i + 1))
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.lock.add_pointdata(triangle)

			# левый верхний треугольник
			vertex_2 = Vertex(j * delta_y_high, length, delta_r * (i + 1))
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			blue_pill_box.lock.add_pointdata(triangle)

	blue_pill_box.lock.add_half_y()
	blue_pill_box.lock.add_half_z()
	blue_pill_box.lock.add_half_x()

	# копируем в прозрачную
	blue_pill_box.base.copy(white_pill_box.base)
	blue_pill_box.cap.copy(white_pill_box.cap)
	blue_pill_box.lock.copy(white_pill_box.lock)

	# TODO: поворот и перенос крышки, основания и крепежа


def create__pill():
	radius = mul
	delta_r = radius / levels
	pill = Pill([0., 1., 0., 1.], [0., 0., 0., 1.])

	# четвертинка поверхности таблетки
	for i in range(levels):
		delta_y_low = m.sqrt(radius ** 2 - (delta_r * i) ** 2) / levels
		delta_y_high = m.sqrt(radius ** 2 - (delta_r * (i + 1)) ** 2) / levels

		# поверхность
		for j in range(levels):
			# правый нижний треугольник
			vertex_1 = Vertex(delta_r * i, delta_y_low * j, m.sqrt(radius ** 2 - r(delta_r * i, delta_y_low * j) ** 2) / 2)
			vertex_2 = Vertex(delta_r * i, delta_y_low * (j + 1), m.sqrt(radius ** 2 - r(delta_r * i, delta_y_low * (j + 1)) ** 2) / 2)
			vertex_3 = Vertex(delta_r * (i + 1), delta_y_high * (j + 1), m.sqrt(radius ** 2 - r(delta_r * (i + 1), delta_y_high * (j + 1)) ** 2) / 2)
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			pill.cover.add_pointdata(triangle)

			# левый верхний треугольник
			vertex_2 = Vertex(delta_r * (i + 1), delta_y_high * j, m.sqrt(radius ** 2 - r(delta_r * (i + 1), delta_y_high * j) ** 2) / 2)
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			pill.cover.add_pointdata(triangle)

	pill.cover.add_half_y()
	pill.cover.add_half_z()

	# разрез
	for i in range(levels):
		delta_y_low = m.sqrt(radius ** 2 - (delta_r * i) ** 2) / (2 * levels)
		delta_y_high = m.sqrt(radius ** 2 - (delta_r * (i + 1)) ** 2) / (2 * levels)

		# поверхность
		for j in range(levels):
			# правый нижний треугольник
			vertex_1 = Vertex(0., delta_r * i, delta_y_low * j)
			vertex_2 = Vertex(0., delta_r * i, delta_y_low * (j + 1))
			vertex_3 = Vertex(0., delta_r * (i + 1), delta_y_high * (j + 1))
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			pill.cross_section.add_pointdata(triangle)

			# левый верхний треугольник
			vertex_2 = Vertex(0., delta_r * (i + 1), delta_y_high * j)
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			pill.cross_section.add_pointdata(triangle)

	pill.cross_section.add_half_y()
	pill.cross_section.add_half_z()

	# TODO: размножаем таблетки и поворачиваем как надо

def create_shader(shader_type, source):
	shader = glCreateShader(shader_type) # Создаем пустой объект шейдера
	glShaderSource(shader, source) # Привязываем текст шейдера к пустому объекту шейдера
	glCompileShader(shader)  # Компилируем шейдер
	return shader  # Возвращаем созданный шейдер

# Процедура перерисовки
def draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	glLineWidth(5)

	# glBegin(GL_TRIANGLES)
	# glColor4f(0., 0., 1., 1.)
	# for triangle in blue_pill_box.pointdata:
	# 	glVertex3f(triangle.vertex_1.x/k, triangle.vertex_1.y/k, triangle.vertex_1.z/k)
	# 	glVertex3f(triangle.vertex_2.x/k, triangle.vertex_2.y/k, triangle.vertex_2.z/k)
	# 	glVertex3f(triangle.vertex_3.x/k, triangle.vertex_3.y/k, triangle.vertex_3.z/k)
	# glEnd()

	glLineWidth(1)
	glBegin(GL_LINES)
	# x
	glColor4f(1., 0., 0., 1.)
	glVertex3f(0., 0., 0.)
	glVertex3f(1., 0., 0.)
	# y
	glColor4f(0., 1., 0., 1.)
	glVertex3f(0., 0., 0.)
	glVertex3f(0., 1., 0.)
	# z
	glColor4f(0., 0., 1., 1.)
	glVertex3f(0., 0., 0.)
	glVertex3f(0., 0., 1.)
	glEnd()

	glutSwapBuffers()  # Выводим все нарисованное в памяти на экран

# Здесь начинется выполнение программы
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(500, 200)
glutInit(sys.argv)
glutCreateWindow("KR")
glutDisplayFunc(draw)
glutIdleFunc(draw)
glClearColor(1., 1., 1., 1)
create__pill_box()
create__pill()
# Создаем вершинный шейдер:
vertex = create_shader(GL_VERTEX_SHADER, """
varying vec4 vertex_color;
            void main(){
                vec4 point = gl_Vertex;
				gl_Position = gl_ModelViewProjectionMatrix * point;
				vec4 color=gl_Color;
                vertex_color = color;
            }""")
# Создаем фрагментный шейдер:
fragment = create_shader(GL_FRAGMENT_SHADER, """
varying vec4 vertex_color;
            void main() {
                gl_FragColor = vertex_color;
}""")
program = glCreateProgram()
glAttachShader(program, vertex)
glAttachShader(program, fragment)
glLinkProgram(program)
glUseProgram(program)
glEnableClientState(GL_VERTEX_ARRAY)
glEnableClientState(GL_COLOR_ARRAY)
glutMainLoop()


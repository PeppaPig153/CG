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
a = mul
b = (mul + k_round)

r = lambda x, y:  m.sqrt(x ** 2 + y ** 2)



class Vertex:
	def __init__(self, x = 0., y = 0., z = 0.):
		self.x = x
		self.y = y
		self.z = z

	def update_vertex(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

class Triangle:
	def __init__(self, vertex_1, vertex_2, vertex_3):
		self.vertex_1 = vertex_1
		self.vertex_2 = vertex_2
		self.vertex_3 = vertex_3
		self.norm = [0., 0., 0.]

	def update_triangle(self, v1, v2, v3):
		self.vertex_1.update_vertex(v1[0], v1[1], v1[2])
		self.vertex_2.update_vertex(v2[0], v2[1], v2[2])
		self.vertex_3.update_vertex(v3[0], v3[1], v3[2])
		# update norm

class Figure:
	def __init__(self, color):
		self.pointdata = []
		self.color = color

	def add_pointdata(self, triangle):
		self.pointdata.append(triangle)


	def generate_figure(self, v1, v2_1, v3, v2_2):
		vertex_1 = Vertex(v1[0], v1[1], v1[2])
		vertex_2 = Vertex(v2_1[0], v2_1[1], v2_1[2])
		vertex_3 = Vertex(v3[0], v3[1], v3[2])
		triangle = Triangle(vertex_1, vertex_2, vertex_3)
		self.add_pointdata(triangle)

		# левый верхний треугольник
		vertex_2 = Vertex(v2_2[0], v2_2[1], v2_2[2])
		triangle = Triangle(vertex_1, vertex_2, vertex_3)
		self.add_pointdata(triangle)

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

	def copy(self, figure):
		for triangle in self.pointdata:
			vertex_1 = Vertex(triangle.vertex_1.x, triangle.vertex_1.y, triangle.vertex_1.z)
			vertex_2 = Vertex(triangle.vertex_2.x, triangle.vertex_2.y, triangle.vertex_2.z)
			vertex_3 = Vertex(triangle.vertex_3.x, triangle.vertex_3.y, triangle.vertex_3.z)
			triangle = Triangle(vertex_1, vertex_2, vertex_3)
			figure.add_pointdata(triangle)

	def rotate(self, angle, axis):
		M = np.zeros(3)
		if(axis == 0): # X
			M = np.array([[1., 0., 0.],
						  [0., m.cos(m.radians(angle)), -m.sin(m.radians(angle))],
						  [0., m.sin(m.radians(angle)), m.cos(m.radians(angle))]])
		if(axis == 1): # Y
			M = np.array([[m.cos(m.radians(angle)), 0., m.sin(m.radians(angle))],
						  [0., 1., 0.],
						  [-m.sin(m.radians(angle)), 0., m.cos(m.radians(angle))]])
		if(axis == 2): # Z
			M = np.array([[m.cos(m.radians(angle)), -m.sin(m.radians(angle)), 0.],
						  [m.sin(m.radians(angle)), m.cos(m.radians(angle)), 0.],
						  [0., 0., 1.]])

		for triangle in self.pointdata:
			triangle.update_triangle(np.dot(M, np.transpose(np.array([triangle.vertex_1.x, triangle.vertex_1.y, triangle.vertex_1.z]))),
									 np.dot(M, np.transpose(np.array([triangle.vertex_2.x, triangle.vertex_2.y, triangle.vertex_2.z]))),
									 np.dot(M, np.transpose(np.array([triangle.vertex_3.x, triangle.vertex_3.y, triangle.vertex_3.z]))))

	def shift(self, dx, dy, dz):
		for triangle in self.pointdata:
			triangle.update_triangle([triangle.vertex_1.x + dx, triangle.vertex_1.y + dy, triangle.vertex_1.z + dz],
									 [triangle.vertex_2.x + dx, triangle.vertex_2.y + dy, triangle.vertex_2.z + dz],
									 [triangle.vertex_3.x + dx, triangle.vertex_3.y + dy, triangle.vertex_3.z + dz])


class PillBox:
	def __init__(self, color):
		self.base = Figure(color)
		self.cap = Figure(color)
		self.lock = Figure(color)

	def rotate(self, angle, axis):
		self.base.rotate(angle, axis)
		self.cap.rotate(angle, axis)
		self.lock.rotate(angle, axis)

	def shift(self, dx, dy, dz):
		self.base.shift(dx, dy, dz)
		self.cap.shift(dx, dy, dz)
		self.lock.shift(dx, dy, dz)

class Pill:
	def __init__(self, color_cover, color_cross_section):
		self.cover = Figure(color_cover)
		self.cross_section = Figure(color_cross_section)

	def rotate(self, angle, axis):
		self.cover.rotate(angle, axis)
		self.cross_section.rotate(angle, axis)

	def shift(self, dx, dy, dz):
		self.cover.shift(dx, dy, dz)
		self.cross_section.shift(dx, dy, dz)



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
			blue_pill_box.base.generate_figure([x, y, 0.],
											   [x+1, y, 0.],
											   [x+1, y + 1, 0.],
											   [x, y + 1, 0.])

	# генерация скруглений по бокам
	delta = h // 2
	delta_y = k_round / levels
	for x in range(w):
		for y in range(levels):
			blue_pill_box.base.generate_figure([x, y * delta_y + delta, round(y * delta_y)],
											   [x + 1, y * delta_y + delta, round(y * delta_y)],
											   [x + 1,  (y + 1) * delta_y + delta, round((y + 1) * delta_y)],
											   [x, (y + 1) * delta_y + delta, round((y + 1) * delta_y)])

	# стенки
	highest_z = k_round
	highest_y = k_round + delta
	for x in range(w):
		for z in range(mul):
			blue_pill_box.base.generate_figure([x, highest_y, highest_z + z],
											   [x + 1, highest_y, highest_z + z],
											   [x + 1, highest_y, highest_z + (z + 1)],
											   [x, highest_y, highest_z + (z + 1)])

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
			blue_pill_box.base.generate_figure([border_x_left, j * delta_y_low, i * delta_z],
											   [border_x_left, (j + 1) * delta_y_low, i * delta_z],
											   [border_x_left, (j + 1) * delta_y_high, (i + 1) * delta_z],
											   [border_x_left, j * delta_y_high, (i + 1) * delta_z])

			# правая перегородка
			blue_pill_box.base.generate_figure([border_x_right, j * delta_y_low, i * delta_z],
											   [border_x_right, (j + 1) * delta_y_low, i * delta_z],
											   [border_x_right, (j + 1) * delta_y_high, (i + 1) * delta_z],
											   [border_x_right, j * delta_y_high, (i + 1) * delta_z])

	# полуокружность co скруглением
	radius = h // 2 + k_round
	delta_r = radius / (2 * levels)
	round_circle = lambda r: max(0., np.sign(r - delta) * round((r - delta)))

	for i in range(2 * levels):
		delta_y_low = 2 * m.sqrt(radius ** 2 - (delta_r * i) ** 2) / h
		delta_y_high = 2 * m.sqrt(radius ** 2 - (delta_r * (i + 1)) ** 2) / h

		for j in range(h // 2):
			blue_pill_box.base.generate_figure([-delta_r * i, delta_y_low * j, round_circle(r(delta_r * i, delta_y_low * j))],
											   [-delta_r * i, delta_y_low * (j + 1), round_circle(r(delta_r * i, delta_y_low * (j + 1)))],
											   [-delta_r * (i + 1), delta_y_high * (j + 1), round_circle(r(delta_r * (i + 1), delta_y_high * (j + 1)))],
											   [-delta_r * (i + 1), delta_y_high * j, round_circle(r(delta_r * (i + 1), delta_y_high * j))])

	# стенки полуокружности
	coord = lambda x: m.sqrt(radius ** 2 - x ** 2)
	for x in range(radius):
		for z in range(mul):
			blue_pill_box.base.generate_figure([-x, coord(x), highest_z + z],
											   [-(x + 1), coord(x + 1), highest_z + z],
											   [-(x + 1), coord(x + 1), highest_z + (z + 1)],
											   [-x, coord(x), highest_z + (z + 1)])

	blue_pill_box.base.add_half_y() # дорисовывает вторую половину
	blue_pill_box.base.copy(blue_pill_box.cap) # копируем в крышку

	# создание крепежа
	radius = mul
	length = h // 2 + k_round

	z = lambda x: m.sqrt(radius ** 2 - x ** 2)

	# цилиндр
	for x in range(radius):
		for y in range(length):
			blue_pill_box.lock.generate_figure([x, y, z(x)],
											   [x + 1, y, z(x + 1)],
											   [x + 1, y + 1, z(x + 1)],
											   [x, y + 1, z(x)])

	blue_pill_box.lock.add_half_y()
	blue_pill_box.lock.add_half_z()
	blue_pill_box.lock.add_half_x()

	ellipse = Figure([0., 0., 1., 1.])

	# овал
	delta_r = b / levels
	for i in range(levels):
		delta_y_low = a * m.sqrt(1. - (delta_r * i / b) ** 2) / levels
		delta_y_high = a * m.sqrt(1. - (delta_r * (i + 1) / b) ** 2) / levels
		# поверхность
		for j in range(levels):
			ellipse.generate_figure([j * delta_y_low, length, delta_r * i],
											   [(j + 1) * delta_y_low, length, delta_r * i],
											   [(j + 1) * delta_y_high, length, delta_r * (i + 1)],
											   [j * delta_y_high, length, delta_r * (i + 1)])
	ellipse.add_half_y()
	ellipse.add_half_z()
	ellipse.add_half_x()
	#ellipse.shift(0., 0., b - radius)


	for triangle in ellipse.pointdata:
		blue_pill_box.lock.add_pointdata(triangle)


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
			pill.cover.generate_figure([delta_r * i, delta_y_low * j, m.sqrt(radius ** 2 - r(delta_r * i, delta_y_low * j) ** 2) / 2],
									   [delta_r * i, delta_y_low * (j + 1), m.sqrt(radius ** 2 - r(delta_r * i, delta_y_low * (j + 1)) ** 2) / 2],
									   [delta_r * (i + 1), delta_y_high * (j + 1), m.sqrt(radius ** 2 - r(delta_r * (i + 1), delta_y_high * (j + 1)) ** 2) / 2],
									   [delta_r * (i + 1), delta_y_high * j, m.sqrt(radius ** 2 - r(delta_r * (i + 1), delta_y_high * j) ** 2) / 2])

	pill.cover.add_half_y()
	pill.cover.add_half_z()

	# разрез
	for i in range(levels):
		delta_y_low = m.sqrt(radius ** 2 - (delta_r * i) ** 2) / (2 * levels)
		delta_y_high = m.sqrt(radius ** 2 - (delta_r * (i + 1)) ** 2) / (2 * levels)

		# поверхность
		for j in range(levels):
			pill.cross_section.generate_figure([0., delta_r * i, delta_y_low * j],
									   [0., delta_r * i, delta_y_low * (j + 1)],
									   [0., delta_r * (i + 1), delta_y_high * (j + 1)],
									   [0., delta_r * (i + 1), delta_y_high * j])

	pill.cross_section.add_half_y()
	pill.cross_section.add_half_z()
	pills.append(pill)


def generate_scene():
	create__pill_box()

	# копируем в прозрачную
	blue_pill_box.base.copy(white_pill_box.base)
	blue_pill_box.cap.copy(white_pill_box.cap)
	blue_pill_box.lock.copy(white_pill_box.lock)

	# поворачиваем крышку
	blue_pill_box.cap.rotate(90, 1) # -90 ???
	blue_pill_box.cap.rotate(180, 2)
	# смещаем крышку
	blue_pill_box.cap.shift(2*b + w, 0., mul + k_round+w)
	# замок
	blue_pill_box.lock.rotate(90, 1) # -90 ???
	blue_pill_box.lock.shift(mul + w, 0., mul)

	# поворачиваем крышку
	white_pill_box.cap.rotate(180, 0)  # -90 ???
	# смещаем крышку
	white_pill_box.cap.shift(0., 0., mul + k_round)
	# замок
	# white_pill_box.lock.shift(w, 0., 0.)

	# поворачиваем и смещаем целиком
	white_pill_box.rotate(30, 2)
	white_pill_box.shift(0., 100., 0.)

	create__pill()

	for i in range(7):
		pill = Pill([0., 1., 0., 1.], [0., 0., 0., 1.])
		pills[0].cover.copy(pill.cover)
		pills[0].cross_section.copy(pill.cross_section)
		pills.append(pill)

	pills[0].rotate(30, 2)
	pills[0].shift(0., 0., mul / 2)

	pills[1].rotate(180, 2)
	pills[1].shift(10, 0., mul / 2)

	pills[2].rotate(90, 2)
	pills[2].shift(40, 30, mul / 2)

	pills[3].rotate(45, 2)
	pills[3].shift(40, 20, mul / 2)

	pills[4].rotate(180, 2)
	pills[4].shift(30, 70., mul / 2)

	#pills[5].rotate(30, 2)
	pills[5].shift(30, 70., mul / 2)

	pills[6].rotate(180, 2)
	pills[6].shift(40, 70., mul / 2)

	# pills[7].rotate(30, 2)
	pills[7].shift(40, 70., mul / 2)


def create_shader(shader_type, source):
	shader = glCreateShader(shader_type) # Создаем пустой объект шейдера
	glShaderSource(shader, source) # Привязываем текст шейдера к пустому объекту шейдера
	glCompileShader(shader)  # Компилируем шейдер
	return shader  # Возвращаем созданный шейдер

# Процедура перерисовки
def draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	# TODO: нарисовать бесконечную белую плоскость

	glLineWidth(5)

	glBegin(GL_TRIANGLES)
	#
	# glColor4f(blue_pill_box.base.color[0], blue_pill_box.base.color[1], blue_pill_box.base.color[2], blue_pill_box.base.color[3])
	# for triangle in blue_pill_box.base.pointdata:
	# 	glVertex3f(triangle.vertex_1.x/k, triangle.vertex_1.y/k, triangle.vertex_1.z/k)
	# 	glVertex3f(triangle.vertex_2.x/k, triangle.vertex_2.y/k, triangle.vertex_2.z/k)
	# 	glVertex3f(triangle.vertex_3.x/k, triangle.vertex_3.y/k, triangle.vertex_3.z/k)
	#
	# for triangle in blue_pill_box.cap.pointdata:
	# 	glVertex3f(triangle.vertex_1.x / k, triangle.vertex_1.y / k, triangle.vertex_1.z / k)
	# 	glVertex3f(triangle.vertex_2.x / k, triangle.vertex_2.y / k, triangle.vertex_2.z / k)
	# 	glVertex3f(triangle.vertex_3.x / k, triangle.vertex_3.y / k, triangle.vertex_3.z / k)
	#
	# for triangle in blue_pill_box.lock.pointdata:
	# 	glVertex3f(triangle.vertex_1.x / k, triangle.vertex_1.y / k, triangle.vertex_1.z / k)
	# 	glVertex3f(triangle.vertex_2.x / k, triangle.vertex_2.y / k, triangle.vertex_2.z / k)
	# 	glVertex3f(triangle.vertex_3.x / k, triangle.vertex_3.y / k, triangle.vertex_3.z / k)
	#
	# glColor4f(0., 0., 0., 1.)
	# # glColor4f(white_pill_box.base.color[0], white_pill_box.base.color[1], white_pill_box.base.color[2], white_pill_box.base.color[3])
	# for triangle in white_pill_box.base.pointdata:
	# 	glVertex3f(triangle.vertex_1.x / k, triangle.vertex_1.y / k, triangle.vertex_1.z / k)
	# 	glVertex3f(triangle.vertex_2.x / k, triangle.vertex_2.y / k, triangle.vertex_2.z / k)
	# 	glVertex3f(triangle.vertex_3.x / k, triangle.vertex_3.y / k, triangle.vertex_3.z / k)
	#
	# for triangle in white_pill_box.cap.pointdata:
	# 	glVertex3f(triangle.vertex_1.x / k, triangle.vertex_1.y / k, triangle.vertex_1.z / k)
	# 	glVertex3f(triangle.vertex_2.x / k, triangle.vertex_2.y / k, triangle.vertex_2.z / k)
	# 	glVertex3f(triangle.vertex_3.x / k, triangle.vertex_3.y / k, triangle.vertex_3.z / k)
	#
	# for triangle in white_pill_box.lock.pointdata:
	# 	glVertex3f(triangle.vertex_1.x / k, triangle.vertex_1.y / k, triangle.vertex_1.z / k)
	# 	glVertex3f(triangle.vertex_2.x / k, triangle.vertex_2.y / k, triangle.vertex_2.z / k)
	# 	glVertex3f(triangle.vertex_3.x / k, triangle.vertex_3.y / k, triangle.vertex_3.z / k)
	glColor4f(pills[0].cover.color[0], pills[0].cover.color[1], pills[0].cover.color[2], pills[0].cover.color[3])
	for pill in pills:
		for triangle in pill.cover.pointdata:
			glVertex3f(triangle.vertex_1.x / k, triangle.vertex_1.y / k, triangle.vertex_1.z / k)
			glVertex3f(triangle.vertex_2.x / k, triangle.vertex_2.y / k, triangle.vertex_2.z / k)
			glVertex3f(triangle.vertex_3.x / k, triangle.vertex_3.y / k, triangle.vertex_3.z / k)

	glColor4f(pills[0].cross_section.color[0], pills[0].cross_section.color[1], pills[0].cross_section.color[2],
			  pills[0].cross_section.color[3])
	for pill in pills:
		for triangle in pill.cross_section.pointdata:
			glVertex3f(triangle.vertex_1.x / k, triangle.vertex_1.y / k, triangle.vertex_1.z / k)
			glVertex3f(triangle.vertex_2.x / k, triangle.vertex_2.y / k, triangle.vertex_2.z / k)
			glVertex3f(triangle.vertex_3.x / k, triangle.vertex_3.y / k, triangle.vertex_3.z / k)

	glEnd()

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


def specialkeys(key, x, y):
	if key == GLUT_KEY_UP:		  # Клавиша вверх
		glRotatef(5, 1, 0, 0)	   # Вращаем на 5 градусов по оси X
	if key == GLUT_KEY_DOWN:		# Клавиша вниз
		glRotatef(-5, 1, 0, 0)	  # Вращаем на -5 градусов по оси X
	if key == GLUT_KEY_LEFT:		# Клавиша влево
		glRotatef(5, 0, 1, 0)	   # Вращаем на 5 градусов по оси Y
	if key == GLUT_KEY_RIGHT:	   # Клавиша вправо
		glRotatef(-5, 0, 1, 0)	  # Вращаем на -5 градусов по оси Y
	glutPostRedisplay()



# Здесь начинется выполнение программы
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(500, 200)
glutInit(sys.argv)
glutCreateWindow("KR")
glutDisplayFunc(draw)
glutIdleFunc(draw)
glutSpecialFunc(specialkeys)
glClearColor(1., 1., 1., 1)
generate_scene()
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


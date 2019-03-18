from OpenGL.GL import *
from OpenGL.GLUT import *
import time
from math import pi
w = 10
h = 20

color = [[244 / 255, 164 / 255, 96 / 255], [244 / 255, 164 / 255, 96 / 255], [244 / 255, 164 / 255, 96 / 255]]

triangles = [[[0.5, 0, 0.5], [0.5, 0, -0.5], [-0.5, 0, -0.5]],
			 [[0.5, 0, 0.5], [-0.5, 0, 0.5], [-0.5, 0, -0.5]]]

pointdata = []
pointcolor = []

# формирует массивы данных для отображения
def create_data():
	global pointdata
	global pointcolor
	import random

	random.seed(5)
	for i in range(h): # по высоте
		for j in range(w): # по ширине
			pointdata.append([i/h-0.5, 0, j/w-0.5])
			pointdata.append([(i+1)/h-0.5, 0, j/w-0.5])
			pointdata.append([(i+1)/h-0.5, 0, (j+1)/w-0.5])
			pointdata.append([i/h-0.5, 0, j/w-0.5])
			pointdata.append([i/h-0.5, 0, (j+1)/w-0.5])
			pointdata.append([(i+1)/h-0.5, 0, (j+1)/w-0.5])
			# color = [random.random(), random.random(), random.random()]
			for k in range(3):
				pointcolor.append(color)
			# color = [random.random(), random.random(), random.random()]
			for k in range(3):
				pointcolor.append(color)


# Процедура обработки специальных клавиш
def specialkeys(key, x, y):
	# Обработчики специальных клавиш
	if key == GLUT_KEY_UP:		  # Клавиша вверх
		glRotatef(5, 1, 0, 0)	   # Вращаем на 5 градусов по оси X
	if key == GLUT_KEY_DOWN:		# Клавиша вниз
		glRotatef(-5, 1, 0, 0)	  # Вращаем на -5 градусов по оси X
	if key == GLUT_KEY_LEFT:		# Клавиша влево
		glRotatef(5, 0, 1, 0)	   # Вращаем на 5 градусов по оси Y
	if key == GLUT_KEY_RIGHT:	   # Клавиша вправо
		glRotatef(-5, 0, 1, 0)	  # Вращаем на -5 градусов по оси Y
	glutPostRedisplay()


# Процедура подготовки шейдера (тип шейдера, текст шейдера)
def create_shader(shader_type, source):
	shader = glCreateShader(shader_type) # Создаем пустой объект шейдера
	glShaderSource(shader, source) # Привязываем текст шейдера к пустому объекту шейдера
	glCompileShader(shader)  # Компилируем шейдер
	return shader  # Возвращаем созданный шейдер


# Процедура перерисовки
def draw():
	global program
	var = glGetUniformLocation(program, 'time')
	glUniform1f(var, time.time() % (2 * pi))

	# print(time.time() % 10)
	glClear(GL_COLOR_BUFFER_BIT)  # Очищаем экран и заливаем серым цветом
	glEnableClientState(GL_VERTEX_ARRAY)  # Включаем использование массива вершин
	glEnableClientState(GL_COLOR_ARRAY)	# Включаем использование массива цветов

	glVertexPointer(3, GL_FLOAT, 0, pointdata)
	glColorPointer(3, GL_FLOAT, 0, pointcolor)
	glDrawArrays(GL_TRIANGLES, 0, 6*w*h)

	glDisableClientState(GL_VERTEX_ARRAY) # Отключаем использование массива вершин
	glDisableClientState(GL_COLOR_ARRAY)  # Отключаем использование массива цветов
	glutSwapBuffers()  # Выводим все нарисованное в памяти на экран


# Здесь начинется выполнение программы
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB) # Использовать двойную буферезацию и цвета в формате RGB (Красный Синий Зеленый)
glutInitWindowSize(500, 500) # Указываем начальный размер окна (ширина, высота)
glutInitWindowPosition(500, 200) # Указываем начальное положение окна относительно левого верхнего угла экрана
glutInit(sys.argv) # Инициализация OpenGl
glutCreateWindow("lab_5") # Создаем окно с заголовком
glutDisplayFunc(draw) # Определяем процедуру, отвечающую за перерисовку
glutIdleFunc(draw) # Определяем процедуру, выполняющуюся при "простое" программы
glutSpecialFunc(specialkeys) # Определяем процедуру, отвечающую за обработку клавиш
glClearColor(1., 1., 1., 1) # Задаем серый цвет для очистки экрана

create_data()
# Создаем вершинный шейдер:
# Положение вершин не меняется
# Цвет вершины - такой же как и в массиве цветов
vertex = create_shader(GL_VERTEX_SHADER, """
uniform float time;
varying vec4 vertex_color;
			void main(){
				vec4 point = gl_Vertex;
				point.y = sin(point.x * 20.0 + time) / 20.0;
				gl_Position = gl_ModelViewProjectionMatrix * point;
				vec4 color =  gl_Color;
				color = color + 1.0 * (point.y + 0.05);
				vertex_color = color;//(gl_Color * (point.y) * 20.0);
			}""")

# Создаем фрагментный шейдер:
# Определяет цвет каждого фрагмента как "смешанный" цвет его вершин
fragment = create_shader(GL_FRAGMENT_SHADER, """
varying vec4 vertex_color;
			void main() {

				gl_FragColor = vertex_color;
}""")

program = glCreateProgram() # Создаем пустой объект шейдерной программы
glAttachShader(program, vertex) # Приcоединяем вершинный шейдер к программе
glAttachShader(program, fragment) # Присоединяем фрагментный шейдер к программе
glLinkProgram(program) # "Собираем" шейдерную программу
glUseProgram(program) # Сообщаем OpenGL о необходимости использовать данную шейдерну программу при отрисовке объектов
import threading


glutMainLoop() # Запускаем основной цикл

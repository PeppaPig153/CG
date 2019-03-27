from OpenGL.GL import *
from OpenGL.GLUT import *
import math as m
import numpy as np

color = [135/255, 206/255, 235/255]

pointdata = []

# параметры
w = 50 # ширина
h = 50 # высота
draw_axis = True # прорисовка осей
draw_invisible_edge = True # прорисовка невидимых граней
transparent = True # прозрачная прорисовка
centre = [0., 0., 0.] # координаты центра

# формирует массивы данных для отображения
def create_data():
	global pointdata

	X=centre[0]
	Y=centre[1]
	Z=centre[2]

	for i in range(h): # по высоте
		for j in range(w): # по ширине
			pointdata.append([[i/h-0.5+X, j/w-0.5+Y, 0+Z],
							  [(i+1)/h-0.5+X, j/w-0.5+Y, 0+Z],
							  [(i+1)/h-0.5+X, (j+1)/w-0.5+Y, 0+Z]])
			pointdata.append([[i/h-0.5+X, j/w-0.5+Y, 0+Z],
							  [i/h-0.5+X, (j+1)/w-0.5+Y, 0+Z],
							  [(i+1)/h-0.5+X, (j+1)/w-0.5+Y, 0+Z]])


def specialkeys(key, x, y):
	# Обработчики специальных клавиш
	if key == GLUT_KEY_UP:		  # Клавиша вверх
		angle = m.radians(5)
		rotation_matrix = [[1, 0, 0],
						   [0, m.cos(angle), -m.sin(angle)],
						   [0, m.sin(angle), m.cos(angle)]]
	if key == GLUT_KEY_DOWN:		# Клавиша вниз
		angle = m.radians(-5)
		rotation_matrix = [[1, 0, 0],
						   [0, m.cos(angle), -m.sin(angle)],
						   [0, m.sin(angle), m.cos(angle)]]
	if key == GLUT_KEY_LEFT:		# Клавиша влево
		angle = m.radians(-5)
		rotation_matrix = [[m.cos(angle), -m.sin(angle), 0],
						   [m.sin(angle), m.cos(angle), 0],
						   [0, 0, 1]]
	if key == GLUT_KEY_RIGHT:	   # Клавиша вправо
		angle = m.radians(5)
		rotation_matrix = [[m.cos(angle), -m.sin(angle), 0],
						   [m.sin(angle), m.cos(angle), 0],
						   [0, 0, 1]]
	for triangle in pointdata:
		for point in triangle:
			new_coordinates = np.dot(rotation_matrix, point)
			for i in range(3):
				point[i]=new_coordinates[i]
	#glutPostRedisplay()


# Процедура подготовки шейдера (тип шейдера, текст шейдера)
def create_shader(shader_type, source):
	shader = glCreateShader(shader_type) # Создаем пустой объект шейдера
	glShaderSource(shader, source) # Привязываем текст шейдера к пустому объекту шейдера
	glCompileShader(shader)  # Компилируем шейдер
	return shader  # Возвращаем созданный шейдер


# Процедура перерисовки
def draw():
	global program
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Очищаем экран и заливаем серым цветом
	if(transparent):
		glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
	else:
		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
	if(not draw_invisible_edge):
		glEnable(GL_DEPTH_TEST)
		#glDepthFunc(GL_LESS)

	glBegin(GL_TRIANGLES) # прорисовка треугольников
	for triangle in pointdata:
		glColor3f(color[0], color[1], color[2])
		for point in triangle:
			glVertex3f(point[0], point[1], point[2])
	glEnd()
	glBegin(GL_LINES)
	if(draw_axis): # прорисовка осей
		#x
		glColor3f(1., 0., 0.)
		glVertex4f(0., 0., 0., 1.)
		glVertex4f(1., 0., 0., 1.)
		#y
		glColor3f(0., 1., 0.)
		glVertex4f(0., 0., 0., 1.)
		glVertex4f(0., 1., 0., 1.)
		#z
		glColor3f(0., 0., 1.)
		glVertex4f(0., 0., 0., 1.)
		glVertex4f(0., 0., 1., 1.)
	glEnd()
	if (draw_invisible_edge):
		glDisable(GL_DEPTH_TEST)
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
vertex = create_shader(GL_VERTEX_SHADER, """
varying vec4 vertex_color;
            void main(){
                vec4 point = gl_Vertex;
                if((point.x+point.y+point.z)==1.0 && (point.x==1.0 || point.y==1.0 || point.z==1.0)){
					point.z=point.z;
				}
				else {
					point.z = point.z+sin((point.x*point.x+point.y*point.y)*50.0)/30.0;
				}
				gl_Position = gl_ModelViewProjectionMatrix * point;
                vertex_color = gl_Color;
            }""")
# Создаем фрагментный шейдер:
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
glEnableClientState(GL_VERTEX_ARRAY)  # Включаем использование массива вершин
glEnableClientState(GL_COLOR_ARRAY)	# Включаем использование массива цветов
glutMainLoop() # Запускаем основной цикл

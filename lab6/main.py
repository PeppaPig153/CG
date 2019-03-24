from OpenGL.GL import *
from OpenGL.GLUT import *

w = 1
h = 2

color = [[244 / 255, 164 / 255, 96 / 255], [244 / 255, 164 / 255, 96 / 255], [244 / 255, 164 / 255, 96 / 255]]

triangles = [[[0.5, 0, 0.5], [0.5, 0, -0.5], [-0.5, 0, -0.5]],
			 [[0.5, 0, 0.5], [-0.5, 0, 0.5], [-0.5, 0, -0.5]]]

pointdata = []
pointcolor = []

#параметры
draw_axis = False

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
			for k in range(2):
				pointcolor.append(color)

	"""for k in range(3):
		tmp = [0., 0., 0.]
		tmp[k] = 1.0
		pointdata.append([0., 0., 0.])
		pointdata.append(tmp)
		pointdata.append([0., 0., 0.])
		pointcolor.append([tmp, tmp, tmp])"""


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
	glClear(GL_COLOR_BUFFER_BIT)  # Очищаем экран и заливаем серым цветом
	glDrawArrays(GL_LINE_STRIP, 0, 6 * w * h)
	glBegin(GL_LINES)
	if(draw_axis): # прорисовка осей
		#x
		glColor3f(1., 0., 0.)
		glVertex3f(0., 0., 0.)
		glVertex3f(1., 0., 0.)
		#y
		glColor3f(0., 1., 0.)
		glVertex3f(0., 0., 0.)
		glVertex3f(0., 1., 0.)
		#z
		glColor3f(0., 0., 1.)
		glVertex3f(0., 0., 0.)
		glVertex3f(0., 0., 1.)
	glEnd()
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
                gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
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
glVertexPointer(3, GL_FLOAT, 0, pointdata)
glColorPointer(3, GL_FLOAT, 0, pointcolor)
glutMainLoop() # Запускаем основной цикл

from OpenGL.GL import *
from OpenGL.GLUT import *
import math as m
import numpy as np


pointdata = []

# параметры
color = [135/255, 206/255, 235/255]
w = 50 # ширина
h = 50 # высота
draw_axis = True # прорисовка осей
draw_invisible_edge = True # прорисовка невидимых граней
transparent = False # прозрачная прорисовка
centre = [0., 0., 0.] # координаты центра
lightPos = [0., 0., 1.] # координаты источника света
lightColor = [1., 1., 1.] # цвет света
lightStrength = 0.1 # яркость света
isOrtho = True # оргтогональное проецирование


def define_normal(point_1, point_2, point_3):
	norm = [
		(point_2[1] - point_1[1]) * (point_3[2] - point_1[2]) - (point_2[2] - point_1[2]) * (point_3[1] - point_1[1]),
		(point_2[0] - point_1[0]) * (point_3[2] - point_1[2]) - (point_2[2] - point_1[2]) * (point_3[0] - point_1[0]),
		(point_2[0] - point_1[0]) * (point_3[1] - point_1[1]) - (point_2[1] - point_1[1]) * (point_3[0] - point_1[0]),
	]
	length=m.sqrt(norm[0]*norm[0]+norm[1]*norm[1]+norm[2]*norm[2])
	light = [point_1[0] - lightPos[0], point_1[1] - lightPos[1], point_1[2] - lightPos[2]]
	if (np.dot(light, norm) > 0):
		length=-length
	for i in range(3):
		norm[i]=norm[i]/length
	return norm

def define_coordinates(x, y, z):
	new_coordinates=[x, y, z]
	new_coordinates[2] += m.sin((x*x + y*y)*50.0)/30.0
	for i in range(3): # смещение в центр координат
		new_coordinates[i]+=centre[i]
	return new_coordinates

# формирует массивы данных для отображения
def create_data():
	global pointdata

	for i in range(h): # по высоте
		for j in range(w): # по ширине
			point_1 = define_coordinates(i/h-0.5, j/w-0.5, 0)
			point_2 = define_coordinates((i+1)/h-0.5, j/w-0.5, 0)
			point_3 = define_coordinates((i+1)/h-0.5, (j+1)/w-0.5, 0)
			norm = define_normal(point_1, point_2, point_3)
			pointdata.append([point_1+norm, point_2+norm, point_3+norm])

			point_1 = define_coordinates(i/h-0.5, j/w-0.5, 0)
			point_2 = define_coordinates((i + 1) / h - 0.5, (j + 1) / w - 0.5, 0)
			point_3 = define_coordinates(i/h-0.5, (j+1)/w-0.5, 0)
			norm = define_normal(point_1, point_2, point_3)
			pointdata.append([point_1+norm, point_2+norm, point_3+norm])


def specialkeys(key, x, y):
	rotation_matrix=[[1., 0., 0.],
					 [0., 1., 0.],
					 [0., 0., 1.]]
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
			new_coordinates = np.dot(rotation_matrix, [point[0], point[1], point[2]])
			for i in range(3):
				point[i]=new_coordinates[i]
		norm = define_normal(triangle[0], triangle[1], triangle[2])
		for point in triangle:
			for i in range(3):
				point[i+3]=norm[i]
	#glutPostRedisplay()


# Процедура подготовки шейдера (тип шейдера, текст шейдера)
def create_shader(shader_type, source):
	shader = glCreateShader(shader_type) # Создаем пустой объект шейдера
	glShaderSource(shader, source) # Привязываем текст шейдера к пустому объекту шейдера
	glCompileShader(shader)  # Компилируем шейдер
	return shader  # Возвращаем созданный шейдер

# Процедура перерисовки
def draw():
	# передача параметров в шейдер
	var = glGetUniformLocation(program, 'lightPos')
	glUniform3f(var, lightPos[0],lightPos[1], lightPos[2])
	var = glGetUniformLocation(program, 'lightColor')
	glUniform3f(var, lightColor[0], lightColor[1], lightColor[2])
	var = glGetUniformLocation(program, 'objectColor')
	glUniform3f(var, color[0], color[1], color[2])
	var = glGetUniformLocation(program, 'lightStrength')
	glUniform1f(var, lightStrength)

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Очищаем экран и заливаем серым цветом
	# прозрачность
	if(transparent):
		glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
	else:
		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
	# прорисовка невидимых граней
	if(not draw_invisible_edge):
		glEnable(GL_DEPTH_TEST)
		#glDepthFunc(GL_LESS)
	# ортогональное и перспективное проецирование
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glTranslatef(0.0, 0.0, -1.0)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	if (isOrtho):
		glOrtho(-1.0, 1.0, -1, 1, 0.1, 100.0)
	else:
		glFrustum(-.1, .1, -.1, .1, 0.1, 100.0)
	# glMatrixMode(GL_MODELVIEW);
	# прорисовка треугольников
	glBegin(GL_TRIANGLES)
	for triangle in pointdata:
		glColor3f(color[0], color[1], color[2])
		for point in triangle:
			glNormal3f(point[3], point[4], point[5])
			glVertex3f(point[0], point[1], point[2])
	glEnd()
	# прорисовка осей
	glBegin(GL_LINES)
	if(draw_axis):
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
	if (draw_invisible_edge):
		glDisable(GL_DEPTH_TEST)
	glutSwapBuffers()  # Выводим все нарисованное в памяти на экран

# Здесь начинется выполнение программы
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(500, 200)
glutInit(sys.argv)
glutCreateWindow("lab_6")
glutDisplayFunc(draw)
glutIdleFunc(draw)
glutSpecialFunc(specialkeys)
glClearColor(1., 1., 1., 1)
# генерация массива точек
create_data()
# Создаем вершинный шейдер:
vertex = create_shader(GL_VERTEX_SHADER, """
uniform vec3 lightPos; 
uniform vec3 lightColor;
uniform vec3 objectColor;
uniform float lightStrength;
varying vec4 vertex_color;
            void main(){
                vec4 point = gl_Vertex;
				gl_Position = gl_ModelViewProjectionMatrix * point;
				vec4 color=gl_Color;
				if(!((point.x+point.y+point.z)==1.0 && (point.x==1.0 || point.y==1.0 || point.z==1.0))){
    				vec3 ambient = lightStrength * lightColor;
    				vec3 Normal = gl_Normal;
    				vec3 norm = normalize(Normal);
    				vec3 FragPos = vec3(point.x, point.y, point.z);
    				vec3 lightDir = normalize(lightPos - FragPos);
    				float diff = max(dot(norm, lightDir), 0.0);
    				vec3 diffuse = diff * lightColor;
    				vec3 result = (ambient + diffuse) * objectColor;
    				color = vec4(result, 1.0f);
				}
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
glVertexPointer(3, GL_FLOAT, 0, pointdata)
glutMainLoop() # Запускаем основной цикл

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

width, height = 500, 500

colors = (
	(0, 255, 255),
	(255, 0, 255),
)

scale = 0.2 # длина стороны треугольника

def Get_verticies(step, layer, row, tr):
	return (
		# верхняя вершина
		(-(scale/2)*row+scale*tr, -(scale) * math.cos(math.radians(30)) * row - (scale / 2) * (step - 1 - layer)), #тут скорее всего координата X поменяется для вращения
		# левая вершина
		(-(scale/2)*(row+1)+scale*tr, -(scale) * math.cos(math.radians(30)) * (row+1) - (scale / 2) * (step - 1 - layer)),
		# правая вершина
		(-(scale/2)*(row+1)+scale*(tr+1), -(scale) * math.cos(math.radians(30)) * (row+1) - (scale / 2) * (step - 1 - layer)),
	)

step = 3 # шаг, на 0 шаге на экране ничего нет

def draw():
	glClear(GL_COLOR_BUFFER_BIT)
	glLineWidth(2)  # ширина линии
	sector = 0
	for layer in range(step): # проход по слоям
		for row in range(layer+1): # проход по каждому ряду текущего слоя
			for tr in range(row+1): # проход по каждому треугольнику в ряду
				glBegin(GL_LINE_LOOP)
				verticies = Get_verticies(step, layer, row, tr)
				for vertex in verticies:
					glColor4f(colors[sector%2][0], colors[sector%2][1], colors[sector%2][2], 1)
					glVertex2f(vertex[0], vertex[1])
				glEnd()
	glFlush()

glutInit()
glutInitDisplayMode(GLUT_RGB)
glutInitWindowSize(width, height)
glutInitWindowPosition(200, 200)
window = glutCreateWindow("Lab_3")
glutDisplayFunc(draw)
glutMainLoop()
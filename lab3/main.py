import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QSlider
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
from OpenGL.GL import *
import math

colors = (
	(0, 255, 255),
	(255, 0, 255),
)

scale = 0.1 # длина стороны треугольника
eps = 0.01

canvas_width = 600
canvas_height =600
window_width = canvas_width
window_height = canvas_height + 30

def rotate(x, y, angle):
	new_x = x * math.cos(angle) - y * math.sin(angle)
	new_y = x * math.sin(angle) + y * math.cos(angle)
	return new_x, new_y

def shift(x, y, angle, eps):
	new_x = x + eps * math.sin(angle)
	new_y = y - eps * math.cos(angle)
	return new_x, new_y

def Get_verticies(step, layer, row, tr, angle):
	top_x = -(scale/2)*row+scale*tr
	top_y = -(scale) * math.cos(math.radians(30)) * row - (scale / 2) * (step - 1 - layer)
	left_x = -(scale/2)*(row+1)+scale*tr
	left_y = -(scale) * math.cos(math.radians(30)) * (row+1) - (scale / 2) * (step - 1 - layer)
	right_x = -(scale/2)*(row+1)+scale*(tr+1)
	right_y = -(scale) * math.cos(math.radians(30)) * (row+1) - (scale / 2) * (step - 1 - layer)
	top_x, top_y = rotate(top_x, top_y, angle)
	left_x, left_y = rotate(left_x, left_y, angle)
	right_x, right_y = rotate(right_x, right_y, angle)
	top_x, top_y = shift(top_x, top_y, angle, eps)
	left_x, left_y = shift(left_x, left_y, angle, eps)
	right_x, right_y = shift(right_x, right_y, angle, eps)

	return ((top_x, top_y), (left_x, left_y), (right_x, right_y))

class GLWidget(QGLWidget):
	def __init__(self, parent):
		super(GLWidget, self).__init__(QGLFormat(QGL.SampleBuffers), parent)
		self.step_num = 1
		self.move(0, 0)
		self.resize(canvas_width, canvas_height)

	def update_step_num(self, opt):
		self.step_num = opt

	def draw(self, step):
		glClear(GL_COLOR_BUFFER_BIT)
		glLineWidth(2)  # ширина линии
		sector = 0
		for layer in range(step): # проход по слоям
			for row in range(layer+1): # проход по каждому ряду текущего слоя
				for tr in range(row+1): # проход по каждому треугольнику в ряду

					for angle_num in range(0, 6):
						angle = angle_num * math.pi / 3
						verticies = Get_verticies(step, layer, row, tr, angle)
						glBegin(GL_LINE_LOOP)
						for vertex in verticies:
							glColor4f(colors[angle_num%2][0], colors[angle_num%2][1], colors[angle_num%2][2], 1)
							glVertex2f(vertex[0], vertex[1])
						glEnd()
		glFlush()

	def paintGL(self):
		self.draw(self.step_num)

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		widget_width = window_width - canvas_width - 20
		centralWidget = QWidget()
		self.setCentralWidget(centralWidget)
		self.glWidget = GLWidget(self)

		self.slider = QSlider(Qt.Horizontal, parent=centralWidget)
		self.slider.setFocusPolicy(Qt.StrongFocus)
		self.slider.move(0, canvas_height)
		self.slider.resize(canvas_width, self.slider.height())
		self.slider.valueChanged.connect(self.change_step_num)

		self.setWindowTitle("lab_3")
		self.resize(window_width, window_height)

	def change_step_num(self, opt):
		self.glWidget.update_step_num(int(opt / 12) + 1)
		self.glWidget.update()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	sys.exit(app.exec_())

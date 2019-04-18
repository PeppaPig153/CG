from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QSlider, QVBoxLayout, QGroupBox, QColorDialog, QLabel, QPushButton, QCheckBox, QGridLayout
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
from PyQt5.QtGui import QColor
import math as m
import numpy as np
import os
from time import time
from math import pi


canvas_width = 600
canvas_height = 600
window_width = int(canvas_width * 1.61803398875)
window_height = canvas_height


class Figure:
	scale = [1 ,1 ,1 ]
	points = []
	colors = []
	normals = []
	color = [135/255, 206/255, 235/255]
	w = 21
	h = 21
	draw_axis = False # прорисовка осей
	draw_invisible_edge = False # прорисовка невидимых граней
	transparent = False # прозрачная прорисовка
	centre = [0., 0., 0.] # координаты центра
	lightPos = [0., 0., 1.] # координаты источника света
	lightColor = [1., 1., 1.] # цвет света
	lightStrength = 0.0 # яркость света
	isOrtho = False # оргтогональное проецирование
	grid = True
	angle_1 = 0
	angle_2 = 0
	xy_angle = 0
	xz_angle = 0
	yz_angle = 0
	freq = 20

	def __init__(self, parent):
		self.parent = parent
		self.create_data()

	def update_number_of_polygons(self, number):
		if self.w == number:
			return
		print('update', number)
		self.w = number
		self.h = number
		self.points = []
		self.colors = []
		self.create_data()


	def create_data(self):
		for i in range(self.h): # по высоте
			for j in range(self.w): # по ширине
				point_1 = [i/self.h-0.5, j/self.w-0.5, 0]
				point_2 = [(i+1)/self.h-0.5, j/self.w-0.5, 0]
				point_3 = [(i+1)/self.h-0.5, (j+1)/self.w-0.5, 0]
				self.points.append(point_1)
				self.points.append(point_2)
				self.points.append(point_3)
				self.colors.append(self.color)

				point_1 = [i/self.h-0.5, j/self.w-0.5, 0]
				point_2 = [(i + 1) / self.h - 0.5, (j + 1) / self.w - 0.5, 0]
				point_3 = [i/self.h-0.5, (j+1)/self.w-0.5, 0]
				self.points.append(point_1)
				self.points.append(point_2)
				self.points.append(point_3)
				self.colors.append(self.color)

	def rotate_figure(self, key):
		if key == 'up':
			self.angle_1 += 5
		elif key == 'down':
			self.angle_1 -= 5
		elif key == 'left':
			self.angle_2 += 5
		elif key == 'right':
			self.angle_2 -= 5
		else:
			 return

	def draw(self):
		var = glGetUniformLocation(self.parent.program, 'lightPos')
		glUniform3f(var, self.lightPos[0],self.lightPos[1], self.lightPos[2])
		var = glGetUniformLocation(self.parent.program, 'lightColor')
		glUniform3f(var, self.lightColor[0], self.lightColor[1], self.lightColor[2])
		var = glGetUniformLocation(self.parent.program, 'objectColor')
		glUniform3f(var, self.color[0], self.color[1], self.color[2])
		var = glGetUniformLocation(self.parent.program, 'scale')
		glUniform3f(var, self.scale[0], self.scale[1], self.scale[2])
		var = glGetUniformLocation(self.parent.program, 'centre')
		glUniform3f(var, self.centre[0], self.centre[1], self.centre[2])
		var = glGetUniformLocation(self.parent.program, 'lightStrength')
		glUniform1f(var, self.lightStrength)
		var = glGetUniformLocation(self.parent.program, 'freq')
		glUniform1f(var, self.freq)
		var = glGetUniformLocation(self.parent.program, 'angle_1s')
		glUniform1f(var, m.sin(m.radians(self.angle_1)))
		var = glGetUniformLocation(self.parent.program, 'angle_2s')
		glUniform1f(var, m.sin(m.radians(self.angle_2)))
		var = glGetUniformLocation(self.parent.program, 'angle_1c')
		glUniform1f(var, m.cos(m.radians(self.angle_1)))
		var = glGetUniformLocation(self.parent.program, 'angle_2c')
		glUniform1f(var, m.cos(m.radians(self.angle_2)))

		# var = glGetUniformLocation(self.parent.program, 'x_angle_c')
		# glUniform1f(var, m.cos(m.radians(self.x_angle)))

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Очищаем экран и заливаем серым цветом
		# прозрачность
		if(self.transparent):
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
		else:
			glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
		# # прорисовка невидимых граней
		if(not self.draw_invisible_edge):
			glEnable(GL_DEPTH_TEST)
			glDepthFunc(GL_LESS)
		# # ортогональное и перспективное проецирование
		# glMatrixMode(GL_MODELVIEW)
		# glLoadIdentity()
		# glTranslatef(0.0, 0.0, -1.0)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		if (self.isOrtho):
			glOrtho(-1.0, 1.0, -1, 1, 0.1, 100.0)
		else:
			glFrustum(-.1, .1, -.1, .1, 0.1, 100.0)
		glMatrixMode(GL_MODELVIEW);


		glVertexPointer(3, GL_FLOAT, 0, self.points)
		glDrawArrays(GL_TRIANGLES, 0, 6*self.w*self.h)


		if(self.draw_axis):
			glBegin(GL_LINES)
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

		if (self.draw_invisible_edge):
			glDisable(GL_DEPTH_TEST)
		glutSwapBuffers()  # Выводим все нарисованное в памяти на экран


class GLWidget(QGLWidget):
	alpha = 0
	beta = 0
	radius = 1
	camera_pos = [1,1,0]
	camera_up = [0,0,1]

	def __init__(self, parent):
		super(GLWidget, self).__init__(QGLFormat(QGL.SampleBuffers), parent)
		self.move(0, 0)
		self.resize(int(parent.width() / 1.61803398875), parent.height())
		self.fig = Figure(self)

	def create_shader(self, shader_type, source):
		shader = glCreateShader(shader_type)
		glShaderSource(shader, source)
		glCompileShader(shader)
		return shader

	def paintGL(self):
		glPushMatrix()
		self.camera_pos[0] = self.radius * m.cos(self.alpha) * m.cos(self.beta)
		self.camera_pos[1] = self.radius * m.sin(self.alpha) * m.cos(self.beta)

		self.camera_pos[2] = self.radius * m.sin(self.beta)
		gluLookAt(
			self.camera_pos[0], self.camera_pos[1], self.camera_pos[2],
			0, 0, 0,
			self.camera_up[0], self.camera_up[1], self.camera_up[2]
			)
		self.fig.draw()
		glPopMatrix()

	def initializeGL(self):
		glViewport(0, 0, canvas_width, canvas_height)
		glClearColor(1., 1., 1., 1)
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		vertex = self.create_shader(GL_VERTEX_SHADER, open(os.path.join(BASE_DIR, 'v_shader.glsl'), 'r').read())
		fragment = self.create_shader(GL_FRAGMENT_SHADER, open(os.path.join(BASE_DIR, 'f_shader.glsl'), 'r').read())
		self.program = glCreateProgram()
		glAttachShader(self.program, vertex)
		glAttachShader(self.program, fragment)
		glLinkProgram(self.program)
		glUseProgram(self.program)
		glEnableClientState(GL_VERTEX_ARRAY)
		glEnableClientState(GL_COLOR_ARRAY)
		glEnableClientState(GL_NORMAL_ARRAY)
		glVertexPointer(3, GL_FLOAT, 0, self.fig.points)
		glColorPointer(3, GL_FLOAT, 0, self.fig.colors)
		glNormalPointer(GL_FLOAT, 0, self.fig.normals)


	def mouseMoveEvent(self, event):

		if event.button() == 1:
			dx = event.x() - self.last_pos.x()
			dy = event.y() - self.last_pos.y()
			self.alpha += dx * 2 * m.pi / canvas_width
			self.beta += dy * 2 * m.pi / canvas_height
			self.last_pos = event.pos()
			self.update()

	def wheelEvent(self, event):
		self.radius += event.angleDelta().y() / 10000
		if self.radius < 0.0001:
			self.radius = 0.0001
		elif self.radius > 1:
			self.radius = 1
		self.update()

	def mousePressEvent(self, event):
		self.last_pos = event.pos()


class MainWindow(QMainWindow):
	def __init__(self):
		widgets_width = window_width - canvas_width
		super(MainWindow, self).__init__()
		self.resize(window_width, window_height)
		centralWidget = QWidget()
		self.setCentralWidget(centralWidget)
		self.glWidget = GLWidget(self)
		self.widgets = QGroupBox(parent = self)

		vbox = QVBoxLayout()
		vbox.setAlignment(Qt.AlignTop)

		vbox.addWidget(QLabel('light'))

		slider = QSlider(Qt.Horizontal)
		slider.setFocusPolicy(Qt.NoFocus)
		slider.valueChanged.connect(self.change_light_strength)
		vbox.addWidget(slider)


		button = QPushButton('Choose color')
		button.clicked.connect(self.change_light_color)
		button.setFocusPolicy(Qt.NoFocus)
		vbox.addWidget(button)

		check = QCheckBox('show axes')
		check.stateChanged.connect(self.change_axis_option)
		check.setFocusPolicy(Qt.NoFocus)
		vbox.addWidget(check)

		check = QCheckBox('draw invisible edges')
		check.stateChanged.connect(self.change_invisible_edges_option)
		check.setFocusPolicy(Qt.NoFocus)
		vbox.addWidget(check)

		check = QCheckBox('transparent')
		check.stateChanged.connect(self.change_transparent_option)
		check.setFocusPolicy(Qt.NoFocus)
		vbox.addWidget(check)

		check = QCheckBox('orthogonal projection')
		check.stateChanged.connect(self.change_projection_option)
		check.setFocusPolicy(Qt.NoFocus)
		vbox.addWidget(check)

		def add_scale_widgets():

			grid = QGridLayout()
			grid.setSpacing(1)
			grid.addWidget(QLabel('X'), 1, 0)
			grid.addWidget(QLabel('Y'), 2, 0)
			grid.addWidget(QLabel('Z'), 3, 0)

			slider = QSlider(Qt.Horizontal)
			slider.setValue(99)
			slider.setFocusPolicy(Qt.NoFocus)
			slider.valueChanged.connect(self.change_x_scale)
			grid.addWidget(slider, 1, 1)

			slider = QSlider(Qt.Horizontal)
			slider.setValue(99)
			slider.setFocusPolicy(Qt.NoFocus)
			slider.valueChanged.connect(self.change_y_scale)
			grid.addWidget(slider, 2, 1)

			slider = QSlider(Qt.Horizontal)
			slider.setValue(99)
			slider.setFocusPolicy(Qt.NoFocus)
			slider.valueChanged.connect(self.change_z_scale)
			grid.addWidget(slider, 3, 1)
			gb = QGroupBox('scale' ,parent=self.widgets)
			gb.setLayout(grid)
			vbox.addWidget(gb)
		add_scale_widgets()
		def add_move_widgets():
			grid = QGridLayout()
			grid.setSpacing(1)
			grid.addWidget(QLabel('X'), 1, 0)
			grid.addWidget(QLabel('Y'), 2, 0)
			grid.addWidget(QLabel('Z'), 3, 0)

			slider = QSlider(Qt.Horizontal)
			slider.setValue(50)
			slider.setFocusPolicy(Qt.NoFocus)
			slider.valueChanged.connect(self.change_x_pos)
			grid.addWidget(slider, 1, 1)

			slider = QSlider(Qt.Horizontal)
			slider.setValue(50)
			slider.setFocusPolicy(Qt.NoFocus)
			slider.valueChanged.connect(self.change_y_pos)
			grid.addWidget(slider, 2, 1)

			slider = QSlider(Qt.Horizontal)
			slider.setValue(50)
			slider.setFocusPolicy(Qt.NoFocus)
			slider.valueChanged.connect(self.change_z_pos)
			grid.addWidget(slider, 3, 1)
			gb = QGroupBox('move' ,parent=self.widgets)
			gb.setLayout(grid)
			vbox.addWidget(gb)
		add_move_widgets()
		vbox.addWidget(QLabel('figure parrameter'))

		slider = QSlider(Qt.Horizontal)
		slider.setValue(20)
		slider.setFocusPolicy(Qt.NoFocus)
		slider.valueChanged.connect(self.change_freq)
		vbox.addWidget(slider)

		vbox.addWidget(QLabel('number of polygons'))

		slider = QSlider(Qt.Horizontal)
		slider.setValue(20)
		slider.setFocusPolicy(Qt.NoFocus)
		slider.valueChanged.connect(self.change_num_of_polygons)
		vbox.addWidget(slider)

		self.widgets.resize(widgets_width, window_height)
		self.widgets.move(canvas_width, 0)
		self.widgets.setLayout(vbox)

		self.setWindowTitle("lab_6")

	def change_num_of_polygons(self, option):
		self.glWidget.fig.update_number_of_polygons(option + (option % 2) + 1)
		self.glWidget.update()

	def change_freq(self, option):
		self.glWidget.fig.freq = ((option + 1) / 4) + 10
		self.glWidget.update()


	def change_x_pos(self, option):
		self.glWidget.fig.centre[0] = option / 100 - 0.5
		self.glWidget.update()

	def change_y_pos(self, option):
		self.glWidget.fig.centre[1] = option / 100 - 0.5
		self.glWidget.update()

	def change_z_pos(self, option):
		self.glWidget.fig.centre[2] = option / 100 - 0.5
		self.glWidget.update()

	def change_x_scale(self, option):
		self.glWidget.fig.scale[0] = option / 100
		self.glWidget.update()

	def change_y_scale(self, option):
		self.glWidget.fig.scale[1] = option / 100
		self.glWidget.update()

	def change_z_scale(self, option):
		self.glWidget.fig.scale[2] = option / 100
		self.glWidget.update()

	def change_axis_option(self, value):
		self.glWidget.fig.draw_axis = value
		self.glWidget.update()

	def change_invisible_edges_option(self, value):
		self.glWidget.fig.draw_invisible_edge = value
		self.glWidget.update()

	def change_transparent_option(self, value):
		self.glWidget.fig.transparent = value
		self.glWidget.update()

	def change_projection_option(self, value):
		self.glWidget.fig.isOrtho = value
		self.glWidget.update()

	def change_light_color(self):
		def color_changed(color):
			color = color.getRgb()
			color = list(color[:-1])
			if color[0]==0 and color[1]==0 and color[2]==0: return
			color[0] /= 255
			color[1] /= 255
			color[2] /= 255
			self.glWidget.fig.lightColor = color
			self.glWidget.update()
		prev_color = self.glWidget.fig.lightColor
		color_dialog = QColorDialog()
		color_dialog.changeEvent = color_changed
		color_dialog.currentColorChanged = color_changed
		color_changed(color_dialog.getColor(QColor(int(prev_color[0] * 255), int(prev_color[1] * 255), int(prev_color[2] * 255), 255)))

	def change_light_strength(self, value):
		self.glWidget.fig.lightStrength = value / 99.0
		self.glWidget.update()

	def keyPressEvent(self, event):
		if event.key() == 16777234:
			self.glWidget.fig.rotate_figure('left')
		elif event.key() == 16777235:
			self.glWidget.fig.rotate_figure('up')
		elif event.key() == 16777236:
			self.glWidget.fig.rotate_figure('right')
		elif event.key() == 16777237:
			self.glWidget.fig.rotate_figure('down')
		self.glWidget.update()



if __name__ == '__main__':
	app = QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	sys.exit(app.exec_())

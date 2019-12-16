import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QComboBox
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
import OpenGL.GL as gl

canvas_width = 400
canvas_height = 400
window_width = int(canvas_width * 1.61803398875)
window_height = canvas_height

options = {
	'GL_POINTS': gl.GL_POINTS,
	'GL_LINES': gl.GL_LINES,
	'GL_LINE_STRIP': gl.GL_LINE_STRIP,
	'GL_LINE_LOOP': gl.GL_LINE_LOOP,
	'GL_TRIANGLES': gl.GL_TRIANGLES,
	'GL_TRIANGLE_STRIP': gl.GL_TRIANGLE_STRIP,
	'GL_TRIANGLE_FAN': gl.GL_TRIANGLE_FAN,
	'GL_QUADS': gl.GL_QUADS,
	'GL_QUAD_STRIP': gl.GL_QUAD_STRIP,
	'GL_POLYGON': gl.GL_POLYGON,
}

verticies = (
	(0.0, 0.9, 255, 0, 255),
	(0.6, 0.6, 0, 0, 128),
	(0.9, 0.0, 255, 255, 0),
	(0.6, -0.6, 255, 20, 147),
	(0.0, -0.9, 139, 0, 0),
	(-0.6, -0.6, 0, 255, 255),
	(-0.9, 0.0, 255, 69, 0),
	(-0.6, 0.6, 0, 100, 0)
)

def draw(option):
	print(option)
	gl.glClear(gl.GL_COLOR_BUFFER_BIT)
	if (option==gl.GL_POINTS):
		gl.glPointSize(5)  # размер точки
	if (option == gl.GL_LINES or option == gl.GL_LINE_STRIP or option == gl.GL_LINE_LOOP):
		gl.glLineWidth(3)  # ширина линии
	gl.glBegin(option)
	for vertex in verticies:
		gl.glColor3f(vertex[2], vertex[3], vertex[4])
		gl.glVertex2f(vertex[0], vertex[1])
	gl.glEnd()
	gl.glFlush()

class GLWidget(QGLWidget):
	def __init__(self, parent):
		super(GLWidget, self).__init__(QGLFormat(QGL.SampleBuffers), parent)
		self.option = gl.GL_POINTS
		self.move(0, 0)
		self.resize(canvas_width, canvas_height)

	def updateOptin(self, opt):
		self.option = opt

	def paintGL(self):
		draw(self.option)

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		centralWidget = QWidget()
		self.setCentralWidget(centralWidget)
		self.comboBox = QComboBox(centralWidget)
		self.comboBox.move(canvas_width + 50, 10)
		for item in options:
			self.comboBox.addItem(item)
		self.comboBox.currentTextChanged.connect(self.change_opt)
		self.glWidget = GLWidget(self)
		self.setWindowTitle("lab_1")
		self.resize(window_width, window_height)

	def change_opt(self, opt):
		self.glWidget.updateOptin(options[opt])
		self.glWidget.update()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	sys.exit(app.exec_())

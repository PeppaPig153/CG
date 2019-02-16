import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QComboBox, QSlider
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
import OpenGL.GL as gl

canvas_width = 400
canvas_height = 400
window_width = int(canvas_width * 1.61803398875)
window_height = canvas_height
alpha_1 = 0.9
alpha_2 = 0.3
alpha_3 = 0.6

test_options = {
	'GL_SCISSOR_TEST': gl.GL_SCISSOR_TEST,
	'GL_ALPHA_TEST': gl.GL_ALPHA_TEST,
	'GL_BLEND': gl.GL_BLEND,
}

func_options = {
	'GL_NEVER': gl.GL_NEVER, # – никогда не пропускает
	'GL_LESS': gl.GL_LESS, # – пропускает, если входное значение альфа меньше, чем значение ref
	'GL_EQUAL': gl.GL_EQUAL, # – пропускает, если входное значение альфа равно значению ref
	'GL_LEQUAL': gl.GL_EQUAL, # – пропускает, если входное значение альфа меньше или равно значения ref
	'GL_GREATER': gl.GL_GREATER, # – пропускает, если входное значение альфа больше, чем значение ref
	'GL_NOTEQUAL': gl.GL_NOTEQUAL, # – пропускает, если входное значение альфа не равно значению ref
	'GL_GEQUAL': gl.GL_GEQUAL, # – пропускает, если входное значение альфа больше или равно значения ref
	'GL_ALWAYS': gl.GL_ALWAYS, # – всегда пропускается, по умолчанию
}

sfactor_options = {
	'GL_ZERO': gl.GL_ZERO,
	'GL_ONE': gl.GL_ONE,
	'GL_DST_COLOR': gl.GL_DST_COLOR,
	'GL_ONE_MINUS_DST_COLOR': gl.GL_ONE_MINUS_DST_COLOR,
	'GL_SRC_ALPHA': gl.GL_SRC_ALPHA,
	'GL_ONE_MINUS_SRC_ALPHA': gl.GL_ONE_MINUS_SRC_ALPHA,
	'GL_DST_ALPHA': gl.GL_DST_ALPHA,
	'GL_ONE_MINUS_DST_ALPHA': gl.GL_ONE_MINUS_DST_ALPHA,
	'GL_SRC_ALPHA_SATURATE': gl.GL_SRC_ALPHA_SATURATE,
}

dfactor_options = {
	'GL_ZERO': gl.GL_ZERO,
	'GL_ONE': gl.GL_ZERO,
	'GL_SRC_COLOR': gl.GL_SRC_COLOR,
	'GL_ONE_MINUS_SRC_COLOR': gl.GL_ONE_MINUS_SRC_COLOR,
	'GL_SRC_ALPHA': gl.GL_SRC_ALPHA,
	'GL_ONE_MINUS_SRC_ALPHA': gl.GL_ONE_MINUS_SRC_ALPHA,
	'GL_DST_ALPHA': gl.GL_ONE_MINUS_SRC_ALPHA,
	'GL_ONE_MINUS_DST_ALPHA': gl.GL_ONE_MINUS_DST_ALPHA,
}

verticies = (
    (-0.4, 0.9, 255, 0, 0, alpha_1),
    (0.4, 0.9, 255, 0, 0, alpha_1),
    (0.0, -0.9, 255, 0, 0, alpha_1),
    (0.9, 0.4, 0, 255, 0, alpha_2),
    (0.9, -0.4, 0, 255, 0, alpha_2),
    (-0.9, 0.0, 0, 255, 0, alpha_2),
    (-0.9, -0.4, 0, 0, 255, alpha_3),
    (-0.9, 0.4, 0, 0, 255, alpha_3),
    (0.9, 0.0, 0, 0, 255, alpha_3)
)

class GLWidget(QGLWidget):
	def __init__(self, parent):
		super(GLWidget, self).__init__(QGLFormat(QGL.SampleBuffers), parent)
		self.test_option = gl.GL_SCISSOR_TEST
		self.func_option = gl.GL_GREATER
		self.sfactor_option = gl.GL_SRC_ALPHA
		self.dfactor_option = gl.GL_ONE_MINUS_SRC_ALPHA
		self.ref = 0.2
		self.move(0, 0)
		self.resize(canvas_width, canvas_height)

	def update_test_optin(self, opt):
		self.test_option = opt

	def update_func_optin(self, opt):
		self.func_option = opt

	def update_sfactor_optin(self, opt):
		self.sfactor_option = opt

	def update_dfactor_optin(self, opt):
		self.dfactor_option = opt

	def update_ref_optin(self, opt):
		self.ref = opt

	def draw(self):
	    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
	    if (self.test_option == gl.GL_SCISSOR_TEST): # тест отсечения
	        gl.glScissor(0, 0, 300, 300)
	    if (self.test_option == gl.GL_ALPHA_TEST): # тест прозрачности
	        gl.glAlphaFunc(self.func_option, self.ref)
	    if (self.test_option == gl.GL_BLEND): # тест смешивания цветов
	        gl.glBlendFunc(self.sfactor_option, self.dfactor_option)

	    gl.glEnable(self.test_option)
	    gl.glBegin(gl.GL_TRIANGLES)
	    for vertex in verticies:
	        gl.glColor4f(vertex[2], vertex[3], vertex[4], vertex[5])
	        gl.glVertex2f(vertex[0], vertex[1])
	    gl.glEnd()
	    gl.glDisable(self.test_option)
	    gl.glFlush()

	def paintGL(self):
		self.draw()

class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		widget_width = window_width - canvas_width - 20
		centralWidget = QWidget()
		self.setCentralWidget(centralWidget)
		self.glWidget = GLWidget(self)

		self.comboBoxTest = QComboBox(centralWidget)
		self.comboBoxTest.move(canvas_width + 10, 10)
		self.comboBoxTest.resize(widget_width, self.comboBoxTest.height())
		for item in test_options:
			self.comboBoxTest.addItem(item)
		self.comboBoxTest.currentTextChanged.connect(self.change_test_opt)

		self.comboBoxFunc = QComboBox(centralWidget)
		self.comboBoxFunc.move(canvas_width + 10, 40)
		self.comboBoxFunc.resize(widget_width, self.comboBoxFunc.height())
		for item in func_options:
			self.comboBoxFunc.addItem(item)
		self.comboBoxFunc.currentTextChanged.connect(self.change_func_opt)

		self.comboBoxSFactor = QComboBox(centralWidget)
		self.comboBoxSFactor.move(canvas_width + 10, 70)
		self.comboBoxSFactor.resize(widget_width, self.comboBoxSFactor.height())
		for item in sfactor_options:
			self.comboBoxSFactor.addItem(item)
		self.comboBoxSFactor.currentTextChanged.connect(self.change_sfactor_opt)

		self.comboBoxDFactor = QComboBox(centralWidget)
		self.comboBoxDFactor.move(canvas_width + 10, 100)
		self.comboBoxDFactor.resize(widget_width, self.comboBoxDFactor.height())
		for item in dfactor_options:
			self.comboBoxDFactor.addItem(item)
		self.comboBoxDFactor.currentTextChanged.connect(self.change_dfactor_opt)

		self.sliderRef = QSlider(Qt.Horizontal, parent=centralWidget)
		self.sliderRef.setFocusPolicy(Qt.StrongFocus)
		self.sliderRef.move(canvas_width + 10, 130)
		self.sliderRef.resize(widget_width, self.sliderRef.height())
		self.sliderRef.valueChanged.connect(self.change_ref_opt)

		self.setWindowTitle("lab_1")
		self.resize(window_width, window_height)

	def change_test_opt(self, opt):
		self.glWidget.update_test_optin(test_options[opt])
		self.glWidget.update()

	def change_func_opt(self, opt):
		self.glWidget.update_func_optin(func_options[opt])
		self.glWidget.update()

	def change_sfactor_opt(self, opt):
		self.glWidget.update_sfactor_optin(sfactor_options[opt])
		self.glWidget.update()

	def change_dfactor_opt(self, opt):
		self.glWidget.update_dfactor_optin(dfactor_options[opt])
		self.glWidget.update()

	def change_ref_opt(self, opt):
		self.glWidget.update_ref_optin(opt / 100)
		self.glWidget.update()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	mainWin = MainWindow()
	mainWin.show()
	sys.exit(app.exec_())

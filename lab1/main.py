from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

width, height = 400, 400

# формат точки: (координата x, координата y, красный цвет, зеленый цвет, синий цвет)
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

option = GL_POINTS # параметр для рисования:
#GL_POINTS
#GL_LINES
#GL_LINE_STRIP
#GL_LINE_LOOP
#GL_TRIANGLES
#GL_TRIANGLE_STRIP
#GL_TRIANGLE_FAN
#GL_QUADS
#GL_QUAD_STRIP
#GL_POLYGON

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    if (option==GL_POINTS):
        glPointSize(5)  # размер точки
    if (option == GL_LINES or option == GL_LINE_STRIP or option == GL_LINE_LOOP):
        glLineWidth(3)  # ширина линии
    glBegin(option)
    for vertex in verticies:
        glColor3f(vertex[2], vertex[3], vertex[4])
        glVertex2f(vertex[0], vertex[1])
    glEnd()
    glFlush()


glutInit()
glutInitDisplayMode(GLUT_RGB)
glutInitWindowSize(width, height)
glutInitWindowPosition(200, 200)
window = glutCreateWindow("Lab_1")
option = GL_POINTS # задаётся параметр для рисования
glutDisplayFunc(draw)
glutMainLoop()

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


#GL_POINTS
def draw_points():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(5) # размер точки
    glBegin(GL_POINTS)
    for vertex in verticies:
        glColor3f(vertex[2], vertex[3], vertex[4])
        glVertex2f(vertex[0], vertex[1])
    glEnd()
    glFlush()

#GL_LINES
def draw_lines():
    glClear(GL_COLOR_BUFFER_BIT)
    glLineWidth(3) # ширина линии
    glBegin(GL_LINES)
    for vertex in verticies:
        glColor3f(vertex[2], vertex[3], vertex[4])
        glVertex2f(vertex[0], vertex[1])
    glEnd()
    glFlush()

#GL_LINE_STRIP
def draw_line_strip():
    glClear(GL_COLOR_BUFFER_BIT)
    glLineWidth(3) # ширина линии
    glBegin(GL_LINE_STRIP)
    for vertex in verticies:
        glColor3f(vertex[2], vertex[3], vertex[4])
        glVertex2f(vertex[0], vertex[1])
    glEnd()
    glFlush()

#GL_LINE_LOOP
def draw_line_loop():
    glClear(GL_COLOR_BUFFER_BIT)
    glLineWidth(3) # ширина линии
    glBegin(GL_LINE_LOOP)
    for vertex in verticies:
        glColor3f(vertex[2], vertex[3], vertex[4])
        glVertex2f(vertex[0], vertex[1])
    glEnd()
    glFlush()

#GL_TRIANGLES
def draw_triangles():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_TRIANGLES)
    for vertex in verticies:
        glColor3f(vertex[2], vertex[3], vertex[4])
        glVertex2f(vertex[0], vertex[1])
    glEnd()
    glFlush()

#GL_TRIANGLE_STRIP
def draw_triangle_strip():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_TRIANGLE_STRIP)
    for vertex in verticies:
        glColor3f(vertex[2], vertex[3], vertex[4])
        glVertex2f(vertex[0], vertex[1])
    glEnd()
    glFlush()

#GL_TRIANGLE_FAN
def draw_triangle_fan():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_TRIANGLE_FAN)
    for vertex in verticies:
        glColor3f(vertex[2], vertex[3], vertex[4])
        glVertex2f(vertex[0], vertex[1])
    glEnd()
    glFlush()

#GL_QUADS
def draw_quads():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_QUADS)
    for vertex in verticies:
        glColor3f(vertex[2], vertex[3], vertex[4])
        glVertex2f(vertex[0], vertex[1])
    glEnd()
    glFlush()


#GL_QUAD_STRIP
def draw_quad_strip():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_QUAD_STRIP)
    for vertex in verticies:
        glColor3f(vertex[2], vertex[3], vertex[4])
        glVertex2f(vertex[0], vertex[1])
    glEnd()
    glFlush()

#GL_POLYGON
def draw_polygon():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POLYGON)
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
glutDisplayFunc(draw_polygon)
glutMainLoop()

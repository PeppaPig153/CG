from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

width, height = 400, 400

Number_of_points = 500

# координаты начала и конца векторов на концах
#P0 = np.zeros((1, 3))
#P1 = np.zeros((1, 3))
#Q0 = np.zeros((1, 3))
#Q1 = np.zeros((1, 3))

is_clicked = False
current_point = []
eps = 0.1

P0 = [-0.5, 0.2, 1]
P1 = [-0.5, 0.6, 1]
Q0 = [0.2, 0.1, 1]
Q1 = [0.5, 0, 1]

points = [P0, P1, Q0, Q1]


M = (
    [1, 0, -3, 2],
    [0, 0, 3, -2],
    [0, 1, -2, 1],
    [0, 0, -1, 1]
)

T = np.zeros((4, 1))

def convert_coordinates(x, y):
    x = (x /width * 2) - 1
    y = - (y /height * 2) + 1
    return x, y

def mouse_click(button, state, x, y):
    global is_clicked
    global current_point
    x, y = convert_coordinates(x, y)
    if button != GLUT_LEFT_BUTTON: return
    if state == GLUT_UP:
        current_point = []
        is_clicked = False
    else:
        for i, point in enumerate(points):
            if ((abs(x - point[0]) < eps) and (abs(y - point[1]) < eps)):
                current_point = i
                is_clicked = True
                break

def mouse_move(x, y):
    x, y = convert_coordinates(x, y)
    if is_clicked == True:
        points[current_point][0] = x
        points[current_point][1] = y
        glutPostRedisplay()

# интерполяция формой Эрмита
def Hermite_interpolation(t):
    for i in range(4):
        T[i]=t**i
    G = np.vstack(points).transpose()
    return G.dot(M).dot(T) # R(t)=GMT

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLineWidth(1)
    pts = np.arange(0, 1, 1 / Number_of_points)
    glBegin(GL_LINE_STRIP)
    for t in pts:
        x, y, z = Hermite_interpolation(t)
        glColor3f(1., 0., 0.)
        glVertex2f(x[0], y[0])
    glEnd()
    glLineWidth(2)
    glBegin(GL_LINE_STRIP)
    glColor3f(0., 0., 0.)
    glVertex2f(points[0][0], points[0][1])
    glVertex2f(points[2][0], points[2][1])
    glEnd()
    glBegin(GL_LINE_STRIP)
    glColor3f(0., 0., 0.)
    glVertex2f(points[1][0], points[1][1])
    glVertex2f(points[3][0], points[3][1])
    glEnd()
    glFlush()


if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)
    window = glutCreateWindow("Lab_4")
    glutDisplayFunc(draw)
    glutMotionFunc(mouse_move)
    glutMouseFunc(mouse_click)
    glClearColor(1,1,1,1)
    glutMainLoop()

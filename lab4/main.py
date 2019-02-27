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

P0 = [-1, 0.2, 1]
P1 = [-0.5, 0.6, 1]
Q0 = [0.2, 0.1, 1]
Q1 = [2, 0, 1]


G = np.vstack((P0, P1, Q0, Q1)).transpose()

M = (
    [1, 0, -3, 2],
    [0, 0, 3, -2],
    [0, 1, -2, 1],
    [0, 0, -1, 1]
)

T = np.zeros((4, 1))



# интерполяция формой Эрмита
def Hermite_interpolation(t):
    for i in range(4):
        T[i]=t**i
    return G.dot(M).dot(T) # R(t)=GMT

def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glLineWidth(3)
    points = np.arange(0, 1, 1 / Number_of_points)
    glBegin(GL_LINE_STRIP)
    for t in points:
        x, y, z = Hermite_interpolation(t)
        glColor3f(1., 0., 0.)
        glVertex2f(x[0], y[0])
    glEnd()
    glFlush()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(width, height)
glutInitWindowPosition(200, 200)
window = glutCreateWindow("Lab_4")
glutDisplayFunc(draw)
glutMainLoop()
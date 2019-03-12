from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math

width, height = 600, 600

w=90
h=60

triangle=(
    (0.5, 1, 0.5),
    (0.5, 1, -0.5),
    (-0.5, 1, -0.5),
    (0.5, 1, 0.5),
    (-0.5, 1, 0.5),
    (-0.5, 1, -0.5),
    )


def camera(x, y, z):
    # поворот относительно оси z
    angle=math.radians(-10)
    rotation_matrix_z=[[math.cos(angle), -math.sin(angle), 0],
                     [math.sin(angle), math.cos(angle), 0],
                     [0, 0, 1]]
    new_coordinates = np.dot(rotation_matrix_z, [[x], [z], [y]]) # ось y поменяна с z

    return new_coordinates[0], new_coordinates[1], new_coordinates[2]



def draw():
    glClear(GL_COLOR_BUFFER_BIT)

    glBegin(GL_LINES)
    #ось x
    glColor3f(1., 0., 0.)
    x, y, z = camera(1, 0, 0)
    glVertex3f(x, y, z)
    x, y, z = camera(-1, 0, 0)
    glVertex3f(x, y, z)
    # ось y
    glColor3f(0., 1., 0.)
    x, y, z = camera(0, 1, 0)
    glVertex3f(x, y, z)
    x, y, z = camera(0, -1, 0)
    glVertex3f(x, y, z)
    # ось z
    glColor3f(0., 0., 1.)
    x, y, z = camera(0, 0, 1)
    glVertex3f(x, y, z)
    x, y, z = camera(0, 0, -1)
    glVertex3f(x, y, z)
    glEnd()

    glLineWidth(2)
    glColor3f(244 / 255, 164 / 255, 96 / 255)
    glBegin(GL_TRIANGLES)
    for i in range(h):
        for j in range(w):
            for point in triangle:
                x, y, z = camera((point[0]/w)*j, point[1], (point[2]/w)*i)
                glVertex3f(x, y, z)
    glEnd()
    glFlush()


if __name__ == '__main__':
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(200, 200)
    window = glutCreateWindow("Lab_5")
    glutDisplayFunc(draw)
    glClearColor(1,1,1,1)
    glutMainLoop()
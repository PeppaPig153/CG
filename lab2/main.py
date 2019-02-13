from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

width, height = 400, 400

# прозрачность для каждого треугольника
alpha_1 = 0.9
alpha_2 = 0.3
alpha_3 = 0.6

# формат точки: (координата x, координата y, красный цвет, зеленый цвет, синий цвет, прозрачность)
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

test = GL_SCISSOR_TEST
#GL_SCISSOR_TEST
#GL_ALPHA_TEST
#GL_BLEND

ref = 0.2 # определяет значение, с которым сравнивается входное значение альфа при тестировании прозрачности
func = GL_GREATER
#GL_NEVER – никогда не пропускает
#GL_LESS – пропускает, если входное значение альфа меньше, чем значение ref
#GL_EQUAL – пропускает, если входное значение альфа равно значению ref
#GL_LEQUAL – пропускает, если входное значение альфа меньше или равно значения ref
#GL_GREATER – пропускает, если входное значение альфа больше, чем значение ref
#GL_NOTEQUAL – пропускает, если входное значение альфа не равно значению ref
#GL_GEQUAL – пропускает, если входное значение альфа больше или равно значения ref
#GL_ALWAYS – всегда пропускается, по умолчанию

sfactor = GL_SRC_ALPHA # задает метод вычисления фактора наложения источника при тестировании смешания цветов
#GL_ZERO
#GL_ONE
#GL_DST_COLOR
#GL_ONE_MINUS_DST_COLOR
#GL_SRC_ALPHA
#GL_ONE_MINUS_SRC_ALPHA
#GL_DST_ALPHA
#GL_ONE_MINUS_DST_ALPHA
#GL_SRC_ALPHA_SATURATE
dfactor = GL_ONE_MINUS_SRC_ALPHA # задает метод вычисления фактора наложения приемника при тестировании смешания цветов
#GL_ZERO
#GL_ONE
#GL_SRC_COLOR
#GL_ONE_MINUS_SRC_COLOR
#GL_SRC_ALPHA
#GL_ONE_MINUS_SRC_ALPHA
#GL_DST_ALPHA
#GL_ONE_MINUS_DST_ALPHA

def draw_test():
    glClear(GL_COLOR_BUFFER_BIT)

    if (test == GL_SCISSOR_TEST): # тест отсечения
        glScissor(0, 0, 300, 300)
    if (test == GL_ALPHA_TEST): # тест прозрачности
        glAlphaFunc(func, ref)
    if (test == GL_BLEND): # тест смешивания цветов
        glBlendFunc(sfactor, dfactor)

    glEnable(test)
    glBegin(GL_TRIANGLES)
    for vertex in verticies:
        glColor4f(vertex[2], vertex[3], vertex[4], vertex[5])
        glVertex2f(vertex[0], vertex[1])
    glEnd()
    glDisable(test)
    glFlush()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(width, height)
glutInitWindowPosition(200, 200)
window = glutCreateWindow("Lab_2")
test = GL_BLEND # установка нужного теста
glutDisplayFunc(draw_test)
glutMainLoop()

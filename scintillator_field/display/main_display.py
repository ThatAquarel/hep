from OpenGL.GL import *
from OpenGL.GLU import *

#from scintillator_field.display.display_2.Visualizer.app import App
from scintillator_field.display.display_1.window import Window


def main_display():
    width, height = 1000, 750
    #app = App((width, height), "title")
    app = Window()
    app.main()



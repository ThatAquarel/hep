from OpenGL.GL import *
from OpenGL.GLU import *

from scintillator_field.display.display_2.Visualizer.app import App
#from scintillator_field.display.display_1.window import Window

from scintillator_field.display.display_1.drafts.refactor_display_1.display_main import Display_1


def main_display():

<<<<<<< HEAD
    width, height = 1000, 750
    app = App((width, height), "title")
    #app = Window()
    #app.main()
=======
    #width, height = 1000, 750
    #app = App((width, height), "title")

    #display = Display_1()
    #display.run_window()

    app = Window()
    app.main()
>>>>>>> be8cd71 (display_1 works for real data. data from 2025-04-09 run.)



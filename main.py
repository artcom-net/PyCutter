"""This module starts the application.

PyCutter is a graphical application that allows to cut page(s) from a PDF file.
Three cut-options are available:
    - range;
    - multiple;
    - all.

"""


from tkinter import Tk

from gui import GuiApp
from app import MainApp


__author__ = 'Artem Kustov'
__email__ = 'artem.kustov@artcom-net.ru'
__version__ = '1.0'


if __name__ == '__main__':
    root = Tk()
    gui = GuiApp(root)
    app = MainApp(gui)
    app.start_app()
    root.mainloop()

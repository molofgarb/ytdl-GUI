#!/usr/bin/env python3

import os, sys
from platform import system

from main_window import MainWindow

if __name__ == "__main__":
    debug = False #debug mode used for development, make false when build
    windows = False
    path = os.getcwd()

    #Get info about environment
    if (system() == "Windows"):
        windows = True
    elif (system() != "Darwin" and system() != "Linux"):
        sys.exit("Operating System not supported")

    #icon stuff
    iconPath = ""
    if getattr(sys, 'frozen', False):
        iconPath = os.path.join(sys._MEIPASS, "resources/logo.ico")
    else:
        iconPath = "./resources/logo.ico"

    data = { #info about environment
        'debug': debug,
        'windows': windows,
        'path': path,
        'iconPath': iconPath
    }

    #defines main window
    root = MainWindow(data)
    root.iconbitmap(iconPath)

    #loop!!
    root.mainloop()



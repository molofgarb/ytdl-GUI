#!/usr/bin/env python3

import os, sys
from platform import system

from main_window import MainWindow

if __name__ == "__main__":
    debug = False
    print(sys.argv)
    if (len(sys.argv) > 1): debug = (sys.argv[1] == 'debug') #debug mode used for development, true if debug argument passed
    windows = False
    path = os.getcwd()
    print(path)
    # path = os.path.realpath(
    #     os.path.join(os.getcwd(), os.path.dirname(__file__)))

    #Get info about environment
    if (system() == "Windows"):
        windows = True
    elif (system() != "Darwin" and system() != "Linux"):
        sys.exit("Operating system not supported")
    else:
        sys.exit("Unknown operating system")

    #icon stuff
    iconPath = ""
    # if getattr(sys, 'frozen', False):
    iconPath = os.path.join(path, ".\\resources\\logo.ico")
    # iconPath = os.path.join(sys._MEIPASS, "..\resources\logo.ico")

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



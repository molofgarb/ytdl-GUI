#!/usr/bin/env python3

import os, sys
from platform import system

from main_window import MainWindow

if __name__ == "__main__":
    windows = False
    debug = False

    if (len(sys.argv) > 1): 
        debug = (sys.argv[1] == '--debug') #debug mode used for development, true if debug argument passed

    #Get info about environment
    if (system() == "Windows"):
        windows = True
    elif (system() != "Darwin" and system() != "Linux"):
        sys.exit("Operating system not supported")
    else:
        sys.exit("Unknown operating system")

    #icon stuff
    path = os.getcwd()
    iconPath = ""
    if debug: iconPath = os.path.join(path, "resources/logo.ico") #for running as script
    else: iconPath = os.path.join(sys._MEIPASS, "resources/logo.ico") #for pyinstaller

    data = { #info about environment
        'debug': debug,
        'windows': windows,
        'path': path,
        'iconPath': iconPath
    }

    if data['debug']: print(path)

    #defines main window
    root = MainWindow(data)
    root.iconbitmap(iconPath)

    #loop!!
    root.mainloop()



#!/usr/bin/env python3

import os, sys
from platform import system

import tkinter as tk

from window_main import MainWindow

if __name__ == "__main__":
    windows = False
    debug = False

    if (len(sys.argv) > 1): 
        debug = (sys.argv[1] == '--debug') #debug mode used for development, true if debug argument passed

    #Get info about environment
    if (system() == "Windows"):
        windows = True
    elif (system() != "Darwin" and system() != "Linux"):
        sys.exit("Unknown operating system")
        

    #icon stuff
    path = os.getcwd()
    iconPath = ""
    if debug: iconPath = os.path.join(path, "resources_data/logo.gif") #for running as script
    else: iconPath = os.path.join(sys._MEIPASS, "resources_data/logo.gif") #for pyinstaller

    data = { #info about environment
        'debug': debug,
        'OS': system(),
        'windows': windows,
        'path': path,
        'iconPath': iconPath
    }

    if data['debug']: print(path)

    #defines main window
    root = MainWindow(data)
    # root.iconbitmap(iconPath)

    #applies icon
    img = tk.Image("photo", file=data['iconPath'])
    root.iconphoto(True, img)
    root.tk.call('wm','iconphoto', root._w, img)

    #loop!!
    root.mainloop()



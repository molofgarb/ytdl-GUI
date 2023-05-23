#!/usr/bin/env python3

import os, sys
from platform import system

import tkinter as tk

from window_main import MainWindow

if __name__ == "__main__":
    windows = False
    debug = False
    opsys = system()

    if (len(sys.argv) > 1): 
        debug = (sys.argv[1] == '--debug') #debug mode used for development, true if debug argument passed

    # get info about environment
    if (opsys == "Windows"):
        windows = True
    elif (opsys != "Darwin" and opsys != "Linux"):
        sys.exit("Unknown operating system")

    # set path
    path = os.path.dirname(sys.executable)
    if debug:
        path = os.getcwd()
    if (path[-28:] == "/ytdl-GUI.app/Contents/MacOS"): # if in .app package
        path = path[:-28] #move out of .app package

    # set iconPath
    iconPath = ""
    if debug:
        iconPath = os.path.join(path, "resources_data/logo.gif") #for running as script
    else: 
        iconPath = os.path.join(sys._MEIPASS, "resources_data/logo.gif") #for pyinstaller

    # info about environment
    data = { 
        'debug': debug,
        'OS': system(),
        'windows': windows,
        'path': path,
        'iconPath': iconPath
    }

    #defines main window
    root = MainWindow(data)
    # root.iconbitmap(iconPath)

    #applies icon
    img = tk.Image("photo", file=data['iconPath'])
    root.iconphoto(True, img)
    root.tk.call('wm','iconphoto', root._w, img)

    #loop!!
    root.mainloop()



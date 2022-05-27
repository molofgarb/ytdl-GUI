import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import filedialog

class DownloadLogger:
    def __init__(self, root, simulate):
        self.root = root
        self.isDebug = root.data['debug'] #debug on?
        self.simulate = simulate

    def debug(self, msg):
        if msg.startswith('[debug] '):
            print(msg)
        else:
            self.info(msg)

    def info(self, msg):
        if self.isDebug: print(msg)
        if msg.startswith('[info]'):
            if self.simulate: #take care of prog. bar in place of dl_hook
                print(self.root.currVideo)
                self.root.currVideo += 1
                self.root.updateProgressBar(self.simulate)
                
            
    def warning(self, msg):
        if self.isDebug: print(msg)

    def error(self, msg):
        if self.isDebug: print(msg)

    def setDownload(self):
        self.simulate = False
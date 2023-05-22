import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import filedialog

from threading import Thread

from yt_dlp.yt_dlp.YoutubeDL import YoutubeDL

from logging import Logger

class DownloadLogger(Logger):
    def __init__(self, root, updateQueue):
        super().__init__("DownloadLogger")

        self.root = root
        self.isDebug = root.data['debug'] #debug on?
        self.updateQueue = updateQueue

    def debug(self, msg):
        if msg.startswith('[debug] '):
            print(msg)
        else:
            self.info(msg)

    # runs for every message
    def info(self, msg: str): #for every download,
        if self.isDebug: 
            print(msg) #debug
        if msg.startswith("[info]"): # for every new video
            self.updateQueue.put(-1)
            print("INFO INCREMENT!!!")
        if msg.startswith("[download]"):
            print("here is the message with stripped spaces:", msg.split(" "))
                
    def warning(self, msg):
        if self.isDebug: print(msg)

    def error(self, msg):
        if self.isDebug: print(msg)
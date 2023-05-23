import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import filedialog

from threading import Thread
from queue import Queue

from yt_dlp.yt_dlp.YoutubeDL import YoutubeDL

from logging import Logger

class DownloadLogger(Logger):
    def __init__(self, root, updateQueue: Queue) -> None:
        super().__init__("DownloadLogger")

        self.root = root
        self.isDebug = root.data['debug'] #debug on?
        self.updateQueue = updateQueue

    def debug(self, msg: str) -> None:
        if msg.startswith('[debug] '):
            print(msg)
        else:
            self.info(msg)

    # runs for every message
    def info(self, msg: str) -> None: #for every download,
        
        arrMsg = msg.split(" ")
        # during a download, looks like: 
        # ['[download]', '', '', '0.1%', 'of', '', '', '', '1.73MiB', 
        # 'at', '', 'Unknown', 'B/s', 'ETA', 'Unknown']

        if self.isDebug: 
            print(msg)
        if arrMsg[0] == "[info]": # new video
            self.updateQueue.put(-1)
        if arrMsg[0] == "[download]": # download status
            for i in range(len(arrMsg)): 
                if arrMsg[i] == "Destination:":
                    self.updateQueue.put(-3)
                    self.updateQueue.put(msg[24:])
                # find the string with the download % if download status
                elif len(arrMsg[i]) != 0 and arrMsg[i][-1] == "%":
                    self.updateQueue.put(float(arrMsg[i][:-1]))

    def warning(self, msg: str) -> None:
        if self.isDebug: print(msg)

    def error(self, msg: str) -> None:
        if self.isDebug: print(msg)
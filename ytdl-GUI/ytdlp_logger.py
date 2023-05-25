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
            print(msg, "\n", arrMsg)
        # advance currvideo for check
        if arrMsg[0] == "[info]":
            self.updateQueue.put("__info") 
        if arrMsg[0] == "[download]": # download status
            for i in range(len(arrMsg)): 

                # add name of file to be downloaded
                if arrMsg[i] == "Destination:":
                    self.updateQueue.put("__filename")
                    self.updateQueue.put(msg[24:])

                # find the string with the download % if download status
                elif len(arrMsg[i]) != 0 and arrMsg[i][-1] == "%":
                    self.updateQueue.put(float(arrMsg[i][:-1]))
                    # done with a video download, advance self.currVideo for download
                    if (arrMsg[i][:-1] == "100"):
                        self.updateQueue.put("__done")

    def warning(self, msg: str) -> None:
        if self.isDebug: print(msg)

    def error(self, msg: str) -> None:
        if self.isDebug: print(msg)
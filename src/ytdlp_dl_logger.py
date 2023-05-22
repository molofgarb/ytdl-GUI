import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import filedialog

from logging import Logger

currProgressBarValue = 0

class DownloadLogger(Logger):
    def __init__(self, root, simulate):
        super().__init__()

        self.root = root
        self.isDebug = root.data['debug'] #debug on?
        self.simulate = simulate

    def debug(self, msg):
        if msg.startswith('[debug] '):
            print(msg)
        else:
            self.info(msg)

    # runs for every download
    def info(self, msg): #for every download,
        if self.isDebug: print(msg) #debug
        if msg.startswith('[info]'): #if new video
            if self.simulate: #take care of prog. bar in place of dl_hook
                if self.isDebug: print("from download_logger, the currvideo is", self.root.currVideo)
                self.root.currVideo += 1
                self.root.updateProgressBar(self.simulate)
                
            
    def warning(self, msg):
        if self.isDebug: print(msg)

    def error(self, msg):
        if self.isDebug: print(msg)

    # def download(self, msg):
    #     if self.isDebug: print('test')

    #     #if nothing pending, then animate ellipses
    #     if (len(self.pending) == 0): 
    #         self.updateProgressBar(False)

    # def setDownload(self):
    #     self.simulate = False
        
#runs during each download (NOT SIMULATE/CHECK), keeps track of status of that individual download
def dl_hook(self, d):
    global currProgressBarValue

    if d['status'] == 'downloading': #update currprogressbar if download to indicate dl prog
        try: #progress as bytes dl'ed
            currProgressBarValue = ( d['downloaded_bytes'] / d['total_bytes'] ) * 100
        except:
            try: #progress as time elapsed
                currProgressBarValue = ( d['elapsed'] / (d['elapsed'] + d['eta']) ) * 100
            except: #dont show anything
                currProgressBarValue = 0

        self.update()

        if self.data['debug']: 
            print('') #prints video download status to stdout

                            # if ((len(self.filenames) == 0) or
                            #         (self.filenames[len(self.filenames) - 1] != ('"' + str(d['filename']) + '.part' + '"'))): #add partfile to end
                            #     self.filenames.append(('"' + str(d['filename']) + '.part' + '"'))

    elif d['status'] == 'finished': #when a download/check has finished 
                # if 'elapsed' in d: #if a download occurred
                    # partfile = self.filenames.pop()
                    # if (partfile == ('"' + str(d['filename']) + '.part' + '"')): #if confirmed to be part file
                    #     self.filenames.append('"' + str(d['filename']) + '"') #add to completed dl list in final directory format
                    # else:
                    #     self.filenames.append(partfile) #if it was something else
        # self.currVideo += 1
        # self.updateProgressBar(False, True)
        currProgressBarValue = 0 #reset curr progress bar
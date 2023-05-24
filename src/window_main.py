import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import filedialog
    
import os, sys
import ctypes
import time

from threading import Thread, enumerate
import queue

from yt_dlp.yt_dlp.YoutubeDL import YoutubeDL

from ytdlp_logger import DownloadLogger
from window_info import InfoWindow
from window_confirm import ConfirmPrompt
from common_tk import updateText


class MainWindow(tk.Tk):
    def __init__(self, data: dict) -> None:
        super().__init__()  #inherit all the stuff from tk.Tk -- base window
        self.data = data #dict from ytdlGUI.py {debug, windows, path, iconPath}

        # =========== STYLE ===========

        #window style
        self.style = { 
            "bgcolor": "#525252",
            "textcolor": "white",
            "buttoncolor": "#656565",
            "checkbuttoncheckcolor": "black",
            "mainfont": ("Verdana", "11")
        }

        # style options
        self.style['styleOptions'] = [
            ("*font", self.style['mainfont'][0] + " " + self.style['mainfont'][1]),
            ("*background", self.style['bgcolor']),
            ("*foreground", self.style['textcolor']),
            ("*Checkbutton*selectcolor", self.style["checkbuttoncheckcolor"]),
            ("*insertBackground", "black")
        ]
        self.style['styleOptionsMac'] = [
            ("*highlightBackground", self.style['bgcolor']), # make background consistent color
            ("*highlightColor", self.style['bgcolor']), # make background consistent color
            ("*Button*foreground", "black") # since bg is locked white, make text black
        ]

        # apply options
        for option in self.style['styleOptions']: super().option_add(option[0], option[1])
        if data['OS'] == "Darwin":
            for option in self.style['styleOptionsMac']: super().option_add(option[0], option[1])

        super().configure( #style for entire window background
            background=self.style["bgcolor"]
        )

        # styled separately because ttk used instead of tk
        self.ttkStyle = ttk.Style(self)
        self.ttkStyle.theme_use("clam")
        self.ttkStyle.configure(
            "format.TRadiobutton",
            background=self.style["bgcolor"], foreground=self.style['textcolor'], 
            font=self.style['mainfont'],
        )
        self.ttkStyle.map("format.TRadiobutton", # make color of radio label dependent on state
                          foreground=[
                              ('hover', self.style['bgcolor']), 
                              ('background', self.style['textcolor'])
                          ]
        )
        self.ttkStyle.configure(
            "format.Horizontal.TProgressbar",
            background=self.style["bgcolor"], foreground="green"
        )

        

        # =========== VARS ===========

        #window data
        self.pending = [] #holds events that will happen

        self.URLs = [] #URLs of files to be downloaded
        self.filenames = [] #names of files as they are downloaded
        self.formats = [] #TODO
        self.currVideo = 0 #index of video in URLs that is being checked/downloaded

        self.updateQueue = queue.Queue()

        #download format 
        self.format = tk.StringVar(self, "b") #default format is best of both (video, audio)

        #options
        self.isExpandOptions = tk.BooleanVar(self, False) #if the options menu should be expanded
        self.ischeckURLs = tk.BooleanVar(self, True) #if URLs should be checked before download
        self.isDeleteOnFinish = tk.BooleanVar(self, True) #if user should be prompted to delete cancelled downloads
        self.isPlaySound = tk.BooleanVar(self, True) #if a sound should be played
        
        #initialize main window
        self.title("ytdl-GUI")

        img = tk.Image("photo", file=data['iconPath'])
        self.iconphoto(True, img) # you may also want to try this.
        self.tk.call('wm','iconphoto', self._w, img)
        self.iconbitmap(data['iconPath'])

        self.eval('tk::PlaceWindow . center') #puts window in center(ish)

        # =========== WIDGETS ===========

        #initialize main frame (located within main window)
        self.frame = tk.Frame(
            self, background=self.style["bgcolor"]
        )
        self.frame.grid(padx=20, pady=(8, 18))

        # =========== DIRECTORY ===========

        #label for directory
        self.directoryLabel = tk.Label(
            self.frame, text="Output Path:"
        )
        self.directoryLabel.grid(sticky="W")

        #directory to download to
        self.directoryText = tk.Text(
            self.frame, height=1, width=62,
            background="white", foreground="black"
        )
        self.directoryText.insert(tk.END, data['path'])
        self.directoryText.grid(row=10, column=0,padx=5, pady=5)

        #button to open directory-choosing prompt
        self.directoryButton = tk.Button(
            self.frame, height=0, width=0,
            text = "...", command=self.setDirectory
        )
        self.directoryButton.grid(row=10, column=1,padx=1, pady=1)

        # =========== INPUT ===========
        #input label
        self.inputLabel = tk.Label(
            self.frame, text = "Videos to Download:"
        )
        self.inputLabel.grid(row=20, sticky="W")
        
        #input text box scroll bar 
        self.inputScroll = tk.Scrollbar(
            self.frame, width=16, 
        )
        self.inputScroll.grid(row=30, column=1, sticky="NS")

        #input text box
        self.inputText = tk.Text(
            self.frame, height=7, width=62,
            yscrollcommand=self.inputScroll.set, 
            background="white", foreground="black"
        )
        self.inputText.grid(row=30, padx=5, pady=5)
        self.inputScroll.configure(command=self.inputText.yview)

        # !!! For Testing !!! should not be exist in production
        if self.data['debug']:
            self.testButton = tk.Button(
                self.frame, height=1, width=6,
                text = "test", command=lambda: ConfirmPrompt(self, "test!"), 
            )
            self.testButton.grid(row=31, sticky="N")

        # =========== FORMAT SELECTION ===========
        self.formatGrid = tk.Frame(
            self.frame
        )
        self.formatGrid.grid(row=40, sticky="ew")

        #label for formats
        self.formatLabel = tk.Label(
            self.formatGrid, text="Format: ", 
        )
        self.formatLabel.grid(column=0, sticky="W")

        #format radio button selection
        self.vidAndAud = ttk.Radiobutton(
            self.formatGrid, text="Video and Audio", style="format.TRadiobutton", variable=self.format, value="best"
        )
        self.vidAndAud.grid(column=1, row=0, sticky="e", padx=18)
        self.vidOnly = ttk.Radiobutton(
            self.formatGrid, text="Video Only", style="format.TRadiobutton", variable=self.format, value="bestvideo"
        )
        self.vidOnly.grid(column=2, row=0, sticky="e", padx=18)
        self.audOnly = ttk.Radiobutton(
            self.formatGrid, text="Audio Only", style="format.TRadiobutton", variable=self.format, value="bestaudio"
        )
        self.audOnly.grid(column=3, row=0, sticky="e", padx=18)
        self.audOnlyCons = ttk.Radiobutton(
            self.formatGrid, text="m4a (audio)", style="format.TRadiobutton", variable=self.format, value="m4a"
        )
        self.audOnlyCons.grid(column=4, row=0, sticky="e", padx=18)

        self.format.set("best") #set default radio value (first button)

        # =========== INPUT BUTTONS ===========
        #button to send text box input
        self.inputButton = tk.Button(
            self.frame, text="Download", 
            command=self.inputURLs, 
        )
        self.inputButton.grid(row=70, padx=5, pady=5)

        #button to clear
        self.clearButton = tk.Button(
            self.frame, text="Clear", 
            command=lambda:self.inputText.delete("1.0", tk.END), 
        )
        self.clearButton.grid(row=70, sticky="E", padx=5, pady=5)

        # =========== STATUS/PROGRESS ===========
        self.progressFrame = tk.Frame(self.frame)
        
        #progress bar for overall downloads
        self.progressBarLabel = tk.Label(self.progressFrame, text = "All Videos:")
        self.progressBarLabel.grid(row=0, column=0, pady=4) 

        self.progressBar = ttk.Progressbar(
            self.progressFrame, orient=HORIZONTAL, length=500, mode='determinate',
            style="format.Horizontal.TProgressbar"
        )
        self.progressBar.grid(row=0, column=1, pady=4) 

        #progress bar for current video download
        self.currProgressBarLabel = tk.Label(self.progressFrame, text = "This Video:")
        self.currProgressBarLabel.grid(row=1, column=0, pady=4) 

        self.currProgressBar = ttk.Progressbar(
            self.progressFrame, orient=HORIZONTAL, length=500, mode='determinate',
            style="format.Horizontal.TProgressbar"
        )
        self.currProgressBar.grid(row=1, column=1, pady=4) 

        self.statusFrame = tk.Frame(self.frame) #will be gridded later when download begins
        self.statusFrame.grid(row=80, padx=2, pady=2)

        # status Label!!
        self.statusLabel = tk.Label(self.statusFrame, text = "Awaiting URL input...\n")
        self.statusLabel.grid(row=0, padx=2, pady=2)

        self.urlLabel = tk.Label(self.statusFrame, text = "<url here>")
        #self.urlLabel.grid(row=1, padx=2, pady=2) #urlLabel default ungrid

        

        # =========== OPTIONS/INFO ===========
        self.expandOptionsButton = tk.Button(self.frame, text = "Expand Options", command=lambda: self.expandOptions())
        self.expandOptionsButton.grid(row=90, padx=2, pady=2, sticky="W")

        self.optionsFrame = tk.Frame(self.frame) #holds options buttons

        #options label
        self.optionsLabel = tk.Label(self.optionsFrame, text = "Options:")
        self.optionsLabel.grid(row=0, sticky='w')

        #play sound when download finished toggle
        self.playSoundCheck = tk.Checkbutton(
            self.optionsFrame, text = "Play sound after download/error",
            variable=self.isPlaySound, onvalue=True, offvalue=False, 
        )
        self.playSoundCheck.grid(row=10, sticky='w')

        #check if URLs are valid before downloading
        self.checkURLsCheck = tk.Checkbutton(
            self.optionsFrame, text = "Check URLs before download",
            variable=self.ischeckURLs, onvalue=True, offvalue=False, 
        )
        self.checkURLsCheck.grid(row=20, sticky='w')

        #delete input on finish toggle
        self.deleteOnFinishCheck = tk.Checkbutton(
            self.optionsFrame, text = "Delete input after download",
            variable=self.isDeleteOnFinish, onvalue=True, offvalue=False, 
        )
        self.deleteOnFinishCheck.grid(row=30, sticky='w')

        #info label
        self.infoButton = tk.Button(
            self.frame, text = "Info",
            command = lambda:InfoWindow(self, self.style), 
        )
        self.infoButton.grid(row=90, column=1, sticky="E")

    # =========== DIRECTORY ===========
    
    #uses tkinter's askdirectory dialog to set directory in text box
    def setDirectory(self) -> None:
        dir = filedialog.askdirectory() #will very likely be valid
        if self.data['debug']: print(self.pending)
        if (dir != ""):
            self.directoryText.delete(1.0, tk.END)
            self.directoryText.insert(tk.END, dir)

    # =========== EXPAND OPTIONS ===========

    #toggles the expansion/minimization of the options frame
    def expandOptions(self) -> None:
        if self.isExpandOptions.get(): #was expanded
            self.expandOptionsButton.configure(text="Expand Options")
            self.optionsFrame.grid_remove()
            self.isExpandOptions.set(False)
        else: #was minimized
            self.expandOptionsButton.configure(text="Minimize Options")
            self.optionsFrame.grid(row=100, padx=2, pady=2, sticky="W")
            self.isExpandOptions.set(True)

    # =========== INPUT/CHECK DOWNLOADS ===========

    #takes inputs, stores them in URLs, and then calls download function
    def inputURLs(self) -> bool:
        self.URLs = self.inputText.get(1.0, tk.END).split()
        path = self.directoryText.get(1.0, tk.END).replace("\n", "")
        try:
            os.chdir(path)
            if len(self.URLs) > 0: #valid URLs
                updateText(self, self.statusLabel, "URLs Received!\n")
                self.downloadURLs()
                return True
            else:
                ConfirmPrompt(self, 
                '''Error: No URLs provided\n\nPlease provide at least one URL''')
                return False
        except Exception as ex:
            ConfirmPrompt(self,
            '''Error: Invalid Download Path\n\nPlease change download path to valid directory''')
            return False

    #make sure all URLs are valid before all downloads begin
    def checkURLs(self, dl_options: dict) -> bool:
        if self.ischeckURLs.get():
            self.currVideo = 0

            try:            
                self.updateProgressBar(True)
                self.ytdlpThread(dl_options, True)
                return True
            
            except Exception as ex:
                ConfirmPrompt(self,
                      f'''Error: Invalid URL\n\n'''
                    + f'''1) Please check your URL #{self.currVideo + 1} '''
                    + f'''again to make sure it is valid and compatible\n''' 
                    + f'''2) Please try using a different format to download these videos''')
                if (self.data['debug']):
                    print(self.URLs, "are the bad URLs")
                return False
            
        return True # True if no check

    # =========== DOWNLOAD URLS ===========

    #downloads URLs in list -- main function
    def downloadURLs(self) -> int:
        self.cancelPending() #clean up any pending after() calls
        self.filenames.clear()

        # set up GUI for downloading
        self.urlLabel.grid(row=1, padx=2, pady=2)
        self.progressBar['value'] = 0
        self.currProgressBar['value'] = 0
        self.progressFrame.grid(row=50)
        self.inputButton.configure(text="Cancel", 
            command=self.cancelDownload) #to cancel download

        dl_options = {
            "paths": {'home': self.directoryText.get(1.0, tk.END)}, 
            "nocheckcertificate": True, 
            "format": self.format.get(),
            'simulate': True,
            'logger': DownloadLogger(self, self.updateQueue)
        }

        if not self.checkURLs(dl_options): #check URLs (if specified)
            self.finishDownload("unsuccessful") #wrap up stuff + reset if bad check
            return 1

        # reinitialize after possible simulation
        dl_options['simulate'] = False
        self.currVideo = 0

        try: #begin downloads
            self.updateProgressBar(False)

            self.ytdlpThread(dl_options, False)
            # self.finishDownload("successful")

            # for thread in enumerate():
            #     print(thread)
            # print("\n\n\n")

        except Exception as ex:
            if len(self.URLs) != 0: #if not caused by cancel
                ConfirmPrompt(self,
                    '''Error: Download issue\n\nThere was an issue with the download. Please try again.''')
                if (self.data['debug']):
                    print(self.URLs, ex)
                self.finishDownload("unsuccessful") #wrap up stuff + reset
            return 2
        
        return 0
    
    def ytdlpThread(self, dl_options: dict, check: bool) -> None:
        # empty updateQueue
        while not self.updateQueue.empty():
            self.updateQueue.get()

        # begin wrapper thread
        downloader = Thread(target=ytdlpWrapper, args=[self, dl_options], daemon=True)
        downloader.start()

        # begin listener thread -- listen for GUI updates
        listener = Thread(target=ytdlpListener, args=[self, downloader, dl_options, check], daemon=True)
        listener.start()
            
    #updates progress bar to indicate progress
    def updateProgressBar(self, is_check: bool) -> bool:
        # get status text depending on YoutubeDL call
        statusText = ""
        dotcount = self.statusLabel.cget("text")[-3:].count('.')
        splittime = int(time.time()) % 3

        self.update()
        # if it was something else
        if dotcount == 0:
            if is_check: # update status for check
                statusText = f"Checking if URL #{self.currVideo + 1} is valid."
            else:
                statusText = f"Video #{self.currVideo + 1} is being downloaded."
        # update dots
        else:
            if is_check: # update status for check
                statusText = f"Checking if URL #{self.currVideo + 1} is valid"
            else:
                statusText = f"Video #{self.currVideo + 1} is being downloaded"
            for i in range(((dotcount % 3) + 1) if (dotcount - 1 == splittime) else dotcount):
                statusText += '.'

        if self.currVideo < len(self.URLs):
            updateText(self, self.statusLabel, statusText)
            updateText(self, self.urlLabel, f"({self.URLs[self.currVideo]})") #display url of video being dl'ed

        # update progress bar
        self.progressBar['value'] = ((self.currVideo)/len(self.URLs)) * 100
        self.update()
        return True

    # =========== FINISH DOWNLOADING ===========

    #cancels download by clearing URLs, deletes downloaded files
    def cancelDownload(self) -> None:
        updateText(self, self.statusLabel, f"Download cancelled")
        self.updateQueue.put("__cancel")
        
        ConfirmPrompt(self,
            "Do you want to delete the already downloaded files?",
            self.filenames)
        
        # self.finishDownload("cancelled") # finishDownload will take care of the rest

    #summary after downloading videos
    def finishDownload(self, endText) -> None:
        updateText(self, self.statusLabel, f'Download {endText}') 
        self.inputButton.configure(text="Download", command=self.inputURLs)
        if self.isPlaySound.get(): self.bell() #makes sound upon completion

        if (endText == "successful" and self.isDeleteOnFinish.get() == True):
            self.inputText.delete("1.0", tk.END) #delete input

        self.URLs.clear() #clears URLs to make YoutubeDL() stop if running

        #reset delay (for visual appeal)
        self.cancelPending() #in case there are already cancels inside 
        self.pending.append(
            self.after(5000, lambda: updateText(self, self.statusLabel,
            "Awaiting URL input...\n")))
        self.pending.append( # remove urlLabel after 5 sec
            self.after(5000, lambda: self.urlLabel.grid_remove()))
        self.pending.append( # remove progresbar after 5 sec
            self.after(5000, lambda: self.progressFrame.grid_remove()))
        self.pending.append( #clear "after" ids
            self.after(6000, lambda: self.cancelPending()))

    #cancels everything in pending and then clears it
    def cancelPending(self) -> None:
        for x in self.pending:
            self.after_cancel(x)
        self.pending.clear()

    # =========== INFO ===========
    def addSampleVideos(self) -> None:
        self.inputText.insert(tk.END,
            "https://www.youtube.com/shorts/9p0pdiTOlzw\n" + #get wifi anywhere you go
            "https://www.youtube.com/watch?v=fFxySUC2vPc\n" + #python subprocess
            "https://youtu.be/Y_pbEOem2HU\n" + #vine boom
            "jNQXAC9IVRw\n" + #me at the zoo
            "https://www.reddit.com/r/Eyebleach/comments/ml2y1g/dramatic_sable/\n"
            + "https://youtu.be/f1A7SdVTlok"
        ) #default text

def ytdlpWrapper(root: MainWindow, dl_options: dict) -> None:
    try:
        YoutubeDL(dl_options).download(root.URLs)
    except SystemExit as ex:
        sys.exit()
            
def ytdlpListener(root: MainWindow, thread: Thread, dl_options: dict, check: bool) -> bool:
    while True:
        root.update()

        # no more videos
        if (root.currVideo >= len(root.URLs)): 
            root.updateProgressBar("successful")
            break

        # new item in queue
        if not root.updateQueue.empty():
            item = root.updateQueue.get()
            print("item: ", item, "\n\n")

            if isinstance(item, float) and item >= 0: # update curr progress
                root.currProgressBar['value'] = item

            elif item == "__done": # done with a video
                root.currVideo += 1 # next video
            
            elif item == "__filename": # new filename, add to self.filenames as partfile
                filename = root.updateQueue.get()
                root.filenames.append(filename)
                root.filenames.append(filename + ".part")

            elif item == "__info" and dl_options['simulate']: # advance when checking
                root.currVideo += 1

            elif item == "__cancel": # user cancel
                # force thread to hit an exception and leave the YoutubeDL().download() call
                ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident),
                                        ctypes.py_object(SystemExit))
                root.updateProgressBar("cancelled")
                break

            root.updateProgressBar(check)
    
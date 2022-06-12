import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import filedialog
import os
import sys

from yt_dlp.YoutubeDL import YoutubeDL

from download_logger import DownloadLogger
from info_window import InfoWindow
from confirm_prompt import ConfirmPrompt
from tk_common import updateText

class MainWindow(tk.Tk):
    def __init__(self, data):
        #inherit all the stuff from tk.Tk
        super().__init__() 

        self.data = data 
        self.pending = []

        self.URLs = []
        self.filenames = []
        self.formats = [] #WIP
        self.currVideo = 0

        self.format = tk.StringVar(self, "b") #default format is best of both
        self.checkURLs = tk.BooleanVar(self, True)
        self.deleteOnFinish = tk.BooleanVar(self, True)
        self.playSound = tk.BooleanVar(self, True)
        
        #initialize main window
        self.title("ytdl-GUI")
        self.iconbitmap(data['iconPath'])
        self.eval('tk::PlaceWindow . center') #puts window in center(ish)

        #initialize main frame (located within main window)
        self.frame = tk.Frame(self)
        self.frame.grid(padx=20, pady=(8, 18))

        # ------- WIDGETS -------
        # =========== DIRECTORY ===========
        #label for directory
        self.directoryLabel = tk.Label(
            self.frame, text="Output Path:"
        )
        self.directoryLabel.grid(sticky="W")

        #directory to download to
        self.directoryText = tk.Text(
            self.frame, height=1, width=68,
        )
        self.directoryText.insert(tk.END, data['path'])
        self.directoryText.grid(column=0, row=1, padx=5, pady=5)

        #button to open directory-choosing prompt
        self.directoryButton = tk.Button(
            self.frame, height=0, width=0,
            text = "...", command=self.setDirectory
        )
        self.directoryButton.grid(column=1, row=1, padx=1, pady=1)

        # =========== INPUT ===========
        #input label
        self.inputLabel = tk.Label(
            self.frame, text = "Videos to download:"
        )
        self.inputLabel.grid(row=2, sticky="W")
        
        #input text box scroll bar
        self.inputScroll = tk.Scrollbar(
            self.frame, width=16
        )
        self.inputScroll.grid(column=1, row=3, sticky="NS")

        #input text box
        self.inputText = tk.Text(
            self.frame, height=7, width=68,
            yscrollcommand=self.inputScroll.set
        )
        self.inputText.grid(row=3, padx=5, pady=5)
        self.inputScroll.configure(command=self.inputText.yview)

        # =========== FORMAT SELECTION ===========
        self.formatGrid = tk.Frame(self.frame)
        self.formatGrid.grid(row=4, sticky="ew")

        #label for formats
        self.formatLabel = tk.Label(
            self.formatGrid, text="Format: "
        )
        self.formatLabel.grid(column=0, sticky="W")

        #format radio button selection
        self.vidAndAud = ttk.Radiobutton(
            self.formatGrid, text="Video and Audio", variable=self.format, value="best"
        )
        self.vidAndAud.grid(column=1, row=0, sticky="e", padx=18)
        self.vidOnly = ttk.Radiobutton(
            self.formatGrid, text="Video Only", variable=self.format, value="bestvideo"
        )
        self.vidOnly.grid(column=2, row=0, sticky="e", padx=18)
        self.audOnly = ttk.Radiobutton(
            self.formatGrid, text="Audio Only", variable=self.format, value="bestaudio"
        )
        self.audOnly.grid(column=3, row=0, sticky="e", padx=18)
        self.audOnlyCons = ttk.Radiobutton(
            self.formatGrid, text="m4a (audio)", variable=self.format, value="m4a"
        )
        self.audOnlyCons.grid(column=4, row=0, sticky="e", padx=18)

        self.format.set("best") #set default radio value (first button)

        # =========== INPUT BUTTONS ===========
        #button to send text box input
        self.inputButton = tk.Button(
            self.frame, text="Download", 
            command=self.inputURLs
        )
        self.inputButton.grid(row=7, padx=5, pady=5)

        #button to clear
        self.clearButton = tk.Button(
            self.frame, text="Clear", 
            command=lambda:self.inputText.delete("1.0", tk.END)
        )
        self.clearButton.grid(row=7, sticky="E", padx=5, pady=5)

        # =========== PROGRESS ===========
        self.progressFrame = tk.Frame(self.frame)

        #progress bar for overall downloads
        self.progressBarLabel = tk.Label(
            self.progressFrame, text = "All Videos:"
        )
        self.progressBarLabel.grid(row=0, column=0, pady=4) 

        self.progressBar = ttk.Progressbar(
            self.progressFrame, orient=HORIZONTAL, length=500, mode='determinate'
        )
        self.progressBar.grid(row=0, column=1, pady=4) 

        #progress bar for current video download
        self.currProgressBarLabel = tk.Label(
            self.progressFrame, text = "This Video:"
        )
        self.currProgressBarLabel.grid(row=1, column=0, pady=4) 
        self.currProgressBar = ttk.Progressbar(
            self.progressFrame, orient=HORIZONTAL, length=500, mode='determinate'
        )
        self.currProgressBar.grid(row=1, column=1, pady=4) 

        # status Label!!
        self.statusLabel = tk.Label(
            self.frame, text = "Awaiting URL input...\n"
        )
        self.statusLabel.grid(row=8, padx=2, pady=2)

        # =========== OPTIONS ===========
        #options label
        self.optionsLabel = tk.Label(
            self.frame, text = "Options:"
        )
        self.optionsLabel.grid(row=9, sticky='w')

        #play sound when download finished toggle
        self.playSoundCheck = tk.Checkbutton(
            self.frame, text = "Play sound after download/error",
            variable=self.playSound, onvalue=True, offvalue=False
        )
        self.playSoundCheck.grid(row=10, sticky='w')

        #check if URLs are valid before downloading
        self.checkURLsCheck = tk.Checkbutton(
            self.frame, text = "Check URLs before download",
            variable=self.checkURLs, onvalue=True, offvalue=False
        )
        self.checkURLsCheck.grid(row=11, sticky='w')

        #delete input on finish toggle
        self.deleteOnFinishCheck = tk.Checkbutton(
            self.frame, text = "Delete input after download",
            variable=self.deleteOnFinish, onvalue=True, offvalue=False
        )
        self.deleteOnFinishCheck.grid(row=12, sticky='w')

        #info label
        self.infoButton = tk.Button(
            self.frame, text = "Info",
            command = lambda:InfoWindow(self)
        )
        self.infoButton.grid(row=12, sticky="E")

    # =========== DIRECTORY ===========
    #uses tkinter's askdirectory dialog to set directory in text box
    def setDirectory(self):
        dir = filedialog.askdirectory() #will very likely be valid
        if (dir != ""):
            self.directoryText.delete(1.0, tk.END)
            self.directoryText.insert(tk.END, dir)

    # =========== DOWNLOADING ===========
    #cancels everything in pending and then clears it
    def cancelPending(self):
        for x in self.pending:
            self.after_cancel(x)
        self.pending.clear()

    #takes inputs, stores them in URLs, and then calls download function
    def inputURLs(self):
        self.URLs = self.inputText.get(1.0, tk.END).split()
        path = self.directoryText.get(1.0, tk.END).replace("\n", "")
        if (os.system('cd "' +  path + '"') == 0): #valid dir
            if len(self.URLs) > 0: #valid URLs
                updateText(self, self.statusLabel, "URLs Received!\n")
                self.downloadURLs()
            else:
                ConfirmPrompt(self, '''Error: No URLs provided\n\n'''
                   + '''Please provide at least one URL''')
        else:
            ConfirmPrompt(self, '''Error: Invalid Download Path\n\n'''
                + '''Please change download path to valid directory''')

    def doCheckURLs(self, dl_options):
        if self.checkURLs.get():
            self.currVideo = 0
            dl_options['simulate'] = True
            try:
                self.updateProgressBar(True)
                YoutubeDL(dl_options).download(self.URLs)
                return True
            except:
                ConfirmPrompt(self, f'''Error: Invalid URL\n\n'''
                    + f'''Please check your URL #{self.currVideo + 1} '''
                    + f'''again to make\n sure it is valid and compatible''')
                self.finishDownload("unsuccessful") #wrap up stuff + reset
        return False
        
        
    #downloads URLs in list -- main function
    def downloadURLs(self):
        self.inputButton.configure(text="Cancel", 
            command=self.cancelDownload) #to cancel download
        self.cancelPending() #get rid of any pending after() calls

        self.progressFrame.grid(row=5) #show progress bars
        self.progressBar['value'] = 0
        self.currProgressBar['value'] = 0

        dl_options = {
            "paths": {'home': self.directoryText.get(1.0, tk.END)}, 
            "nocheckcertificate": True, 
            "format": self.format.get(),
            'simulate': True,
            'logger': DownloadLogger(self, True),
            'progress_hooks': [self.dl_hook],
        }

        if (self.checkURLs.get() == self.doCheckURLs(dl_options)): #check URLs?
            dl_options['simulate'] = dl_options['logger'].simulate = False
            self.currVideo = 0
            try: #begin downloads
                self.updateProgressBar(False)
                YoutubeDL(dl_options).download(self.URLs)
                self.finishDownload("successful") #wrap up stuff + reset
            except:
                if len(self.URLs) != 0: #if not caused by cancel
                    ConfirmPrompt(self, '''Error: Download issue\n\n'''
                        + '''There was an issue with the download''')
                    self.finishDownload("unsuccessful") #wrap up stuff + reset

    #runs during each download, keeps track of status
    def dl_hook(self, d):
        if d['status'] == 'downloading':
            try: #progress as bytes dl'ed
                self.currProgressBar['value'] = ( d['downloaded_bytes'] /
                    d['total_bytes'] ) * 100
            except:
                try: #progress as time elapsed
                    self.currProgressBar['value'] = ( d['elapsed'] /
                        (d['elapsed'] + d['eta']) ) * 100
                except: #dont show anything
                    self.currProgressBar['value'] = 0
            self.update()
            if self.data['debug']: print('') #prints video download status to stdout
        elif d['status'] == 'finished':
            if 'elapsed' in d: #if a download occurred
                self.filenames.append(d['filename']) #add to completed dl list
            self.currVideo += 1
            self.updateProgressBar(False)
            self.currProgressBar['value'] = 0 #reset curr progress bar
            
    #updates progress bar to indicate progress
    def updateProgressBar(self, is_sim):
        if is_sim and self.currVideo < len(self.URLs): #for URL check
            updateText(self, self.statusLabel, f'''Checking if URL #'''
                + f'''{self.currVideo + 1} is valid... \n'''
                + f'''({self.URLs[self.currVideo]})''')
        elif (not self.currVideo >= len(self.URLs)): #for download
            updateText(self, self.statusLabel, f'''Video {str(self.currVideo + 1)}''' 
               + f''' is being downloaded... \n ({self.URLs[self.currVideo]})''')
        self.progressBar['value'] = ((self.currVideo)/len(self.URLs)) * 100
        self.update()

    #cancels download by clearing URLs, deletes downloaded files
    def cancelDownload(self):
        updateText(self, self.statusLabel, f"Download cancelled")
        self.URLs.clear() #this will cause an error with downloadURLs(), stopping it
        self.finishDownload("cancelled")

        ConfirmPrompt(self, "Do you want to delete the already downloaded files?",
            self.filenames)

    #summary after downloading videos
    def finishDownload(self, endText):
        updateText(self, self.statusLabel, f'Download {endText}\n') 
        self.inputButton.configure(text="Download", command=self.inputURLs)
        if self.playSound.get(): self.bell() #makes sound upon completion

        if (endText == "successful" and self.deleteOnFinish.get() == True):
            self.inputText.delete("1.0", tk.END) #delete input
        self.URLs.clear() #clears URLs to make YoutubeDL() stop if running

        #reset delay (for visual appeal)
        self.pending.append(
            self.after(5000, lambda: updateText(self, self.statusLabel,
            "Awaiting URL input...\n"))
        )
        self.pending.append(
            self.after(5000, lambda: self.progressFrame.grid_remove())
        )

    # =========== INFO ===========
    def addSampleVideos(self):
        self.inputText.insert(tk.END,
            "https://www.youtube.com/shorts/9p0pdiTOlzw\n" + #get wifi anywhere you go
            "https://www.youtube.com/watch?v=fFxySUC2vPc\n" + #python subprocess
            "https://youtu.be/Y_pbEOem2HU\n" + #vine boom
            "jNQXAC9IVRw\n" + #me at the zoo
            "https://www.reddit.com/r/Eyebleach/comments/ml2y1g/dramatic_sable/"
        ) #default text
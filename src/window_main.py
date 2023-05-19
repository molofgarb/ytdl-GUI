import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import filedialog
    
import os, sys
# from multiprocessing import Process
from threading import Thread

from yt_dlp.yt_dlp.YoutubeDL import YoutubeDL

from ytdlp_dl_logger import DownloadLogger
from window_info import InfoWindow
from window_confirm import ConfirmPrompt
from common_tk import updateText

class MainWindow(tk.Tk):
    def __init__(self, data):
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

        # styled separately because ttk used instead of tk
        self.ttkStyle = ttk.Style(self)
        self.ttkStyle.theme_use("clam")
        self.ttkStyle.configure(
            "format.TRadiobutton",
            background=self.style["bgcolor"], foreground=self.style['textcolor'], font=self.style['mainfont'],
            state="normal"
        )
        self.ttkStyle.map("format.TRadiobutton", 
                          foreground=[('hover', self.style['bgcolor']), 
                                      ('background', self.style['textcolor'])
                                     ]
                        )
        self.ttkStyle.configure(
            "format.Horizontal.TProgressbar",
            background=self.style["bgcolor"]
        )

        super().configure( #style for entire window background
            background=self.style["bgcolor"]
        )

        # =========== VARS ===========

        #window data
        self.pending = [] #holds events that will happen

        self.URLs = [] #URLs of files to be downloaded
        self.filenames = [] #names of files as they are downloaded
        self.formats = [] #TODO
        self.process = 0 # holds YoutubeDL() process
        self.currVideo = 0 #index of video in URLs that is being checked/downloaded

        #download format 
        self.format = tk.StringVar(self, "b") #default format is best of both

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
                text = "test", command=lambda: ConfirmPrompt(self, self.data, "test!"), 
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
    def setDirectory(self):
        dir = filedialog.askdirectory() #will very likely be valid
        if self.data['debug']: print(self.pending)
        if (dir != ""):
            self.directoryText.delete(1.0, tk.END)
            self.directoryText.insert(tk.END, dir)

    # =========== EXPAND OPTIONS ===========

    #toggles the expansion/minimization of the options frame
    def expandOptions(self):
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
    def inputURLs(self):
        self.URLs = self.inputText.get(1.0, tk.END).split()
        path = self.directoryText.get(1.0, tk.END).replace("\n", "")
        if (os.system('cd "' +  path + '"') == 0): #valid dir
            if len(self.URLs) > 0: #valid URLs
                updateText(self, self.statusLabel, "URLs Received!\n")
                self.downloadURLs()
            else:
                ConfirmPrompt(self, self.data, self.style, 
                '''Error: No URLs provided\n\nPlease provide at least one URL''')
        else:
            ConfirmPrompt(self, self.data, self.style, 
            '''Error: Invalid Download Path\n\nPlease change download path to valid directory''')

    #make sure all URLs are valid before all downloads begin
    def checkURLs(self, dl_options):
        if self.ischeckURLs.get():
            self.currVideo = 0
            dl_options['simulate'] = True
            try:
                self.updateProgressBar(True)
                YoutubeDL(dl_options).download(self.URLs)
                return True
            except Exception as ex:
                ConfirmPrompt(self, self.data, self.style, 
                      f'''Error: Invalid URL\n\n'''
                    + f'''1) Please check your URL #{self.currVideo + 1} '''
                    + f'''again to make sure it is valid and compatible\n''' 
                    + f'''2) Please try using a different format to download these videos''')
                if (self.data['debug']):
                    print(self.URLs, "are the bad URLs")
        return False

    # =========== DOWNLOAD URLS ===========

    #downloads URLs in list -- main function
    def downloadURLs(self):
        self.inputButton.configure(text="Cancel", 
            command=self.cancelDownload) #to cancel download
        self.cancelPending() #get rid of any pending after() calls

        self.progressFrame.grid(row=50) #show progress bars
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

        if (self.ischeckURLs.get() and not self.checkURLs(dl_options)): #check URLs?
            print('here')
            self.finishDownload("unsuccessful") #wrap up stuff + reset if bad check
            return 1

        dl_options['simulate'] = dl_options['logger'].simulate = False
        self.currVideo = 0
        self.process = Thread(target=YoutubeDL(dl_options).download, args=(self.URLs,))

        try: #begin downloads
            self.urlLabel.grid(row=1, padx=2, pady=2)
            self.updateProgressBar(False)
            self.process.start() # everything from here on out is owned by self.process (i think)

        except Exception as ex:
            if len(self.URLs) != 0: #if not caused by cancel
                ConfirmPrompt(self, self.data, self.style, 
                    '''Error: Download issue\n\nThere was an issue with the download. Please try again.''')
                if (self.data['debug']):
                    print(self.URLs, ex)
                self.finishDownload("unsuccessful") #wrap up stuff + reset

    #runs during each download (NOT SIMULATE/CHECK), keeps track of status of that individual download
    def dl_hook(self, d):

        #if nothing pending, then animate ellipses
        if (len(self.pending) == 0): 
            self.updateProgressBar(False)

        if d['status'] == 'downloading': #update currprogressbar if download to indicate dl prog
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
            if ((len(self.filenames) == 0) or
                (self.filenames[len(self.filenames) - 1] != ('"' + str(d['filename']) + '.part' + '"'))
            ): #add partfile to end
                self.filenames.append(('"' + str(d['filename']) + '.part' + '"'))

        elif d['status'] == 'finished': #when a download/check has finished 
            if 'elapsed' in d: #if a download occurred
                partfile = self.filenames.pop()
                if (partfile == ('"' + str(d['filename']) + '.part' + '"')): #if confirmed to be part file
                    self.filenames.append('"' + str(d['filename']) + '"') #add to completed dl list in final directory format
                else:
                    self.filenames.append(partfile) #if it was something else
            self.currVideo += 1
            self.updateProgressBar(False, True)
            self.currProgressBar['value'] = 0 #reset curr progress bar
            
    #updates progress bar to indicate progress
    def updateProgressBar(self, is_check, keep_el=False):
        if (is_check and (self.currVideo < len(self.URLs))): #for URL check
            updateText(self, self.statusLabel, f'''Checking if URL #'''
                + f'''{self.currVideo + 1} is valid...''')

        elif (self.currVideo < len(self.URLs)): #for download

            #below is ellipses animation stuff
            onedot = self.statusLabel.cget("text")[-3:] == "ed."
            twodot = self.statusLabel.cget("text")[-3:] == "d.."
            threedot = self.statusLabel.cget("text")[-3:] == "..."
            if ((onedot and not keep_el) or (twodot and keep_el)): #one dot
                updateText(self, self.statusLabel, f'''Video {str(self.currVideo + 1)}''' 
               + f''' is being downloaded..''')
            elif ((twodot and not keep_el) or (threedot and keep_el)): #two dot
                updateText(self, self.statusLabel, f'''Video {str(self.currVideo + 1)}''' 
               + f''' is being downloaded...''')
            else: #three dots or no dots or something weird
                updateText(self, self.statusLabel, f'''Video {str(self.currVideo + 1)}''' 
               + f''' is being downloaded.''')
            self.pending.append( #sits in pending to indicate ellipse do-not-change, change if gone
                self.after(1000, lambda: self.cancelPending())
            )
            
        if (self.currVideo < len(self.URLs)): #update URL label to reflect current check
            updateText(self, self.urlLabel, f'''({self.URLs[self.currVideo]})''') #display url of video being dl'ed

        if (self.currVideo == len(self.URLs)) and (not is_check): # last video is done (out of range)
            self.finishDownload("successful") #wrap up stuff + reset
            return 0 # this may be bad

        self.progressBar['value'] = ((self.currVideo)/len(self.URLs)) * 100
        self.update()

        

    # =========== FINISH DOWNLOADING ===========

    #cancels download by clearing URLs, deletes downloaded files
    def cancelDownload(self):
        updateText(self, self.statusLabel, f"Download cancelled")
        self.URLs.clear() #this will cause an error with downloadURLs(), stopping it
        
        ConfirmPrompt(self, self.data, self.style, 
            "Do you want to delete the already downloaded files?",
            self.filenames)
        
        self.finishDownload("cancelled") # finishDownload will take care of the rest

    #summary after downloading videos
    def finishDownload(self, endText):
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
            "Awaiting URL input...\n"))
        )
        self.pending.append( # remove urlLabel after 5 sec
            self.after(5000, lambda: self.urlLabel.grid_remove())
        )
        self.pending.append( # remove progresbar after 5 sec
            self.after(5000, lambda: self.progressFrame.grid_remove())
        )
        self.pending.append( #clear "after" ids
            self.after(6000, lambda: self.cancelPending())
        )

        # close the thread that owns this function object
        if self.process != 0 and self.process.is_alive():
            if self.data['debug']: print("exit!")
            # self.process.join()
            sys.exit()

        #cancels everything in pending and then clears it
    def cancelPending(self):
        for x in self.pending:
            self.after_cancel(x)
        self.pending.clear()

    # =========== INFO ===========
    def addSampleVideos(self):
        self.inputText.insert(tk.END,
            "https://www.youtube.com/shorts/9p0pdiTOlzw\n" + #get wifi anywhere you go
            "https://www.youtube.com/watch?v=fFxySUC2vPc\n" + #python subprocess
            "https://youtu.be/Y_pbEOem2HU\n" + #vine boom
            "jNQXAC9IVRw\n" + #me at the zoo
            "https://www.reddit.com/r/Eyebleach/comments/ml2y1g/dramatic_sable/\n" +
            "https://youtu.be/f1A7SdVTlok"
        ) #default text
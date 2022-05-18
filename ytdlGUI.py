import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import filedialog

import os, sys
from platform import system
import subprocess
import time

import webbrowser

from yt_dlp import YoutubeDL


# ======== Environment ========

windows = False
whereami = os.getcwd()

#Get info about environment
opsys = system()
if (opsys == "Windows"):
    windows = True
elif (opsys != "Darwin" and opsys != "Linux"):
    sys.exit("Operating System not supported")

#icon stuff
iconPath = ""
if getattr(sys, 'frozen', False):
    iconPath = os.path.join(sys._MEIPASS, "resources/logo.ico")
else:
    iconPath = "resources/logo.ico"

# ======== Window Construction ========

#updates a label with new text, text
def updateText(root, widget, text):
    widget.configure(text=text)
    root.update()

class InfoWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

        self.title("Info")
        self.iconbitmap(iconPath)
        root.eval(f'tk::PlaceWindow {str(self)} center')

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, padx=20, pady=10)

        self.name = tk.Label(
            self.frame, text="ytdl-GUI by molofgarb"
        )
        self.name.grid(row=0, sticky="w", padx=5, pady=2)

        self.readmeButton = tk.Button(
            self.frame, text="Open Readme",
            command=lambda: webbrowser.open_new_tab("README.md")
        )
        self.readmeButton.grid(row=1, sticky="W", padx=5, pady=5)

        self.sitesButton = tk.Button(
            self.frame, text="Supported Websites",
            command=lambda: webbrowser.open_new_tab("supportedsites.md")
        )
        self.sitesButton.grid(row=2, sticky='w', padx=5, pady=5)

        self.thanksLabel = tk.Label(
            self.frame, text="\nThank you for using ytdl-GUI!"
        )
        self.thanksLabel.grid(row=3, sticky='w')

        self.repoLabel = tk.Label(
            self.frame, text="\nytdl-GUI GitHub:",
        )
        self.repoLabel.grid(row=4, sticky="W")

        self.repoLink = tk.Label(
            self.frame, text="https://github.com/molofgarb/ytdl-GUI",
            fg="blue", cursor="hand2"
        )
        self.repoLink.grid(row=5, sticky="W")
        self.repoLink.bind(
            "<Button-1>", lambda: webbrowser.open_new_tab("https://github.com/molofgarb/ytdl-GUI")
        )

        self.ytdlpRepoLabel = tk.Label(
            self.frame, text="\nyt-dlp GitHub:",
        )
        self.ytdlpRepoLabel.grid(row=6, sticky="W")

        self.ytdlpRepoLink = tk.Label(
            self.frame, text="https://github.com/yt-dlp/yt-dlp",
            fg="blue", cursor="hand2"
        )
        self.ytdlpRepoLink.grid(row=7, sticky="W")
        self.ytdlpRepoLink.bind(
            "<Button-1>", lambda e: webbrowser.open_new_tab("https://github.com/yt-dlp/yt-dlp")
        )

        # =========== DEBUG ===========
        self.debugLabel = tk.Label(
            self.frame, text="Debug Functions:",
        )
        self.debugLabel.grid(row=0, column=1)
        #adds sample videos
        self.sampleButton = tk.Button(
            self.frame, text = "Add sample videos",
            command = root.addSampleVideos
        )
        self.sampleButton.grid(row=1, column=1, pady=5)

        #adds sample videos
        self.removeSampleButton = tk.Button(
            self.frame, text = "Delete Sample Videos",
            command = self.removeSampleVideos
        )
        self.removeSampleButton.grid(row=2, column=1, pady=5, padx=10)

    def removeSampleVideos(self):
        cmd = 'del' if (windows) else 'rm'
        os.system(cmd + ' "(subprocess) solved! FileNotFoundError - [WinError 2] The system cannot find the file specified [fFxySUC2vPc].mp4"')
        os.system(cmd + ' "Dramatic Sable [BDqOmwM].mp4"')
        os.system(cmd + ' "get wifi anywhere you go vine ad scam [9p0pdiTOlzw].mp4"')
        os.system(cmd + ' "Me at the zoo [jNQXAC9IVRw].mp4"')
        os.system(cmd + ' "Vine Boom Sound Effect [Y_pbEOem2HU].mp4"')



class ConfirmPrompt(tk.Toplevel):
    def __init__(self, root, promptText, data = 0):
        super().__init__(root)
        self.promptText = promptText
        self.data = data

        if self.promptText == "Do you want to download these videos?":
            self.title("Download Confirmation")
        elif self.promptText == "Do you want to delete the already downloaded files?":
            self.title("Delete Confirmation")

        self.iconbitmap(iconPath)
        root.eval(f'tk::PlaceWindow {str(self)} center')

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, padx=2, pady=10)

        # ------- WIDGETS -------
        self.questionLabel = tk.Label(
            self.frame, text = promptText
        )
        self.questionLabel.grid(sticky="N", padx=15)
        
        self.yesButton = tk.Button(
            self.frame, text="Yes",
            width=6,
            command=lambda: self.answer(True)
        )
        self.noButton = tk.Button( #No/Ok
            self.frame, text = "Ok",
            width=6, 
            command=lambda: self.answer(False)
        )

        if len(promptText) < 5: #yes/no
            if promptText[:5] != "Error":
                updateText(self, self.noButton, "No")
                self.questionLabel.configure(columnspan=2)
                self.yesButton.grid(row=1, sticky="N", padx=30, pady=20)
                self.noButton.grid(column=1, row=1, sticky="N", padx=30, pady=20)
        else: #ok
            self.noButton.grid(column=0, row=1, sticky="N", padx=30, pady=20)

    def answer(self, action):
        self.destroy()
        self.update()
        if action:
            #download prompt
            if self.promptText == "Do you want to download these videos?":
                self.master.saveDirectory()
                self.master.downloadURLs()
            #delete prompt
            elif self.promptText == "Do you want to delete the already downloaded files?":
                print(self.data)
                for filename in self.data:
                    print("d\n")
                    cmd = 'del' if (windows) else 'rm'
                    os.system(cmd + ' "' + filename + '"')
        


class MainWindow(tk.Tk):
    def __init__(self):
        #inherit all the stuff from tk.Tk
        super().__init__() 

        self.outDir = whereami
        self.cancel = False
        self.URLs = []
        self.filenames = []
        self.currVideo = 0
        self.deleteOnFinish = True

        #initialize main window
        self.title("ytdl-GUI")
        self.iconbitmap(iconPath)
        self.eval('tk::PlaceWindow . center') #puts window in center(ish)

        #initialize main frame (located within main window)
        self.frame = tk.Frame(self)
        self.frame.grid(padx=20, pady=5)

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
        self.directoryText.insert(tk.END, whereami)
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

        self.format = tk.StringVar(self, "b") #default format is best of both

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

        # =========== MISC ===========
        #info label
        self.infoButton = tk.Button(
            self.frame, text = "Info",
            command = lambda:InfoWindow(self)
        )
        self.infoButton.grid(row=9, sticky="E", pady=8)

        #delete input on finish toggle
        self.deleteOnFinishCheck = tk.Checkbutton(
            self.frame, text = "Delete input after download",
            variable=self.deleteOnFinish, onvalue=True, offvalue=False
        )
        self.deleteOnFinishCheck.select()
        self.deleteOnFinishCheck.grid(row=9, sticky='w')

    # =========== DOWNLOADING ===========
    #takes inputs, stores them in URLs, and then calls download function
    def inputURLs(self):
        input1 = self.inputText.get(1.0, tk.END)
        self.URLs = input1.split() 
        if len(self.URLs) > 0: #valid URLs
            updateText(self, self.statusLabel, "URLs Received!\n")
            self.downloadURLs()
        else:
            updateText(self, self.statusLabel, "Invalid input\n")
            self.after(5000, lambda: updateText(self, self.statusLabel, "Awaiting URL input...\n"))
        
    #downloads URLs in list -- main function
    def downloadURLs(self):
        self.progressFrame.grid(row=5) #show progress bars
        self.currVideo = 0
        self.inputButton.configure(text="Cancel", command=lambda:self.cancelDownload()) #to cancel download

        dl_options = {"paths": {'home': self.outDir}, 
            "nocheckcertificate": True, 
            "format": self.format.get(),
            'progress_hooks': [self.dl_hook]
        }

        #begin downloads
        self.updateProgressBar()
        try:
            YoutubeDL(dl_options).download(self.URLs) #done one-by-one on purpose
            self.finishDownload("successful") #wrap up stuff + reset
        except:
            ConfirmPrompt(self, "Error: Invalid URL\n\nPlease check your URLs again and make\n sure they are valid and compatible")
            self.finishDownload("unsuccessful") #wrap up stuff + reset

    #runs during each download
    def dl_hook(self, d):
        if d['status'] == 'downloading':
            try: #progress as bytes dl'ed
                self.currProgressBar['value'] = ((d['downloaded_bytes'])/d['total_bytes']) * 100
            except:
                try: #progress as time elapsed
                    self.currProgressBar['value'] = ((d['elapsed'])/(d['elapsed'] + d['eta'])) * 100
                except: #dont show anything
                    self.currProgressBar['value'] = 0
            self.update()
        elif d['status'] == 'finished':
            if 'elapsed' in d: #if a download occurred
                self.filenames.append(d['filename']) #add to completed dl list
            self.currVideo += 1
            self.currProgressBar['value'] = 0 #reset progress bars
            self.updateProgressBar()
            
    #updates progress bar to indicate progress
    def updateProgressBar(self):
        if not (self.currVideo >= len(self.URLs)):
            updateText(self, self.statusLabel, f'Video {str(self.currVideo + 1)} is being downloaded...\n'
                f'({self.URLs[self.currVideo]})')
        self.progressBar['value'] = ((self.currVideo)/len(self.URLs)) * 100
        self.update()

    #cancels download by clearing URLs, deletes downloaded files
    def cancelDownload(self):
        updateText(self, self.statusLabel, f"Download cancelled")
        self.URLs.clear() #this will cause an error with downloadURLs(), stopping it
        self.finishDownload("cancelled")

        ConfirmPrompt(self, "Do you want to delete the already downloaded files?", self.filenames)

    #summary after downloading videos
    def finishDownload(self, endText):
        updateText(self, self.statusLabel, f'Download {endText}\n') 
        self.inputButton.configure(text="Download", command=self.inputURLs)
        if (endText != "cancelled" and self.deleteOnFinish == True):
            self.inputText.delete("1.0", tk.END) #delete input
        
        self.URLs.clear()
        self.after(5000, lambda: updateText(self, self.statusLabel, "Awaiting URL input...\n"))
        self.after(5000, lambda: self.progressFrame.grid_remove())

    # =========== INFO ===========
    def addSampleVideos(self):
        self.inputText.insert(tk.END,
            "https://www.youtube.com/shorts/9p0pdiTOlzw\n" + #get wifi anywhere you go
            "https://www.youtube.com/watch?v=fFxySUC2vPc\n" + #python subprocess
            "https://youtu.be/Y_pbEOem2HU\n" + #vine boom
            "jNQXAC9IVRw\n" + #me at the zoo
            "https://www.reddit.com/r/Eyebleach/comments/ml2y1g/dramatic_sable/"
        ) #default text

    # =========== DIRECTORY ===========
    #uses tkinter's askdirectory dialog to set directory in text box
    def setDirectory(self):
        dir = filedialog.askdirectory()
        if (dir != ""):
            self.directoryText.delete("1.0", tk.END)
            self.directoryText.insert(tk.END, dir)

    #updates directory field with directory in text box
    def saveDirectory(self):
        self.outDir = self.directoryText.get(1.0, tk.END)




#defines main window
root = MainWindow()
root.iconbitmap(iconPath)

#loop!!
root.mainloop()



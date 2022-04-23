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

ytdlCall = "yt-dlp"

opsys = system()
windows = False
whereami = ""

#Get info about environment
if (opsys == "Windows"):
    windows = True
elif (opsys != "Darwin" and opsys != "Linux"):
    sys.exit("Operating System not supported")

#figure out working directory 
if (opsys == "Windows"):
    whereami = subprocess.check_output(['cd'], shell=True) 
else: #macOS or linux
    whereami = subprocess.check_output(['pwd'], shell=True)

#icon stuff for windows
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
            command=self.openReadme
        )
        self.readmeButton.grid(row=1, sticky="W", padx=5, pady=5)

        self.thanksLabel = tk.Label(
            self.frame, text="\nThank you for using ytdl-GUI!"
        )
        self.thanksLabel.grid(row=2)

        self.repoLabel = tk.Label(
            self.frame, text="\nytdl-GUI GitHub:",
        )
        self.repoLabel.grid(row=3, sticky="W")

        self.repoLink = tk.Label(
            self.frame, text="https://github.com/molofgarb/ytdl-GUI",
            fg="blue", cursor="hand2"
        )
        self.repoLink.grid(row=4, sticky="W")
        self.repoLink.bind(
            "<Button-1>", lambda: webbrowser.open_new_tab("https://github.com/molofgarb/ytdl-GUI")
        )

        self.ytdlpRepoLabel = tk.Label(
            self.frame, text="\nyt-dlp GitHub:",
        )
        self.ytdlpRepoLabel.grid(row=5, sticky="W")

        self.ytdlpRepoLink = tk.Label(
            self.frame, text="https://github.com/yt-dlp/yt-dlp",
            fg="blue", cursor="hand2"
        )
        self.ytdlpRepoLink.grid(row=6, sticky="W")
        self.ytdlpRepoLink.bind(
            "<Button-1>", lambda e: webbrowser.open_new_tab("https://github.com/yt-dlp/yt-dlp")
        )

    def openReadme(self):
        try:
            os.startfile("README.md")
        except:
            raise Exception("Readme not found")



class ConfirmPrompt(tk.Toplevel):
    def __init__(self, root, promptText, data = 0):
        super().__init__(root)

        self.title("Download Confirmation")
        self.iconbitmap(iconPath)
        root.eval(f'tk::PlaceWindow {str(self)} center')

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, padx=2, pady=10)

        self.promptText = promptText
        self.data = data

        # ------- WIDGETS -------
        self.questionLabel = tk.Label(
            self.frame, text = promptText
        )
        self.questionLabel.grid(sticky="N", columnspan=2)
        
        self.yesButton = tk.Button(
            self.frame, text="Yes",
            width=6,
            command=lambda: self.answer("Y")
        )
        self.yesButton.grid(row=1, sticky="N", padx=30, pady=20)

        self.noButton = tk.Button(
            self.frame, text = "No",
            width=6, 
            command=lambda: self.answer("N")
        )
        self.noButton.grid(column=1, row=1, sticky="N", padx=30, pady=20)

    def answer(self, answer):
        self.destroy()
        self.update()
        #if download prompt
        if self.promptText == "Do you want to download these videos?":
            self.master.saveDirectory()
            self.master.downloadURLs(self.data)
        #if delete prompt
        elif self.promptText == "Do you want to delete the already downloaded files?":
            pass #figure out how to track what files are downloaded/find 
        


class MainWindow(tk.Tk):
    def __init__(self):
        #inherit all the stuff from tk.Tk
        super().__init__() 

        self.outDir = whereami

        #initialize main window
        self.title("ytdl-GUI")
        self.iconbitmap(iconPath)
        self.eval('tk::PlaceWindow . center') #puts window in center

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

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


        # =========== INPUT BUTTONS ===========
        #button to send text box input
        self.inputButton = tk.Button(
            self.frame, text="Download", 
            command=self.inputURLs
        )
        self.inputButton.grid(row=6, padx=5, pady=5)

        #button to clear
        self.clearButton = tk.Button(
            self.frame, text="Clear", 
            command=lambda:self.inputText.delete("1.0", tk.END)
        )
        self.clearButton.grid(row=6, sticky="E", padx=5, pady=5)

        # =========== MISC ===========
        #progress bar for downloads
        self.progressBar = ttk.Progressbar(
            self.frame, orient=HORIZONTAL, length=550, mode='determinate'
        )

        # status Label!!
        self.statusLabel = tk.Label(
            self.frame, text = "Awaiting URL input...\n"
        )
        self.statusLabel.grid(row=7, padx=2, pady=2)

        #adds sample videos to download box
        self.sampleButton = tk.Button(
            self.frame, text = "Add sample videos",
            command = self.addSampleVideos
        )
        self.sampleButton.grid(row=8, sticky="W", pady=8)

        #info label
        self.infoButton = tk.Button(
            self.frame, text = "Info",
            command = lambda:InfoWindow(self)
        )
        self.infoButton.grid(row=8, sticky="E", pady=8)

    #takes inputs from <inputtxt> and stores them in <URLs>
    def inputURLs(self):
        input1 = self.inputText.get(1.0, tk.END)
        URLs = input1.split() 
        if len(URLs) > 0: updateText(self, self.statusLabel, "URLs Received!\n")
        if len(URLs) == 1:
            ConfirmPrompt(self, "Do you want to download this video?", URLs)
        elif len(URLs) > 1:
            ConfirmPrompt(self, "Do you want to download these videos?", URLs)
        
    #downloads URLs in list
    def downloadURLs(self, URLs):
        self.progressBar.grid(row=5, pady=4)
        dl_options = {"paths": {'home': self.outDir}, 
            "nocheckcertificate": True, 
            "format": self.format.get()
        }
        ydl = YoutubeDL(dl_options) #create YoutubeDL obj with above options
        self.inputButton.configure(text="Cancel", command=lambda:self.cancelDownload(i, URLs)) #to cancel download
        for i in range(len(URLs)): #begin to download videos
            updateText(self, self.statusLabel, f'Downloading video {str(i + 1)}...\n ({URLs[i]})')
            try:
                ydl.download(URLs[i]) #done one-by-one on purpose
            except:
                updateText(self, self.statusLabel, f'Error: {URLs[i]} cannot be downloaded')
                time.sleep(2)
            self.updateProgress(i + 1, len(URLs))
        #wrap up stuff + reset
        self.finishDownload("finished")

    #uses tkinter's askdirectory dialog to set directory in text box
    def setDirectory(self):
        dir = filedialog.askdirectory()
        if (dir != ""):
            self.directoryText.delete("1.0", tk.END)
            self.directoryText.insert(tk.END, dir)

    #updates directory field with directory in text box
    def saveDirectory(self):
        self.outDir = self.directoryText.get(1.0, tk.END)

    def updateProgress(self, progress, total):
        self.progressBar['value'] = (progress/total) * 100

    def finishDownload(self, endText):
        updateText(self, self.statusLabel, f'Download {endText}\n') 
        self.inputButton.configure(text="Download", command=self.inputURLs)
        self.after(5000, lambda: updateText(self, self.statusLabel, "Awaiting URL input...\n"))
        self.after(5000, lambda: self.progressBar.grid_remove())

    def cancelDownload(self, i, URLs):
        updateText(self, self.statusLabel, f"Cancelled, deleting videos...")
        URLs.clear() #this will cause an error with downloadURLs(), stopping it
        #same end-of-dl stuff
        self.finishDownload("cancelled")
        #for deleting already-downloaded videos
        ConfirmPrompt(self, "Do you want to delete the already downloaded files?")

    def addSampleVideos(self):
        self.inputText.insert(tk.END,
            "https://www.youtube.com/shorts/9p0pdiTOlzw\n" + #get wifi anywhere you go
            "https://www.youtube.com/watch?v=fFxySUC2vPc\n" + #python subprocess
            "https://youtu.be/Y_pbEOem2HU\n" + #vine boom
            "jNQXAC9IVRw\n" + #me at the zoo
            "https://www.reddit.com/r/Eyebleach/comments/ml2y1g/dramatic_sable/"
        ) #default text



#defines main window
root = MainWindow()
root.iconbitmap(iconPath)

#loop!!
root.mainloop()



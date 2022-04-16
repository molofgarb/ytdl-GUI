#ytdlGUI.py -- Ethan Shieh
#4/13/2022

import tkinter as tk
from tkinter import filedialog

import os, sys
from platform import system
from subprocess import check_output
import time

import webbrowser

from yt_dlp import YoutubeDL


# ======== Environment ========

ytdlCall = "yt-dlp"
windows = False

whereami = ""
opsys = system()

#Get info about environment
if (opsys == "Windows"):
    windows = True
elif (opsys != "Darwin" and opsys != "Linux"):
    sys.exit("Operating System not supported")

#figure out working directory 
if (opsys == "Windows"):
    whereami = check_output(['cd'], shell=True) 
else: #macOS or linux
    whereami = check_output(['pwd'], shell=True)

#icon stuff for windows
iconPath = ""
if getattr(sys, 'frozen', False):
    iconPath = os.path.join(sys._MEIPASS, "resources/logo.ico")
else:
    iconPath = "resources/logo.ico"

# ======== Window Construction ========

#updates a label with new text, text
def updateLabel(root, label, text):
    label.configure(text=text)
    root.update()

class InfoWindow(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

        self.title("Info")
        self.iconbitmap(iconPath)
        root.eval(f'tk::PlaceWindow {str(self)} center')

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, padx=20, pady=20)

        self.readmeButton = tk.Button(
            self.frame, text = "Open Readme",
            command = self.openReadme
        )
        self.readmeButton.grid(row=0, sticky="W", padx=5, pady=5)

        self.repoLabel = tk.Label(
            self.frame, text = "\nGitHub:",
        )
        self.repoLabel.grid(row=1, sticky="W")

        self.repoLink = tk.Label(
            self.frame, text = "https://github.com/molofgarb/ytdl-GUI",
            fg = "blue", cursor = "hand2"
        )
        self.repoLink.grid(row=2)
        self.repoLink.bind(
            "<Button-1>", lambda e: webbrowser.open_new_tab("https://github.com/molofgarb/ytdl-GUI")
        )

        self.thanksLabel = tk.Label(
            self.frame, text = "\nThank you for using ytdl-GUI!"
        )
        self.thanksLabel.grid(row=3)

    def openReadme(self):
        try:
            os.startfile("README.md")
        except:
            raise Exception("Readme not found")



class DownloadPrompt(tk.Toplevel):
    def __init__(self, root, URLs = []):
        super().__init__(root)

        self.title("Download Confirmation")
        self.iconbitmap(iconPath)
        root.eval(f'tk::PlaceWindow {str(self)} center')

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, padx=2, pady=10)

        self.URLs = URLs

        # ------- WIDGETS -------
        self.questionLabel = tk.Label(
            self.frame, text = "Do you want to download these videos?"
        )
        self.questionLabel.grid(sticky="N", columnspan=2)
        
        self.yesButton = tk.Button(
            self.frame, text = "Yes",
            width=6,
            command = self.confirm
        )
        self.yesButton.grid(row=1, sticky="N", padx=30, pady=20)

        self.noButton = tk.Button(
            self.frame, text = "No",
            width=6, 
            command = self.destroy
        )
        self.noButton.grid(column=1, row=1, sticky="N", padx=30, pady=20)

    def confirm(self):
        self.destroy()
        self.update()
        self.master.saveDirectory()
        self.master.downloadURLs(self.URLs)     



class MainWindow(tk.Tk):
    def __init__(self):
        #inherit all the stuff from tk.Tk
        super().__init__() 

        self.outDir = whereami

        #initialize main window
        self.title("ytdl-GUI")
        self.iconbitmap(iconPath)
        self.eval('tk::PlaceWindow . center') #puts window in center

        #initialize main frame (located within main window)
        self.frame = tk.Frame(self)
        self.frame.grid(padx=20, pady=5)

        # ------- WIDGETS -------
        #label for directory
        self.directoryLabel = tk.Label(
            self.frame, text = "Output Path:"
        )
        self.directoryLabel.grid(sticky="W")

        #directory to download to
        self.directoryText = tk.Text(
            self.frame, height = 1, width = 68,
        )
        self.directoryText.insert(tk.END, whereami)
        self.directoryText.grid(column=0, row=1, padx=5, pady=5)

        #button to open directory-choosing prompt
        self.directoryButton = tk.Button(
            self.frame, height = 0, width = 0,
            text = "...", command = self.setDirectory
        )
        self.directoryButton.grid(column=1, row=1, padx=1, pady=1)

        #input label
        self.inputLabel = tk.Label(
            self.frame, text = "Videos to download:"
        )
        self.inputLabel.grid(row=2, sticky="W")
        
        #input text box
        self.inputText = tk.Text(
            self.frame, height = 7, width = 68
        )
        
        self.inputText.grid(row=3, padx=5, pady=5)
        
        #button to send text box input
        self.inputButton = tk.Button(
            self.frame, text = "Download", 
            command = self.inputURLs
        )
        self.inputButton.grid(row=4, padx=5, pady=5)
        
        # Label!!
        self.statusLabel = tk.Label(
            self.frame, text = "Awaiting URL input\n"
        )
        self.statusLabel.grid(row=5, padx=2, pady=2)

        #adds sample videos to download box
        self.sampleButton = tk.Button(
            self.frame, text = "Add sample videos",
            command = self.addSampleVideos
        )
        self.sampleButton.grid(row=6, sticky="W", pady=8)

        #info label
        self.infoButton = tk.Button(
            self.frame, text = "Info",
            command = self.openInfoWindow
        )
        self.infoButton.grid(row=6, sticky="E", pady=8)

    #takes inputs from <inputtxt> and stores them in <URLs>
    def inputURLs(self):
        input1 = self.inputText.get(1.0, tk.END)
        URLs = input1.split() 
        updateLabel(self, self.statusLabel, "URLs Received!\n")
        DownloadPrompt(self, URLs)
        
    #downloads URLs in list
    def downloadURLs(self, URLs):
        options = {"paths": {'home': self.outDir}, "nocheckcertificate": True}
        ydl = YoutubeDL(options)
        for i in range(len(URLs)):
            updateLabel(self, self.statusLabel, f'Downloading video {str(i + 1)}...\n ({URLs[i]})')
            try:
                ydl.download(URLs[i])
            except:
                updateLabel(self, self.statusLabel, f'Error: {URLs[i]} is not a valid URL')
                time.sleep(2)
        updateLabel(self, self.statusLabel, "Done downloading!\n")

    #uses tkinter's askdirectory dialog to set directory in text box
    def setDirectory(self):
        dir = filedialog.askdirectory()
        self.directoryText.delete("1.0", tk.END)
        self.directoryText.insert(tk.END, dir)

    #updates directory field with directory in text box
    def saveDirectory(self):
        self.outDir = self.directoryText.get(1.0, tk.END)

    def openInfoWindow(self):
        InfoWindow(self)
    
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

#loop!!
root.mainloop()



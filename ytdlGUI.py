#ytdlGUI.py -- Ethan Shieh
#4/13/2022

import tkinter as tk
from tkinter import filedialog
import sys 
import subprocess 
import platform 
from yt_dlp import YoutubeDL


# ======== Environment Check ========

ytdlCall = "yt-dlp"
windows = False

whereami = ""
opsys = platform.system()

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

# ======== Window Construction ========

#updates a label with new text, text
def updateLabel(root, label, text):
    label.configure(text=text)
    root.update()

class DownloadPrompt(tk.Toplevel):
    def __init__(self, master, URLs = []):
        super().__init__(master)

        self.title("Download Confirmation")
        master.eval(f'tk::PlaceWindow {str(self)} center')

        self.URLs = URLs

        # ------- WIDGETS -------
        self.questionLabel = tk.Label(
            self,
            text = "Do you want to download these youtube videos?"
        )
        self.questionLabel.grid(column=0, row=0, sticky="N", columnspan=2)
        self.columnconfigure(0, weight=1)
        
        self.yesButton = tk.Button(
            self,
            text = "Yes",
            command = self.confirm
        )
        self.yesButton.grid(column=0, row=1, sticky="N", padx=50, pady=20)

        self.noButton = tk.Button(
            self,
            text = "No",
            command = self.destroy
        )
        self.noButton.grid(column=1, row=1, sticky="N", padx=50, pady=20)

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
        self.title("ytdlGUI! by molofgarb")
        self.eval('tk::PlaceWindow . center') #puts window in center

        #initialize main frame (located within main window)
        self.frame = tk.Frame(self)
        self.frame.grid(padx=20, pady=20)

        # ------- WIDGETS -------
        #directory to download to
        self.directoryText = tk.Text(
            self.frame,
            height = 1,
            width = 60,
        )
        self.directoryText.insert(tk.END, whereami)
        self.directoryText.grid(column=0, row=0, padx=5, pady=5)

        #button to open directory-choosing prompt
        self.directoryButton = tk.Button(
            self.frame,
            height = 0,
            width = 0,
            text = "...",
            command = self.setDirectory
        )
        self.directoryButton.grid(column=1, row=0, padx=1, pady=1)
        
        #input text box
        self.inputText = tk.Text(
            self.frame,
            height = 5,
            width = 60
        )
        self.inputText.insert(tk.END,
            "https://www.youtube.com/shorts/9p0pdiTOlzw\n" + #get wifi anywhere you go
            "https://www.youtube.com/watch?v=fFxySUC2vPc\n" + #python subprocess
            "https://youtu.be/Y_pbEOem2HU\n" + #vine boom
            "https://youtu.be/jNQXAC9IVRw\n" #me at the zoo
        ) #default text
        self.inputText.grid(column=0, row=1, padx=5, pady=5)
        
        #button to send text box input
        self.inputButton = tk.Button(
            self.frame,
            text = "Download", 
            command = self.inputURLs
        )
        self.inputButton.grid(column=0, row=2, padx=5, pady=5)
        
        # Label!!
        self.statusLabel = tk.Label(
            self.frame,
            text = "I will be overwritten!"
        )
        self.statusLabel.grid(column=0, row=3, padx=5, pady=5)

    #takes inputs from <inputtxt> and stores them in <URLs>
    def inputURLs(self):
        input1 = self.inputText.get(1.0, tk.END)
        URLs = input1.split() 
        for i in range(len(URLs)):
            thisURL = URLs[i].split("/")
            if (thisURL[2] != "youtu.be" and thisURL[2] != "www.youtube.com"):
                raise Exception("Incorrect URL Type")
            else:
                if (thisURL[3] == "shorts"):
                    URLs[i] = thisURL[4]
        updateLabel(self, self.statusLabel, "URLs Received!")
        DownloadPrompt(self, URLs)
        
    #downloads URLs in list
    def downloadURLs(self, URLs):
        options = {"paths": {'home': self.outDir}}
        ydl = YoutubeDL(options)
        for i in range(len(URLs)):
            updateLabel(self, self.statusLabel, "Downloading video " + str(i + 1) + "...")
            ydl.download(URLs[i])
        updateLabel(self, self.statusLabel, "Done downloading!")

    #uses tkinter's askdirectory dialog to set directory in text box
    def setDirectory(self):
        dir = filedialog.askdirectory()
        self.directoryText.delete("1.0", tk.END)
        self.directoryText.insert(tk.END, dir)

    #updates directory field with directory in text box
    def saveDirectory(self):
        self.outDir = self.directoryText.get(1.0, tk.END)

    


def main():
    root = MainWindow()
    root.mainloop()


if __name__ == "__main__":
    main()

#ytdlGUI.py -- Ethan Shieh
#4/13/2022

import tkinter as tk
import sys 
import subprocess 
import platform 
from yt_dlp import YoutubeDL as ytdl


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

# #debug
# print(opsys)

#figure out working directory 
if (opsys == "Windows"):
    whereami = subprocess.check_output(['cd'], shell=True) 
else: #macOS or linux
    whereami = subprocess.check_output(['pwd'], shell=True)

# #make sure yt-dlp/youtube-dl is accessible by the program
# if (subprocess.run([ytdlCall], shell=True, stderr=subprocess.DEVNULL).returncode != 2): #yt-dlp
#         ytdlCall = "youtube-dl"
#         if (subprocess.run([ytdlCall], shell=True, stderr=subprocess.DEVNULL).returncode != 2): #youtube-dl
#             sys.exit("youtube-dl/yt-dlp not found")

# ======== Window Construction ========

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
        self.label1 = tk.Label(
            self,
            text = "Do you want to download these youtube videos?"
        )
        self.label1.grid(column=0, row=0, sticky="N", columnspan=2)
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
        self.master.downloadURLs(self.URLs)     



class MainWindow(tk.Tk):
    def __init__(self):
        #inherit all the stuff from tk.Tk
        super().__init__() 

        #initialize main window
        self.title("ytdlGUI! by molofgarb")
        self.eval('tk::PlaceWindow . center') #puts window in center

        #initialize main frame (located within main window)
        self.frame = tk.Frame(self)
        self.frame.grid(padx=20, pady=20)

        # ------- WIDGETS -------
        #input text box
        self.inputtxt = tk.Text(
            self.frame,
            height = 5,
            width = 50
        )
        self.inputtxt.insert(tk.INSERT,
            "https://www.youtube.com/shorts/9p0pdiTOlzw\n" + #get wifi anywhere you go
            "https://www.youtube.com/watch?v=fFxySUC2vPc\n" + #python subprocess
            "https://youtu.be/Y_pbEOem2HU\n" + #vine boom
            "https://youtu.be/jNQXAC9IVRw\n" #me at the zoo
        ) #default text
        self.inputtxt.grid(column=0, row=0, padx=5, pady=5)
        
        #button to send text box input
        self.inputButton = tk.Button(
            self.frame,
            text = "Download", 
            command = self.inputURLs
        )
        self.inputButton.grid(column=0, row=1, padx=5, pady=5)
        
        # Label!!
        self.label1 = tk.Label(
            self.frame,
            text = "I will be overwritten!"
        )
        self.label1.grid(column=0, row=2, padx=5, pady=5)

    #takes inputs from <inputtxt> and stores them in <URLs>
    def inputURLs(self):
        #receive and process URLs
        self.input1 = self.inputtxt.get(1.0, "end-1c")
        URLs = self.input1.split() 
        # print(URLs)
        for i in range(len(URLs)):
            thisURL = URLs[i].split("/")
            if (thisURL[2] != "youtu.be" and thisURL[2] != "www.youtube.com"):
                raise Exception("Incorrect URL Type")
            else:
                if (thisURL[3] == "shorts"):
                    URLs[i] = thisURL[4]
        updateLabel(self, self.label1, "URLs Received!")
        # print(URLs)
        DownloadPrompt(self, URLs)
        
    #downloads URLs in array
    def downloadURLs(self, URLs):
        for i in range(len(URLs)):
            ytdl().download(URLs[i])
            updateLabel(self, self.label1, "Downloading video " + str(i + 1) + "...")
        updateLabel(self, self.label1, "Done downloading!")


def main():
    root = MainWindow()
    root.mainloop()


if __name__ == "__main__":
    main()

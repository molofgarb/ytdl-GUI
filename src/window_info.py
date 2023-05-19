import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import filedialog

import os
import webbrowser

class InfoWindow(tk.Toplevel):
    def __init__(self, root, style):
        super().__init__(root)

        self.windows = root.data['windows']

        self.style = style
        # style options
        self.styleOptions = [
            ("*font", self.style['mainfont'][0] + " " + self.style['mainfont'][1]),
            ("*background", self.style['bgcolor']),
            ("*foreground", self.style['textcolor']),
            ("*Checkbutton*selectcolor", self.style["checkbuttoncheckcolor"])
        ]
        self.styleOptionsMac = [
            ("*highlightBackground", self.style['bgcolor']), # make background consistent color
            ("*Button*foreground", "black") # since bg is locked white, make text black
        ]

        # apply options
        for option in self.style['styleOptions']: super().option_add(option[0], option[1])
        if root.data['OS'] == "Darwin":
            for option in self.style['styleOptionsMac']: super().option_add(option[0], option[1])

        super().configure( #style for entire window background
            background=self.style["bgcolor"]
        )

        self.title("Info")
        # self.iconbitmap(root.data['iconPath'])
        root.eval(f'tk::PlaceWindow {str(self)} center')

        self.frame = tk.Frame(self)
        self.frame.grid(row=0, padx=20, pady=10)

        self.name = tk.Label(
            self.frame, text="ytdl-GUI by molofgarb",
        )
        self.name.grid(row=0, sticky="w", padx=(10, 0), pady=2)

        self.readmeButton = tk.Button(
            self.frame, text="Open Readme",
            command=lambda: webbrowser.open("README.html")
        )
        self.readmeButton.grid(row=1, sticky="w", padx=(10, 0), pady=5)

        self.sitesButton = tk.Button(
            self.frame, text="Supported Websites",
            command=lambda: webbrowser.open("supportedsites.html")
        )
        self.sitesButton.grid(row=2, sticky='w', padx=(10, 0), pady=5)

        self.thanksLabel = tk.Label(
            self.frame, text="\nThank you for using ytdl-GUI!",
        )
        self.thanksLabel.grid(row=3, sticky='w')

        self.repoLabel = tk.Label(
            self.frame, text="\nytdl-GUI GitHub:",
        )
        self.repoLabel.grid(row=4, sticky="W")

        self.repoLink = tk.Label(
            self.frame, text="https://github.com/molofgarb/ytdl-GUI",
            cursor="hand2", foreground="#007bff", font="Verdana 11 underline"
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
            cursor="hand2", foreground="#007bff", font="Verdana 11 underline"
        )
        self.ytdlpRepoLink.grid(row=7, sticky="W")
        self.ytdlpRepoLink.bind(
            "<Button-1>", lambda e: webbrowser.open_new_tab("https://github.com/yt-dlp/yt-dlp")
        )

        # =========== DEBUG ===========
        self.debugLabel = tk.Label(
            self.frame, text="Debug Functions:",
        )
        self.debugLabel.grid(row=0, column=1, sticky='w', padx=(20, 10))
        #adds sample videos
        self.sampleButton = tk.Button(
            self.frame, text = "Add sample videos",
            command = root.addSampleVideos
        )
        self.sampleButton.grid(row=1, column=1, sticky='w', padx=(20, 10), pady=5)

        #adds sample videos
        self.removeSampleButton = tk.Button(
            self.frame, text = "Delete Sample Videos",
            command = self.removeSampleVideos
        )
        self.removeSampleButton.grid(row=2, column=1, sticky='w', padx=(20, 10), pady=5)

    def removeSampleVideos(self):
        cmd = 'del' if (self.windows) else 'rm'
        sampleVideos = [
            '"(subprocess) solved! FileNotFoundError - [WinError 2] The system cannot find the file specified [fFxySUC2vPc].mp4"',
            '"Dramatic Sable [BDqOmwM].mp4"',
            '"get wifi anywhere you go vine ad scam [9p0pdiTOlzw].mp4"',
            '"Me at the zoo [jNQXAC9IVRw].mp4"',
            '"Vine Boom Sound Effect [Y_pbEOem2HU].mp4"'
            '"https://youtu.be/f1A7SdVTlok"'
        ]
        for x in sampleVideos:
            os.system(cmd + ' ' + x)
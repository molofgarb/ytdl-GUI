import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import filedialog

import os

from tk_common import updateText

class ConfirmPrompt(tk.Toplevel):
    def __init__(self, root, data, style, promptText, filenames=None):
        super().__init__(root)

        self.data = data
        self.style = style

        super().configure( #style for entire window background
            background=self.style["bgcolor"]
        )

        self.promptText = promptText
        self.filenames = filenames #LEFT OFF

        if self.promptText == "Do you want to delete the already downloaded files?":
            self.title("Delete Confirmation")
        elif promptText.startswith("Error"):
            self.title("Error")
        else:
            self.title("Title")

        self.iconbitmap(root.data['iconPath'])
        root.eval(f'tk::PlaceWindow {str(self)} center')

        self.frame = tk.Frame(self, background=self.style["bgcolor"])
        self.frame.grid(row=0, padx=2, pady=10)

        # ------- WIDGETS -------
        self.questionLabel = tk.Label(
            self.frame, text = promptText,
            background=self.style["bgcolor"], foreground=self.style["textcolor"], font=self.style['mainfont']
        )
        self.questionLabel.grid(sticky="N", columnspan=1 if promptText.startswith("Error") else 2, padx=15)

        self.yesButton = tk.Button(
            self.frame, text="Yes",
            width=6,
            background=self.style["buttoncolor"], foreground=self.style["textcolor"], font=self.style['mainfont'],
            command=lambda: self.answer(True)
        )
        self.noButton = tk.Button( #No/Ok
            self.frame, text = "Ok",
            width=6, 
            background=self.style["buttoncolor"], foreground=self.style["textcolor"], font=self.style['mainfont'],
            command=lambda: self.answer(False)
        )

        if promptText.startswith("Error"): #error prompt (ok)
            self.noButton.grid(column=0, row=1, sticky="N", padx=30, pady=20)
            if root.playSound.get(): self.bell() #sound
        else: #if confirm prompt (yes/no)
            updateText(self, self.noButton, "No")
            self.yesButton.grid(row=1, sticky="N", padx=30, pady=20)
            self.noButton.grid(column=1, row=1, sticky="N", padx=30, pady=20)


    def answer(self, action):
        self.update()
        if self.data["debug"]: print(self.filenames, self.data['path'])
        if action: #delete prompt
            if self.promptText == "Do you want to delete the already downloaded files?":
                # print(self.filenames)
                cmd = 'del' if (self.data['windows']) else 'rm'
                for filename in self.filenames:
                        os.system(cmd + ' ' + filename)
        self.destroy()
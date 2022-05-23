import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import filedialog

import os

from tk_common import updateText

class ConfirmPrompt(tk.Toplevel):
    def __init__(self, root, promptText):
        super().__init__(root)
        self.promptText = promptText

        if self.promptText == "Do you want to delete the already downloaded files?":
            self.title("Delete Confirmation")
        elif promptText.startswith("Error"):
            self.title("Error")
        else:
            self.title("Title")

        self.iconbitmap(root.data['iconPath'])
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

        if promptText.startswith("Error"): #error prompt (ok)
            self.noButton.grid(column=0, row=1, sticky="N", padx=30, pady=20)
            if root.playSound.get(): self.bell() #sound
        else: #if confirm prompt (yes/no)
            self.questionLabel.configure(columnspan=2)
            updateText(self, self.noButton, "No")
            self.yesButton.grid(row=1, sticky="N", padx=30, pady=20)
            self.noButton.grid(column=1, row=1, sticky="N", padx=30, pady=20)

    def answer(self, action):
        self.destroy()
        self.update()
        if action:
            #delete prompt
            if self.promptText == "Do you want to delete the already downloaded files?":
                print(self.data)
                for filename in self.data:
                    print("d\n")
                    cmd = 'del' if (self.root.data['windows']) else 'rm'
                    os.system(cmd + ' "' + filename + '"')
import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter import filedialog

import os

from common_tk import updateText

class ConfirmPrompt(tk.Toplevel):
    def __init__(self, root, promptText: str):
        super().__init__(root)
    
        self.style = root.style

        # apply options
        for option in self.style['styleOptions']: super().option_add(option[0], option[1])
        if root.data['OS'] == "Darwin":
            for option in self.style['styleOptionsMac']: super().option_add(option[0], option[1])

        super().configure( #style for entire window background
            background=self.style["bgcolor"]
        )

        self.filenames = root.filenames
        self.data = root.data
        self.promptText = promptText

        if self.promptText == "Do you want to delete the already downloaded files?":
            self.title("Delete Confirmation")
        elif promptText.startswith("Error"):
            self.title("Error")
        else:
            self.title("<title>")

        # self.iconbitmap(root.data['iconPath'])
        root.eval(f'tk::PlaceWindow {str(self)} center')

        self.frame = tk.Frame(self, background=self.style["bgcolor"])
        self.frame.grid(row=0, padx=2, pady=10)

        # ------- WIDGETS -------
        self.questionLabel = tk.Label(
            self.frame, text = promptText,
        )
        self.questionLabel.grid(sticky="N", columnspan=1 if promptText.startswith("Error") else 2, padx=15)

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
            if root.isPlaySound.get(): self.bell() #sound
        else: #if confirm prompt (yes/no)
            updateText(self, self.noButton, "No")
            self.yesButton.grid(row=1, sticky="N", padx=30, pady=20)
            self.noButton.grid(column=1, row=1, sticky="N", padx=30, pady=20)


    def answer(self, action: bool) -> None:
        self.update()

        if self.data["debug"]: print(self.filenames, "\n", self.data['path'], "<ConfirmPrompt answer()>")
        if action: # do something prompt (used in delete prompt)
            if self.promptText == "Do you want to delete the already downloaded files?": # delete prompt
                for filename in self.filenames: 
                    try:
                        os.remove(filename)
                    except Exception as ex1:
                        try:
                            os.remove(filename + ".part")
                        except Exception as ex2:
                            continue
            elif ...:
                ...

        self.destroy()
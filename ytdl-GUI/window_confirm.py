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

        isError = promptText.startswith("Error")
        isInfo = promptText.startswith("Info")

        if self.promptText == "Do you want to delete the already downloaded files?":
            self.title("Delete Confirmation")
        elif isError:
            self.title("Error")
        elif isInfo:
            self.title("Info")
        else:
            self.title("<title>")

        # self.iconbitmap(root.data['iconPath'])
        root.eval(f'tk::PlaceWindow {str(self)} center')

        self.frame = tk.Frame(self, background=self.style["bgcolor"])
        self.frame.grid(row=0, padx=2, pady=10)

        # ------- WIDGETS -------
        self.questionLabel = tk.Label(
            self.frame, text = promptText, justify=('left' if isInfo else 0)
        )
        self.questionLabel.grid(sticky='n',
                columnspan=(1 if isError or isInfo else 2), 
                padx=15, 
        )

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

        if isError or isInfo: #error prompt (ok)
            self.noButton.grid(column=0, row=1, sticky="N", padx=30, pady=20)
            if isError and root.isPlaySound.get(): self.bell() #sound
        else: #if confirm prompt (yes/no)
            updateText(self, self.noButton, "No")
            self.yesButton.grid(row=1, sticky="N", padx=30, pady=20)
            self.noButton.grid(column=1, row=1, sticky="N", padx=30, pady=20)

    # called when Yes, No, Ok answers selected in prompt to perform the answer to the question
    # currently, the only action is to delete downloaded files
    # closes itself once it receives an answer
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

        self.destroy()
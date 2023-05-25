# updates a label with new text, text
# root is any tkinter window
# widget is any tkinter widget
def updateText(root, widget, text: str) -> None:
    widget.configure(text=text)
    root.update()
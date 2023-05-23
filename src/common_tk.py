#updates a label with new text, text
def updateText(root, widget, text: str) -> None:
    widget.configure(text=text)
    root.update()
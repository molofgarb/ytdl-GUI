#updates a label with new text, text
def updateText(root, widget, text):
    widget.configure(text=text)
    root.update()
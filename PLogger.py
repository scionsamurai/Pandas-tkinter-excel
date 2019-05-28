import tkinter as tk
import sys

class PrintLogger(): # create file like object
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        try:
            self.textbox.insert(tk.END, text) # write text to textbox
        except:
            pass
            # could also scroll to end of textbox here to make sure always visible

    def flush(self): # needed for file like object
        pass
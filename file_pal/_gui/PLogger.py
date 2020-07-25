import tkinter as tk
import sys

class PrintLogger(): # create file like object
    def __init__(self, textbox): # pass reference to text widget
        self.textbox = textbox # keep ref

    def write(self, text):
        try:
            self.textbox.insert(tk.END, text) # write text to textbox
            self.textbox.see(tk.END)
        except:
            pass

    def flush(self): # needed for file like object
        pass

from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT, Toplevel, IntVar
from tkinter.ttk import Frame, Label, Entry, Button, Checkbutton
class SortPopup:
    def __init__(self):
        super().__init__()
        self.output1 = ""
        self.save = False
        self.initUI()

    def initUI(self):
        self.new_win = Toplevel()
        self.new_win.title("Sort Option")

        frame1 = Frame(self.new_win)
        frame1.pack(fill=X)

        lbl2 = Label(frame1, text="Column(s) to sort?")
        lbl2.pack(side=LEFT, padx=5, pady=10)

        frame2 = Frame(self.new_win)
        frame2.pack(fill=X)

        self.entry1 = Entry(frame2, textvariable=self.output1)
        self.entry1.pack(fill=X, padx=5, expand=True)

        frame3 = Frame(self.new_win)
        frame3.pack(fill=X)

        self.save_var = IntVar()
        self.save_var.set(1)
        Checkbutton(frame3, text="Save until unchecked?", variable=self.save_var).pack()

        frame4 = Frame(self.new_win)
        frame4.pack(fill=X)

        btn = Button(frame4, text="Submit", command=(lambda e=self.entry1: self.onSubmit(e, self.save_var.get())))
        btn.pack(padx=5, pady=10)

        self.new_win.wait_window()

    def onSubmit(self, ent, save):
        self.output1 = ent.get()
        self.save = save
        self.new_win.destroy()
        return self.output1, save
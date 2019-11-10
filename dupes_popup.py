from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT, RIGHT, Toplevel, IntVar
from tkinter.ttk import Frame, Label, Entry, Button, Checkbutton
from functools import partial
class DupesPopup:
    def __init__(self):
        super().__init__()
        # self allow the variable to be used anywhere in the class
        self.output1 = ""
        self.output2 = ""
        self.save = False
        self.initUI()

    def initUI(self):
        self.new_win = Toplevel()
        self.new_win.title("Remove Duplicates")

        frame1 = Frame(self.new_win)
        frame1.pack(fill=X)

        lbl2 = Label(frame1, text="Column(s) to check for duplicates?")
        lbl2.pack(side=LEFT, padx=5, pady=10)

        frame2 = Frame(self.new_win)
        frame2.pack(fill=X)

        self.entry1 = Entry(frame2, textvariable=self.output1)
        self.entry1.pack(fill=X, padx=5, expand=True)

        lbl1 = Label(frame2, text=" Keep :")
        lbl1.pack(side=LEFT, pady=10)

        self.first_var = IntVar()
        last_var = IntVar()
        self.first_var.set(1)
        last_var.set(0)
        Checkbutton(frame2, text="First occurrence",variable=self.first_var).pack()
        Checkbutton(frame2, text="Last occurrence",variable=last_var).pack()
        self.first_var.trace("w", partial(self.changed, first=self.first_var, last=last_var))
        last_var.trace("w", partial(self.changed, first=self.first_var, last=last_var, func=1))

        frame3 = Frame(self.new_win)
        frame3.pack(fill=X)

        # Command tells the form what to do when the button is clicked
        btn = Button(frame3, text="Submit", command=(lambda e=self.entry1: self.onSubmit(e, self.first_var, self.save_var.get())))
        btn.pack(padx=5, pady=10)

        frame4 = Frame(self.new_win)
        frame4.pack(fill=X)

        self.save_var = IntVar()
        self.save_var.set(1)
        Checkbutton(frame4, text="Save until unchecked?", variable=self.save_var).pack()
        self.new_win.wait_window()

    def changed(self,*args, first=None, last=None, func=0):
        if func ==0:
            if first.get() == 1:
                last.set(0)
            else:
                last.set(1)
        else:
            if last.get() == 1:
                first.set(0)
            else:
                first.set(1)

    def onSubmit(self,ent,first_v, save):
        self.output1 = ent.get()
        if first_v.get():
            first_last = "first"
        else:
            first_last = "last"
        self.output2 = first_last
        self.save = save
        self.new_win.destroy()
        return self.output1, self.output2, save

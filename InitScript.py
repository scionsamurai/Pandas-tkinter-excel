#!/usr/bin/python3
from tkinter import *
from tkinter import filedialog
import os, warnings, tables
import pandas as pd
from RetrieveInput import Retrieve_Input
from Open_File import OpenFile
from Make_Forms import MakeForm
warnings.filterwarnings("error")

my_filetypes = [('all files', '.*'), ('CSV files', '.csv')]
fields = 'Header To Search', '  Search Item(s)', 'Output Directory'
li = []
li_dict = {}
answer = []
LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

def fetch(entries):
   for entry in entries:
      field = entry#columns.values
      text  = entry[1].get()#.columns.values
      #print(list(filter(bool, (entry[1].get()).splitlines())))
      #print(Split_Entry.split(entry[1].get()))
      #new_list =list(filter(bool, (entry[1].get()).splitlines()))
      #print(new_list)
      print('%s: "%s"' % (field, text))

def intro_dialog(tkThang):
   answer = filedialog.askopenfilenames(parent=tkThang,
                                        initialdir=os.getcwd(),
                                        title="Please select one or more files:",
                                        filetypes=my_filetypes)
   return answer

def popupmsg(msg):
   popup = Tk()
   popup.wm_title("!")
   label = Label(popup, text=msg, font=NORM_FONT)
   label.pack(side="top", fill="x", pady=10)
   B1 = Button(popup, text="Okay", command=popup.destroy)
   B1.pack()
   popup.mainloop()

def df_to_hdf():
   combined_frames = pd.concat(li, axis=0, sort=False, ignore_index=True)
   combined_frames.to_hdf('data.h5', key='df', mode='w')
   print('saved')


if __name__ == '__main__':
   root = Tk()
   root.title(".csvDB 1.0")
   #root.iconbitmap(r'C:\Users\SsDamurai\Desktop\newP.ico')
   search_files = []
   global auto_open_box, ents
   answer.extend(intro_dialog(root))
   #print(answer)
   answer = list(filter(bool, answer))
   #print(answer)
   form1 = MakeForm()
   ents = form1.make(root, fields,1)
   form2= MakeForm(data_frames=li,frame_keys=li_dict, input_box1=ents[0][1],input_box2=ents[1][1])
   ents2 = form2.make(root, answer,2)
   opt_form = MakeForm()
   inp = Retrieve_Input()

   for i in answer:
      li.append(OpenFile.open_file(i))
      li_dict[i] = (len(li) - 1)

   root.bind('<Return>', (lambda event, e=ents: inp.row_frames(e, ents2, li, auto_open_box, 'xlsx')))
   #b1 = Button(root, text='Show', command=(lambda e=ents: fetch(ents)))
   #b1.pack(side=LEFT, padx=5, pady=5)
   b2 = Button(root, text='Quit', command=root.quit)
   b2.pack(side=RIGHT, padx=5, pady=5)
   #print(li[0].columns.values)
   auto_open_box = IntVar()
   open_var = Checkbutton(root, text='Auto Open?', variable=auto_open_box)
   open_var.pack(side=RIGHT)
   b3 = Button(root, text='Output Options',
               command=(lambda e=ents: opt_form.make(func=5)))
   b3.pack(side=RIGHT, padx=5, pady=5)
   b4 = Button(root, text='Search Criteria',
               command=(lambda e=ents: inp.row_frames(e, ents2, li, auto_open_box, 'xlsx')))
   b4.pack(side=LEFT, padx=5, pady=5)
   b5 = Button(root, text='Save HDF File(s)',
               command=(lambda e='no value': df_to_hdf()))
   b5.pack(side=LEFT, padx=5, pady=5)
   root.mainloop()

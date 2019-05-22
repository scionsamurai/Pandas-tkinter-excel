from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os, warnings, tables, shelve
import pandas as pd
from RetrieveInput import Retrieve_Input
from Open_File import OpenFile
from Make_Forms import MakeForm
warnings.filterwarnings("error")
warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning)

my_filetypes = [('all files', '.*'), ('CSV files', '.csv')]
output_filetypes = [('HD5', '.h5'), ('CSV files', '.csv')]
fields = 'Header To Search', '  Search Item(s)'#, 'Output Directory'
li = []
li_dict = {}
answer = []
LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

def fetch(entries):
   save_var = messagebox.askokcancel("Title", "Do you want to save?")
   print(save_var)
   for entry in entries:
      field = entry#columns.values
      text  = entry[1].get()#.columns.values

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
   new_output = []
   answer = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                         title="Please select save location and name:",
                                         filetypes=output_filetypes,
                                         defaultextension='.h5')

   for i in range(0, len(li)):
      new_output.append(li[i])
   new_new_output = pd.concat(new_output, axis=0, sort=False, ignore_index=True)
   if answer[-3:] == '.h5':
      new_new_output.to_hdf(answer, key='df', mode='w')
   elif answer[-4:] == '.csv':
      new_new_output.to_csv(answer, index=False)
   print('saved')

def donothing():
    x=0
    return x

def close_files(root):
    global answer, footer, ents2, li, li_dict
    close_var = messagebox.askyesno(".csvDB 1.1", "Do you want to close checked files?")
    if close_var == True:
        for file in answer[::-1]:
            if ents2[li_dict[file]][2].get() == 1:
                del li[li_dict[file]]
                del li_dict[file]
                answer.remove(file)
        for file in answer:
            li_dict[file] = answer.index(file)
        footer.pack_forget()
        footer.destroy()
        footer = Frame(root)
        ents2 = form2.make(footer, answer, 2)
        footer.pack()

def open_more(root):
    global answer, footer, ents2
    loc_answer = []
    loc_answer.extend(intro_dialog(root))
    loc_answer = list(filter(bool, loc_answer))
    footer.pack_forget()
    footer.destroy()
    footer = Frame(root)
    for file in loc_answer:
        if file not in answer:
            answer.append(file)
            li.append(OpenFile.open_file(file))
            li_dict[file] = (len(li) - 1)
    ents2 = form2.make(footer, answer, 2)
    footer.pack()

def resort():
    global answer, footer, ents2
    footer.pack_forget()
    footer.destroy()
    footer = Frame(root)
    ents3 = form2.make(footer, answer, 6)
    b1 = Button(footer, text='Save Order', command=(lambda e=root: resort_p2(ents3)))
    b1.pack(side=RIGHT, padx=5, pady=5)
    footer.pack()

def resort_p2(ents3):
    global answer, footer, ents2, li, form2
    temp_list = []
    for i in ents3:
        temp_list.append((i[0],i[1].get()))
    temp_list.sort(key= sortSecond)

    temp2_list = []
    for i in temp_list:
        temp2_list.append(i[0])
    temp_li = []
    for file in temp2_list:
        temp_li.append(li[li_dict[file]])
    li = temp_li
    answer = temp2_list
    form2.li_dict = li_dict
    form2.li = li
    for file in answer:
        li_dict[file] = answer.index(file)

    footer.pack_forget()
    footer.destroy()
    footer = Frame(root)
    ents2 = form2.make(footer, answer, 2)
    footer.pack()

def sortSecond(val):
    return val[1]

def open_opt_button(opt_form):
    Cust_files = opt_form.make(func=7)

def  passive_open_file():
    global answer, footer, ents2
    var_file = shelve.open('var_file')
    try:
        for gen_set in var_file['opt_gen_rules']:
            if gen_set[0] == 'Delimiter':
                if gen_set[1] == 'DV' or gen_set[1] == '':
                    delimiter = ','
                else:
                    delimiter = gen_set[1]
            elif gen_set[0] == 'Terminator':
                if gen_set[1] == 'DV' or gen_set[1] == '':
                    terminator = None
                else:
                    terminator = gen_set[1]
            elif gen_set[0] == 'Header Line':
                if gen_set[1] == 'DV' or gen_set[1] == '':
                    header_line = 0
                else:
                    header_line = int(gen_set[1])
            elif gen_set[0] == 'Index Column':
                if gen_set[1] == 'DV' or gen_set[1] == '':
                    index_col = None
                else:
                    index_col = int(gen_set[1])
            elif gen_set[0] == 'Chunk':
                if gen_set[1] == 'DV' or gen_set[1] == '':
                    chunk = None
                else:
                    chunk = int(gen_set[1])
            elif gen_set[0] == 'Verbose':
                if gen_set[1] == 'DV' or gen_set[1] == '':
                    verbose = True
                else:
                    verbose = gen_set[1]
    except KeyError:
        delimiter = ','
        terminator = None
        header_line = 0
        index_col = None
        chunk = None
        verbose = True
    try:
        only_cols =  var_file['spec_col_rules']
    except KeyError:
        only_cols = None
    try:
        dtypes =  var_file['col_dtypes']
        for key, value in dtypes.items():
            if value == 'Text':
                dtypes[key] = str
            elif value == 'Number':
                dtypes[key] = float
    except KeyError:
        dtypes = None

    files_answer = filedialog.askopenfilenames(parent=footer,
                                         initialdir=os.getcwd(),
                                         title="Please select one or more files:",
                                         filetypes=my_filetypes)
    footer.pack_forget()
    footer.destroy()
    footer = Frame(root)
    for file in files_answer:
        if file not in answer:
            answer.append(file)
            li.append(OpenFile.open_file(file, delimiter, header_line, index_col, chunk, verbose,
                                         terminator, only_cols, dtypes))
            li_dict[file] = (len(li) - 1)
    ents2 = form2.make(footer, answer, 2)
    footer.pack()
    var_file.close()

if __name__ == '__main__':
   root = Tk()
   root.title(".csvDB 1.1")
   root.iconbitmap(r'C:\Users\SsDamurai\Desktop\newP.ico')
   global auto_open_box, ents, footer, form2

   header = Frame(root)
   body = Frame(root)
   footer = Frame(root)
   row = Frame(root)

   answer.extend(intro_dialog(root))
   answer = list(filter(bool, answer))

   form1 = MakeForm()
   ents = form1.make(header, fields,1)
   header.pack()
   form2= MakeForm(data_frames=li,frame_keys=li_dict, input_box1=ents[0][1],input_box2=ents[1][1])
   ents2 = form2.make(footer, answer,2)
   opt_form = MakeForm(pass_func=passive_open_file)
   body.pack()


   menubar = Menu(root)
   filemenu = Menu(menubar, tearoff=0)
   submenu = Menu(root)
   subsubmenu = Menu(root)
   submenu.add_command(label="Full/Default", command=(lambda e='no value': open_more(root)))
   subsubmenu.add_command(label="Change Settings", command=(lambda e=ents: open_opt_button(opt_form)))
   subsubmenu.add_command(label="Select File", command=(lambda e=ents: passive_open_file()))
   submenu.add_cascade(label="CSV Custom", menu=subsubmenu)
   filemenu.add_command(label="Save HDF File", command=(lambda e='no value': df_to_hdf()))
   filemenu.add_cascade(label="Open", menu=submenu)
   filemenu.add_command(label="Output Options", command=(lambda e=ents: opt_form.make(func=5)))
   filemenu.add_command(label="Close Selected", command=(lambda e=ents2: close_files(root)))
   filemenu.add_separator()
   filemenu.add_command(label="Exit", command=root.quit)
   menubar.add_cascade(label="File", menu=filemenu)

   helpmenu = Menu(menubar, tearoff=0)
   helpmenu.add_command(label="License", command=donothing())
   helpmenu.add_command(label="Fetch", command=(lambda e=ents: fetch(ents)))
   menubar.add_cascade(label="Help", menu=helpmenu)

   root.config(menu=menubar)

   opt_form = MakeForm()
   inp = Retrieve_Input()

   for i in answer:
      li.append(OpenFile.open_file(i))
      li_dict[i] = (len(li) - 1)

   root.bind('<Return>', (lambda event, e=ents: inp.row_frames(e, ents2, li, auto_open_box, 'xlsx')))
   b4 = Button(body, text='Search',
               command=(lambda e=ents: inp.row_frames(e, ents2, li, auto_open_box, 'xlsx')))
   b4.pack(side=LEFT, padx=5, pady=5)
   auto_open_box = IntVar()
   open_var = Checkbutton(body, text='Auto Open', variable=auto_open_box)
   open_var.pack(side=LEFT)
   b5 = Button(body, text='Sort Files',
               command=(lambda e=root: resort()))
   b5.pack(side=RIGHT, padx=5, pady=5)
   footer.pack()
   root.mainloop()

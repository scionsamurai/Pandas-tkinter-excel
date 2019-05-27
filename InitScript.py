from tkinter import *
from tkinter import messagebox
import multiprocessing
from multiprocessing import Pool
from tkinter import filedialog, simpledialog
import os, warnings, tables, shelve
import pandas as pd
from RetrieveInput import Retrieve_Input
from functools import partial
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

def fetch():
   #save_var = messagebox.askokcancel("Title", "Do you want to save?")
   #print(save_var)
   new_list = ''
   for item in answer:
      if answer.index(item) != len(answer):
         new_list += item+'\n'
      else:
          new_list += item
   popupmsg(new_list)
   """
   item_list = simpledialog.askstring("Input", "What value(s) would you like to search?", parent=root)
   search_header = simpledialog.askstring("Input", "Under what Header are we searching the value(s)?", parent=root)

   directory = filedialog.askdirectory(parent=root,
                                        initialdir=os.getcwd(),
                                        title="Please select Directory:")
"""
   #print(answer)
   #print(li_dict)
   #for entry in entries:
   #   field = entry#columns.values
   #   text  = entry[1].get()#.columns.values


def changed(*args, widget=None):
    global header, footer, ents, ents2, form1, form2
    header.pack_forget()
    header.destroy()
    footer.pack_forget()
    footer.destroy()
    header = Frame(root)
    footer = Frame(root)
    if widget.get() > 1:
        ents4 = form1.make(header, widget.get(), 11)
    else:
        ents = form1.make(header, fields, 1)
    ents2 = form2.make(footer, answer, 2)
    #input_box1 = ents[0][1], input_box2 = ents[1][1]
    form2.ents1 = ents[0][1]
    form2.ents2 = ents[1][1]
    header.pack()
    footer.pack()

def intro_dialog(tkThang):
   answer = filedialog.askopenfilenames(parent=tkThang,
                                        initialdir=os.getcwd(),
                                        title="Please select one or more files:",
                                        filetypes=my_filetypes)
   return answer

def popupmsg(msg):
   popup = Toplevel()
   popup.title("!")
   label = Label(popup, text=msg, font=NORM_FONT)
   label.pack(side="top", fill="x", pady=10)
   B1 = Button(popup, text="Okay", command=popup.destroy)
   B1.pack()
   popup.mainloop()

def df_to_hdf():
   global ents2
   new_output = []
   answer = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                         title="Please select save location and name:",
                                         filetypes=output_filetypes,
                                         defaultextension='.h5')

   for i in range(0, len(li)):
      if ents2[i][2].get() == 1:
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
    close_var = messagebox.askyesno("File Snipper 1.0", "Do you want to close checked files?")
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

def read_csv(filename):
    new_only_col = []
    var_file = shelve.open('var_file')
    try:
        for gen_set in var_file['opt_gen_rules']:
            if gen_set[0] == 'Header Line':
                if gen_set[1] == 'DV' or gen_set[1] == '':
                    header_line = 0
                else:
                    header_line = int(gen_set[1])
            elif gen_set[0] == 'Index Column':
                if gen_set[1] == 'DV' or gen_set[1] == '':
                    index_col = None
                else:
                    index_col = int(gen_set[1])
            elif gen_set[0] == 'Verbose':
                if gen_set[1] == 0:
                    verbose = False
                else:
                    verbose = True
    except KeyError:
        header_line = 0
        index_col = None
        verbose = False
    try:
        only_cols = var_file['spec_col_rules']
    except KeyError:
        only_cols = None
    try:
        dtypes = var_file['col_dtypes']
        for key, value in dtypes.items():
            if value == 'Text':
                dtypes[key] = str
            elif value == 'Number':
                dtypes[key] = float
    except KeyError:
        dtypes = None
    try:
        return (pd.read_excel(filename, sheet_name=0, header=header_line, index_col=index_col,
                             usecols=only_cols, dtype=dtypes, verbose=verbose), (filename))
    except PermissionError as e:
        print(e)

def main(file_list):
    pool = Pool(processes=4)
    new_list = []
    for x in file_list:
        if x not in answer:
            new_list.append(x)
    df_list = pool.map(read_csv, new_list)
    for i in range(len(new_list)):
        li.append(df_list[i][0])
        answer.append(df_list[i][1])
        li_dict[df_list[i][1]] = (len(li) - 1)

def all_in_dir(root, func=0):
    global answer, header, footer, ents, ents2
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
                if gen_set[1] == 0:
                    verbose = False
                else:
                    verbose = True
    except KeyError:
        delimiter = ','
        terminator = None
        header_line = 0
        index_col = None
        chunk = None
        verbose = False
    try:
        only_cols = var_file['spec_col_rules']
    except KeyError:
        only_cols = None
    try:
        dtypes = var_file['col_dtypes']
        for key, value in dtypes.items():
            if value == 'Text':
                dtypes[key] = str
            elif value == 'Number':
                dtypes[key] = float
    except KeyError:
        dtypes = None

    loc_answer = []
    excel_files = []
    check_name_temp = messagebox.askyesno("File Snipper 1.0", "Do you want to specify the first characters?")
    if check_name_temp == True:
        name_str = simpledialog.askstring("File Snipper 1.0",
                                           "First part of name for the files you want to open?",
                                           parent=root)
    if func == 1:
        directory = filedialog.askdirectory(parent=root,
                                            initialdir=os.getcwd(),
                                            title="Please select Directory:")
        for path, subdirs, files in os.walk(directory):
            for name in files:
                if check_name_temp == True:
                    if name[:len(name_str)] == name_str:
                        if ((name[-4:])[:3] == 'xls') or (name[-4:] == '.xls'):
                            if name[:2] != '~$':
                                excel_files.append((path + '/' + name))
                        elif (name[-4:] == '.csv') or (name[-3:] == '.h5'):
                            loc_answer.append((path + '/' + name))
                else:
                    if ((name[-4:])[:3] == 'xls') or (name[-4:] == '.xls'):
                        if name[:2] != '~$':
                            excel_files.append((path + '/' + name))
                    elif (name[-4:] == '.csv') or (name[-3:] == '.h5'):
                        loc_answer.append((path + '/' + name))
        main(excel_files)
    else:
        loc_answer.extend(intro_dialog(root))
    loc_answer = list(filter(bool, loc_answer))
    footer.pack_forget()
    footer.destroy()
    footer = Frame(root)
    del_list = []
    for file in loc_answer:
        if file not in answer:
            try:
                dataframe = OpenFile.open_file(file, delimiter, header_line, index_col, chunk, verbose,
                                               terminator, only_cols, dtypes)
                if dataframe.empty != True:
                    li.append(dataframe)
                    answer.append(file)
                    li_dict[file] = (len(li) - 1)
                else:
                    temp_f = file.split('/')
                    new_f = temp_f[(len(temp_f) - 1)]
                    del_list.append(new_f)
            except PermissionError as e:
                print(e)
    for i in del_list:
        print('Failed to Open :' + i)
    ents2 = form2.make(footer, answer, 2)
    footer.pack()
    var_file.close()

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
    global answer, header, footer, ents, ents2
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
                if gen_set[1] == 0:
                    verbose = False
                else:
                    verbose = True
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
    del_list = []
    for file in files_answer:
        if file not in answer:
            dataframe = OpenFile.open_file(file, delimiter, header_line, index_col, chunk, verbose,
                                             terminator, only_cols, dtypes)
            if dataframe.empty != True:
                li.append(dataframe)
                answer.append(file)
                li_dict[file] = (len(li) - 1)
            else:
                temp_f = file.split('/')
                new_f = temp_f[(len(temp_f) - 1)]
                del_list.append(new_f)
    for i in del_list:
        print('Failed to Open :' + i)

    ents2 = form2.make(footer, answer, 2)
    footer.pack()
    var_file.close()

if __name__ == '__main__':
   multiprocessing.freeze_support()
   root = Tk()
   root.title("File Snipper 1.0")
   #root.iconbitmap(r'C:\Users\SsDamurai\Desktop\newP.ico')
   global auto_open_box, ents,header, body, footer, form1, form2

   header = Frame(root)
   body = Frame(root)
   row = Frame(root)
   footer = Frame(root)

   #answer.extend(intro_dialog(root))
   #answer = list(filter(bool, answer))
   answer = []
   opt_form = MakeForm()
   inp = Retrieve_Input()

   del_list = []
   for i in answer:
      dataframe = OpenFile.open_file(i)
      if dataframe.empty != True:
         li.append(dataframe)
         li_dict[i] = (len(li) - 1)
      else:
         ind = answer.index(i)
         del_list.append(ind)
   for i in del_list[::-1]:
       temp_f = answer[i].split('/')
       new_f = temp_f[(len(temp_f) - 1)]
       print('Failed to Open :' + new_f)
       del answer[i]

   form1 = MakeForm()
   ents = form1.make(header, fields,1)


   form2= MakeForm(data_frames=li,frame_keys=li_dict, input_box1=ents[0][1],input_box2=ents[1][1])
   ents2 = form2.make(footer, answer,2)
   opt_form = MakeForm(pass_func=passive_open_file)



   menubar = Menu(root)
   filemenu = Menu(menubar, tearoff=0)
   submenu = Menu(root, tearoff=0)
   submenu.add_command(label="Input Options", command=(lambda e=ents: open_opt_button(opt_form)))
   submenu.add_command(label="Select File", command=(lambda e=ents: passive_open_file()))
   submenu.add_command(label="All in Dir", command=(lambda e='no value': all_in_dir(root,1)))
   filemenu.add_command(label="Save Selected", command=(lambda e='no value': df_to_hdf()))
   filemenu.add_cascade(label="Open", menu=submenu)
   filemenu.add_command(label="Output Options", command=(lambda e=ents: opt_form.make(func=5)))
   filemenu.add_command(label="Close Selected", command=(lambda e=ents2: close_files(root)))
   filemenu.add_separator()
   filemenu.add_command(label="Exit", command=root.quit)
   menubar.add_cascade(label="File", menu=filemenu)

   helpmenu = Menu(menubar, tearoff=0)
   helpmenu.add_command(label="License", command=donothing())
   helpmenu.add_command(label="Fetch", command=(lambda e=ents: fetch()))
   menubar.add_cascade(label="Help", menu=helpmenu)

   root.config(menu=menubar)
   root.bind('<Return>', (lambda event, e=ents: inp.row_frames(e, ents2, li, auto_open_box, 'xlsx')))


   b4 = Button(body, text=' Search ',
               command=(lambda e=ents: inp.row_frames(e, ents2, li, auto_open_box, 'xlsx')))
   b4.pack(side=LEFT, padx=5, pady=5)
   auto_open_box = IntVar()
   auto_open_box.set(1)
   open_var = Checkbutton(body, text='Auto Open', variable=auto_open_box)
   open_var.pack(side=LEFT)
   b5 = Button(body, text='Sort Files',
               command=(lambda e=root: resort()))
   b5.pack(side=LEFT, padx=5, pady=5)
   and_var = IntVar(body)
   and_var.set(1)
   a = OptionMenu(body,and_var, *range(1,5))
   and_var.trace("w", partial(changed, widget=and_var))
   #a.pack(side=RIGHT)
   body.pack()
   header.pack()
   footer.pack()

   root.mainloop()

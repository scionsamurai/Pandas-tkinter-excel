"""
File_Pal
========

Provides
  1. Interface for Pandas Loading/Searching Excel/CSV files.
  2. Fast and Easy searching of loaded Files.
"""
# Put together by James Ruikka
from tkinter import *
import multiprocessing
from multiprocessing import Pool
from tkinter import filedialog, simpledialog, messagebox
import os, warnings, tables, shelve, webbrowser
import pandas as pd
import numpy as np
from footer_frame import MakeFooter
import importlib,pkgutil
from file_frame import FileFrame
from retrieve_info import Retrieve_R
from functools import partial
from open_file_2 import OpenFile
from Make_Forms import MakeForm
from SplitEntry import Split_Entry
from func_file import GenFuncs
from PLogger import PrintLogger
warnings.filterwarnings("error")
warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning)

my_filetypes = [('all files', '.*'), ('CSV files', '.csv')]
fields = 'Header To Search', '   Search Item(s)   '
li = []
answer = []
err_dial_pressed = False

def fetch(pandas_obj):
   """
   Print first Files Memory Usage and file list.
   :param pandas_obj: Input DataFrame.
   """
   if isinstance(pandas_obj, pd.DataFrame):
       usage_b = pandas_obj.memory_usage(deep=True).sum()
   else:
       usage_b = pandas_obj.memory_usage(deep=True)
   usage_mb = usage_b / 1024 ** 2 # convert bytes to megabytes
   print("{:03.2f} MB".format(usage_mb))
   print(pandas_obj.info(verbose=True))
   print('----header_W/filler_value : filler_value----')
   print(answer)

def p_license(gdict):
    filename = gdict["__file__"]
    return os.path.dirname(filename)

def close_files(toor):
    """
    Close Dataframes that are checked in main window.
    """
    global answer, footer, ents2, li
    close_var = messagebox.askyesno("File_Pal_1.1", "Do you want to close checked files?")
    if close_var:
        for file in answer[::-1]:
            ind = answer.index(file)
            if ents2[ind][2].get() == 1:
                del li[ind]
                answer.remove(file)
        clear_footer()

def open_files(func=1):
    """
    Select and Open Files.
    :param func: ==1 Open Selected files from within a folder .
    :param func: ==2 Open files within Selected Directory.
    """
    global answer, footer,ents, ents2, row
    inp_opts = GenFuncs.get_inp_opts()
    new_list = []
    loc_answer = []
    if func==1:
        files_answer = filedialog.askopenfilenames(parent=footer,
                                                   initialdir=os.getcwd(),
                                                   title="Please select one or more files:",
                                                   filetypes=my_filetypes)
        try:
            new_list, loc_answer = GenFuncs.get_file_list(files_answer,answer,func=1)
        except TypeError:
            new_list, loc_answer = [], []
    elif func==2:
        check_name_temp = messagebox.askyesno("File_Pal_1.1", "Do you want to specify the first characters?")
        if check_name_temp:
            name_str = simpledialog.askstring("File_Pal_1.1",
                                              "First part of name for the files you want to open?",
                                              parent=root)
        else:
            name_str = ''
        directory = filedialog.askdirectory(parent=root,
                                            initialdir=os.getcwd(),
                                            title="Please select Directory:")
        try:
            new_list, loc_answer = GenFuncs.get_file_list(directory, answer, check_name_temp, name_str, func=2)
        except TypeError:
            new_list, loc_answer = [], []
    if (len(loc_answer) + len(new_list)) > 0:
        if inp_opts[0]['Main Win Criteria']:
            temp_opts = list(inp_opts)
            search_column = (ents[0][1].get()).strip()
            real_list = Split_Entry.split(ents[1][1].get())
            temp_opts.extend((search_column, real_list))
            inp_opts = temp_opts
        if (len(new_list) > 1) and (inp_opts[0]['CPU Cores'] > 1):
            pool = Pool(processes=inp_opts[0]['CPU Cores'])
            df_list = pool.map(partial(OpenFile.open_file, inp_options=inp_opts, root=row), new_list)
            for i in range(len(new_list)):
                if not df_list[i][0].empty:
                    frame_class = FileFrame(df_list[i][0], df_list[i][1], df_list[i][2])
                    li.append(frame_class)
                    answer.append(df_list[i][1])
                else:
                    print(df_list[i][1] + ' didn\'t have the certian input requirements.')
        else:
            loc_answer.extend(new_list)
        try:
            for file in loc_answer:
                if file not in answer:
                    try:
                        dataframe = OpenFile.open_file(file, inp_opts, row)
                        if not dataframe[0].empty:
                            frame_class = FileFrame(dataframe[0],dataframe[1], dataframe[2])
                            li.append(frame_class)
                            answer.append(file)

                        clear_footer()
                    except PermissionError as e:
                        print(e)
                        print('This file is currently locked.')
                        clear_footer()
                    except ValueError as e:
                        print(e)
                        clear_footer()
        except KeyboardInterrupt as e:
            print(e)

def resort():
    """
    Refresh main window footer to have file and entry to start Resort.
    """
    global answer, footer, ents2
    footer.pack_forget()
    footer.destroy()
    footer = Frame(root)
    ents3 = form2.make(footer, answer, 1,1)
    b1 = Button(footer, text='Save Order', command=(lambda e=root: resort_p2(ents3)))
    b1.pack(side=RIGHT, padx=5, pady=5)
    footer.pack()

def resort_p2(ents3):
    """
    Refresh main window footer to have original layout with new order.
    """
    global answer, footer, ents2, li, form2, row
    temp_list = []
    for i in ents3:
        try:
            num = int(i[1].get())
        except:
            print(f"{i[1].get()} not a number? Defaulting to 0")
            num = 0
        temp_list.append((i[0],num))
    temp_list.sort(key= sort_second)

    temp2_list = []
    for i in temp_list:
        temp2_list.append(i[0])
    temp_li = []
    for file in temp2_list:
        ind = answer.index(file)
        temp_li.append(li[ind])
    li = temp_li
    del temp_li
    answer = temp2_list

    form2.answer = answer
    clear_footer()

def clear_footer():
    global footer, answer, ents2, li, row
    footer.pack_forget()
    footer.destroy()
    row.pack_forget()
    row.destroy()
    row = Frame(root)
    footer = Frame(root)
    Label(row, text=' --- Files / Search Order --- ').pack()
    ents2 = MakeFooter.update_footer(footer, answer, li, ents, body)
    row.pack()
    footer.pack()

def clear_values():
    ents[0][1].delete(0, END)
    ents[1][1].delete(0, END)

def open_help_gs(func=1):
    if func == 1:
        webbrowser.open_new(r"https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/README.md")
    else:
        webbrowser.open_new(r"https://github.com/scionsamurai/Pandas-tkinter-excel/blob/Test/LICENSE")

def sort_second(val):
    return val[1]

def ask_quit():
    if messagebox.askyesno("Quit", "Do you want to quit now?"):
        try:
            root.destroy()
        except:
            pass

def err_dialog():
    """
    Redirects print commands to output in newly generated Dialog window .
    """
    global err_dial_pressed, err_window
    try:
        win_exists_var = Toplevel.winfo_exists(err_window)
    except NameError:
        win_exists_var = 0
    if win_exists_var != 1:
        err_window = Toplevel()
        err_window.title("Info Dialog")
        t = Text(err_window)
        t.pack()
        p1 = PrintLogger(t)
        t.see('end')
        sys.stdout = p1
        err_dial_pressed = True

if __name__ == '__main__':
   multiprocessing.freeze_support()
   root = Tk()
   root.title("File_Pal_1.1")
   global auto_open_box, ents,header, body, footer, form2

   header = Frame(root)
   body = Frame(root)
   row = Frame(root)
   footer = Frame(root)


   answer = []
   form2 = MakeForm()
   ents = form2.make(header, fields,1)
   form2= MakeForm(answer_in=answer)
   ents2 = MakeFooter.update_footer(footer, answer, li, ents, body)

   menubar = Menu(root)
   filemenu = Menu(menubar, tearoff=0)
   submenu = Menu(root, tearoff=0)
   submenu.add_command(label="Select File", command=(lambda e=ents: open_files()))
   submenu.add_command(label="All in Dir", command=(lambda e='no value': open_files(2)))
   filemenu.add_cascade(label="Open", menu=submenu)
   filemenu.add_command(label="Sort Files", command=(lambda e=root: resort()))
   filemenu.add_command(label="Close Selected", command=(lambda e=ents2: close_files(root)))
   filemenu.add_command(label="Options", command=(lambda e=ents: form2.make(func=2)))
   menubar.add_cascade(label="File", menu=filemenu)
   helpmenu = Menu(menubar, tearoff=0)
   helpmenu.add_command(label="Getting Started", command=(lambda e=ents: open_help_gs()))
   helpmenu.add_command(label="License", command=(lambda e=ents: open_help_gs(2)))
   #helpmenu.add_command(label="Info Dialog", command=(lambda e=ents2: err_dialog()))
   #helpmenu.add_command(label="Fetch", command=(lambda e=ents: fetch(li[0].df)))
   menubar.add_cascade(label="Help", menu=helpmenu)
   root.config(menu=menubar)
   root.bind('<Return>', (lambda event, e=ents: Retrieve_R.ow_frames(e, ents2, li, auto_open_box, 'xlsx',
                                                                     answer, row)))
   root.bind('<Control-c>', (lambda event: clear_footer()))
   b4 = Button(body, text=' Search ', command=(lambda e=ents: Retrieve_R.ow_frames(e, ents2, li, auto_open_box, 'xlsx',
                                                                                   answer, row)))
   b4.pack(side=LEFT, padx=5, pady=5)
   auto_open_box = IntVar()
   auto_open_box.set(1)
   open_var = Checkbutton(body, text='Auto Open', variable=auto_open_box)
   open_var.pack(side=LEFT)


   b5 = Button(body, text='Clear Inputs',command=(lambda e=root: clear_values()))
   Label(row, text=' --- Files / Search Order --- ').pack()
   b5.pack(side=LEFT, padx=5, pady=5)
   body.pack()
   header.pack()
   row.pack()
   footer.pack()
   root.protocol("WM_DELETE_WINDOW", ask_quit)
   root.mainloop()

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
import os, warnings, tables, shelve
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
plugz = []
plug_ind = []
checkable_butts = []
li = []
answer = []
err_dial_pressed = False

def get_class_name(mod_name):
    """Return the class name from a plugin name"""
    output = ""

    # Split on the _ and ignore the 1st word plugin
    words = mod_name.split("_")[1:]

    # Capitalise the first letter of each word and add to string
    for word in words:
        output += word.title()
    return output

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

def print_l():
    x =open(os.path.join(p_license(globals()), "LICENSE")).read()
    print(x)

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
        footer.pack_forget()
        footer.destroy()
        footer = Frame(toor)
        ents2 = MakeFooter.update_footer(footer, answer, li, ents, body)
        form2.answer = answer
        footer.pack()

def open_files(func=1):
    """
    Select and Open Files.
    :param func: ==1 Open Selected files from within a folder .
    :param func: ==2 Open files within Selected Directory.
    """
    global answer, footer,ents, ents2
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
            df_list = pool.map(partial(OpenFile.open_file, inp_options=inp_opts, root=footer), new_list)
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
                        dataframe = OpenFile.open_file(file, inp_opts, footer)
                        # #frame , location/key, (cols:NA_Fill vals
                        if not dataframe[0].empty:
                            frame_class = FileFrame(dataframe[0],dataframe[1], dataframe[2])
                            li.append(frame_class)
                            answer.append(file)

                        footer.pack_forget()
                        footer.destroy()
                        footer = Frame(root)
                        footer.pack()
                    except PermissionError as e:
                        print(e)
                        print('This file is currently locked.')
                        clear_footer()
                    except ValueError as e:
                        print(e)
                        clear_footer()
        except KeyboardInterrupt as e:
            print(e)
        ents2 = MakeFooter.update_footer(footer, answer, li, ents, body)

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
    global answer, footer, ents2, li, form2
    temp_list = []
    for i in ents3:
        temp_list.append((i[0],i[1].get()))
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

    footer.pack_forget()
    footer.destroy()
    footer = Frame(root)
    ents2 = MakeFooter.update_footer(footer, answer, li, ents, body)
    form2.answer = answer
    footer.pack()

def clear_footer():
    global footer, answer, ents2, li
    footer.pack_forget()
    footer.destroy()
    footer = Frame(root)
    ents2 = MakeFooter.update_footer(footer, answer, li, ents, body)
    footer.pack()

def sort_second(val):
    return val[1]

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

def get_plugz(path):
    modules = pkgutil.iter_modules(path=[path])

    for loader, mod_name, ispkg in modules:
        # Ensure that module isn't already loaded
        if mod_name not in sys.modules:
            # Import module
            loaded_mod = __import__(path + "." + mod_name, fromlist=[mod_name])

            # Load class from imported module
            class_name = get_class_name(mod_name)
            loaded_class = getattr(loaded_mod, class_name)

            # Create an instance of the class
            if path == "plugins":
                plugz.append([class_name, loaded_class()])
                plug_ind.append(class_name)
            elif path == "checkable_sets":
                checkable_butts.append([class_name, loaded_class()])

def changed(*args, var, plug_name, code):
    update_plugs_list(var,plug_name,code)

def update_plugs_list (var, plug_name, code, save_set=False):
    try:
    	var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
    	try:
            plug_l = var_file['plug_lists']
    	except KeyError:
            plug_l = {}
    	plug_l[plug_name] = [var.get(), code, save_set]
    	var_file['plug_lists'] = plug_l
    	var_file.close()
    except:
    	print("error at line 255 opening var_file")

if __name__ == '__main__':
   multiprocessing.freeze_support()
   root = Tk()
   root.title("File_Pal_1.1")
   global auto_open_box, ents,header, body, footer, form2

   header = Frame(root)
   body = Frame(root)
   row = Frame(root)
   footer = Frame(root)

   get_plugz("plugins")
   get_plugz("checkable_sets")

   answer = []
   form2 = MakeForm()
   ents = form2.make(header, fields,1)
   form2= MakeForm(answer_in=answer)
   ents2 = MakeFooter.update_footer(footer, answer, li, ents, body)

   menubar = Menu(root)
   filemenu = Menu(menubar, tearoff=0)
   submenu = Menu(root, tearoff=0)
   #submenu2 = Menu(root, tearoff=0)
   submenu3 = Menu(root, tearoff=0)
   submenu.add_command(label="Select File", command=(lambda e=ents: open_files()))
   submenu.add_command(label="All in Dir", command=(lambda e='no value': open_files(2)))
   filemenu.add_cascade(label="Open", menu=submenu)
   #filemenu.add_cascade(label="Plugins", menu=submenu2)
   #for name, instance in plugz:
   #    ind = plug_ind.index(name)
   #    submenu2.add_command(label=name, command=(lambda e=ind: plugz[e][1].run(li,answer,ents2,auto_open_box, root)))
   filemenu.add_command(label="Options", command=(lambda e=ents: form2.make(func=2)))
   for name, instance in checkable_butts:
       temp_var = IntVar()
       temp_var.set(0)
       update_plugs_list(temp_var, name, instance)
       temp_var.trace("w", partial(changed, var=temp_var, plug_name=name, code=instance))
       submenu3.add_checkbutton(label=name, variable=temp_var)

   #submenu3.add_command(label="More >", command=(lambda e=ents: form2.make(func=2)))
   filemenu.add_command(label="Close Selected", command=(lambda e=ents2: close_files(root)))
   filemenu.add_separator()
   filemenu.add_command(label="Exit", command=root.quit)
   menubar.add_cascade(label="File", menu=filemenu)
   helpmenu = Menu(menubar, tearoff=0)
   helpmenu.add_command(label="License", command=(lambda e=ents: print_l()))
   #helpmenu.add_command(label="Info Dialog", command=(lambda e=ents2: err_dialog()))
   #helpmenu.add_command(label="Fetch", command=(lambda e=ents: fetch(li[0].df)))
   menubar.add_cascade(label="Help", menu=helpmenu)
   root.config(menu=menubar)
   root.bind('<Return>', (lambda event, e=ents: Retrieve_R.ow_frames(e, ents2, li, auto_open_box, 'xlsx',
                                                                     answer, footer)))
   root.bind('<Control-c>', (lambda event: clear_footer()))
   b4 = Button(body, text=' Search ', command=(lambda e=ents: Retrieve_R.ow_frames(e, ents2, li, auto_open_box, 'xlsx',
                                                                                   answer, footer)))
   b4.pack(side=LEFT, padx=5, pady=5)
   auto_open_box = IntVar()
   auto_open_box.set(1)
   open_var = Checkbutton(body, text='Auto Open', variable=auto_open_box)
   open_var.pack(side=LEFT)


   b5 = Button(body, text='Sort Files',command=(lambda e=root: resort()))
   b5.pack(side=LEFT, padx=5, pady=5)
   body.pack()
   header.pack()
   footer.pack()
   root.mainloop()

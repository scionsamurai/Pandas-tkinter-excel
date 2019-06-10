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
from SplitEntry import Split_Entry
from PLogger import PrintLogger
warnings.filterwarnings("error")
warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning)

my_filetypes = [('all files', '.*'), ('CSV files', '.csv')]
output_filetypes = [('HD5', '.h5'), ('CSV files', '.csv')]
fields = 'Header To Search', '  Search Item(s)'#, 'Output Directory'
li = []
li_dict = {}
answer = []
err_dial_pressed = False
LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

def fetch(pandas_obj):
   #save_var = messagebox.askokcancel("Title", "Do you want to save?")
   #print(save_var)
   if isinstance(pandas_obj, pd.DataFrame):
       usage_b = pandas_obj.memory_usage(deep=True).sum()
   else:
       usage_b = pandas_obj.memory_usage(deep=True)
   usage_mb = usage_b / 1024 ** 2 # convert bytes to megabytes
   print("{:03.2f} MB".format(usage_mb))
   print(pandas_obj.info(verbose=True))

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
    close_var = messagebox.askyesno("File_Pal_1.0", "Do you want to close checked files?")
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

def open_files(func=1):
    global answer, footer,ents, ents2
    del_list = []
    new_list = []
    inp_opts = get_inp_opts()
    loc_answer = []
    if func==1:
        results_only = messagebox.askyesno("File_Pal_1.0", "Open only lines with main window search criteria?")
        files_answer = filedialog.askopenfilenames(parent=footer,
                                                   initialdir=os.getcwd(),
                                                   title="Please select one or more files:",
                                                   filetypes=my_filetypes)
        if len(files_answer) > 0:
            try:
                for file in files_answer:
                    if file not in answer:
                        if ((file[-4:])[:3] == 'xls') or (file[-4:] == '.xls'):
                            if file[:2] != '~$':
                                new_list.append(file)
                        elif (file[-4:] == '.csv') or (file[-3:] == '.h5'):
                            loc_answer.append(file)
            except KeyboardInterrupt as e:
                print(e)
    elif func==2:
        check_name_temp = messagebox.askyesno("File_Pal_1.0", "Do you want to specify the first characters?")
        if check_name_temp == True:
            name_str = simpledialog.askstring("File_Pal_1.0",
                                              "First part of name for the files you want to open?",
                                              parent=root)
        results_only = messagebox.askyesno("File_Pal_1.0", "Open only lines with main window search criteria?")
        directory = filedialog.askdirectory(parent=root,
                                            initialdir=os.getcwd(),
                                            title="Please select Directory:")
        for path, subdirs, files in os.walk(directory):
            for name in files:
                if check_name_temp == True:
                    if (name[-4:] == '.csv') or (name[-3:] == '.h5'):
                            if name[:len(name_str)].lower() == name_str.lower():
                                if name not in answer:
                                    loc_answer.append((path + '/' + name))
                    elif ((name[-4:])[:3] == 'xls') or (name[-4:] == '.xls'):
                        if name[:2] != '~$':
                            if name[:len(name_str)] == name_str:
                                if name not in answer:
                                    new_list.append((path + '/' + name))

                else:
                    if (name[-4:] == '.csv') or (name[-3:] == '.h5'):
                        if name not in answer:
                            loc_answer.append((path + '/' + name))
                    elif ((name[-4:])[:3] == 'xls') or (name[-4:] == '.xls'):
                        if name[:2] != '~$':
                            if name not in answer:
                                new_list.append((path + '/' + name))
    if (len(loc_answer) + len(new_list)) > 0:
        if results_only == True:
            temp_opts = list(inp_opts)
            search_column = (ents[0][1].get()).strip()
            real_list = Split_Entry.split(ents[1][1].get())
            temp_opts.extend((search_column, real_list))
            inp_opts = temp_opts

        footer.pack_forget()
        footer.destroy()
        footer = Frame(root)
        open = OpenFile()
        if (len(new_list) > 1) and (inp_opts[0]['CPU Cores'] > 1):
            pool = Pool(processes=inp_opts[0]['CPU Cores'])
            df_list = pool.map(partial(open.open_file, inp_options=inp_opts), new_list)
            for i in range(len(new_list)):
                if df_list[i][0].empty != True:
                    li.append(df_list[i][0])
                    answer.append(df_list[i][1])
                    li_dict[df_list[i][1]] = (len(li) - 1)
                else:
                    print(df_list[i][1] + ' didn\'t have the certian input requirements.')
        else:
            loc_answer.extend(new_list)
        try:
            for file in loc_answer:
                if file not in answer:
                    try:
                        dataframe = open.open_file(file, inp_opts)
                        #print(dataframe[0])
                        if dataframe[0].empty != True:
                            li.append(dataframe[0])
                            answer.append(file)
                            li_dict[file] = (len(li) - 1)
                        else:
                            temp_f = file.split('/')
                            new_f = temp_f[(len(temp_f) - 1)]
                            del_list.append(new_f)
                    except PermissionError as e:
                        print(e)
        except KeyboardInterrupt as e:
            print(e)
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

def get_inp_opts():
    gen_rules = {}
    var_file = shelve.open('var_file')
    try:
        for gen_set in var_file['opt_gen_rules']:
            if gen_set[0] == 'Delimiter':
                if gen_set[1] == 'DV' or gen_set[1] == '':
                    gen_rules['Delimiter'] = ','
                else:
                    gen_rules['Delimiter'] = gen_set[1]
            elif gen_set[0] == 'Terminator':
                if gen_set[1] == 'DV' or gen_set[1] == '':
                    gen_rules['Terminator'] = None
                else:
                    gen_rules['Terminator'] = gen_set[1]
            elif gen_set[0] == 'Header Line':
                if gen_set[1] == 'DV' or gen_set[1] == '':
                    gen_rules['Header Line'] = 0
                else:
                    gen_rules['Header Line'] = int(gen_set[1])
            elif gen_set[0] == 'Index Column':
                if gen_set[1] == 'DV' or gen_set[1] == '':
                    gen_rules['Index Column'] = None
                else:
                    gen_rules['Index Column'] = int(gen_set[1])
            elif gen_set[0] == 'Chunk':
                if gen_set[1] == 'DV' or gen_set[1] == '':
                    gen_rules['Chunk'] = None
                else:
                    gen_rules['Chunk'] = int(gen_set[1])
            elif gen_set[0] == 'CPU Cores':
                if gen_set[1] == 1 or gen_set[1] == '':
                    gen_rules['CPU Cores'] = 1
                    tcores = 1
                else:
                    gen_rules['CPU Cores'] = int(gen_set[1])
                    tcores = int(gen_set[1])
            elif gen_set[0] == 'Verbose':
                if gen_set[1] == 0:
                    gen_rules['Verbose'] = False
                else:
                    gen_rules['Verbose'] = True
            elif gen_set[0] == 'Header Func':
                if gen_set[1] == 0:
                    gen_rules['Header Func'] = False
                else:
                    gen_rules['Header Func'] = True
    except KeyError:
        gen_rules['Delimiter'] = ','
        gen_rules['Terminator'] = None
        gen_rules['Header Line'] = 0
        gen_rules['Index Column'] = None
        gen_rules['Chunk'] = None
        gen_rules['CPU Cores'] = 1
        gen_rules['Verbose'] = False
        gen_rules['Header Func'] = False
        tcores = 1
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
        head_func_dtypes = var_file['head_func_types']
    except KeyError:
        head_func_dtypes = None
    var_file.close()
    return (gen_rules,only_cols,dtypes,head_func_dtypes)

def err_dialog():
    global err_dial_pressed
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
   root.title("File_Pal_1.0")
   #root.iconbitmap(r'C:\Users\SsDamurai\Desktop\newP.ico')
   global auto_open_box, ents,header, body, footer, form1, form2

   header = Frame(root)
   body = Frame(root)
   row = Frame(root)
   footer = Frame(root)

   answer = []
   opt_form = MakeForm()
   inp = Retrieve_Input()
   form1 = MakeForm()
   ents = form1.make(header, fields,1)
   form2= MakeForm(data_frames=li,frame_keys=li_dict, input_box1=ents[0][1],input_box2=ents[1][1])
   ents2 = form2.make(footer, answer,2)
   opt_form = MakeForm()

   menubar = Menu(root)
   filemenu = Menu(menubar, tearoff=0)
   submenu = Menu(root, tearoff=0)
   submenu.add_command(label="Input Options", command=(lambda e=ents: opt_form.make(func=7)))
   submenu.add_command(label="Select File", command=(lambda e=ents: open_files()))
   submenu.add_command(label="All in Dir", command=(lambda e='no value': open_files(2)))
   filemenu.add_command(label="Save Selected", command=(lambda e='no value': df_to_hdf()))
   filemenu.add_cascade(label="Open", menu=submenu)
   filemenu.add_command(label="Output Options", command=(lambda e=ents: opt_form.make(func=5)))
   filemenu.add_command(label="Close Selected", command=(lambda e=ents2: close_files(root)))
   filemenu.add_separator()
   filemenu.add_command(label="Exit", command=root.quit)
   menubar.add_cascade(label="File", menu=filemenu)
   helpmenu = Menu(menubar, tearoff=0)
   helpmenu.add_command(label="License", command=donothing())
   helpmenu.add_command(label="Info Dialog", command=(lambda e=ents2: err_dialog()))
   helpmenu.add_command(label="Fetch", command=(lambda e=ents: fetch(li[0])))
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

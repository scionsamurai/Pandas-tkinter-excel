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
import os, warnings, tables
import pandas as pd
import numpy as np
from file_frame import FileFrame
from retrieve_info import Retrieve_R
from functools import partial
from open_file_2 import OpenFile
from Make_Forms import MakeForm
from SplitEntry import Split_Entry
from scrollbarClass import Scrollable
from func_file import GenFuncs
from PLogger import PrintLogger
warnings.filterwarnings("error")
warnings.filterwarnings('ignore',category=pd.io.pytables.PerformanceWarning)

my_filetypes = [('all files', '.*'), ('CSV files', '.csv')]
output_filetypes = [('HD5', '.h5'), ('CSV files', '.csv')]
fields = 'Header To Search', '   Search Item(s)   '
li = []
answer = []
err_dial_pressed = False
x = 0
x2 = 45

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

def drop_dups():
    global auto_open_box
    initiateQ = messagebox.askyesno("Drop Duplicates","Would you like to drop duplicates from the checked files?")
    new_output = []
    first_last_Q = messagebox.askyesno("Drop Duplicates","Would you like to keep the first occurrence?\n (Last occurrence kept if \"No\")")
    counter_count = 0
    delete_list = []
    counter_dict = {}
    if first_last_Q:
        first_last = "first"
    else:
        first_last = "last"
    if initiateQ:
        for key in answer:
            if ents2[answer.index(key)][2].get() == 1:
                if li[answer.index(key)].fill_val != {}:
                    temp_df = li[answer.index(key)].df.copy()
                    for col, val in li[answer.index(key)].fill_val.items():
                        temp_df[col].replace(val, np.NaN, inplace=True)
                    temp_df['Counter'] = range(counter_count, len(temp_df) +counter_count)
                    counter_dict[key] = [counter_count,len(temp_df)+counter_count]
                    counter_count += len(temp_df)
                    new_output.append(temp_df)
                else:
                    ph = li[answer.index(key)].df
                    ph['Counter'] = range(counter_count, len(ph) +counter_count)
                    counter_dict[key] = [counter_count, len(ph)+counter_count]
                    counter_count += len(ph)
                    new_output.append(li[answer.index(key)].df)
        try:
            new_new_output = pd.concat(new_output, axis=0, sort=False, ignore_index=True)
        except ValueError:
            new_new_output = new_output
        ask_headers = simpledialog.askstring("Drop Duplicates","What Columns would you like to check for duplicates?")
        headers_list = Split_Entry.split(ask_headers)
        new_new_output.drop_duplicates(headers_list, first_last,inplace=True)
        keep_all_Q = messagebox.askyesno("Drop Duplicates", "Keep all results?")
        if not keep_all_Q:
            for key, value in counter_dict.items():
                output_file_Q = messagebox.askyesno("Drop Duplicates", "Keep rows from " + key + "?")
                if not output_file_Q:
                    delete_list.append(counter_dict[key])
                    counter_dict[key] = []
        for list in delete_list:
            new_new_output.drop(new_new_output.index[(new_new_output['Counter'] >= list[0]) &
                                                     (new_new_output['Counter'] <= list[1])], inplace=True)
        del new_new_output['Counter']
        Retrieve_R.ow_frames("", new_new_output, "", auto_open_box, 'xlsx', "", func=1)
def df_to_hdf():
   """
   Save Dataframes that are checked in main window to a single file.
   """
   global ents2
   new_output = []
   save_answer = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                         title="Please select save location and name:",
                                         filetypes=output_filetypes,
                                         defaultextension='.h5')
   for key in answer:
       if ents2[answer.index(key)][2].get() == 1:
           if li[answer.index(key)].fill_val != {}:
               temp_df = li[answer.index(key)].df.copy()
               for col, val in li[answer.index(key)].fill_val.items():
                   temp_df[col].replace(val, np.NaN, inplace=True)
               new_output.append(temp_df)
   try:
       new_new_output = pd.concat(new_output, axis=0, sort=False, ignore_index=True)
   except ValueError:
       new_new_output = new_output
   if save_answer[-3:] == '.h5':
      new_new_output.to_hdf(save_answer, key='df', mode='w', format='table')
   elif save_answer[-4:] == '.csv':
      new_new_output.to_csv(save_answer, index=False)
   print('saved')
   del new_output

def donothing():
    x=0
    return x

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
        ents2 = file_frame(footer, answer)
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

        footer.pack_forget()
        footer.destroy()
        footer = Frame(root)
        if (len(new_list) > 1) and (inp_opts[0]['CPU Cores'] > 1):
            pool = Pool(processes=inp_opts[0]['CPU Cores'])
            df_list = pool.map(partial(OpenFile.open_file, inp_options=inp_opts), new_list)
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
                        dataframe = OpenFile.open_file(file, inp_opts)
                        # #frame , location/key, (cols:NA_Fill vals
                        if not dataframe[0].empty:
                            frame_class = FileFrame(dataframe[0],dataframe[1], dataframe[2])
                            li.append(frame_class)
                            answer.append(file)
                    except PermissionError as e:
                        print(e)
        except KeyboardInterrupt as e:
            print(e)
        ents2 = file_frame(footer, answer)
        footer.pack()

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
    ents2 = file_frame(footer, answer)
    form2.answer = answer
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

def file_frame(rootx, fields):
    """
    Generates footer Frame of main window with opened files listed.
    :param rootx: Parent Frame.
    :param fields: List of open files.
    :return: List of Files with checkbutton Status.
    """
    lrow = Frame(rootx)
    Label(lrow, text=' --- Files / Search Order --- ').pack()
    lrow.pack()
    entries = []
    for field in fields:
        temp_field = field.split('/')
        new_field = 'Search:  ' + temp_field[(len(temp_field) - 1)]
        vrow = Frame(rootx)
        var1 = IntVar()
        var1.set(1)
        ent = Checkbutton(vrow, text=new_field, variable=var1)
        bx = Button(vrow, text='Headers', command=(lambda e=field: header_button(key=e)))
        vrow.pack(side=TOP, fill=X, padx=5, pady=2)
        ent.pack(side=LEFT)
        bx.pack(side=RIGHT)
        entries.append((field, ent, var1))
    return entries

def page_func(list,p_frame,row_c, func, file, bod, set_info=None):
    """
    Creates Next/Last page buttons for Header windows if they are needed
    :param list: Values list generated to Header window
    :param p_frame: Parent Frame to generate buttons
    :param row_c: Row number to apply buttons
    :param func: Command/Function to Generate with each Button
    :param file: Name of the file for generated header list
    :param bod: Parent Frames Parent Frame - for refreshing window
    :param set_info: Selected Column
    :return: True if one of the buttons are generated - for updating the row count for next buttons
    """
    temp_count = False
    if len(list[:x2]) / 45 > 1:
        Button(p_frame, text='Previous Page',
               command=(lambda e=file: func(e, bod, set_info, 'prev'))).grid(row=row_c, column=1, padx=1)
        temp_count = True
    if len(list) > len(list[:x2]):
        Button(p_frame, text='Next Page',
               command=(lambda e=file: func(e, bod, set_info, 'next'))).grid(row=row_c, column=2, padx=1)
        temp_count = True
    return temp_count

def header_button(key, root2=None, set_info=None, func=0):
    """
    Generates a window with the headers from associated file listed.
    :param key: File Name
    :param root2: Parent Frame
    :param set_info: Place holder variable to make input more uniform with header_values input for button function
    :param func: Function to specify if generating Next or Last page
    """
    global opt_window, x, x2
    ind = answer.index(key)
    field = li[ind].df.columns.values
    temp_field = key.split('/')
    new_field = temp_field[(len(temp_field) - 1)]
    if root2 is not None:
        root2.destroy()
    else:
        try:
            win_exists_var = Toplevel.winfo_exists(opt_window)
        except NameError:
            win_exists_var = 0
        if win_exists_var != 1:
            opt_window = Toplevel()
            opt_window.title(new_field)
        else:
            opt_window.destroy()
            opt_window = Toplevel()
            opt_window.title(new_field)
    body = Frame(opt_window)
    scrollable_body = Scrollable(body)
    body.pack()
    if func == 'next':
        x += 45
        x2 += 45
    elif func == 'prev':
        x -= 45
        x2 -= 45
    else:
        x = 0
        x2 = 45
    count = 0
    for f in field[x:x2]:
        count += 1
        Button(scrollable_body, text=f,
               command=(lambda e=f: GenFuncs.update_entry(opt_window, e, ents[0][1], 1))).grid(row=count, column=1,
                                                                                     padx=1)
        Button(scrollable_body, text='Result\'s within Column',
               command=(lambda e=f: header_values(key, body, e))).grid(row=count, column=2, padx=1)
    count += 1
    temp_count = page_func(field,scrollable_body,count, header_button, key, body)
    if temp_count:
        count += 1
    Button(scrollable_body, text="Exit", command=(lambda e=root2: e.destroy())).grid(column=2)
    scrollable_body.update()
    opt_window.mainloop()

def header_values(key, root2, set_info, func=0):
    """
    Generates a window with the values from clicked header.
    :param key: File Name
    :param root2: Parent Frame
    :param set_info: Column Name
    :param func: Function to specify if generating Next or Last page
    """
    global opt_window, ents, ents2, x, x2
    ents[0][1].delete(0, END)
    ents[0][1].insert(0, (str(set_info)))
    ents[1][1].delete(0, END)
    root2.destroy()
    body3 = Frame(opt_window)
    temp_field = key.split('/')
    new_field = temp_field[(len(temp_field) - 1)]
    opt_window.title(new_field + ' / ' + str(set_info))
    scrollable_body = Scrollable(body3)
    body3.pack()
    slimmed_list, count_dict = get_col_vals(key, set_info)
    if func == 'next':
        x += 45
        x2 += 45
    elif func == 'prev':
        x -= 45
        x2 -=45
    else:
        x = 0
        x2 = 45
    count = 0
    for field in slimmed_list[x:x2]:
        count += 1
        ind = answer.index(key)
        if set_info in li[ind].fill_val:
            if field == li[ind].fill_val[set_info]:
                new_field = 'Blank'
            else:
                new_field = field
        else:
            if pd.isnull(field):
                new_field = 'Blank'
            else:
                new_field = field
        Button(scrollable_body, text=new_field,
               command=(lambda e=field: GenFuncs.update_entry(body, e, ents[1][1]))).grid(row=count, column=1,
                                                                                      padx=1)
        Label(scrollable_body, width=15,
              text=("Total Results: " + str(count_dict[field]))).grid(row=count, column=2, pady=5, padx=1)

    count += 1
    temp_count = page_func(slimmed_list, scrollable_body, count, header_values, key, body3, set_info)
    if temp_count:
        count += 1
    Button(scrollable_body, text="Reset Items",
           command=(lambda e="nothing": GenFuncs.update_entry(opt_window, e, ents[1][1], 2))).grid(row=count, column=1, padx=1)
    Button(scrollable_body, text="Exit",
           command=(lambda e=opt_window: e.destroy())).grid(row=count, column=2, pady=5, padx=1)
    scrollable_body.update()
    opt_window.mainloop()

def get_col_vals(key, col):
    """
    Creates List of values from within column with Dictionary indicating Value counts - List is returned in Descending
    Count order.
    :param key: File Name
    :param col: Column Name
    :return: Returns List (in Descending count order) and Dictionary with count
    """
    ind = answer.index(key)
    col_val_list = li[ind].df[col].values
    count_dict = {}
    slimmed_list = []
    for value in col_val_list:
        try:
            count_dict[value] += 1
        except KeyError:
            count_dict[value] = 1
    for key1, value in sorted(count_dict.items(), key=lambda item: item[1])[::-1]:
        slimmed_list.append(key1)
    return slimmed_list, count_dict

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
   ents2 = file_frame(footer, answer)

   menubar = Menu(root)
   filemenu = Menu(menubar, tearoff=0)
   submenu = Menu(root, tearoff=0)
   submenu.add_command(label="Select File", command=(lambda e=ents: open_files()))
   submenu.add_command(label="All in Dir", command=(lambda e='no value': open_files(2)))
   filemenu.add_command(label="Save Selected", command=(lambda e='no value': df_to_hdf()))
   filemenu.add_cascade(label="Open", menu=submenu)
   filemenu.add_command(label="Drop Duplicates", command=(lambda e='no value': drop_dups()))
   filemenu.add_command(label="Options", command=(lambda e=ents: form2.make(func=2)))
   filemenu.add_command(label="Close Selected", command=(lambda e=ents2: close_files(root)))
   filemenu.add_separator()
   filemenu.add_command(label="Exit", command=root.quit)
   menubar.add_cascade(label="File", menu=filemenu)
   helpmenu = Menu(menubar, tearoff=0)
   helpmenu.add_command(label="License", command=donothing())
   helpmenu.add_command(label="Info Dialog", command=(lambda e=ents2: err_dialog()))
   helpmenu.add_command(label="Fetch", command=(lambda e=ents: fetch(li[0].df)))
   menubar.add_cascade(label="Help", menu=helpmenu)
   root.config(menu=menubar)
   root.bind('<Return>', (lambda event, e=ents: Retrieve_R.ow_frames(e, ents2, li, auto_open_box, 'xlsx', answer)))
   b4 = Button(body, text=' Search ', command=(lambda e=ents: Retrieve_R.ow_frames(e, ents2, li,
                                                                                   auto_open_box, 'xlsx', answer)))
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

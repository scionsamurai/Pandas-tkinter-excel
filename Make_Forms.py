from tkinter import *
from scrollbarClass import Scrollable
import shelve, os, sys, re
import pandas as pd
from functools import partial
class MakeForm:
    def __init__(self, data_frames=[], frame_keys={},input_box1=False, input_box2=False):
        self.entries = []
        self.li = data_frames
        self.li_dict = frame_keys
        self.ents1 = input_box1
        self.ents2 = input_box2
        self.footer = False
        self.header_dtypes = {}
        self.my_filetypes = [('all files', '.*'), ('CSV files', '.csv'),('HD5', '.h5'),('xls','.xls')]
        self.NA_dict = {}
        self.x = 0
        self.x2 = 45

    def make(self, root=None, fields=[], func=0, body=False, body2=False, key=False, set_info=False, NAdict={}):
        if func == 1:
            self.entries = []
            fields = 'Header To Search', '  Search Item(s)'
            for field in fields:
                row = Frame(root)
                lab = Label(row, width=15, text=field, anchor='w')
                ent = Entry(row)
                row.pack(side=TOP, fill=X, padx=5, pady=2)
                lab.pack(side=LEFT)
                ent.pack(side=RIGHT, expand=YES, fill=X)
                self.entries.append((field, ent))
            return self.entries
        elif func == 2:
            lrow = Frame(root)
            Label(lrow, text=' --- Files / Search Order --- ').pack()
            lrow.pack()
            self.NA_dict = NAdict
            self.entries = []
            for field in fields:
                temp_field = field.split('/')
                new_field = 'Search:  ' + temp_field[(len(temp_field) - 1)]
                row = Frame(root)
                var1 = IntVar()
                var1.set(1)
                ent = Checkbutton(row, text=new_field, variable=var1)
                bx = Button(row, text='Headers',
                            command=(lambda e=field: self.headers_option_button(e)))
                row.pack(side=TOP, fill=X, padx=5, pady=2)
                ent.pack(side=LEFT)
                bx.pack(side=RIGHT)
                self.entries.append((field, ent, var1))
            return self.entries
        elif func == 3:
            count = 0
            for f in fields[self.x:self.x2]:
                count += 1
                Button(body2, text=f,
                            command=(lambda e=f: self.update_entry(root, e, self.ents1, 1))).grid(row=count, column=1,
                                                                                                  padx=1)
                Button(body2, text='Result\'s within Column',
                       command=(lambda e=f: self.update_column_win(body,e, key))).grid(row=count, column=2,  padx=1)
            count += 1
            temp_count = False
            if len(fields[:self.x2]) / 45 > 1:
                Button(body2, text='Previous Page',
                       command=(lambda e=key: self.headers_option_button(e, root=body, func='prev'))).grid(row=count,column=1,padx=1)
                temp_count = True
            if len(fields) > len(fields[:self.x2]):
                Button(body2, text='Next Page',
                       command=(lambda e=key: self.headers_option_button(e, root=body, func='next'))).grid(row=count,column=2, padx=1)
                temp_count = True
            if temp_count == True:
                count += 1
            Button(body2, text="Exit", command=(lambda e=root: e.destroy())).grid(column=2)
            body2.update()
            root.mainloop()
        elif func == 4:
            count = 0
            for field in fields[self.x:self.x2]:
                count += 1
                if set_info in self.NA_dict[key]: #if (column) in
                    if field == self.NA_dict[key][set_info]:
                        new_field = 'Blank'
                    else:
                        new_field = field
                else:
                    if pd.isnull(field):
                        new_field = 'Blank'
                    else:
                        new_field = field
                Button(body2, text=new_field,
                            command=(lambda e=field: self.update_entry(body, e, self.ents2))).grid(row=count, column=1,
                                                                                                padx=1)
                Label(body2, width=15,
                      text=("Total Results: " + str(NAdict[field]))).grid(row=count, column=2,pady=5, padx=1)

            count += 1
            temp_count = False
            if len(fields[:self.x2])/45 > 1:
                Button(body2, text='Previous Page',
                       command=(lambda e=set_info: self.update_column_win(body, e, key, func='prev'))).grid(row=count,
                                                                                                              column=1,
                                                                                                              padx=1)
                temp_count = True
            if len(fields) > len(fields[:self.x2]):
                Button(body2, text='Next Page',
                       command=(lambda e=set_info: self.update_column_win(body,e, key, func='next'))).grid(row=count,
                                                                                  column=2, padx=1)
                temp_count = True
            if temp_count == True:
                count += 1
            Button(body2, text="Reset Items",
                   command=(lambda e="nothing": self.update_entry(root, e, self.ents2, 2))).grid(row=count,
                                                                                                 column=1,padx=1)
            Button(body2, text="Exit", command=(lambda e=root: e.destroy())).grid(row=count, column=2,pady=5, padx=1)
            body2.update()
            root.mainloop()
        elif func == 6:
            self.entries = []
            for field in fields:
                temp_field = field.split('/')
                new_field = temp_field[(len(temp_field) - 1)]
                row = Frame(root)
                lab = Label(row, width=15, text=new_field, anchor='w')
                ent2 = Entry(row, width=2)
                lab.pack(side=LEFT)
                row.pack(side=TOP, fill=X, padx=5, pady=2)
                ent2.pack(side=RIGHT)
                self.entries.append((field, ent2))
            return self.entries
        elif func == 7:
            global  opt_window, footer_1, opt_footer
            IN_or_OUT = 'File Input', 'Search Output'
            try:
                win_exists_var = Toplevel.winfo_exists(opt_window)
            except NameError:
                win_exists_var = 0

            if win_exists_var != 1:
                opt_window = Toplevel()
                opt_window.title("File_Pal_1.0")
                header = Frame(opt_window)
                body1 = Frame(opt_window)
                footer_1 = Frame(opt_window)
                variable = StringVar(header)
                variable.set('Click Here')
                w = OptionMenu(header, variable, *IN_or_OUT)
                header.pack()
                variable.trace("w", partial(self.changed_1, widget=variable))
                w.pack(padx=20)
                Label(body1, text=' --- Options --- ').pack()
                body1.pack()
                opt_window.mainloop()
        elif func == 8:
            self.entries = []
            gen_opts = 'Delimiter', 'Terminator', 'Header Line', 'Index Column', 'Chunk', 'CPU Cores', 'Verbose',\
                       'Header Func', 'Main Win Criteria'
            gen_def = {'Delimiter':',','Terminator':'DV', 'Header Line':'DV', 'Index Column':'DV',
                       'Chunk':'DV', 'CPU Cores':1, 'Verbose':0}
            var_file = shelve.open('var_file')
            temp_dict ={}
            try:
                rules = var_file['opt_gen_rules']
                for gen_set in rules:
                    if gen_set[0] == 'Delimiter':
                        temp_dict['Delimiter'] = gen_set[1]
                    elif gen_set[0] == 'Terminator':
                        temp_dict['Terminator'] = gen_set[1]
                    elif gen_set[0] == 'Header Line':
                        temp_dict['Header Line'] = gen_set[1]
                    elif gen_set[0] == 'Index Column':
                        temp_dict['Index Column'] = gen_set[1]
                    elif gen_set[0] == 'Chunk':
                        temp_dict['Chunk'] = gen_set[1]
                    elif gen_set[0] == 'CPU Cores':
                        temp_dict['CPU Cores'] = gen_set[1]
                    elif gen_set[0] == 'Verbose':
                        temp_dict['Verbose'] = gen_set[1]
                    elif gen_set[0] == 'Header Func':
                        temp_dict['Header Func'] = gen_set[1]
                    elif gen_set[0] == 'Main Win Criteria':
                        temp_dict['Main Win Criteria'] = gen_set[1]
            except KeyError:
                pass

            var_file.close()
            for opt in gen_opts:
                if opt != 'Verbose' and opt != 'Header Func' and opt != 'Main Win Criteria':
                    row = Frame(opt_footer)
                    lab = Label(row, width=12, text=opt, anchor='w')
                    ent = Entry(row, width=3)
                    row.pack(side=TOP, fill=X, padx=5, pady=2)
                    lab.pack(side=LEFT)
                    ent.pack(side=RIGHT, expand=YES, fill=X)

                    if opt in temp_dict:
                        ent.insert(0, temp_dict[opt])
                    elif opt in gen_def:
                        ent.insert(0, gen_def[opt])
                    self.entries.append((opt, ent))
                else:
                    row = Frame(opt_footer)
                    var1 = IntVar()
                    if opt == 'Header Func':
                        var1.trace("w", partial(self.changed_4,root=opt_footer, var=var1))
                    ent = Checkbutton(row, text=opt, variable=var1)
                    if opt in temp_dict:
                        var1.set(temp_dict[opt])
                    elif opt in gen_def:
                        var1.set(gen_def[opt])
                    row.pack(side=TOP, fill=X, padx=5, pady=2)
                    ent.pack(side=RIGHT)

                    self.entries.append((opt, (var1)))

            last_row = Frame(opt_footer)
            sec_last_row = Frame(opt_footer)
            bload = Button(last_row, text='Save Changes',
                           command=(lambda e='dont get lambda': self.opt_rule()))
            bload.pack(side=RIGHT)
            breset = Button(sec_last_row, text='Reset',
                           command=(lambda e='dont get lambda': self.opt_rule(2)))
            breset.pack(side=RIGHT)
            sec_last_row.pack()
            last_row.pack()
            return self.entries
        elif func == 11:
            self.entries = []
            for i in range(fields):
                row = Frame(root)
                mid_row = Frame(root)
                lab = Label(row, width=7, text="Header", anchor='w')
                ent = Entry(row, width=10)
                lab2 = Label(row, width=7, text="Item(s)", anchor='w')
                ent2 = Entry(row, width=10)
                row.pack(side=TOP, fill=X, padx=5, pady=4)
                lab.pack(side=LEFT)
                ent.pack(side=LEFT)
                lab2.pack(side=LEFT)
                ent2.pack(side=LEFT)
                if i < (fields-1):
                    lab = Label(mid_row, width=7, text="And", anchor='w')
                    lab.pack(side=LEFT)
                    mid_row.pack()
                self.entries.append(('Header To Search', ent))
                self.entries.append(('  Search Item(s)',ent2))
            return self.entries
        elif func == 9:
            IN_OPTIONS = NAdict['in_list']
            header = Frame(footer_1)
            body = Frame(footer_1)
            opt_footer = Frame(footer_1)
            variable = StringVar(header)
            variable.set('Click Here')
            w = OptionMenu(header, variable, *IN_OPTIONS)
            header.pack()
            variable.trace("w", partial(NAdict['change_func'], widget=variable))
            w.pack()
            body.pack()
        elif func == 10:
            var_file = shelve.open('var_file')
            try:
                dir_loc = var_file['dir_location']
            except KeyError:
                dir_loc = os.getcwd()
            try:
                glob_dec_place = var_file['glob_dec_place']
            except KeyError:
                glob_dec_place = False
            try:
                font_type_size = var_file['font_rules']
            except KeyError:
                font_type_size = {}
            var_file.close()
            row1 = Frame(opt_footer)
            lab = Label(row1, width=8, text='Font Style', anchor='w')
            ent = Entry(row1, width=8)
            lab.pack(side=LEFT)
            ent.pack(side=LEFT)
            lab1 = Label(row1, width=7, text='Font Size', anchor='w')
            ent1 = Entry(row1, width=2)
            lab1.pack(side=LEFT)
            ent1.pack(side=LEFT)
            lab2 = Label(row1, width=11, text='Decimal Places', anchor='w')
            ent2 = Entry(row1, width=2)
            lab2.pack(side=LEFT)
            ent2.pack(side=LEFT)
            row1.pack(side=TOP, padx=5, pady=2)
            if font_type_size != {}:
                ent.insert(0,(str(list(font_type_size.keys())[0])))
                ent1.insert(0,(str(list(font_type_size.values())[0])))
            if glob_dec_place != False:
                ent2.insert(0,(str(glob_dec_place)))
            row2 = Frame(opt_footer)
            bsave = Button(row2, text='Save Changes',
                           command=(lambda e='dont get lambda': self.save_font(ent, ent1,ent2)))
            bsave.pack(side=LEFT)
            bexport = Button(row2, text='Export Settings',
                           command=(lambda e='dont get lambda': self.exp_imp_sets(row2,dir_loc,2)))
            bexport.pack(side=LEFT)
            bimport = Button(row2, text='Import Settings',
                           command=(lambda e='dont get lambda': self.exp_imp_sets(row2,dir_loc)))
            bimport.pack(side=LEFT)
            row2.pack()

            last_row = Frame(opt_footer)
            bchange_dir = Button(last_row, text='Output Dir',
                           command=(lambda e='dont get lambda': self.update_dir(last_row,opt_footer)))
            bchange_dir.pack(side=LEFT)

            Label(last_row, text=dir_loc, anchor='w').pack()
            last_row.pack(fill=X)
        elif func == 14:
            row = Frame(opt_footer)
            row2 = Frame(opt_footer)
            self.footer = Frame(opt_footer)
            lab = Label(row2, text=NAdict['label'])
            ent = Entry(row, width=13)
            variable = StringVar(row)
            bsave = Button(row, text=NAdict['but_name'],
                           command=(lambda e='nothin': self.but_func(ent, opt_footer, NAdict['dict/list'],
                                                                          NAdict['reset_l_func'],variable)))
            row.pack(side=TOP, fill=X, padx=5, pady=2)
            row2.pack(side=TOP, fill=X, padx=5, pady=2)
            lab.pack(side=TOP)
            bsave.pack(side=LEFT)
            ent.pack(side=LEFT)
            if NAdict['list_opts'] != []:
                variable.set(NAdict['list_opts'][0])
                w = OptionMenu(row, variable, *NAdict['list_opts'])
                w.pack(side=LEFT)

            var_file = shelve.open('var_file')
            try:
                rules = var_file[NAdict['dict/list']]
                self.print_lab(rules, func=NAdict['reset_l_func'])
                breset = Button(self.footer, text='Reset List',
                                command=(lambda e='what this': self.reset_col_list(func=NAdict['reset_l_func'])))
                breset.pack()
            except KeyError:
                pass
                #print('Default rules')
            var_file.close()
            self.footer.pack()
            return 'usecols', ent

    def update_entry(self, root, set_info, field_to_update, func=0):
        if func == 1:
            try:
                field_to_update.delete(0, END)
                field_to_update.insert(0, (str(set_info)))
            except:
                print('error at update_entry')
            root.destroy()
        elif func == 2:
            field_to_update.delete(0, END)
        else:
            field_to_update.insert(0, (str(set_info) + "\t"))

    def update_column_win(self, root, set_info, key, func=0):
        global opt_window
        self.ents1.delete(0, END)
        self.ents1.insert(0, (str(set_info)))
        self.ents2.delete(0, END)
        root.destroy()
        body = Frame(opt_window)
        temp_field = key.split('/')
        new_field = temp_field[(len(temp_field) - 1)]
        opt_window.title(new_field + ' / ' + str(set_info))
        scrollable_body = Scrollable(body)
        body.pack()
        count_dict = {}
        slimmed_list = []
        data = self.li[self.li_dict[key]]
        num = data[set_info].values
        if func == 'next':
            self.x += 45
            self.x2 += 45
        elif func == 'prev':
            self.x -= 45
            self.x2 -=45
        else:
            self.x = 0
            self.x2 = 45
        for value in num:
            try:
                count_dict[value] += 1
            except KeyError:
                count_dict[value] = 1
        for key1, value in sorted(count_dict.items(), key=lambda item: item[1])[::-1]:
            slimmed_list.append(key1)
        self.make(opt_window, slimmed_list, 4, body=body, body2=scrollable_body, key=key, set_info=set_info, NAdict=count_dict)

    def headers_option_button(self, key, root=None, func=0):
        global opt_window
        field = (self.li[self.li_dict[key]]).columns.values
        temp_field = key.split('/')
        new_field = temp_field[(len(temp_field) - 1)]
        if root is not None:
            root.destroy()
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
            self.x += 45
            self.x2 += 45
        elif func == 'prev':
            self.x -= 45
            self.x2 -= 45
        else:
            self.x = 0
            self.x2 = 45

        self.make(opt_window, field, 3, body=body, body2=scrollable_body, key=key)

    def opt_rule(self, func=1):
        var_file = shelve.open('var_file')
        rules = []
        if func == 1:
            for entry in self.entries:
                rules.append((entry[0],entry[1].get()))
            var_file['opt_gen_rules'] = rules
        else:
            try:
                del var_file['opt_gen_rules']
            except KeyError:
                print('Already set to defaults.')
        var_file.close()

    def changed_1(self,*args, widget=None):
        global footer_1, opt_window, inp_ents, opt_footer
        # might need try except here
        footer_1.pack_forget()
        footer_1.destroy()
        footer_1 = Frame(opt_window)
        try:
            opt_footer.pack_forget()
            opt_footer.destroy()
            opt_footer = Frame(opt_window)
        except NameError:
            pass
        supply_dict = {}
        if widget.get() == 'File Input':
            supply_dict['in_list'] = 'General', 'Set Col DataType'#, 'Specify Columns'
            supply_dict['change_func'] = self.changed_2
            inp_ents = self.make(footer_1, func=9, NAdict=supply_dict)
        elif widget.get() == 'Search Output':
            supply_dict['in_list'] = 'General', 'Column Lead Zeros', 'Column Spacing', 'Round Decimal Place'
            supply_dict['change_func'] = self.changed_3
            inp_ents = self.make(footer_1, func=9, NAdict=supply_dict)
        footer_1.pack()

    def changed_2(self,*args, widget=None):
        global opt_footer, opt_window, inp_ents
        # might need try except here
        opt_footer.pack_forget()
        opt_footer.destroy()
        opt_footer = Frame(opt_window)
        if widget.get() == 'General':
            inp_ents = self.make(opt_footer, func=8)
        elif widget.get() == 'Specify Columns': #
            supply_dict = {}
            supply_dict['label'] = 'Load only columns with the headers'
            supply_dict['but_name'] = 'Add Column: '
            supply_dict['list_opts'] = []
            supply_dict['dict/list'] = 'spec_col_rules'
            supply_dict['reset_l_func'] = 1
            inp_ents = self.make(opt_footer, func=14, NAdict=supply_dict)
        elif widget.get() == 'Set Col DataType':
            supply_dict = {}
            supply_dict['label'] = 'Saved Column/Datatype Rules'
            supply_dict['but_name'] = 'Add Col/Dtype:'
            supply_dict['list_opts'] = 'Text', 'Text'#, 'Number'
            supply_dict['dict/list'] = 'col_dtypes'
            supply_dict['reset_l_func'] = 2
            inp_ents = self.make(opt_footer, func=14, NAdict=supply_dict)
        opt_footer.pack()

    def changed_3(self,*args, widget=None):
        global opt_footer, opt_window, inp_ents
        # might need try except here
        opt_footer.pack_forget()
        opt_footer.destroy()
        opt_footer = Frame(opt_window)
        if widget.get() == 'General':
            inp_ents = self.make(opt_footer, func=10)
        elif widget.get() == 'Column Lead Zeros':
            supply_dict = {}
            supply_dict['label'] = 'Saved Column/Lead Zero Rules'
            supply_dict['but_name'] = 'Col Name/# 0\'s'
            supply_dict['list_opts'] = list(range(25))
            supply_dict['dict/list'] = 'lead_zeroes'
            supply_dict['reset_l_func'] = 4
            inp_ents = self.make(opt_footer, func=14, NAdict=supply_dict)
        elif widget.get() == 'Column Spacing':
            supply_dict = {}
            supply_dict['label'] = 'Saved Column/Width Rules'
            supply_dict['but_name'] = 'Col Index/Width'
            supply_dict['list_opts'] = list(range(25))
            supply_dict['dict/list'] = 'col_spacing'
            supply_dict['reset_l_func'] = 3
            inp_ents = self.make(opt_footer, func=14, NAdict=supply_dict)
        elif widget.get() == 'Round Decimal Place':
            supply_dict = {}
            supply_dict['label'] = 'Saved Decimal Place Rules'
            supply_dict['but_name'] = 'Col Index/Decimals'
            supply_dict['list_opts'] = 'tenths', 'hundredths', 'thousandths', '10 thousandths',\
                                       '100 thousandths', 'millionths'
            supply_dict['dict/list'] = 'decimal_places'
            supply_dict['reset_l_func'] = 5
            inp_ents = self.make(opt_footer, func=14, NAdict=supply_dict)
        opt_footer.pack()

    def changed_4(self,*args,root=None, var=None):
        self.footer = Frame(root)
        var_file = shelve.open('var_file')
        try:
            state = var_file['head_func_state']
        except KeyError:
            state = 0
        var_file['head_func_state'] = var.get()
        if var.get() == 0:
            temp_r_list = []
            rules = var_file['opt_gen_rules']
            for rule in rules:
                if rule[0] != 'Header Func':
                    temp_r_list.append((rule[0], rule[1]))
                else:
                    temp_r_list.append((rule[0], 0))
            var_file['opt_gen_rules'] = temp_r_list
        else:
            if state != 1:
                file_w_headers = filedialog.askopenfilename(parent=self.footer,
                                                            initialdir=os.getcwd(),
                                                            title="Example File with Col headers starting at A1 for logic:",
                                                            filetypes=self.my_filetypes)
                if file_w_headers[-4:] == '.csv':
                    header_data = pd.read_csv(file_w_headers, nrows=150)
                    col_vals = header_data.columns.values
                    for col in col_vals:
                        self.header_dtypes[col.strip()] = header_data[col].dtype
                    var_file['head_func_types'] = self.header_dtypes
                    print(var_file['head_func_types'])
                elif file_w_headers[-3:] == '.h5':
                    header_data = pd.read_hdf(file_w_headers, stop=150)
                    col_vals = header_data.columns.values
                    for col in col_vals:
                        self.header_dtypes[col.strip()] = header_data[col].dtype
                    var_file['head_func_types'] = self.header_dtypes
                    print(var_file['head_func_types'])
                elif ((file_w_headers[-4:])[:3] == 'xls') or (file_w_headers[-4:] == '.xls'):
                    if file_w_headers[:2] != '~$':
                        header_data = pd.read_excel(file_w_headers, sheet_name=0, nrows=150)
                        col_vals = header_data.columns.values
                        for col in col_vals:
                            self.header_dtypes[col.strip()] = header_data[col].dtype
                        var_file['head_func_types'] = self.header_dtypes
                        print(var_file['head_func_types'])
                else:
                    var.set(0)
                    messagebox.showinfo('Error', 'Not a valid file type.')
                    var_file['head_func_state'] = 0
        var_file.close()
        #print(self.header_dtypes)

    def reset_defaults(self):
        var_file = shelve.open('var_file')
        try:
            del var_file['opt_gen_rules']
        except KeyError:
            pass
        #try:
        #    del var_file['spec_col_rules']
        #except KeyError:
        #    pass
        var_file.close()

    def but_func(self, ent, root, lisct,func_num, var=None):
        self.footer.pack_forget()
        self.footer.destroy()
        self.footer = Frame(root)
        var_file = shelve.open('var_file')
        try:
            rules = var_file[lisct]
        except KeyError:
            if func_num != 1:
                rules = {}
            else:
                rules = []

        if func_num == 5:
            if ent.get() not in rules:
                if var.get() == 'tenths':
                    dec_format = '0.0'
                elif var.get() == 'hundredths':
                    dec_format = '0.00'
                elif var.get() == 'thousandths':
                    dec_format = '0.000'
                elif var.get() == '10 thousandths':
                    dec_format = '0.0000'
                elif var.get() == '100 thousandths':
                    dec_format = '0.00000'
                elif var.get() == 'millionths':
                    dec_format = '0.000000'
                rules[ent.get()] = dec_format
        elif func_num != 1:
            if ent.get() not in rules:
                rules[ent.get()] = var.get()
        else:
            rules.append(ent.get())
        var_file[lisct] = rules
        var_file.close()
        self.print_lab(rules,func_num)
        breset = Button(self.footer, text='Reset List',
                        command=(lambda e='what this': self.reset_col_list(func=func_num)))
        breset.pack(side=RIGHT)
        self.footer.pack()

    def reset_col_list(self, func=1):
        try:
            var_file = shelve.open('var_file')
            if func == 2:
                del var_file['col_dtypes']
            elif func == 3:
                del var_file['col_spacing']
            elif func == 4:
                del var_file['lead_zeroes']
            elif func == 5:
                del var_file['decimal_places']
            else:
                del var_file['spec_col_rules']
            var_file.close()
            self.footer.pack_forget()
            self.footer.destroy()
        except KeyError:
            print('No settings in list')

    def print_lab(self,rules, func=1):
        dict_funcs = 2, 3, 4, 5
        if func in dict_funcs:
            for key, value in rules.items():
                text_var = key.strip() + " : " + value
                row = Frame(self.footer)
                lab = Label(row, text=text_var, anchor='w')
                row.pack(side=TOP, fill=X, padx=5, pady=2)
                lab.pack(side=LEFT)
        else:
            for i in rules:
                row = Frame(self.footer)
                lab = Label(row, text=i, anchor='w')
                row.pack(side=TOP, fill=X, padx=5, pady=2)
                lab.pack(side=LEFT)

    def save_font(self, style, size, glob_dec_place):
        var_file = shelve.open('var_file')
        var_file['font_rules'] = {style.get(): size.get()}
        var_file['glob_dec_place'] = glob_dec_place.get()
        var_file.close()

    def donothing(self):
        x = 0
        return x

    def update_dir(self, root, roots_root):
        directory = filedialog.askdirectory(parent=root,
                                            initialdir=os.getcwd(),
                                            title="Please select Directory:")
        root.pack_forget()
        root.destroy()
        root = Frame(roots_root)
        var1_file = shelve.open('var_file')
        var1_file['dir_location'] = directory
        var1_file.close()
        bchange_dir = Button(root, text='Output Dir',
                             command=(lambda e='dont get lambda': self.update_dir(root, roots_root)))
        bchange_dir.pack(side=LEFT)

        Label(root, text=directory, anchor='w').pack()
        root.pack()

    def exp_imp_sets(self,root, dir, func=1):
        my_filetypes = [('Text Documents', '.txt')]
        if func == 1:
            eltit = "Select saved file:"
            edom = 'r'
            place_holda = filedialog.askopenfilename
        else:
            eltit = "Save as:"
            edom = 'w'
            place_holda = filedialog.asksaveasfile

        file_w_headers = place_holda(parent=root, initialdir=dir, title=eltit, filetypes=my_filetypes)
        if func == 1:
            file_name = file_w_headers
        else:
            file_name =file_w_headers.name
            file_w_headers.close()
        setting_file = open(file_name,edom)
        var_file = shelve.open('var_file')
        rule_list = []
        if func == 1:
            space_dict = {}
            zero_dict = {}
            font_dict = {}
            dec_dict = {}
            glob_dec = False
            lines = setting_file.readlines()
            for line in lines:
                new_list = re.split('::::', line)
                if new_list[0] == 'col_spacing':
                    space_dict[new_list[1]] = new_list[2].strip()
                elif new_list[0] == 'lead_zeroes':
                    zero_dict[new_list[1]] = new_list[2].strip()
                elif new_list[0] == 'font_rules':
                    font_dict[new_list[1]] = new_list[2].strip()
                elif new_list[0] == 'decimal_places':
                    dec_dict[new_list[1]] = new_list[2].strip()
                elif new_list[0] == 'glob_dec_place':
                    glob_dec = new_list[1]
            var_file['col_spacing'] = space_dict
            var_file['lead_zeroes'] = zero_dict
            var_file['font_rules'] = font_dict
            var_file['decimal_places'] = dec_dict
            var_file['glob_dec_place'] = glob_dec
        else:
            try:
                col_width = var_file['col_spacing']
                for col, val in col_width.items():
                    rule_list.append('col_spacing'+ '::::' + col + '::::' + str(val) + '\n')
            except KeyError:
                pass
            try:
                zeros_dict = var_file['lead_zeroes']
                for col, val in zeros_dict.items():
                    rule_list.append('lead_zeroes'+ '::::' + col + '::::' + str(val) + '\n')
            except KeyError:
                pass
            try:
                font_rules = var_file['font_rules']
                rule_list.append('font_rules' + '::::' + list(font_rules.keys())[0] + '::::' +
                                 str(list(font_rules.values())[0]) + '\n')
            except KeyError:
                pass
            try:
                dec_places = var_file['decimal_places']
                rule_list.append('decimal_places' + '::::' + list(dec_places.keys())[0] + '::::' +
                                 str(list(dec_places.values())[0]) + '\n')
            except KeyError:
                pass
            try:
                glob_dec_places = var_file['glob_dec_place']
                rule_list.append('glob_dec_place' + '::::' + str(glob_dec_places) + '\n')
            except KeyError:
                pass
            setting_file.writelines(rule_list)

        var_file.close()
        setting_file.close()

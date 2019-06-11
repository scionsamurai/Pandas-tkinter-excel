from tkinter import *
from scrollbarClass import Scrollable
import shelve, os, sys, re
import pandas as pd
from functools import partial
class MakeForm:
    def __init__(self, data_frames=[], frame_keys={},input_box1=False, input_box2=False):
        self.entries = []
        self.entries2 = {}
        self.li = data_frames
        self.li_dict = frame_keys
        self.ents1 = input_box1
        self.ents2 = input_box2
        self.footer = False
        self.header_dtypes = {}
        self.my_filetypes = [('all files', '.*'), ('CSV files', '.csv'),('HD5', '.h5'),('xls','.xls')]
        self.NA_dict = {}

    def make(self, root=None, fields=[], func=0,body=False, key=False, set_info=False, NAdict={}):
        if func == 1:
            self.entries = []
            fields = 'Header To Search', '  Search Item(s)'  # , 'Output Directory'
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
            self.entries2 = {}
            scrollable_body = Scrollable(body)
            count = 0
            for f in fields:
                count += 1
                row1 = len(self.entries2)
                b1 = Button(scrollable_body, text=f,
                            command=(lambda e=f: self.update_entry(root, e, self.ents1, 1))).grid(row=row1, column=1,
                                                                                                  padx=1)
                Button(scrollable_body, text='Result\'s within Column',
                       command=(lambda e=f: self.update_column_win(root,
                                                                   e, key))).grid(row=row1,
                                                                                  column=2,  padx=1)
                self.entries2[f] = b1
                if count > 50:
                    break
            Button(scrollable_body, text="Exit", command=(lambda e=root: e.destroy())).grid(column=2)
            scrollable_body.update()
            root.mainloop()
            return self.entries2
        elif func == 4:
            scrollable_body = Scrollable(body)
            count_dict = {}
            slimmed_list = []
            count = 0
            data = self.li[self.li_dict[key]]
            num = data[set_info].values
            for value in num:
                try:
                    count_dict[value] += 1
                except KeyError:
                    count_dict[value] = 1
            for key1, value in sorted(count_dict.items(), key=lambda item: item[1])[::-1]:
                slimmed_list.append(key1)
                count += 1
                if count > 50:
                    break
            for field in slimmed_list:
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

                row1 = len(self.entries2)
                b1 = Button(scrollable_body, text=new_field,
                            command=(lambda e=field: self.update_entry(root, e, self.ents2))).grid(row=row1, column=1,
                                                                                                padx=1)
                Label(scrollable_body, width=15,
                      text=("Total Results: " + str(count_dict[field]))).grid(row=row1, column=2, columnspan=25,pady=5, padx=1)
                self.entries2[field] = b1
            Button(scrollable_body, text="Reset Items",
                   command=(lambda e="nothing": self.update_entry(root, e, self.ents2, 2))).grid(column=1)
            Button(scrollable_body, text="Exit", command=(lambda e=root: e.destroy())).grid(column=2)
            scrollable_body.update()
            root.mainloop()
            return self.entries2
        elif func == 5:
            global headers_window
            try:
                win_exists_var = Toplevel.winfo_exists(headers_window)
            except NameError:
                win_exists_var = 0
            if win_exists_var != 1:
                headers_window = Toplevel()
                headers_window.title('Output File Options')
                header = Frame(headers_window)
                body = Frame(headers_window)
                footer = Frame(headers_window)
                row = Frame(header)
                Label(header, text=' --- Text Rule --- ').pack()
                lab = Label(row, width=10, text='Column(s)')
                ent = Entry(row, width=3)
                lab2 = Label(row, width=9, text='Col Width')
                ent2 = Entry(row, width=2)
                lab4 = Label(row, width=5, text='Size')
                ent4 = Entry(row, width=3)
                row.pack(side=TOP, fill=X, padx=5, pady=2)
                lab.pack(side=LEFT)
                ent.pack(side=LEFT)
                lab2.pack(side=LEFT)
                ent2.pack(side=LEFT)
                lab4.pack(side=LEFT)
                ent4.pack(side=LEFT)
                header.pack()
                body.pack()

                footer.pack()
                row3 = Frame(body)
                lab6 = Label(row3, width=10, text='Font Style')
                ent6 = Entry(row3, width=13)
                row3.pack(fill=X, padx=5, pady=2)
                row2 = Frame(body)
                Label(body, text=' --- Leading Zeros Rule --- ').pack()
                lab3 = Label(row2, width=10, text='Col Header')
                ent3 = Entry(row2, width=13)
                lab3_1 = Label(row2, width=8, text='Total #s')
                ent3_1 = Entry(row2, width=2)
                lab3.pack(side=LEFT)
                ent3.pack(side=LEFT)
                lab3_1.pack(side=LEFT)
                ent3_1.pack(side=LEFT)
                row2.pack(fill=X, padx=5, pady=2)
                lab6.pack(side=LEFT)
                ent6.pack(side=LEFT)
                row4 = Frame(footer)
                b1 = Button(row4, text='Add Rule',
                            command=(lambda e='nothin': self.add_rule('rules', ent, ent2, ent3, ent6, ent4, ent3_1)))
                row4.pack(fill=X, padx=5, pady=2)
                breset = Button(row4, text='Reset Rule(s)',
                                command=(lambda e='dont get lambda': self.reset_rules('rules')))
                breset.pack(side=RIGHT)
                rprint = Button(row4, text='Print Rule(s)',
                                command=(lambda e='what this': self.print_rules('rules')))
                rprint.pack(side=RIGHT)
                b1.pack(side=LEFT)
                var_file = shelve.open('var_file')
                try:
                    last_loc = var_file['rules_location']
                except KeyError:
                    last_loc = ''
                try:
                    dir_loc = var_file['dir_location']
                except KeyError:
                    dir_loc = ''
                var_file.close()
                row5 = Frame(footer)
                lab5 = Label(row5, width=10, text='Rules Dir')
                ent5 = Entry(row5)
                lab5.pack(side=LEFT)
                ent5.pack(side=LEFT)
                ent5.insert(0, last_loc)
                row5.pack(fill=X, padx=5, pady=2)
                row6 = Frame(footer)
                row6.pack(fill=X, padx=5, pady=2)
                breset = Button(row6, text='Open Rule(s)',
                                command=(lambda e='dont get lambda': self.get_rules(ent5)))
                breset.pack(side=RIGHT)
                rprint = Button(row6, text='Save Rule(s)',
                                command=(lambda e='what this': self.save_rules(ent5)))
                rprint.pack(side=RIGHT)
                row7 = Frame(footer)
                lab7 = Label(row7, width=10, text='Output Dir')
                ent7 = Entry(row7)
                lab7.pack(side=LEFT)
                ent7.pack(side=LEFT)
                ent7.insert(0, dir_loc)
                row7.pack(fill=X, padx=5, pady=2)
                row8 = Frame(footer)
                row8.pack(fill=X, padx=5, pady=2)
                breset = Button(row8, text='Save Output Dir',
                                command=(lambda e='dont get lambda': self.save_dir(ent7)))
                breset.pack(side=RIGHT)

                headers_window.mainloop()
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
            global opt_footer, opt_window
            IN_OPTIONS = 'General', 'Specify Columns', 'Set Col DataType'
            try:
                win_exists_var = Toplevel.winfo_exists(opt_window)
            except NameError:
                win_exists_var = 0

            if win_exists_var != 1:
                opt_window = Toplevel()
                opt_window.title("File_Pal_1.0")
                header = Frame(opt_window)
                body = Frame(opt_window)
                opt_footer = Frame(opt_window)
                variable = StringVar(header)
                variable.set('Click Here')
                w = OptionMenu(header, variable, *IN_OPTIONS)
                Label(header, text="Input Options").pack()
                row2 = Frame(opt_window)
                breset = Button(row2, text='Default Value\'s',
                                command=(lambda e='what this': self.reset_defaults()))
                breset.pack(side=RIGHT)
                row2.pack(padx=20)
                header.pack()
                variable.trace("w", partial(self.changed, widget=variable))
                w.pack()
                body.pack()
                opt_window.mainloop()
        elif func == 8:
            gen_opts = 'Delimiter', 'Terminator', 'Header Line', 'Index Column', 'Chunk', 'CPU Cores', 'Verbose',\
                       'Header Func'
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
            except KeyError:
                print('Default rules')

            var_file.close()
            for opt in gen_opts:
                if opt != 'Verbose' and opt != 'Header Func':
                    row = Frame(root)
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
                    row = Frame(root)
                    var1 = IntVar()
                    if opt == 'Header Func':
                        var1.trace("w", partial(self.changed2,root=root, var=var1))
                    ent = Checkbutton(row, text=opt, variable=var1)
                    if opt in temp_dict:
                        var1.set(temp_dict[opt])
                    elif opt in gen_def:
                        var1.set(gen_def[opt])
                    row.pack(side=TOP, fill=X, padx=5, pady=2)
                    ent.pack(side=RIGHT)

                    self.entries.append((opt, (var1)))

            last_row = Frame(root)
            bload = Button(last_row, text='Save Changes',
                           command=(lambda e='dont get lambda': self.opt_rule()))
            bload.pack(side=RIGHT)
            last_row.pack()
            return self.entries
        elif func == 9:
            row = Frame(root)
            row2 = Frame(root)
            self.footer = Frame(root)
            lab = Label(row2, text='Load only columns with the headers ')
            ent = Entry(row, width=25)
            bsave = Button(row, text='Add Column: ',
                           command=(lambda e='nothin': self.add_column(ent, root)))
            row.pack(side=TOP, fill=X, padx=5, pady=2)
            row2.pack(side=TOP, fill=X, padx=5, pady=2)
            lab.pack(side=TOP)
            bsave.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            var_file = shelve.open('var_file')
            rules = []
            try:
                rules = var_file['spec_col_rules']
            except KeyError:
                print('Default rules')
            var_file.close()
            for i in rules:
                row = Frame(self.footer)
                lab = Label(row, text=i, anchor='w')
                row.pack(side=TOP, fill=X, padx=5, pady=2)
                lab.pack(side=LEFT)
            breset = Button(self.footer, text='Reset List',
                            command=(lambda e='what this': self.reset_col_list()))
            breset.pack()
            self.footer.pack()

            return ('usecols', ent)
        elif func == 10:
            IN_TYPES = 'Text', 'Number'
            row = Frame(root)
            row2 = Frame(root)
            self.footer = Frame(root)
            lab = Label(row2, text='Saved Column/Datatype Rules')
            ent = Entry(row, width=13)
            variable = StringVar(row)
            bsave = Button(row, text='Add Col/Dtype:',
                           command=(lambda e='nothin': self.col_dtype(ent,variable, root)))
            variable.set('Text')
            w = OptionMenu(row, variable, *IN_TYPES)
            row.pack(side=TOP, fill=X, padx=5, pady=2)
            row2.pack(side=TOP, fill=X, padx=5, pady=2)
            lab.pack(side=TOP)
            bsave.pack(side=LEFT)
            ent.pack(side=LEFT)
            w.pack(side=LEFT)

            var_file = shelve.open('var_file')
            rules = []
            try:
                rules = var_file['col_dtypes']
                for key, value in rules.items():
                    text_var = key.strip() + " : " + value
                    row = Frame(self.footer)
                    lab = Label(row, text=text_var, anchor='w')
                    row.pack(side=TOP, fill=X, padx=5, pady=2)
                    lab.pack(side=LEFT)
                breset = Button(self.footer, text='Reset List',
                                command=(lambda e='what this': self.reset_col_list(func=2)))
                breset.pack()
            except KeyError:
                print('Default rules')
            var_file.close()
            self.footer.pack()
            return ('usecols', ent)
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

    def update_column_win(self, root, set_info, key):
        self.ents1.delete(0, END)
        self.ents1.insert(0, (str(set_info)))
        self.ents2.delete(0, END)
        root.destroy()
        self.entries2 = {}
        headers_window = Toplevel()
        headers_window.title(key)
        results = (self.li[self.li_dict[key]][set_info]).values
        new_string = list(dict.fromkeys(results))
        header = Frame(headers_window)
        body = Frame(headers_window)
        footer = Frame(headers_window)
        header.pack()
        body.pack()
        footer.pack()
        Label(header, text="Results").pack()
        Label(footer, text="Results Footer").pack()

        self.make(headers_window,
                  new_string, 4, body=body, key=key,
                  set_info=set_info)

    def headers_option_button(self, key):
        field = (self.li[self.li_dict[key]]).columns.values
        headers_window = Toplevel()
        headers_window.title(key)
        header = Frame(headers_window)
        body = Frame(headers_window)
        footer = Frame(headers_window)
        header.pack()
        body.pack()
        footer.pack()
        Label(header, text="The Header").pack()
        Label(footer, text="The Footer").pack()
        self.make(headers_window, field, 3,body=body, key=key)

    def add_rule(self,shelf_key,col,width,rule,font,font_size,rule_digits):
        var_file = shelve.open('var_file')
        try:
            rules = var_file[shelf_key]
            del var_file[shelf_key]
        except KeyError:
            print('first rule')
            rules = []
        rule_get = (rule.get()).strip()
        rules.append([col.get(),width.get(),rule_get,font.get(),font_size.get(),rule_digits.get()])
        var_file[shelf_key] = rules
        var_file.close()
        col.delete(0, END)
        width.delete(0, END)
        rule.delete(0, END)
        font.delete(0, END)
        font_size.delete(0, END)
        rule_digits.delete(0, END)

    def opt_rule(self):
        var_file = shelve.open('var_file')
        rules = []
        for entry in self.entries:
            rules.append((entry[0],entry[1].get()))
        var_file['opt_gen_rules'] = rules

        var_file.close()

    def reset_rules(self,shelf_key):
        var_file = shelve.open('var_file')
        try:
            del var_file[shelf_key]
        except KeyError:
            print('No Rules to Reset')
        var_file.close()

    def print_rules(self,shelf_key):
        var_file = shelve.open('var_file')
        try:
            for rule in var_file[shelf_key]:
                print(rule)
        except KeyError:
            print('No Rules to Print')
        var_file.close()

    def save_rules(self, file):
        var1_file = shelve.open('var_file')
        try:
            rules = var1_file['rules']
            var1_file['rules_location'] = file.get()
        except KeyError:
            print('first rule')
            rules = []
        var1_file.close()
        var_file = shelve.open(file.get())
        var_file['rules'] = rules
        print('rule set')
        var_file.close()

    def save_dir(self, file):
        var1_file = shelve.open('var_file')
        var1_file['dir_location'] = file.get()
        var1_file.close()

    def get_rules(self, file):
        var_file = shelve.open(file.get())
        try:
            rules = var_file['rules']
        except KeyError:
            print('Error')
            rules = []
        var_file.close()
        var1_file = shelve.open('var_file')
        var1_file['rules'] = rules
        var1_file.close()

    def changed(self,*args, widget=None):
        global opt_footer, opt_window, inp_ents
        # might need try except here
        opt_footer.pack_forget()
        opt_footer.destroy()
        opt_footer = Frame(opt_window)
        form3 = MakeForm()
        if widget.get() == 'General':
            inp_ents = form3.make(opt_footer, func=8)
        elif widget.get() == 'Specify Columns':
            inp_ents = form3.make(opt_footer, func=9)
        elif widget.get() == 'Set Col DataType':
            inp_ents = form3.make(opt_footer, func=10)
        else:
            print("Where'd that setting come from?")
        opt_footer.pack()

    def changed2(self,*args,root=None, var=None):
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
        try:
            del var_file['spec_col_rules']
        except KeyError:
            pass
        try:
            del var_file['col_dtypes']
        except KeyError:
            pass
        var_file.close()

    def add_column(self, ent, root):
        self.footer.pack_forget()
        self.footer.destroy()
        self.footer = Frame(root)
        var_file = shelve.open('var_file')
        rules = []
        try:
            rules = var_file['spec_col_rules']
        except KeyError:
            print('Default rules')
        rules.append(ent.get())
        rules = list(dict.fromkeys(rules))
        var_file['spec_col_rules'] = rules
        var_file.close()

        for i in rules:
            row = Frame(self.footer)
            lab = Label(row, text=i, anchor='w')
            row.pack(side=TOP, fill=X, padx=5, pady=2)
            lab.pack(side=LEFT)
        breset = Button(self.footer, text='Reset List',
                        command=(lambda e='what this': self.reset_col_list()))
        breset.pack(side=RIGHT)
        self.footer.pack()

    def col_dtype(self, ent, var, root):
        self.footer.pack_forget()
        self.footer.destroy()
        self.footer = Frame(root)
        var_file = shelve.open('var_file')
        rules = {}
        try:
            rules = var_file['col_dtypes']
        except KeyError:
            print('Default rules')
        if ent.get() not in rules:
            rules[ent.get()] =var.get()

        var_file['col_dtypes'] = rules
        var_file.close()

        print(rules)
        for key, value in rules.items():
            text_var = key.strip() + " : " + value
            row = Frame(self.footer)
            lab = Label(row, text=text_var, anchor='w')
            row.pack(side=TOP, fill=X, padx=5, pady=2)
            lab.pack(side=LEFT)
        breset = Button(self.footer, text='Reset List',
                        command=(lambda e='what this': self.reset_col_list(func=2)))
        breset.pack(side=RIGHT)
        self.footer.pack()

    def reset_col_list(self, func=1):
        try:
            if func == 2:
                var_file = shelve.open('var_file')
                del var_file['col_dtypes']
                var_file.close()
                self.footer.pack_forget()
                self.footer.destroy()
            else:
                var_file = shelve.open('var_file')
                del var_file['spec_col_rules']
                var_file.close()
                self.footer.pack_forget()
                self.footer.destroy()
        except KeyError:
            print('No settings in list')



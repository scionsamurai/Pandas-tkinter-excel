"""
Class to store tkinter Frames that don't read from df classes
"""
from tkinter import *
from _gui.scrollbarClass import Scrollable
import shelve, os, sys, tempfile
import pandas as pd
from functools import partial
from _funcs.func_file import GenFuncs
class MakeForm:
    def __init__(self, answer_in=[]):
        self.entries = []
        self.answer = answer_in
        self.footer = False
        self.header_dtypes = {}
        self.my_filetypes = [('all files', '.*'), ('CSV files', '.csv'),('HD5', '.h5'),('xls','.xls')]
        self.x = 0
        self.x2 = 45

    def make(self, root=None, fields=[], func=0, func2=0, NAdict={}):
        if func == 1:
            """
            Main window -
            :param func2: 1= Input box1 and input box2, 0 = footer Generated by resort
            :param fields: Labels for Entry boxes
            """
            self.entries = []
            for field in fields:
                row = Frame(root)
                if func2 == 1:
                    ent = Entry(row, width=2)
                    file_name = GenFuncs.strip_dir(field)
                else:
                    ent = Entry(row)
                    file_name = field
                lab = Label(row, text=file_name, anchor='w')
                row.pack(side=TOP, fill=X, padx=5, pady=2)
                lab.pack(side=LEFT)
                if func2 == 1:
                    ent.pack(side=RIGHT)
                else:
                    ent.pack(side=RIGHT, expand=YES, fill=X)
                self.entries.append((field, ent))
            return self.entries
        elif func == 2:
            """
            Options Initial window
            """
            global  opt_window, footer_1, opt_footer
            IN_or_OUT = 'File Input', 'Search Output'
            try:
                win_exists_var = Toplevel.winfo_exists(opt_window)
            except NameError:
                win_exists_var = 0
            if win_exists_var != 1:
                opt_window = Toplevel()
                opt_window.title("File_Pal_1.1")
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
        elif func == 3:
            """
            General Input Options Frame
            """
            self.entries = []
            gen_opts = 'Delimiter', 'Terminator', 'Header Line', 'Index Column', 'Chunk', 'CPU Cores', 'Verbose',\
                       'Header Func', 'Main Win Criteria'
            gen_def = {'Delimiter':',','Terminator':'DV', 'Header Line':'DV', 'Index Column':'DV',
                       'Chunk':'DV', 'CPU Cores':1, 'Verbose':0}
            temp_dict = GenFuncs.gen_set()
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
        elif func == 4:
            """
            Search Output Options Initial Frame
            :param NAdict: Options list
            """
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
        elif func == 5:
            """
            General Output Options Frame
            """
            var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
            try:
                dir_loc = var_file['dir_location']
            except KeyError:
                dir_loc = tempfile.gettempdir()
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
            if glob_dec_place != False and glob_dec_place.strip() != 'False':
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
        elif func == 6:
            """
            General options List Frame
            :param NAdict['label']: Label above list and below input field
            :param NAdict['but_name']: Button Label
            :param NAdict['list_opts']: Drop down list options
            :param NAdict['dict/list']: shelve dict/list name
            """
            row = Frame(opt_footer)
            row2 = Frame(opt_footer)
            self.footer = Frame(opt_footer)
            lab = Label(row2, text=NAdict['label'])
            ent = Entry(row, width=13)
            variable = StringVar(row)
            bsave = Button(row, text=NAdict['but_name'],
                           command=(lambda e='nothin': self.but_func(ent, opt_footer, NAdict['dict/list'],variable)))
            row.pack(side=TOP, fill=X, padx=5, pady=2)
            row2.pack(side=TOP, fill=X, padx=5, pady=2)
            lab.pack(side=TOP)
            bsave.pack(side=LEFT)
            ent.pack(side=LEFT)
            if NAdict['list_opts'] != []:
                variable.set(NAdict['list_opts'][0])
                w = OptionMenu(row, variable, *NAdict['list_opts'])
                w.pack(side=LEFT)

            var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
            try:
                rules = var_file[NAdict['dict/list']]
                self.print_lab(rules, NAdict['dict/list'])
                breset = Button(self.footer, text='Reset List',
                                command=(lambda e='what this': self.reset_col_list(NAdict['dict/list'])))
                breset.pack()
            except KeyError:
                pass
            var_file.close()
            self.footer.pack()
            return 'usecols', ent
        elif func == 7:
            """
                Generates footer Frame of main window with opened files listed.
                :param rootx: Parent Frame.
                :param fields: List of open files.
                :return: List of Files with checkbutton Status.
                """
            entries = []
            for field in fields:
                temp_field = field.split('/')
                new_field = 'Search:  ' + temp_field[(len(temp_field) - 1)]
                vrow = Frame(root)
                var1 = IntVar()
                var1.set(1)
                ent = Checkbutton(vrow, text=new_field, variable=var1)
                bx = Button(vrow, text='Headers', command=(lambda e=field: header_button(key=e)))
                vrow.pack(side=TOP, fill=X, padx=5, pady=2)
                ent.pack(side=LEFT)
                bx.pack(side=RIGHT)
                entries.append((field, ent, var1))
            return entries
        elif func == 8:
            var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
            try:
                profs = var_file['Profilez']
            except KeyError:
                profs = {}
            var_file.close()

            def save_prof(name):
                global opt_footer, inp_ents
                var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
                try:
                    space_dict = var_file['col_spacing']
                except:
                    space_dict = {}
                try:
                    zero_dict = var_file['lead_zeroes']
                except:
                    zero_dict = {}
                try:
                    font_dict = var_file['font_rules']
                except:
                    font_dict = {}
                try:
                    dec_dict = var_file['decimal_places']
                except:
                    dec_dict = {}
                try:
                    if glob_dec.strip() != 'False':
                        glob_dec = var_file['glob_dec_place']
                    else:
                        glob_dec = False
                except:
                    glob_dec = False
                profs[name.get()] = [space_dict, zero_dict, font_dict, dec_dict, glob_dec, name.get()]
                var_file['Profilez'] = profs
                var_file.close()
                opt_footer.pack_forget()
                opt_footer.destroy()
                opt_footer = Frame(opt_window)
                opt_footer.pack()
                inp_ents = self.make(opt_footer, func=8)

            def imp_prof(name):
                var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
                loadin_sets = profs[name]
                var_file['col_spacing'] = loadin_sets[0]
                var_file['lead_zeroes'] = loadin_sets[1]
                var_file['font_rules'] = loadin_sets[2]
                var_file['decimal_places'] = loadin_sets[3]
                var_file['glob_dec_place'] = loadin_sets[4]
                var_file.close()

            def del_prof(name):
                global opt_footer, inp_ents
                var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
                temp_profs = var_file['Profilez']
                del temp_profs[name]
                var_file['Profilez'] = temp_profs
                var_file.close()
                opt_footer.pack_forget()
                opt_footer.destroy()
                opt_footer = Frame(opt_window)
                opt_footer.pack()
                inp_ents = self.make(opt_footer, func=8)

            for p, v in profs.items():
                rowx = Frame(opt_footer)
                rowx.pack()
                import_settings = Button(rowx, text=v[5], command=(lambda e='dont get lambda': imp_prof(v[5])))
                import_settings.pack(side=LEFT)
                del_but = Button(rowx, text="Delete", command=(lambda e=v[5]: del_prof(e)))
                del_but.pack(side=LEFT)
            brow = Frame(opt_footer)
            brow.pack()
            lbut = Button(brow, text="Save Profile", command=(lambda e='dont get lambda': save_prof(ent2)))
            ent2 = Entry(brow, width=15)
            lbut.pack(side=LEFT)
            ent2.pack(side=LEFT)

    def opt_rule(self, func=1):
        """
        Save/Reset General Input Settings
        :param func: 1=Save 0=Reset
        """
        var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
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
        """
        Drop down menu for the Options Initial window
        :param widget: Value for Input/output option
        """
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
            inp_ents = self.make(footer_1, func=4, NAdict=supply_dict)
        elif widget.get() == 'Search Output':
            supply_dict['in_list'] = 'General', 'Column Lead Zeros', 'Column Spacing'#,\
                                     #'Round Decimal Place', 'Profiles', 
            supply_dict['change_func'] = self.changed_3
            inp_ents = self.make(footer_1, func=4, NAdict=supply_dict)
        footer_1.pack()

    def changed_2(self,*args, widget=None):
        """
        Drop down menu for the Input Options
        :param widget: Value for Selected Input option
        """
        global opt_footer, opt_window, inp_ents
        # might need try except here
        opt_footer.pack_forget()
        opt_footer.destroy()
        opt_footer = Frame(opt_window)
        if widget.get() == 'General':
            inp_ents = self.make(opt_footer, func=3)
        elif widget.get() == 'Specify Columns':
            supply_dict = {}
            supply_dict['label'] = 'Load only columns with the headers'
            supply_dict['but_name'] = 'Add Column: '
            supply_dict['list_opts'] = []
            supply_dict['dict/list'] = 'spec_col_rules'
            inp_ents = self.make(opt_footer, func=6, NAdict=supply_dict)
        elif widget.get() == 'Set Col DataType':
            supply_dict = {}
            supply_dict['label'] = 'Saved Column/Datatype Rules'
            supply_dict['but_name'] = 'Add Col/Dtype:'
            supply_dict['list_opts'] = 'Text', 'Text'#, 'Number'
            supply_dict['dict/list'] = 'col_dtypes'
            inp_ents = self.make(opt_footer, func=6, NAdict=supply_dict)
        opt_footer.pack()

    def changed_3(self,*args, widget=None):
        """
        Drop down menu for the Output Options
        :param widget: Value for Selected Output option
        """
        global opt_footer, opt_window, inp_ents
        # might need try except here
        opt_footer.pack_forget()
        opt_footer.destroy()
        opt_footer = Frame(opt_window)
        if widget.get() == 'Profiles':
            inp_ents = self.make(opt_footer, func=8)
        elif widget.get() == 'General':
            inp_ents = self.make(opt_footer, func=5)
        elif widget.get() == 'Column Lead Zeros':
            supply_dict = {}
            supply_dict['label'] = 'Saved Column/Lead Zero Rules'
            supply_dict['but_name'] = 'Col Name/# Digit\'s'
            supply_dict['list_opts'] = list(range(25))[1:]
            supply_dict['dict/list'] = 'lead_zeroes'
            inp_ents = self.make(opt_footer, func=6, NAdict=supply_dict)
        elif widget.get() == 'Column Spacing':
            supply_dict = {}
            supply_dict['label'] = 'Saved Column/Width Rules'
            supply_dict['but_name'] = 'Col Index/Width'
            supply_dict['list_opts'] = list(range(25))[1:]
            supply_dict['dict/list'] = 'col_spacing'
            inp_ents = self.make(opt_footer, func=6, NAdict=supply_dict)
        elif widget.get() == 'Round Decimal Place':
            supply_dict = {}
            supply_dict['label'] = 'Saved Decimal Place Rules'
            supply_dict['but_name'] = 'Col Index/Decimals'
            supply_dict['list_opts'] = 'tenths', 'hundredths', 'thousandths', '10 thousandths',\
                                       '100 thousandths', 'millionths'
            supply_dict['dict/list'] = 'decimal_places'
            inp_ents = self.make(opt_footer, func=6, NAdict=supply_dict)
        opt_footer.pack()

    def changed_4(self,*args,root=None, var=None):
        """
        Function selects Example file with correctly aligned header for file opening Header Verification
        :param root: Parent Frame
        :param var: Traced checkbutton variable
        """
        self.footer = Frame(root)
        var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
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

    def but_func(self, ent, root, lisct, var=None):
        """
        Add setting button Function from input/output list-like settings
        :param ent: User typed Information
        :param root: Parent Frame
        :param lisct: shelve dict/list name
        :param var: Chosen drop down variable
        """
        self.footer.pack_forget()
        self.footer.destroy()
        self.footer = Frame(root)
        var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
        try:
            rules = var_file[lisct]
        except KeyError:
            if lisct != 'spec_col_rules':
                rules = {}
            else:
                rules = []

        if lisct == 'decimal_places':
            if ent.get() not in rules and ent.get() != '':
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
                if len(ent.get().split(':')) == 2:
                    rules[ent.get().strip()] = dec_format
        elif lisct != 'spec_col_rules':
            if ent.get().strip() not in rules and ent.get() != '':
                if lisct != 'col_spacing' and lisct != 'lead_zeroes':
                    rules[ent.get().strip()] = var.get()
                elif lisct == 'lead_zeroes':
                    if len(ent.get().strip().split(':')) != 2:
                        rules[ent.get().strip()] = var.get()
                elif len(ent.get().strip().split(':')) == 2:
                    rules[ent.get().strip()] = var.get()
        else:
            rules.append(ent.get().strip())
        var_file[lisct] = rules
        var_file.close()
        self.print_lab(rules,lisct)
        breset = Button(self.footer, text='Reset List', command=(lambda e='what this': self.reset_col_list(lisct)))
        breset.pack(side=RIGHT)
        self.footer.pack()

    def reset_col_list(self, lisct):
        """
        Button that Resets Currently viewing Option List
        :param lisct: shelve dict/list name
        """
        try:
            var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
            del var_file[lisct]
            var_file.close()
            self.footer.pack_forget()
            self.footer.destroy()
        except KeyError:
            print('No settings in list')

    def print_lab(self,rules, lisct):
        """
        Refreshes List-like options footer frame
        :param rules: Dictionary of saved settings from currently list-like option currently viewing
        :param lisct: shelve dict/list name
        """
        if lisct != 'spec_col_rules':
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
        """
        Button for saving currently updated general output options
        :param style: Font Style
        :param size: Font Size
        :param glob_dec_place: Global Decimal Places
        """
        var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
        if style.get() != "":
            nstyle = style.get()
        else:
            nstyle = False
        if size.get() != "":
            nsize = size.get()
        else:
            nsize = False
        var_file['font_rules'] = {nstyle: nsize}
        if glob_dec_place.get()  != '':
            var_file['glob_dec_place'] = glob_dec_place.get()
        else:
            var_file['glob_dec_place'] = False
        var_file.close()

    def update_dir(self, root, roots_root):
        """
        General output button for changing search output Directory.
        :param root: Parent Frame
        :param roots_root: Parent Frames Parent Frame
        """
        directory = filedialog.askdirectory(parent=root,
                                            initialdir=os.getcwd(),
                                            title="Please select Directory:")
        root.pack_forget()
        root.destroy()
        root = Frame(roots_root)
        var1_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
        var1_file['dir_location'] = directory
        var1_file.close()
        bchange_dir = Button(root, text='Output Dir',
                             command=(lambda e='dont get lambda': self.update_dir(root, roots_root)))
        bchange_dir.pack(side=LEFT)

        Label(root, text=directory, anchor='w').pack()
        root.pack()

    def exp_imp_sets(self,root, dir, func=1):
        """
        Button for Exporting/Importing Output Settings
        :param root: Parent Frame
        :param dir: Default Search output directory
        :param func: 1= Import, 0= Export
        """
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
        if file_w_headers:
            GenFuncs.exp_imp_func(file_w_headers,edom)
        
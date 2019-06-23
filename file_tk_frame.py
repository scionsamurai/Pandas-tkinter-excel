from tkinter import *
class TkFileFrame:
    def __init__(self, file_name, get_cols, get_col_vals):
        self.file = file_name
        self.get_vals = get_col_vals
        global opt_window
        #ind = self.answer.index(key)
        #field = self.li[ind].df.columns.values
        field = get_cols(self.file)
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

        self.make(opt_window, field, 3, body=body, body2=scrollable_body, key=file_name)

    def make(self, root=None, fields=[], func=0, body=False, body2=False, key=False, set_info=False, NAdict={}):
        if func == 3:
            count = 0
            for f in fields[self.x:self.x2]:
                count += 1
                Button(body2, text=f,
                       command=(lambda e=f: self.update_entry(root, e, self.ents1, 1))).grid(row=count, column=1,
                                                                                             padx=1)
                Button(body2, text='Result\'s within Column',
                       command=(lambda e=f: self.update_column_win(body, e, key))).grid(row=count, column=2, padx=1)
            count += 1
            temp_count = False
            if len(fields[:self.x2]) / 45 > 1:
                Button(body2, text='Previous Page',
                       command=(lambda e=key: self.headers_option_button(e, root=body, func='prev'))).grid(row=count,
                                                                                                           column=1,
                                                                                                           padx=1)
                temp_count = True
            if len(fields) > len(fields[:self.x2]):
                Button(body2, text='Next Page',
                       command=(lambda e=key: self.headers_option_button(e, root=body, func='next'))).grid(row=count,
                                                                                                           column=2,
                                                                                                           padx=1)
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
                ind = self.answer.index(key)
                if set_info in self.li[ind].fill_val:
                    if field == self.li[ind].fill_val[set_info]:
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
                      text=("Total Results: " + str(NAdict[field]))).grid(row=count, column=2, pady=5, padx=1)

            count += 1
            temp_count = False
            if len(fields[:self.x2]) / 45 > 1:
                Button(body2, text='Previous Page',
                       command=(lambda e=set_info: self.update_column_win(body, e, key, func='prev'))).grid(row=count,
                                                                                                            column=1,
                                                                                                            padx=1)
                temp_count = True
            if len(fields) > len(fields[:self.x2]):
                Button(body2, text='Next Page',
                       command=(lambda e=set_info: self.update_column_win(body, e, key, func='next'))).grid(row=count,
                                                                                                            column=2,
                                                                                                            padx=1)
                temp_count = True
            if temp_count == True:
                count += 1
            Button(body2, text="Reset Items",
                   command=(lambda e="nothing": self.update_entry(root, e, self.ents2, 2))).grid(row=count,
                                                                                                 column=1, padx=1)
            Button(body2, text="Exit", command=(lambda e=root: e.destroy())).grid(row=count, column=2, pady=5, padx=1)
            body2.update()
            root.mainloop()

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
        slimmed_list, count_dict = self.get_vals(key, set_info)
        if func == 'next':
            self.x += 45
            self.x2 += 45
        elif func == 'prev':
            self.x -= 45
            self.x2 -=45
        else:
            self.x = 0
            self.x2 = 45
        self.make(opt_window, slimmed_list, 4, body=body,
                  body2=scrollable_body, key=key, set_info=set_info, NAdict=count_dict)

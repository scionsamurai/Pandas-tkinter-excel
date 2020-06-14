from tkinter import *
from scrollbarClass import Scrollable
from func_file import GenFuncs
import pandas as pd
class MakeFooter:
    def update_footer(rootx, fields, li, ents, body):
        """
        Generates footer Frame of main window with opened files listed.
        :param rootx: Parent Frame.
        :param fields: List of open files.
        :return: List of Files with checkbutton Status.
        """
        x = 0
        x2 = 45

        def page_func(list, p_frame, row_c, func, file, bod, set_info=None):
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
            ind = fields.index(key)
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
                       command=(lambda e=f: GenFuncs.update_entry(opt_window, e, ents[0][1], 1))).grid(row=count,
                                                                                                       column=1,
                                                                                                       padx=1)
                Button(scrollable_body, text='Results within Column',
                       command=(lambda e=f: header_values(key, body, e))).grid(row=count, column=2, padx=1)
            count += 1
            temp_count = page_func(field, scrollable_body, count, header_button, key, body)
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
            global opt_window, x, x2
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
                x2 -= 45
            else:
                x = 0
                x2 = 45
            count = 0
            for field in slimmed_list[x:x2]:
                count += 1
                ind = fields.index(key)
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
                   command=(lambda e="nothing": GenFuncs.update_entry(opt_window, e, ents[1][1], 2))).grid(row=count,
                                                                                                           column=1,
                                                                                                           padx=1)
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
            ind = fields.index(key)
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


        lrow = Frame(rootx)
        Label(lrow, text=' --- Files / Search Order --- ').pack()
        lrow.pack()
        entries = []
        if len(fields) < 7:
            for field in fields:
                temp_field = field.split('/')
                new_field = 'Search:  ' + temp_field[(len(temp_field) - 1)]
                vrow = Frame(rootx)
                var1 = IntVar()
                var1.set(1)
                ent = Checkbutton(vrow, text=new_field, variable=var1)
                bx = Button(vrow, text='Headers', command=(lambda e=field: header_button(key=e)))
                ent.pack(side=LEFT)
                bx.pack(side=RIGHT)
                entries.append((field, ent, var1))
                vrow.pack()
        else:
            vscrollbar = Scrollbar(rootx, orient=VERTICAL)
            vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
            canvas = Canvas(rootx, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set) #rootx,
            canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
            vscrollbar.config(command=canvas.yview)
            canvas.xview_moveto(0)
            canvas.yview_moveto(0)
            scroll_frame = Frame(canvas)
            scroll_frame.pack()
            scroll_bar_id = canvas.create_window(0, 0, window=scroll_frame, anchor='nw')

            def functiontry(event):
                size = (scroll_frame.winfo_reqwidth(), scroll_frame.winfo_reqheight())
                canvas.config(scrollregion="0 0 %s %s" % size)
                if scroll_frame.winfo_reqwidth() != canvas.winfo_width():
                    # update the canvas's width to fit the inner frame
                    canvas.config(width=scroll_frame.winfo_reqwidth())
            scroll_frame.bind("<Configure>",functiontry)

            def _configure_canvas(event):
                if scroll_frame.winfo_reqwidth() != canvas.winfo_width():
                    # update the inner frame's width to fill the canvas
                    canvas.itemconfigure(scroll_bar_id, width=canvas.winfo_width())

            canvas.bind('<Configure>', _configure_canvas)
            for field in fields:
                temp_field = field.split('/')
                new_field = 'Search:  ' + temp_field[(len(temp_field) - 1)]
                vrow = Frame(scroll_frame)
                var1 = IntVar()
                var1.set(1)
                ent = Checkbutton(vrow, text=new_field, variable=var1)
                bx = Button(vrow, text='Headers', command=(lambda e=field: header_button(key=e)))
                vrow.pack(side=TOP, fill=X, padx=5, pady=2)
                ent.pack(side=LEFT)
                bx.pack(side=RIGHT)
                entries.append((field, ent, var1))
        return entries


"""
Retrieve Input Options and Output File
"""
from _funcs.SplitEntry import Split_Entry
from _funcs.SearchDF import SearchDataFrame
import pandas as pd
import shelve, os, time
import xlsxwriter
from sys import platform
from _funcs.func_file import GenFuncs
if platform == "linux" or platform == "linux2":
    import subprocess, sys

_test = False
if not _test:
    from tkinter.ttk import Progressbar
    from tkinter import HORIZONTAL, StringVar, Label, Frame, X

class Retrieve_R:
    def ow_frames(input_criteria, opened_files, data_frames, auto_open_var, output_type, file_list, root2=False, func=0, file_name='default'):
        """
        Search Open Files by Input Criteria and output file
        :param input_criteria: Search Column and Search Item(s)
        :param opened_files: List of opened files with Checkbutton variables
        :param data_frames: list of open files(classes)
        :param auto_open_var: Main window Checkbutton variable for Auto-Open
        :param output_type: type of output - set to xlsx for a while
        :param file_list: Search Order List
        """
        def get_checked_l():
            checked_list = []
            for file in file_list:  # Iterate through DataFrames using i as index
                ind = file_list.index(file)
                if opened_files[ind][2].get() == 1:
                    checked_list.append(file)
            return checked_list
        start = time.time()
        new_output = []  # Search results per DataFrame
        if not _test:
            root = Frame(root2)
            progress = Progressbar(root, orient=HORIZONTAL, length=300, mode='determinate')
            progress.pack(fill=X)
            v = StringVar()
            Label(root, textvariable=v).pack()
            root.pack()

        if func == 0 or func == 3:
            if func == 0:
                print('Searching:\n' + input_criteria[1][1].get())
                search_column = (input_criteria[0][1].get()).strip()
                out_d_and_n, zeros_dict, font_type_size, col_width, dec_rules,\
                dec_place = GenFuncs.get_out_opts(input_criteria, search_column,output_type)  # Load Settings
            elif func == 3:
                out_d_and_n, zeros_dict, font_type_size, col_width, dec_rules,\
                dec_place = GenFuncs.get_out_opts(input_criteria, input_criteria[0],output_type, func=1, file_name=file_name)  # Load Settings

            checked_l = get_checked_l()

            for file in checked_l:
                ind = file_list.index(file)
                if not _test:
                    progress_bar_ind = checked_l.index(file)
                    progress['value'] = (((progress_bar_ind+1)/len(checked_l))*100)/2
                    v.set("Searching : " + GenFuncs.strip_dir(file))
                    root.update_idletasks()
                if func != 3:
                    results = data_frames[ind].search_col(search_column, input_criteria[1][1].get(),
                                                        zeros_dict)  # <-need to move
                else:
                    results = data_frames[ind].search_col(input_criteria[0], input_criteria[1],
                                                        zeros_dict)
                try:
                    if not results.empty:
                        new_output.append(results)
                except AttributeError:
                    pass
        else:
            new_new_output = opened_files
            output_type = 'xlsx'
            out_d_and_n, zeros_dict, font_type_size, \
            col_width, dec_rules, dec_place = GenFuncs.get_out_opts("", "",output_type, func=1, file_name=file_name)  # Load Settings

        output_directory = os.path.dirname(out_d_and_n)

        for FP_out in os.listdir(output_directory): # Clean output folder of past search items
            if FP_out.endswith("FP_out.xlsx"):
                try:
                    os.remove(os.path.join(output_directory, FP_out))
                except PermissionError:
                    pass

        if dec_place != False:
            dec_var = '%.' + str(dec_place) + 'f'
        else:
            dec_var = "%.2f"
        if not _test:
            v.set("Formatting Output")
            root.update_idletasks()
        try:
            if func == 0 or func == 3:
                try:
                    new_new_output = pd.concat(new_output, axis=0, sort=False, ignore_index=True)
                except:
                    print("No results")
                    if not _test:
                        progress.destroy()
                        v.set("No results")
                        root.update_idletasks()
                        time.sleep(2)
                        root.destroy()
                    return

            #var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
            #try:
            #    plug_dicts = var_file['plug_lists']
            #    var_file.close()
            #    for key, value in plug_dicts.items():
            #        if value[0] == 1:
            #            new_new_output = value[1].run(new_new_output)
            #except KeyError:
            #    var_file.close()
                #print('fail retrieve_info')

            cols_index = []
            for col in new_new_output:
                cols_index.append(col)
            if output_type == 'csv':
                new_new_output.to_csv(out_d_and_n, index=False)
            elif output_type == 'xlsx':
                writer_orig = pd.ExcelWriter(out_d_and_n, engine='xlsxwriter')
                new_new_output.to_excel(writer_orig, index=False, sheet_name='SearchOutput', float_format=dec_var)
                workbook = writer_orig.book
                worksheet = writer_orig.sheets['SearchOutput']
                size = 10
                f_rule_cnt = len(font_type_size) + len(col_width) + len(dec_rules)
                crnt_rule = 0
                if font_type_size != {}:  # Set Global Font Size / Type
                    try:
                        size = int(list(font_type_size.values())[0])
                        if size != False:
                            workbook.formats[0].set_font_size(size)
                        if list(font_type_size.keys())[0] != False:
                            workbook.formats[0].set_font_name(list(font_type_size.keys())[0])
                        if not _test:
                            progress['value'] = (((crnt_rule /f_rule_cnt) * 100) / 2) + 50
                            crnt_rule += 1
                            v.set(v.get()+".")
                            root.update_idletasks()
                    except IndexError:
                        pass
                if len(col_width) > 0:  # Set Column / Widths
                    for rule in col_width.items():
                        worksheet.set_column(rule[0], int(rule[1]))
                        if not _test:
                            progress['value'] = (((crnt_rule /f_rule_cnt) * 100) / 2) + 50
                            crnt_rule += 1
                            v.set(v.get()+".")
                            root.update_idletasks()
                try:
                    writer_orig.save()
                except Exception as e:
                    print (e)
                    print("File with same criteria already open?")
            if auto_open_var.get() == 1:
                try:
                    if platform == "linux" or platform == "linux2":
                        opener = "open" if sys.platform == "darwin" else "xdg-open"
                        subprocess.call([opener, out_d_and_n])
                    else:
                        os.startfile(out_d_and_n, 'open')
                except:
                    print('Error while trying to open application\nPlease set default xlsx application')
                end = time.time()
                print('-------' + str(end - start) + '-------')
            else:
                end = time.time()
                print('-------' + str(end - start) + '-------')
                print('done')
            if not _test:
                root.destroy()

        except PermissionError as e:
            print(str(e)[:28] + ": Close File Before Searching")

    def esult_frames(data_frame, search_column, real_list, file_name):
        """
        For opening only rows with results that match main window search criteria
        :param data_frame: New frame created from file
        :param search_column: Column to search                  -from main window
        :param real_list: Stripped list of item(s) to search    -from main window
        :param file_name: Current Files Name
        :return: Results from File
        """
        new_output = []
        new_field = GenFuncs.strip_dir(file_name)
        if not isinstance(real_list, str):
            list_str_var =  2
        else:
            list_str_var = 1
        new_output.append(SearchDataFrame.criteria_by_column(search_column, real_list, new_field,
                                                             list_str_var, data_frame))
        try:
            if new_output == [None]:
                new_output2 =pd.DataFrame({'A': []})
        except ValueError:
            new_output2 = pd.concat(new_output, axis=0, sort=False, ignore_index=True)
        return new_output2


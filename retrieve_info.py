"""
Retrieve Input Options and Output File
"""
from SplitEntry import Split_Entry
from SearchDF import SearchDataFrame
import pandas as pd
import shelve, os, time
import xlsxwriter
from sys import platform
from func_file import GenFuncs
if platform == "linux" or platform == "linux2":
    import subprocess, sys
class Retrieve_R:
    def ow_frames(input_criteria, opened_files, data_frames, auto_open_var, output_type, file_list, func=0):
        """
        Search Open Files by Input Criteria and output file
        :param input_criteria: Search Column and Search Item(s)
        :param opened_files: List of opened files with Checkbutton variables
        :param data_frames: list of open files(classes)
        :param auto_open_var: Main window Checkbutton variable for Auto-Open
        :param output_type: type of output - set to xlsx for a while
        :param file_list: Search Order List
        """
        start = time.time()
        new_output = []  # Search results per DataFrame
        if func == 0:

            print('Searching:\n' + input_criteria[1][1].get())
            search_column = (input_criteria[0][1].get()).strip()
            output_directory, zeros_dict, font_type_size, \
            col_width, dec_rules, dec_place = GenFuncs.get_out_opts(input_criteria, search_column,
                                                                    output_type)  # Load Settings

            for file in file_list:  # Iterate through DataFrames using i as index
                ind = file_list.index(file)
                if opened_files[ind][
                    2].get() == 1:  # If tkinter checkbutton next to file name is checked -> Open the file
                    results = data_frames[ind].search_col(search_column, input_criteria[1][1].get(), zeros_dict)
                    try:
                        if not results.empty:
                            new_output.append(results)
                    except AttributeError:
                        pass
        else:
            new_new_output = opened_files
            output_type = 'xlsx'
            output_directory, zeros_dict, font_type_size, \
            col_width, dec_rules, dec_place = GenFuncs.get_out_opts("", "",output_type, func=1)  # Load Settings
        if dec_place != False:
            dec_var = '%.' + str(dec_place) + 'f'
        else:
            dec_var = "%.2f"
        try:
            try:
                if func == 0:
                    new_new_output = pd.concat(new_output, axis=0, sort=False, ignore_index=True)
                if output_type == 'csv':
                    new_new_output.to_csv(output_directory, index=False)
                elif output_type == 'xlsx':
                    writer_orig = pd.ExcelWriter(output_directory, engine='xlsxwriter')
                    new_new_output.to_excel(writer_orig, index=False, sheet_name='SearchOutput', float_format=dec_var)
                    workbook = writer_orig.book
                    worksheet = writer_orig.sheets['SearchOutput']
                    size = 10
                    if font_type_size != {}: # Set Global Font Size / Type
                        try:
                            size = int(list(font_type_size.values())[0])
                            workbook.formats[0].set_font_size(size)
                            workbook.formats[0].set_font_name(list(font_type_size.keys())[0])
                        except IndexError:
                            pass
                    if len(col_width) > 0: # Set Column / Widths
                        for rule in col_width.items():
                            worksheet.set_column(rule[0], int(rule[1]))
                    if len(dec_rules) > 0: # Set Column / Decimal places
                        for key, val in dec_rules.items():
                            num_format = workbook.add_format({'num_format': val})
                            worksheet.set_column(key, size, num_format)


                    writer_orig.save()
                if auto_open_var.get() == 1:
                    if platform == "linux" or platform == "linux2":
                        opener = "open" if sys.platform == "darwin" else "xdg-open"
                        subprocess.call([opener, output_directory])
                    else:
                        os.startfile(output_directory, 'open')
                    end = time.time()
                    print('-------' + str(end - start) + '-------')
                else:
                    end = time.time()
                    print('-------' + str(end - start) + '-------')
                    print('done')
            except ValueError as e:
                print(e) #"No Matches")

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


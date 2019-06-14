from SplitEntry import Split_Entry
from SearchDF import SearchDataFrame
import pandas as pd
import shelve, os, time
import xlsxwriter
class Retrieve_Input:
    def __init__(self):
        self.no_value = 0

    def row_frames(self,input_criteria, opened_files, data_frames, auto_open_var, output_type, NA_head_dict):
        start = time.time()
        new_output = [] # Search results per DataFrame
        print('Searching:\n' + input_criteria[1][1].get())
        search_column = (input_criteria[0][1].get()).strip()
        output_directory, zeros_dict, font_type_size, \
        col_width, dec_rules = self.get_rules(input_criteria, search_column, output_type) # Load Settings
        for i in range(0, len(data_frames)): # Iterate through DataFrames using i as index
            temp_field = (opened_files[i][0]).split('/')
            new_field = temp_field[(len(temp_field) - 1)]
            if opened_files[i][2].get() == 1: # If tkinter checkbutton next to file name is checked -> Open the file
                real_list = Split_Entry.split(input_criteria[1][1].get()) # Splits main window Search Item(s) into list
                temp_output = pd.DataFrame({'A':[]})
                if isinstance(real_list, str) == False:
                    func_var = 2
                else:
                    func_var = 1
                try:
                    temp_output = SearchDataFrame.criteria_by_column(search_column, real_list, new_field, func_var,
                                                                     data_frames[i]).copy()
                    for col in NA_head_dict[opened_files[i][0]]: # Strip space saving Filler Values from output
                        temp_output[col].replace(NA_head_dict[opened_files[i][0]][col], None, inplace=True)
                    if not temp_output.empty: # if Search had results add them to new_output list
                        new_output.append(temp_output)
                except (TypeError, AttributeError):
                    pass

        try:
            try:
                new_new_output = pd.concat(new_output, axis=0, sort=False, ignore_index=True)
                for key, val in zeros_dict.items(): # Apply Leading Zeros rules to output
                    try:
                        temp_str = '{0:0>' + str(val) + '}'
                        if str(new_new_output[key].dtype)[:3] == 'int' or \
                                str(new_new_output[key].dtype)[:3] == 'uin' or \
                                str(new_new_output[key].dtype)[:5] == 'float': # For Numbers
                            new_new_output[key] = new_new_output[key].apply(lambda x: temp_str.format(x))
                        else: # For Strings
                            try:
                                new_new_output[key] = new_new_output[key].str.zfill(int(val))
                            except AttributeError:
                                pass
                    except KeyError: # Catch if Rule Header wasn't in output results
                        print(key + ' isn\'t in output.')
                if output_type == 'csv':
                    new_new_output.to_csv(output_directory, index=False)
                elif output_type == 'xlsx':
                    writer_orig = pd.ExcelWriter(output_directory, engine='xlsxwriter')
                    new_new_output.to_excel(writer_orig, index=False, sheet_name='SearchOutput', float_format="%.2f")
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

    def result_frames(self, data_frame, search_column, real_list, file_name):
        new_output = [] # ^^^Function to specify rows when opening file (with main window search criteria)
        temp_field = file_name.split('/')
        new_field = temp_field[(len(temp_field) - 1)]
        if isinstance(real_list, str) == False:
            new_output.append(SearchDataFrame.criteria_by_column(search_column,
                                                                 real_list,
                                                                 new_field, 2, data_frame))
        else:
            new_output.append(SearchDataFrame.criteria_by_column(search_column,
                                                                 real_list,
                                                                 new_field, 1, data_frame))
        try:
            if new_output == [None]:
                new_output2 =pd.DataFrame({'A': []})
        except ValueError:
            new_output2 = pd.concat(new_output, axis=0, sort=False, ignore_index=True)
        return new_output2

    def get_rules(self, input_criteria, search_column, output_type):
        if isinstance(Split_Entry.split(input_criteria[1][1].get()), str) == False:
            if len(Split_Entry.split(input_criteria[1][1].get())) > 1:
                output_dir = search_column + "(" + str(
                    len(Split_Entry.split(input_criteria[1][1].get()))) + ")." + output_type
            else:
                output_dir = Split_Entry.split(input_criteria[1][1].get()) + "." + output_type
        else:
            output_dir = Split_Entry.split(input_criteria[1][1].get()) + "." + output_type

        var_file = shelve.open('var_file')
        try:
            col_width = var_file['col_spacing']
        except KeyError:
            col_width = {}
        try:
            zeros_dict = var_file['lead_zeroes']
        except KeyError:
            zeros_dict = {}
        try:
            output_path = var_file['dir_location']
            output_directory = os.path.join(output_path, output_dir)
        except KeyError:
            output_directory = output_dir
        try:
            font_rules = var_file['font_rules']
        except KeyError:
            font_rules = {}
        try:
            dec_rules = var_file['decimal_places']
        except KeyError:
            dec_rules = {}

        var_file.close()
        return output_directory, zeros_dict, font_rules, col_width, dec_rules

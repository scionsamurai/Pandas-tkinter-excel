from SplitEntry import Split_Entry
from SearchDF import SearchDataFrame
import pandas as pd
import numpy as np
import shelve, os, time
import xlsxwriter
class Retrieve_Input:
    def __init__(self):
        self.no_value = 0

    def row_frames(self,input_criteria, opened_files, data_frames, auto_open_var, output_type, NA_head_dict):
        start = time.time()
        new_output = []
        print('Searching:\n' + input_criteria[1][1].get())
        search_column = (input_criteria[0][1].get()).strip()
        for i in range(0, len(data_frames)):
            temp_field = (opened_files[i][0]).split('/')
            new_field = temp_field[(len(temp_field) - 1)]
            if opened_files[i][2].get() == 1:
                real_list = Split_Entry.split(input_criteria[1][1].get())
                temp_output = pd.DataFrame({'A':[]})
                if isinstance(real_list, str) == False:
                    try:
                        temp_output = SearchDataFrame.criteria_by_column(search_column,real_list, new_field, 2,
                                                                             data_frames[i]).copy()
                        for col in NA_head_dict[opened_files[i][0]]:
                            temp_output[col].replace(NA_head_dict[opened_files[i][0]][col], np.NaN, inplace=True)
                        if not temp_output.empty:
                            new_output.append(temp_output)
                    except (TypeError, AttributeError):
                        pass
                        #return pd.DataFrame({'A':[]}), None
                else:
                    try:
                        temp_output = SearchDataFrame.criteria_by_column(search_column, real_list, new_field, 1,
                                                                         data_frames[i]).copy()
                        for col in NA_head_dict[opened_files[i][0]]:
                            temp_output[col].replace(NA_head_dict[opened_files[i][0]][col], np.NaN, inplace=True)
                        if not temp_output.empty:
                            new_output.append(temp_output)
                    except (TypeError, AttributeError):
                        pass
                        #return pd.DataFrame({'A':[]}), None

        try:
            output_directory, zeros_dict, font_type_size, col_width = self.get_rules(input_criteria, search_column,
                                                                                     output_type)
            try:
                new_new_output = pd.concat(new_output, axis=0, sort=False, ignore_index=True)
                for key, val in zeros_dict.items():
                    try:
                        temp_str = '{0:0>' + str(val) + '}'
                        if str(new_new_output[key].dtype)[:3] == 'int' or \
                                str(new_new_output[key].dtype)[:3] == 'uin' or \
                                str(new_new_output[key].dtype)[:5] == 'float':
                            new_new_output[key] = new_new_output[key].apply(lambda x: temp_str.format(x))
                        else:
                            try:
                                new_new_output[key] = new_new_output[key].str.zfill(int(val))
                            except AttributeError:
                                pass
                    except KeyError:
                        print(key + ' isn\'t in output.')
                if output_type == 'csv':
                    new_new_output.to_csv(output_directory, index=False)
                elif output_type == 'xlsx':
                    writer_orig = pd.ExcelWriter(output_directory, engine='xlsxwriter')
                    new_new_output.to_excel(writer_orig, index=False, sheet_name='SearchOutput')
                    workbook = writer_orig.book
                    worksheet = writer_orig.sheets['SearchOutput']
                    if font_type_size != {}:
                        workbook.formats[0].set_font_size(int(list(font_type_size.values())[0]))
                        workbook.formats[0].set_font_name(list(font_type_size.keys())[0])
                    if len(col_width) > 0:
                        for rule in col_width.items():
                            worksheet.set_column(rule[0], int(rule[1]))


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
        new_output = []
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
        except:
            output_directory = output_dir
        try:
            font_rules = var_file['font_rules']
        except KeyError:
            font_rules = {}
        var_file.close()
        return output_directory, zeros_dict, font_rules, col_width

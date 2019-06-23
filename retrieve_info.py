from SplitEntry import Split_Entry
from SearchDF import SearchDataFrame
import pandas as pd
import shelve, os, time
import xlsxwriter
from func_file import GenFuncs
class Retrieve_R:
    def ow_frames(input_criteria, opened_files, data_frames, auto_open_var, output_type, file_list):
        start = time.time()
        new_output = [] # Search results per DataFrame

        def get_rules(input_crit, search_col, out_type):
            if not isinstance(Split_Entry.split(input_crit[1][1].get()), str):
                if len(Split_Entry.split(input_crit[1][1].get())) > 1:
                    output_dir = search_col + "(" + str(
                        len(Split_Entry.split(input_crit[1][1].get()))) + ")." + out_type
                else:
                    output_dir = Split_Entry.split(input_crit[1][1].get()) + "." + out_type
            else:
                output_dir = Split_Entry.split(input_crit[1][1].get()) + "." + out_type

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
            try:
                try:
                    dec_place = var_file['glob_dec_place'].strip()
                except AttributeError:
                    dec_place = var_file['glob_dec_place']
            except KeyError:
                dec_place = False
            var_file.close()
            return output_directory, zeros_dict, font_rules, col_width, dec_rules, int(dec_place)

        print('Searching:\n' + input_criteria[1][1].get())
        search_column = (input_criteria[0][1].get()).strip()
        output_directory, zeros_dict, font_type_size, \
        col_width, dec_rules, dec_place = get_rules(input_criteria, search_column, output_type) # Load Settings
        if dec_place != False:
            dec_var = '%.' + str(dec_place) + 'f'
        else:
            dec_var = "%.2f"
        for file in file_list: # Iterate through DataFrames using i as index
            ind = file_list.index(file)
            if opened_files[ind][2].get() == 1: # If tkinter checkbutton next to file name is checked -> Open the file
                results = data_frames[ind].search_col(search_column, input_criteria[1][1].get(),zeros_dict)
                try:
                    if not results.empty:
                        new_output.append(results)
                except AtributeError:
                    pass

        try:
            try:
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

    def result_frames(data_frame, search_column, real_list, file_name):
        new_output = [] # ^^^Function to specify rows when opening file (with main window search criteria)
        new_field = GenFuncs.strip_dir(file_name)
        if not isinstance(real_list, str):
            new_output.append(SearchDataFrame.criteria_by_column(search_column,real_list, new_field, 2, data_frame))
        else:
            new_output.append(SearchDataFrame.criteria_by_column(search_column,  real_list,  new_field, 1, data_frame))
        try:
            if new_output == [None]:
                new_output2 =pd.DataFrame({'A': []})
        except ValueError:
            new_output2 = pd.concat(new_output, axis=0, sort=False, ignore_index=True)
        return new_output2


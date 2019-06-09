from SplitEntry import Split_Entry
from SearchDF import SearchDataFrame
import pandas as pd
import shelve, os, time
import xlsxwriter
class Retrieve_Input:
    def __init__(self):
        self.no_value = 0
    def row_frames(self,input_criteria, opened_files, data_frames, auto_open_var, output_type):
        start = time.time()
        new_output = []
        print('Searching:\n' + input_criteria[1][1].get())
        search_column = (input_criteria[0][1].get()).strip()
        for i in range(0, len(data_frames)):
            temp_field = (opened_files[i][0]).split('/')
            new_field = temp_field[(len(temp_field) - 1)]
            if opened_files[i][2].get() == 1:
                real_list = Split_Entry.split(input_criteria[1][1].get())
                if isinstance(real_list, str) == False:
                    new_output.append(SearchDataFrame.criteria_by_column(search_column,
                                                                         real_list,
                                                                         new_field, 2, data_frames[i]))
                else:
                    new_output.append(SearchDataFrame.criteria_by_column(search_column,
                                                                         real_list,
                                                                         new_field, 1, data_frames[i]))

        try:
            if isinstance(Split_Entry.split(input_criteria[1][1].get()), str) == False:
                if len(Split_Entry.split(input_criteria[1][1].get())) > 1:
                    output_dir = search_column + "(" + str(len(Split_Entry.split(input_criteria[1][1].get()))) + ")." + output_type
                else:
                    output_dir = Split_Entry.split(input_criteria[1][1].get()) + "." + output_type
            else:
                output_dir = Split_Entry.split(input_criteria[1][1].get()) + "." + output_type
            var_file = shelve.open('var_file')
            try:
                rules = var_file['rules']
            except KeyError:
                print('No Rules to assign')
                rules = []
            try:
                output_path = var_file['dir_location']
                output_directory = os.path.join(output_path,output_dir)
            except:
                output_directory = output_dir
                print('saving to default directory')
            var_file.close()
            try:
                new_new_output = pd.concat(new_output, axis=0, sort=False, ignore_index=True)
                for rule in rules:
                    if rule[2] != '':
                        try:
                            temp_str = '{0:0>' + str(rule[5]) + '}'
                            if str(new_new_output[rule[2]].dtype)[:3] == 'int' or\
                                    str(new_new_output[rule[2]].dtype)[:5] == 'float':
                                new_new_output[rule[2]] = new_new_output[rule[2]].apply(lambda x: temp_str.format(x))
                            else:
                                new_new_output[rule[2]] = new_new_output[rule[2]].str.zfill(int(rule[5]))
                        except KeyError:
                            print(rule[2] + ' isn\'t in output.')
                        #rules.remove(rule)
                        #num_format = workbook.add_format({'num_format': rule[2]})
                if output_type == 'csv':
                    new_new_output.to_csv(output_directory, index=False)
                elif output_type == 'xlsx':
                    writer_orig = pd.ExcelWriter(output_directory, engine='xlsxwriter')
                    new_new_output.to_excel(writer_orig, index=False, sheet_name='SearchOutput')
                    workbook = writer_orig.book
                    worksheet = writer_orig.sheets['SearchOutput']
                    #[col.get(),width.get(),rule.get(),font.get(),font_size.get()]
                    if len(rules) > 0:
                        for rule in rules:
                            if rule[2] == '':
                                num_format = None
                            else:
                                pass
                                #num_format = workbook.add_format({'num_format': rule[2]})
                            if (rule[0] == '') and (rule[5] == ''):
                                workbook.formats[0].set_font_size(int(rule[4]))
                                workbook.formats[0].set_font_name(rule[3])
                            else:
                                try:
                                    worksheet.set_column(rule[0], int(rule[1]), num_format)
                                except ValueError:
                                    pass



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

"""
General Functions Pulled to trim primary code
"""
import shelve, os, re, tempfile, time
from _funcs.SplitEntry import Split_Entry

class GenFuncs:
    def add_lead_0s(df, zeros_dict):
        for key1, val in zeros_dict.items():  # Apply Leading Zeros rules to output
            key = key1.strip()
            try:
                temp_str = '{0:0>' + str(val) + '}'
                if str(df[key].dtype)[:3] == 'int' or str(df[key].dtype)[:3] == 'uin' or \
                        str(df[key].dtype)[:5] == 'float':  # For Numbers
                    df[key] = df[key].apply(lambda x: temp_str.format(x))
                elif str(df[key].dtype)[:3] == 'cat':
                    df[key] = df[key].astype('object')
                    df[key] = df[key].str.zfill(int(val))
                else:  # For Strings
                    try:
                        df[key] = df[key].str.zfill(int(val))
                    except AttributeError:
                        pass
            except KeyError:  # Catch if Rule Header wasn't in output results
                pass
        return df

    def get_inp_opts():
        """
        Get Input options from shelve File
        :return: gen_rules          -Delimiter, Line Terminator, Header Line, Index Column,
                                        Chunk Size, Cpu Cores, Verbose, Header Function,
                                         Main window Criteria
        :return: only_cols          -Specify Columns to open ---not currently available
        :return: dtypes             -Specify Column/Data_Type's
        :return: head_func_dtypes   -List of Example Column/Data_type's from header_func
        """
        gen_rules = {}
        var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
        try:
            for gen_set in var_file['opt_gen_rules']:
                if gen_set[0] == 'Delimiter':
                    if gen_set[1] == 'DV' or gen_set[1] == '':
                        gen_rules['Delimiter'] = ','
                    else:
                        gen_rules['Delimiter'] = gen_set[1]
                elif gen_set[0] == 'Terminator':
                    if gen_set[1] == 'DV' or gen_set[1] == '':
                        gen_rules['Terminator'] = None
                    else:
                        gen_rules['Terminator'] = gen_set[1]
                elif gen_set[0] == 'Header Line':
                    if gen_set[1] == 'DV' or gen_set[1] == '':
                        gen_rules['Header Line'] = 0
                    else:
                        gen_rules['Header Line'] = int(gen_set[1])
                elif gen_set[0] == 'Index Column':
                    if gen_set[1] == 'DV' or gen_set[1] == '':
                        gen_rules['Index Column'] = None
                    else:
                        gen_rules['Index Column'] = int(gen_set[1])
                elif gen_set[0] == 'Chunk':
                    if gen_set[1] == 'DV' or gen_set[1] == '':
                        gen_rules['Chunk'] = 10000
                    else:
                        gen_rules['Chunk'] = int(gen_set[1])
                elif gen_set[0] == 'CPU Cores':
                    if gen_set[1] == 1 or gen_set[1] == '':
                        gen_rules['CPU Cores'] = 1
                    else:
                        gen_rules['CPU Cores'] = int(gen_set[1])
                elif gen_set[0] == 'Verbose':
                    if gen_set[1] == 0:
                        gen_rules['Verbose'] = False
                    else:
                        gen_rules['Verbose'] = True
                elif gen_set[0] == 'Header Func':
                    if gen_set[1] == 0:
                        gen_rules['Header Func'] = False
                    else:
                        gen_rules['Header Func'] = True
                elif gen_set[0] == 'Main Win Criteria':
                    if gen_set[1] == 0:
                        gen_rules['Main Win Criteria'] = False
                    else:
                        gen_rules['Main Win Criteria'] = True
        except KeyError:
            gen_rules['Delimiter'] = ','
            gen_rules['Terminator'] = None
            gen_rules['Header Line'] = 0
            gen_rules['Index Column'] = None
            gen_rules['Chunk'] = 10000
            gen_rules['CPU Cores'] = 1
            gen_rules['Verbose'] = False
            gen_rules['Header Func'] = False
            gen_rules['Main Win Criteria'] = False
        try:
            only_cols = var_file['spec_col_rules']
        except KeyError:
            only_cols = None
        try:
            dtypes = var_file['col_dtypes']
            for key, value in dtypes.items():
                if value == 'Text':
                    dtypes[key] = str
                elif value == 'Number':
                    dtypes[key] = float
        except KeyError:
            dtypes = None
        try:
            head_func_dtypes = var_file['head_func_types']
        except KeyError:
            head_func_dtypes = None
        var_file.close()
        return gen_rules, only_cols, dtypes, head_func_dtypes

    def get_file_list(input_list, already_open_list, check_name=False, name_str=False, func=1):
        """
        For splitting list of files into excel list and csv/h5 list
        :param already_open_list: List of files that are already opened
        :param check_name: Bool Value for specifying leading characters of files you want to open In Directory
        :param name_str: Leading characters specified for opening files in Directory
        :param func: 1=Selected Files from Directory, 2=All files in selected Directory
        :return: Excel list, CSV/H5 list
        """
        new_list = []
        loc_answer = []
        if func == 1:
            if len(input_list) > 0:
                try:
                    for file in input_list:
                        if file not in already_open_list:
                            if ((file[-4:])[:3] == 'xls') or (file[-4:] == '.xls'):
                                if file[:2] != '~$':
                                    new_list.append(file)
                            elif (file[-4:] == '.csv') or (file[-3:] == '.h5'):
                                loc_answer.append(file)
                    return new_list, loc_answer
                except KeyboardInterrupt as e:
                    print(e)
                    return [], []
        elif func == 2:
            for path, subdirs, files in os.walk(input_list):
                for name in files:
                    if check_name:
                        if (name[-4:] == '.csv') or (name[-3:] == '.h5'):
                            if name[:len(name_str)].lower() == name_str.lower():
                                if name not in already_open_list:
                                    loc_answer.append((path + '/' + name))
                        elif ((name[-4:])[:3] == 'xls') or (name[-4:] == '.xls'):
                            if name[:2] != '~$':
                                if name[:len(name_str)] == name_str:
                                    if name not in already_open_list:
                                        new_list.append((path + '/' + name))
                    else:
                        if (name[-4:] == '.csv') or (name[-3:] == '.h5'):
                            if name not in already_open_list:
                                loc_answer.append((path + '/' + name))
                        elif ((name[-4:])[:3] == 'xls') or (name[-4:] == '.xls'):
                            if name[:2] != '~$':
                                if name not in already_open_list:
                                    new_list.append((path + '/' + name))
                return new_list, loc_answer

    def exp_imp_func(file, edom):
        """
        For reading/writing output settings to txt file
        :param edom:mode 'r'=Read, 'w'=Write
        """
        if edom == 'r':
            file_name = file
        else:
            file_name =file.name
            file.close()
        setting_file = open(file_name, edom)
        var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
        rule_list = []
        if edom == 'r':
            space_dict = {}
            zero_dict = {}
            font_dict = {}
            dec_dict = {}
            glob_dec = False
            lines = setting_file.readlines()
            for line in lines:
                new_list = re.split('::::', line)
                if new_list[0] == 'col_spacing':
                    space_dict[new_list[1]] = new_list[2].strip()
                elif new_list[0] == 'lead_zeroes':
                    zero_dict[new_list[1]] = new_list[2].strip()
                elif new_list[0] == 'font_rules':
                    font_dict[new_list[1]] = new_list[2].strip()
                elif new_list[0] == 'decimal_places':
                    dec_dict[new_list[1]] = new_list[2].strip()
                elif new_list[0] == 'glob_dec_place':
                    if new_list[1].strip() != 'False':
                        glob_dec = new_list[1]
                    else:
                        glob_dec = False
            var_file['col_spacing'] = space_dict
            var_file['lead_zeroes'] = zero_dict
            var_file['font_rules'] = font_dict
            var_file['decimal_places'] = dec_dict
            if glob_dec != False:
                var_file['glob_dec_place'] = glob_dec
        else:
            try:
                col_width = var_file['col_spacing']
                for col, val in col_width.items():
                    rule_list.append('col_spacing' + '::::' + col + '::::' + str(val) + '\n')
            except KeyError:
                pass
            try:
                zeros_dict = var_file['lead_zeroes']
                for col, val in zeros_dict.items():
                    rule_list.append('lead_zeroes' + '::::' + col + '::::' + str(val) + '\n')
            except KeyError:
                pass
            try:
                font_rules = var_file['font_rules']
                rule_list.append('font_rules' + '::::' + list(font_rules.keys())[0] + '::::' +
                                 str(list(font_rules.values())[0]) + '\n')
            except KeyError:
                pass
            try:
                glob_dec_places = var_file['glob_dec_place']
                rule_list.append('glob_dec_place' + '::::' + str(glob_dec_places) + '\n')
            except KeyError:
                pass
            setting_file.writelines(rule_list)
        var_file.close()
        setting_file.close()

    def gen_set():
        """
        For loading Input settings from shelve file
        :return: Dictionary with General input settings
        """
        var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
        temp_dict = {}
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
                elif gen_set[0] == 'Main Win Criteria':
                    temp_dict['Main Win Criteria'] = gen_set[1]
        except KeyError:
            pass

        var_file.close()
        return temp_dict

    def get_out_opts(input_crit, search_col, out_type, func=0, file_name=''):
        """
        Get Output options from shelve file
        :param input_crit: Search Column and Search Item(s)
        :param search_col: Stripped Search Column
        :param out_type: type of output - set to xlsx for a while
        """
        main_f_name = input_crit[1][1].get()
        
        if "\\" in main_f_name: # Clean File name of slashes
            main_f_name = main_f_name.replace("\\","")
        if "/" in main_f_name:
            main_f_name = main_f_name.replace("/","")

        if func == 0:
            if not isinstance(Split_Entry.split(input_crit[1][1].get()), str):
                if len(Split_Entry.split(input_crit[1][1].get())) > 1:
                    output_dir = search_col + "(" + str(
                        len(Split_Entry.split(input_crit[1][1].get()))) + ")" + "FP_out." + out_type
                else:
                    output_dir = Split_Entry.split(main_f_name) + "FP_out" + "." + out_type
            else:
                output_dir = Split_Entry.split(main_f_name) + "FP_out" + "." + out_type
            output_dir = output_dir.replace('\t','_')

        var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
        try:
            col_width = var_file['col_spacing']
        except KeyError:
            col_width = {}
        try:
            zeros_dict = var_file['lead_zeroes']
        except KeyError:
            zeros_dict = {}
        try:
            if func == 0:
                output_path = var_file['dir_location']
                output_directory = os.path.join(output_path, output_dir)
            else:
                output_path = var_file['dir_location']
                output_directory = os.path.join(output_path, (file_name + "FP_out" + "." + out_type))
        except KeyError:
            if func == 0:
                output_directory = os.path.join(tempfile.gettempdir(),output_dir)
            else:
                output_directory = "remove_dup_test.xlsx"
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
                if dec_place == 'False':
                    dec_place = False
            except AttributeError:
                dec_place = var_file['glob_dec_place']
            try:
                dec_place = int(dec_place)
            except:
                print('General Decimal places isn\'t a number. Not using setting.')
                dec_place = False
        except KeyError:
            dec_place = False
        var_file.close()
        return output_directory, zeros_dict, font_rules, col_width, dec_rules, dec_place

    def strip_dir(file_dir):
        """
        Strips the directory (windows) from the file name.
        :return: File name without (windows) directory
        """
        temp_list = file_dir.split('/')
        file_name = temp_list[(len(temp_list) - 1)]
        return file_name

    def file_opened(file_name):
        var_file1 = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
        try:
            var_file = var_file1['opened_files']
        except KeyError as e:
            #print(e)
            var_file = {}
        var_file1.close()
        if file_name in list(var_file.keys()):
            orig_headers = var_file[file_name][0]
            last_opened = var_file[file_name][1]
            col_names = var_file[file_name][2]
            skipped_rows = var_file[file_name][3]
            skipped_cols = var_file[file_name][4]
            total_rows = var_file[file_name][5]
            file_stats = os.stat(file_name)
            last_modified = int(round(file_stats.st_mtime * 1000))
            if (last_opened-last_modified)>0:
                return orig_headers, col_names, skipped_rows, skipped_cols, total_rows
            else:
                return False
        else:
            return False
    
    def update_opened_list(file_name, orig_headers, col_names, skipped_rows, skipped_cols, total_rows):
        var_file = shelve.open(os.path.join(os.path.expanduser('~'),'var_file'))
        time_n = int(round(time.time() * 1000))
        try:
            var1_file = var_file['opened_files']
        except KeyError as e:
            #print(f"{e} --- opened_files")
            var1_file = {}
        var1_file[file_name] = (orig_headers,time_n, col_names, skipped_rows, skipped_cols, total_rows)
        var_file['opened_files'] = var1_file
        var_file.close()
        print("saved Col names for faster file opens later.")

import pandas as pd
import time
class OpenFile:
    def open_file(entry, delimiter=None,header_line=0, index_col=None, chunk=None , verbose=False,terminator=None,
                  only_col=None, dtypes=None):
        temp_field = entry.split('/')
        new_field = temp_field[(len(temp_field) - 1)]
        print('Opening ' + new_field)
        start = time.time()

        if entry[-4:] == '.csv':
            if delimiter != None:
                df = pd.read_csv(entry, sep=delimiter, header=None, nrows=1, low_memory=False)
                orig_headers = df.values.tolist()
                stripped_headers = []
                for item in orig_headers[0]:
                    try:
                        stripped_headers.append(item.strip())
                    except AttributeError:
                        stripped_headers.append(item)
                new_dtypes = {}
                if dtypes != None:
                    if 'ALL' in dtypes:
                        if dtypes['ALL'] == 'Text':
                            new_dtypes = str
                    else:
                        for key, value in dtypes.items():
                            # print(orig_headers[0])
                            if key in orig_headers[0]:
                                new_dtypes[key] = value
                            elif key.strip() in orig_headers[0]:
                                new_dtypes[key.strip()] = value
                            elif key in stripped_headers:
                                ind = stripped_headers.index(key)
                                new_dtypes[orig_headers[0][ind]] = value
                            elif key.strip() in stripped_headers:
                                ind = stripped_headers.index(key.strip())
                                new_dtypes[orig_headers[0][ind]] = value
                            else:
                                print(key + ':not found in ' + new_field)
                    if new_dtypes == {}:
                        new_dtypes = None
                if only_col != None:
                    new_only_col = []
                    for item in only_col:
                        if item in orig_headers[0]:
                            new_only_col.append(item)
                        elif item.strip() in orig_headers[0]:
                            new_only_col.append(item.strip())
                        elif item in stripped_headers:
                            ind = stripped_headers.index(item)
                            new_only_col.append(orig_headers[0][ind])
                        elif item.strip() in stripped_headers:
                            ind = stripped_headers.index(item.strip())
                            new_only_col.append(orig_headers[0][ind])
                        else:
                            print(item + ':not found in ' + new_field)

                    try:
                        data = pd.read_csv(entry, sep=delimiter, header=header_line, index_col=index_col,
                                           usecols=new_only_col, dtype=new_dtypes, verbose=verbose,
                                           lineterminator=terminator, low_memory=False)
                        data.columns = [col.strip() for col in data.columns]
                        return data
                    except ValueError as e:
                        print(e)
                else:
                    try:
                        data = pd.read_csv(entry, sep=delimiter, header=header_line, index_col=index_col,
                                           dtype=new_dtypes, verbose=verbose, lineterminator=terminator,
                                           low_memory=False)
                        data.columns = [col.strip() for col in data.columns]
                        end = time.time()
                        print('-------'+ str(end-start) +'-------')
                        return data
                    except ValueError as e:
                        print(e)

            else:
                df = pd.read_csv(entry, header=None, nrows=1, low_memory=False)
                # print(df.values.tolist())
                orig_headers = df.values.tolist()
                stripped_headers = []
                for item in orig_headers[0]:
                    try:
                        stripped_headers.append(item.strip())
                    except AttributeError:
                        stripped_headers.append(item)
                new_dtypes = {}
                if dtypes != None:
                    for key, value in dtypes.items():
                        if key in orig_headers[0]:
                            new_dtypes[key] = value
                        elif key.strip() in orig_headers[0]:
                            new_dtypes[key.strip()] = value
                        elif key in stripped_headers:
                            ind = stripped_headers.index(key)
                            new_dtypes[orig_headers[0][ind]] = value
                        elif key.strip() in stripped_headers:
                            ind = stripped_headers.index(key.strip())
                            new_dtypes[orig_headers[0][ind]] = value
                        else:
                            print(key + ':not found in ' + new_field)
                    if new_dtypes == {}:
                        new_dtypes = None
                if only_col != None:
                    new_only_col = []
                    for item in only_col:
                        if item in orig_headers[0]:
                            new_only_col.append(item)
                        elif item.strip() in orig_headers[0]:
                            new_only_col.append(item.strip())
                        elif item in stripped_headers:
                            ind = stripped_headers.index(item)
                            new_only_col.append(orig_headers[0][ind])
                        elif item.strip() in stripped_headers:
                            ind = stripped_headers.index(item.strip())
                            new_only_col.append(orig_headers[0][ind])
                        else:
                            print(item + ':not found in ' + new_field)

                    try:
                        data = pd.read_csv(entry, header=header_line, chunksize=chunk, index_col=index_col,
                                           usecols=new_only_col, dtype=new_dtypes, verbose=verbose,
                                           lineterminator=terminator, low_memory=False)
                        data.columns = [col.strip() for col in data.columns]
                        return data
                    except ValueError as e:
                        print(e)
                else:
                    try:
                        data = pd.read_csv(entry, header=header_line, chunksize=chunk, index_col=index_col,
                                           dtype=new_dtypes, verbose=verbose, lineterminator=terminator,
                                           low_memory=False)
                        data.columns = [col.strip() for col in data.columns]
                        return data
                    except ValueError as e:
                        print(e)
        elif (entry[-4:] == 'xlsx') or (entry[-4:] == '.xls') or ((entry[-4:])[:3] == 'xls'):
            df = pd.read_excel(entry, sheet_name=0, header=None, nrows=1)
            orig_headers = df.values.tolist()
            stripped_headers = []
            for item in orig_headers[0]:
                try:
                    stripped_headers.append(item.strip())
                except AttributeError:
                    stripped_headers.append(item)
            print('header checkpoint')
            new_only_col = []
            new_dtypes = {}
            try:
                for item in only_col:
                    if item in orig_headers[0]:
                        new_only_col.append(item)
                    elif item.strip() in orig_headers[0]:
                        new_only_col.append(item.strip())
                    elif item in stripped_headers:
                        ind = stripped_headers.index(item)
                        new_only_col.append(orig_headers[0][ind])
                    elif item.strip() in stripped_headers:
                        ind = stripped_headers.index(item.strip())
                        new_only_col.append(orig_headers[0][ind])
            except TypeError:
                new_only_col = None
            if dtypes != None:
                if 'ALL' in dtypes:
                    if dtypes['ALL'] == 'Text':
                        new_dtypes = str
                else:
                    for key, value in dtypes.items():
                        # print(orig_headers[0])
                        if key in orig_headers[0]:
                            new_dtypes[key] = value
                        elif key.strip() in orig_headers[0]:
                            new_dtypes[key.strip()] = value
                        elif key in stripped_headers:
                            ind = stripped_headers.index(key)
                            new_dtypes[orig_headers[0][ind]] = value
                        elif key.strip() in stripped_headers:
                            ind = stripped_headers.index(key.strip())
                            new_dtypes[orig_headers[0][ind]] = value
                        else:
                            print(key + ':not found in ' + new_field)
            if new_dtypes == {}:
                new_dtypes = None
            data = pd.read_excel(entry, sheet_name=0, header=header_line, index_col=index_col,
                                 usecols=new_only_col, dtype=new_dtypes, verbose=verbose)
            data.columns = [col.strip() for col in data.columns]
            end = time.time()
            print('-------'+ str(end-start) +'-------')
            return data
        elif entry[-3:] == '.h5':
            data = pd.read_hdf(entry,'df')
            end = time.time()
            print('-------'+ str(end-start) +'-------')
            return data
        else:
            df_empty = pd.DataFrame({'A':[]})
            end = time.time()
            print('-------'+ str(end-start) +'-------')
            return df_empty
    def map_func(data_frame, indexes):
        new_list = {}
        new_list.update(indexes)
        for column in data_frame.columns.values:
            for value in data_frame[column].values:
                if value not in indexes:
                    new_list[value] = ((len(indexes)+1) + len(new_list))
        for item in new_list:
            for column in data_frame.columns.values:
                data_frame[column].map({item:new_list[item]})
        return new_list

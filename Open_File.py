import pandas as pd
class OpenFile:
    def open_file(entry):
        #for i in entries:
        temp_field = entry.split('/')
        new_field = temp_field[(len(temp_field) - 1)]
        print('Opening ' + new_field[:-4])
        if entry[-4:] == '.csv':
            data = pd.read_csv(entry, low_memory=False)
            data.columns = [col.strip() for col in data.columns]
            return data
        elif (entry[-4:] == 'xlsx') or (entry[-4:] == '.xls') or ((entry[-4:])[:3] == 'xls'):
            data = pd.read_excel(entry, sheet_name=0)
            data.columns = [col.strip() for col in data.columns]
            return data
        else:
            print('Not a valid file type...yet.')
                # print(data)
                # print(data.head())
    def map_func(data_frame, indexes):
        new_list = {}
        new_list.update(indexes)
        for column in data_frame.columns.values:
            for value in data_frame[column].values:
                if value not in indexes:
                    new_list[value] = ((len(indexes)+1) + len(new_list))
        #temp_list = new_list.update(indexes)
        for item in new_list:
            #print(item)
            for column in data_frame.columns.values:
                data_frame[column].map({item:new_list[item]})
        return new_list

class Split_Entry:
    def split(entry):
        entry = entry
        if len(entry.split()) > 1: #'\t'
            temp_set = entry.split() #'\t'
            real_list = []
            for item in temp_set:
                if len(list(filter(bool, item.splitlines()))) > 1:
                    new_string = list(filter(bool, item.splitlines()))
                    for string in new_string:
                        real_list.append(string)
                else:
                    real_list.append(item.strip())
            real_list = list(dict.fromkeys(real_list))
            return real_list
        elif len(list(filter(bool, entry.splitlines()))) > 1:
            new_string = list(filter(bool, entry.splitlines()))
            new_string = list(dict.fromkeys(new_string))
            return new_string
        else:
            search_item = entry.strip()
            return search_item
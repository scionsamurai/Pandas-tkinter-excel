"""
For splitting input into list separated by \n and \t's
"""
class Split_Entry:
    def split(entry, func=0):
        def remove_dups(xlist):
            xlist = list(dict.fromkeys(xlist)) # Remove duplicates due to Dicts only able to have 1 key per item
            if '' in xlist:
                xlist.remove('') # Remove whitespace value
            if len(xlist) == 1:
                xlist = xlist[0] # Return just item if there is just 1 result / not list with single item
            return xlist
        def strip_list(nlist, removeDups=False):
            n_list = []
            for n in nlist:
                n_list.append(n.strip()) # For item in list strip items whitespace
            if removeDups:
                n_list = remove_dups(n_list) # Remove duplicates from list if set removeDupes=True
            return n_list
        if func == 1:
            return remove_dups(entry)
        if len(entry.split('\t')) > 1 and len(entry.split('\n')) > 1: # If list contains tabs and new lines
            t_split_l = entry.split('\t')
            split_l = []
            for t_split in t_split_l:
                n_split_l = t_split.split('\n')
                split_l.extend(strip_list(n_split_l))
            split_l = remove_dups(split_l)
            return split_l
        elif len(entry.split('\t')) > 1: # Else if list contains only tabs
            t_split_l = entry.split('\t')
            split_l = strip_list(t_split_l, True)
            return split_l
        elif len(entry.split('\n')) > 1: # Else if list contains only new lines
            n_split_l = entry.split('\n')
            split_l = strip_list(n_split_l, True)
            return split_l
        else: # Else return item with lead/trail whitespace stripped
            return entry.strip()

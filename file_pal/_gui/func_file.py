"""
General Functions Pulled to trim primary code
"""
from tkinter import END
class GenFuncs:
    def update_entry(root, set_info, field_to_update, func=0):
        """
        Header button Function for updating main window input fields
        :param set_info: Info to add to input field
        :param field_to_update: Field to update
        :param func: 1=Delete field/Add Info, 2=Delete field, Else=Add Info+Tab
        """
        if func == 1:
            try:
                field_to_update.delete(0, END)
                field_to_update.insert(0, (str(set_info)))
            except TypeError:
                print('error at update_entry')
            root.destroy()
        elif func == 2:
            field_to_update.delete(0, END)
        else:
            def isint(x):
                try:
                    a = float(x)
                    b = int(a)
                except ValueError:
                    return False
                else:
                    return a==b
            try:
                if isint(set_info):
                    field_to_update.insert(0, (str(set_info) + "\t"))
                else:
                    try:
                        if float(set_info):
                            print('Can\'t insert value due to extra decimals in value on original file.')
                    except:
                        field_to_update.insert(0, (str(set_info) + "\t"))
            except:
                field_to_update.insert(0, (str(set_info) + "\t"))
    

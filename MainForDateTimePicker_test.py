# 05/08/2019
# 22:15

from tkinter import Tk
from DateTimePicker_classdef import DateTimePicker

# main
root = Tk()
root.title('DateTime picker')
root.geometry(f'200x300+500+50')
my_calendar = DateTimePicker(root)
root.mainloop()
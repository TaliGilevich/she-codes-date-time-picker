# 05/08/2019
# 22:15

from tkinter import Frame
from Calendar_classdef import Calendar
from Clock_classdef import Clock

class DateTimePicker(Frame):
    """This method represents a date-time-picker
    Inherits from the Tkinter Frame Class.
    Responsible for providing framework date and time selection

    TBD: storing and providing up-to-date information regarding the selected date and time (generates appropriate datetime object).

    """
    def __init__(self, container):
        super().__init__(container)
        self.create_widgets(container)

    def create_widgets(self, container):
        self.frm_main_datetime_picker = Frame(container)
        self.frm_main_datetime_picker.pack()

        self.calendar = Calendar(self.frm_main_datetime_picker)
        self.clock = Clock(self.frm_main_datetime_picker)
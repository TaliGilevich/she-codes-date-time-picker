# 05/08/2019
# 22:15

from datetime import time
from tkinter import Frame, Button, Label, Entry, StringVar, DISABLED, NORMAL

class Clock(Frame):
    """This class represents a time-picker.
    Inherits from the Tkinter Frame Class.
    Object of this class is designed to serve as time-picker component within DateTimePicker.
    Responsible for providing framework for setting hour and minute values in following ways:
    - direct typing into appropriate field
    - increment / decrement of the value via UI(up and down buttons)
    - increment / decrement of the value via keyboard (up and down arrow keys)

    TBD: storing and providing up-to-date information regarding the selected time.

    """
    # class variables
    font_name = 'Tahoma 10'
    frame_bdwidth = 6
    frame_bgcolor = 'snow3'  # to be updated
    widget_bdwidth = 0
    arrowbtn_font = '"Wingdings 3" 9'
    arrow_up_text = '' # displayed: up-pointing triangle  #'\u23EB'    # to watch here: https://unicode-search.net/unicode-namesearch.pl?term=TRIANGLE #'\u2660' :)
    arrow_down_text = '' # displayed: down-pointing triangle #'\u23EC'
    entry_bgcolor = 'snow' #ivory'#'white'

    default_clockdef_bgcolor = 'snow'#'ivory'#'SystemButtonFace'
    default_clockdef_fontcolor = 'SystemButtonText'
    selected_clockdef_bgcolor = 'palevioletred4'#'pink4'
    selected_clockdef_fontcolor = 'white'#'ivory'#'floral white'

    min_hour_12 = 1   # minimum hour value in 12-hours clock format
    max_hour_12 = 12  # maximum hour value in 12-hours clock format
    min_hour_24 = time.min.hour   # 0    #datetime.time.min.hour
    max_hour_24 = time.max.hour   # 23   #datetime.time.max.hour
    min_minute = time.min.minute  # 0    #datetime.time.min.minute
    max_minute = time.max.minute  # 59   #datetime.time.max.minute

    def __init__(self, container):
        """ctor"""

        super().__init__(container)

        # control variables for hour and minute(the clock is initialized to 00:00)
        self.hh_ctrlvar = StringVar()
        self.hh_ctrlvar.set('00')
        self.mm_ctrlvar = StringVar()
        self.mm_ctrlvar.set('00')

        self.is_24hour_clock = True  # the clock is initialized to 24hour-clock format
        self.is_AM = True  # hour value is set to 0 therefore initializing this flag to True does not contradict this setting (although it is not relevant while in 24hours format)

        self.create_widgets(container)

        # events
        # enabling increment / decrement of the hour and minute values using up and down arrow keyboard keys
        # (since the clock is initialized to 00:00, it is only possible to increment hour and minute values)
        self.hourdown_funcid = None
        self.hourup_funcid = self.entry_hh.bind('<Up>', self.action_hour_up)
        self.minutedown_funcid = None
        self.minuteup_funcid = self.entry_mm.bind('<Up>', self.action_minute_up)
        # enabling typing into hh and mm fields
        self.entry_hh.bind('<KeyRelease>', self.action_enter_hour)
        self.entry_mm.bind('<KeyRelease>', self.action_enter_minute)

        # initializtion to 24hour-clock format
        self.action_set_24hour_clock()

    def create_widgets(self, container):
        """This method defines UI of the time picker"""
        self.frm_main_clock = Frame(container, bg=__class__.frame_bgcolor, bd=__class__.frame_bdwidth)
        self.frm_main_clock.grid(row=1)

        self.frm_time = Frame(self.frm_main_clock, bg=__class__.frame_bgcolor)
        self.frm_time.grid(row=0, column=0, padx=3)

        self.frm_clockdef = Frame(self.frm_main_clock, bg=__class__.frame_bgcolor)
        self.frm_clockdef.grid(row=0, column=1, padx=3)

        self.btn_hh_up = Button(self.frm_time, command=self.action_hour_up, text=__class__.arrow_up_text, font=__class__.arrowbtn_font, bg=__class__.frame_bgcolor, bd=__class__.widget_bdwidth) #font=__class__.arrowbtn_font, , bd=__class__.widget_bdwidth
        self.btn_hh_up.grid(row=0, column=0)

        self.entry_hh = Entry(self.frm_time, insertbackground=__class__.entry_bgcolor, font=__class__.font_name, width=2, bg=__class__.entry_bgcolor, bd=__class__.widget_bdwidth, text=self.hh_ctrlvar)
        self.entry_hh.grid(row=1, column=0)

        self.btn_hh_down = Button(self.frm_time, state=DISABLED, command=self.action_hour_down, text=__class__.arrow_down_text, font=__class__.arrowbtn_font, bg=__class__.frame_bgcolor, bd=__class__.widget_bdwidth)
        self.btn_hh_down.grid(row=2, column=0)

        self.lbl_colon = Label(self.frm_time, text=':', bg=__class__.frame_bgcolor)
        self.lbl_colon.grid(row=1, column=1)

        self.btn_mm_up = Button(self.frm_time, command=self.action_minute_up, text=__class__.arrow_up_text, font=__class__.arrowbtn_font, bg=__class__.frame_bgcolor, bd=__class__.widget_bdwidth)
        self.btn_mm_up.grid(row=0, column=2)

        self.entry_mm = Entry(self.frm_time, font=__class__.font_name, width=2, bg=__class__.entry_bgcolor, bd=__class__.widget_bdwidth, text=self.mm_ctrlvar)
        self.entry_mm.grid(row=1, column=2)

        self.btn_mm_down = Button(self.frm_time, state=DISABLED, command=self.action_minute_down, text=__class__.arrow_down_text, font=__class__.arrowbtn_font, bg=__class__.frame_bgcolor, bd=__class__.widget_bdwidth)
        self.btn_mm_down.grid(row=2, column=2)

        self.btn_AM = Button(self.frm_clockdef, command=self.action_define_AM, text='AM', font=__class__.font_name, bd=__class__.widget_bdwidth)
        self.btn_AM.grid(row=0, column=0, ipadx=2, padx=2, pady=3)

        self.btn_PM = Button(self.frm_clockdef, command=self.action_define_PM, text='PM', font=__class__.font_name, bd=__class__.widget_bdwidth)
        self.btn_PM.grid(row=0, column=2, ipadx=2, padx=2, pady=3)

        self.btn_12 = Button(self.frm_clockdef, command=self.action_set_12hour_clock, text='12', font=__class__.font_name, bd=__class__.widget_bdwidth)
        self.btn_12.grid(row=3, column=0, ipadx=3, pady=3)

        self.btn_24 = Button(self.frm_clockdef, command=self.action_set_24hour_clock, text='24', font=__class__.font_name, bd=__class__.widget_bdwidth)
        self.btn_24.grid(row=3, column=2, ipadx=3, pady=3)

    def action_set_24hour_clock(self, event=None):
        """This method is a callback for mouse click on 24hour-clock button
        It is responsible for setting definitions according to required clock format as follows:
        - conversion hour value into 24hour-clock format
        - disabling AM and PM buttons as not relevant
        - making decision whether to block further increment or decrement of the hour according to the format limits

        """
        self.is_24hour_clock = True

        # disabling AM and PM buttons as not relevant for 24hour-clock format
        for btn in (self.btn_AM, self.btn_PM):
            btn.configure(state=DISABLED, bg=__class__.default_clockdef_bgcolor, fg=__class__.default_clockdef_fontcolor)

        # displaying 24hour-clock button as selected, 12hour-clock button as not selected(default view)
        self.btn_24.configure(bg=__class__.selected_clockdef_bgcolor, fg=__class__.selected_clockdef_fontcolor)
        self.btn_12.configure(bg=__class__.default_clockdef_bgcolor, fg=__class__.default_clockdef_fontcolor)

        # retrieving value of the currently displayed hour
        displayed_hour = int(self.hh_ctrlvar.get())

        # recalculation of the displayed hour according to 24hours clock(based on existing value of the is_AM flag)
        if self.is_AM:
            if displayed_hour == 12:  # 12AM is midnight
                displayed_hour -= 12  # 12AM is converted into 0(00 is to be displayed)
        else: # i.e. PM
            if displayed_hour < 12:
                displayed_hour += 12  # hours between 1 - 11 inclusive are to be converted into 13 - 23 respectively

        # validations and settings
        self.config_hour(displayed_hour)

    def action_set_12hour_clock(self, event=None):
        """This method is a callback for mouse click on 12hour-clock button
        It is responsible for setting definitions according to required clock format as follows:
        - conversion hour value into 12hour-clock format and setting value of the is_AM flag accordingly
        - enabling AM and PM buttons and setting their view based on current is_AM definition
        - making decision whether to block further increment or decrement of the hour according to the clock format limits

        """
        self.is_24hour_clock = False  # i.e., it is 12-hours clock
        self.btn_12.configure(bg=__class__.selected_clockdef_bgcolor, fg=__class__.selected_clockdef_fontcolor)
        self.btn_24.configure(bg=__class__.default_clockdef_bgcolor, fg=__class__.default_clockdef_fontcolor)

        # retrieving value of the currently displayed hour
        displayed_hour = int(self.hh_ctrlvar.get())

        # determining value of the is_AM flag based on displayed hour
        self.is_AM = displayed_hour < 12  # True if displayed hour is between 0 - 11 inclusive, otherwise PM

        # recalculation of the displayed hour according to 12-hours clock (based on the current value of the is_AM flag)
        if self.is_AM:
            self.btn_AM.configure(state=NORMAL, bg=__class__.selected_clockdef_bgcolor, fg=__class__.selected_clockdef_fontcolor)
            self.btn_PM.configure(state=NORMAL, bg=__class__.default_clockdef_bgcolor, fg=__class__.default_clockdef_fontcolor)
            if displayed_hour == __class__.min_hour_24:  # i.e. 0 (e.g. midnight)
                displayed_hour += 12  # i.e. 0 by 24-hour clock is converted into 12 AM
        else:  # PM
            self.btn_PM.configure(state=NORMAL, bg=__class__.selected_clockdef_bgcolor, fg=__class__.selected_clockdef_fontcolor)
            self.btn_AM.configure(state=NORMAL, bg=__class__.default_clockdef_bgcolor, fg=__class__.default_clockdef_fontcolor)
            if displayed_hour in range (13, 24):
                displayed_hour -= 12  # hours in range 13 - 23 inclusive are to be converted into 1 - 11 respectively

        # validations and settings
        self.config_hour(displayed_hour)

    def action_define_AM(self, event=None):
        """This method is a callback for mouse-click on AM button
        It is responsible for the following:
        - setting valuie of the is_AM flag to True
        - activating the AM indicator (i.e. displaying AM button as selected)
        - disactivating PM indicator (i.e. 'deselecting' the PM button)

        """
        self.is_AM = True
        self.btn_AM.configure(bg=__class__.selected_clockdef_bgcolor, fg=__class__.selected_clockdef_fontcolor)
        self.btn_PM.configure(bg=__class__.default_clockdef_bgcolor, fg=__class__.default_clockdef_fontcolor)

    def action_define_PM(self, event=None):
        """This method is a callback for mouse-click on PM button
        It is responsible for the following:
        - setting valuie of the is_AM flag to False
        - activating the PM indicator (i.e. displaying PM button as selected)
        - disactivating AM indicator (i.e. 'deselecting' the AM button)

        """
        self.is_AM = False
        self.btn_PM.configure(bg=__class__.selected_clockdef_bgcolor, fg=__class__.selected_clockdef_fontcolor)
        self.btn_AM.configure(bg=__class__.default_clockdef_bgcolor, fg=__class__.default_clockdef_fontcolor)

    def action_enter_hour(self, event=None):
        """This method is a callback for typing into the hour entry field
         It is responsible to pass inserted value to auxiliary function for further validations

         """
        # retrieving hour value typed by the user from appropriate control variable
        displayed_hour = self.hh_ctrlvar.get()

        # validations and settings
        self.config_hour(displayed_hour)

    def config_hour(self, hour_val):
        """This method is responsible for the processing of the user input as follows:
         - validations and fixes(i.e. setting valid value instead) if necessary
         - making decision whether to block further increment or decrement of the hour

         """
        # limits definitions based on the clock format
        if self.is_24hour_clock:
            max_hour = __class__.max_hour_24
            min_hour = __class__.min_hour_24
        else:
            max_hour = __class__.max_hour_12
            min_hour = __class__.min_hour_12

        # validating and fixing value inserted by the user(if necessary)
        if isinstance(hour_val, str):  # str means it was typing therefore validation is required (otherwise, int: increment or decrement via buttons / arrowkeys)
            if hour_val.isdigit():  # string that consists of digits only
                hour_val = int(hour_val)
                if hour_val > max_hour:
                    hour_val = max_hour
                elif hour_val < min_hour:
                    hour_val = min_hour
            else:  # string that contains not only digits
                hour_val = min_hour

        # updating the control variable: valid value(zero-padded if necessary) is being immediately reflected in UI
        self.hh_ctrlvar.set(f'{hour_val:02}')

        # enabling both increnent and decrement of the value either via UI(hour-up, hour-down buttons) or via keyboard(arrow-up and arrow-down keys)
        for btn in (self.btn_hh_down, self.btn_hh_up): btn.configure(state=NORMAL)  # enabling hour-up and hour-down buttons
        self.hourup_funcid = self.entry_hh.bind('<Up>', self.action_hour_up)  # binding a callback for the arrow-up keyboard key
        self.hourdown_funcid = self.entry_hh.bind('<Down>', self.action_hour_down)  # binding a callback for the arrow-down keyboard key

        # making decision whether to block increment or decrement of the hour judging by its current value:
        # in case upper or lower limit value is reached, blocking corresponding option both via UI and via keyboard
        if hour_val == min_hour:
            self.btn_hh_down.configure(state=DISABLED)
            self.entry_hh.unbind('<Down>', self.hourdown_funcid)
        elif hour_val == max_hour:
            self.btn_hh_up.configure(state=DISABLED)
            self.entry_hh.unbind('<Up>', self.hourup_funcid)

    def action_hour_up(self, event=None):
        """This method is a callback for mouse click on hour-up button / for hitting arrow-up keyboard key
         It is responsible for the following:
         incrementing displayed hour value by 1
         passing it to auxiliary function for further validations and settings

         """
        # incrementing current value stored in appropriate control variable by 1
        displayed_hour = int(self.hh_ctrlvar.get()) + 1

        # validations and settings
        self.config_hour(displayed_hour)

    def action_hour_down(self, event=None):
        """This method is a callback for mouse click on hour-down button / for hitting arrow-down keyboard key
         It is responsible for the following:
         decrementing displayed hour value by 1
         passing it to auxiliary function for further validations and settings

         """
        # decrementing current value stored in appropriate control variable by 1
        displayed_hour = int(self.hh_ctrlvar.get()) - 1

        # validations and settings
        self.config_hour(displayed_hour)

    def config_minute(self, minute_val):
        """This method is responsible for the processing of the user input as follows:
         - validations and fixes(i.e. setting valid value instead) if necessary
         - making decision whether to block further increment or decrement of the minute

         """
        # validating and fixing value inserted by the user(if necessary)
        if isinstance(minute_val, str):  # str means it was typing therefore validation is required (otherwise, int: increment or decrement via buttons / arrowkeys)
            if minute_val.isdigit():  # string that consists of digits only
                minute_val = int(minute_val)
                if minute_val >  __class__.max_minute:
                    minute_val =  __class__.max_minute
                elif minute_val <  __class__.min_minute:
                    minute_val = __class__.min_minute
            else:  # string that contains not only digits
                minute_val = __class__.min_minute

        # updating the control variable: valid value(zero-padded if necessary) is being immediately reflected in UI
        self.mm_ctrlvar.set(f'{minute_val:02}')

        # enabling both increnent and decrement of the value either via UI(minute-up, minute-down buttons) or via keyboard(arrow-up and arrow-down keys)
        for btn in (self.btn_mm_down, self.btn_mm_up): btn.configure(state=NORMAL)  # enabling minute-up and minute-down buttons
        self.minuteup_funcid = self.entry_mm.bind('<Up>', self.action_minute_up)  # binding a callback for the arrow-up keyboard key
        self.minutedown_funcid = self.entry_mm.bind('<Down>', self.action_minute_down)  # binding a callback for the arrow-down keyboard key

        # making decision whether to block increment or decrement of the minute judging by its current value:
        # in case upper or lower limit value is reached, blocking corresponding option both via UI and via keyboard
        if minute_val == __class__.min_minute:
            self.btn_mm_down.configure(state=DISABLED)
            self.entry_mm.unbind('<Down>', self.minutedown_funcid)
        elif minute_val == __class__.max_minute:
            self.btn_mm_up.configure(state=DISABLED)
            self.entry_mm.unbind('<Up>', self.minuteup_funcid)

    def action_minute_up(self, event=None):
        """This method is a callback for mouse click on minute-up button / for hitting arrow-up keyboard key
         It is responsible for the following:
         incrementing displayed minute value by 1
         passing it to auxiliary function for further validations and settings

         """
        # incrementing current value stored in appropriate control variable by 1
        displayed_minute = int(self.mm_ctrlvar.get())+1

        # validations and settings
        self.config_minute(displayed_minute)

    def action_minute_down(self, event=None):
        """This method is a callback for mouse click on minute-down button / for hitting arrow-down keyboard key
         It is responsible for the following:
         decrementing displayed minute value by 1
         passing it to auxiliary function for further validations and settings

         """
        # decrementing current value stored in appropriate control variable by 1
        displayed_minute = int(self.mm_ctrlvar.get())-1

        # validations and settings
        self.config_minute(displayed_minute)

    def action_enter_minute(self, event=None):
        """This method is a callback for typing into the minute entry field
         It is responsible to pass inserted value to auxiliary function for further validations

        """
        # retrieving minute value typed by the user from appropriate control variable
        displayed_minute = self.mm_ctrlvar.get()

        # validations and settings
        self.config_minute(displayed_minute)


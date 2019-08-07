# 05/08/2019
# 22:15

import datetime
from calendar import Calendar, weekheader, setfirstweekday
setfirstweekday(6)  # Sunday is specified to be the first day of the week (necessary for the weekheader_string to start from Sunday)

from tkinter import Frame, Label
from DayKey_classdef import DayKey

class MonthDispatcher():
    """This class is responsible for displaying calendar of the given month of the year.
    If necessary, completes monthdatescalendar generated by Python to make it contain exactly 6 weeks
    (relevant data is retrieved from the monthdatescalendar(s) of the preceding and / or succeeding months)
    Creates list of DayKey widgets based on above-mentioned monthdatescalendar and displays it as 6 x 7 matrix.

    TBD: detecting date selection event, building datetime object and providing it to external units or to encapsulating class Calendar

    """
    # class variables
    today_date = datetime.date.today()

    weekheader_string = weekheader(2)  # i.e. 'Su Mo Tu We Th Fr Sa'
    weekheader_font = 'Consolas 9 bold'
    #weekheader_bgcolor = 'snow2'
    #bgcolor = 'snow2'

    def __init__(self, container, year, month_seqnum):
        """ctor"""
        self.all_days_lst = []  # list of DayKey widgets representing the days to be displayed according to the given month+year combination

        self.create_widgets(container)
        self.arrange_month(year, month_seqnum)

    def create_widgets(self, container):
        """This method defines UI of the calendar of the given month"""
        self.lbl_weekheader = Label(container, text=f'{__class__.weekheader_string}', font=__class__.weekheader_font) #, bg=__class__.weekheader_bgcolor
        self.lbl_weekheader.grid(row=0)

        self.frm_month_area = Frame(container)
        self.frm_month_area.grid(row=1)

    def generate_month_calendar(self, year, month_seqnum):
        """This method is responsible for generating 6-weeks monthdatescalendar for the given month of the year"""

        # Sunday is specified to be the first day of the week (necessary for appropriate deployment of the days of month)
        cal = Calendar(firstweekday=6)

        # list of weeks of the given month of the year as full weeks; week is list of seven datetime.date objects
        month_dates_cal = cal.monthdatescalendar(year, month_seqnum)
        weeks_cnt = len(month_dates_cal)  # i.e. weeks in the monthdatescalendar generated by Python

        # adding either one or two weeks to complete to the total of 6 weeks
        if weeks_cnt < 6:
            # in case first day of the given month is the first day of the week(i.e. Sunday),
            # it is necessary to add the last week of the preceding month
            if month_dates_cal[0][0].day == 1:
                prev_month_seqnum = month_seqnum - 1
                prev_year = year
                if prev_month_seqnum == 0:
                    prev_month_seqnum = 12
                    prev_year = year - 1

                month_dates_cal.insert(0, cal.monthdatescalendar(prev_year, prev_month_seqnum)[-1])  # week index is -1 i.e. the last week of the preceding month
                weeks_cnt = len(month_dates_cal)

            # if (either originally or after adding the last week of the preceding month) one week is missing to complete to the total of 6,
            # it is necessary to append the first week of the succeeding month
            if weeks_cnt == 5:
                next_year = year
                next_month_seqnum = month_seqnum + 1
                if next_month_seqnum == 13:
                    next_month_seqnum = 1
                    next_year = year + 1

                nextmonth_cal = cal.monthdatescalendar(next_year, next_month_seqnum)
                nextmonth_week = 1  # first week of the succeeding month contains days of the given month therefore the second week is to be appended
                if nextmonth_cal[0][0].day == 1:
                    nextmonth_week = 0  # in case the first day of the succeeding month is the first day of the week(i.e. Sunday), the first week is to be appended

                month_dates_cal.append(nextmonth_cal[nextmonth_week])

        # list flattening:
        month_dates_cal = [day for week in month_dates_cal for day in week]
        return month_dates_cal

    def arrange_month(self, year, month_seqnum):
        """This method is responsible for displaying a 6-weeks calendar consisting of the DayKey widgets for the given month of the year"""
        month_cal = self.generate_month_calendar(year, month_seqnum)  # flattebed list of the datetime.date objects

        # building list of DayKey widgets based on the generated month calendar
        for daykey in self.all_days_lst:
            daykey.grid_forget()
        self.all_days_lst.clear()
        self.all_days_lst.extend([DayKey(self.frm_month_area, textval=date_object.day) for date_object in month_cal])

        # setting appearance of the today's day
        if __class__.today_date in month_cal:
            today_ordnum = month_cal.index(__class__.today_date)
            self.all_days_lst[today_ordnum].is_today = True
            self.all_days_lst[today_ordnum].design()

        # determining the scope of the given month:
        # days between the first of the given month(inclusive) and the first of the succeeding month(exclusive) belong to the given month
        # days out of this scope belong to preceding or to succeeding month respectively i.e. considered offmonth_days
        given_month_the_1st, next_month_the_1st = [ordnum for ordnum, date in enumerate(month_cal) if month_cal[ordnum].day == 1]

        # setting appearance of the offmonth days
        offmonth_daykeys_lst = self.all_days_lst[:given_month_the_1st]
        offmonth_daykeys_lst.extend(self.all_days_lst[next_month_the_1st:])
        for daykey in offmonth_daykeys_lst:
            daykey.is_off_month = True
            daykey.design()

        # displaying the month calendar
        week_len = 7  # determines number of columns in the 6 x 7 matrix representing the calendar of the month
        for ordnum, daykey in enumerate(self.all_days_lst):
            daykey.grid(row=ordnum // week_len, column=ordnum % week_len, ipadx=2, ipady=1)

import datetime #datetime lib
import calendar #calendar object for easy datetime arrays and printing
from colorama import Style, Fore, init #For coloured output in bash
init(convert=True) #Coloured text doesn't work with git bash out the box so added this to help

import tkinter
from tkcalendar import *

cal = calendar.Calendar()
txt_cal = calendar.TextCalendar()




app = tkinter.Tk()
app.title('Calendar')
app.geometry('300x200')

tkcalendar = TkCalendar()

tkinter.Label(app, text='{} {}'.format(2021, 12)).pack()

frame = tkcalendar.formatmonth(app, 2021, 12)
frame.pack()

app.mainloop()

import datetime #datetime lib
import calendar #calendar object for easier printing so we don't have to just reinvent it with datetime arrays
from colorama import Style, Fore, init #For coloured output in bash
init(convert=True) #Coloured text doesn't work with git bash out the box so added this to help
import tkinter # For GUI
from tkinter import messagebox
from tkcalendar import * #Self made helper class for visualizing the calendar
import csv # To read/write to the "db" file

#helper function to add to our task array for both reading DB and parsing a new task
def addtask(date, task):
    global tasks
    if date not in tasks.keys(): #If the date is not yet in the dict add it
        tasks[date] = [task]
    else:
        tasks[date].append(task)

#Parse new task on button press and add it to the dict if it was valid
def parsetask():
    date = date_entry.get()
    task = task_entry.get()
    try:
        date = datetime.datetime.strptime(date, "%d.%m.%Y")
        addtask(date, task)
        #Clear fields
        date_entry.delete(0, 'end')
        task_entry.delete(0, 'end')
    except ValueError:
        messagebox.showerror(title='Wrong format', message='Please use dd.mm.yyyy format for date.')

def changemonth(date):
    global cal_frame
    global app
    current.set(date.strftime("%B %Y"))
    newFrame = tkcalendar.formatmonth(app, date.year, date.month)
    if cal_frame is not None:
        cal_frame.destroy()
    cal_frame = newFrame
    newFrame.pack()

def prevmonth():
    global current
    #Update the title
    lastMonth = datetime.datetime.strptime(current.get(), "%B %Y") + datetime.timedelta(days=-1)
    current.set(date.strftime("%B %Y"))
    changemonth(lastMonth)

def nextmonth():
    global current
    #Update the title
    nextMonth = datetime.datetime.strptime(current.get(), "%B %Y") + datetime.timedelta(weeks=4, days=3)
    current.set(date.strftime("%B %Y"))
    changemonth(nextMonth)

#Load tasks from file into a dict on initial load
tasks = {}
try:
    with open('tasks.csv', 'r',newline='') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            date = datetime.datetime.fromisoformat(row[0])
            addtask(date, row[1])
except FileNotFoundError: #Catch if the file doesn't exist
    open('tasks.csv', 'w+')

app = tkinter.Tk()
app.title('Calendar')

current_date = datetime.date.today()
current = tkinter.StringVar()
current.set(current_date.strftime("%B %Y"))

tkcalendar = TkCalendar(list(tasks.keys()))

header = tkinter.Frame(app)
header.pack()

tkinter.Button(header, text='<-', command=prevmonth).grid(row=0, column=0)
monthLabel = tkinter.Label(header, textvariable=current, font="Roboto 14 bold")
monthLabel.grid(row=0, column=1)
tkinter.Button(header, text='->', command=nextmonth).grid(row=0, column=2)

cal_frame = tkcalendar.formatmonth(app, current_date.year, current_date.month)
cal_frame.pack()

tasks_frame = tkinter.Frame(app)
tasks_frame.pack(side=tkinter.BOTTOM)

tkinter.Label(tasks_frame, text=f'Today\'s tasks ({datetime.date.today().strftime("%d.%m.")})', font='Roboto 12 bold').pack()
for date, entries in tasks.items():
    if date.day == datetime.date.today().day:
        for task in entries:
            task_label = tkinter.Label(tasks_frame, text=task)
            task_label.pack()

entry_frame = tkinter.Frame(app)
entry_frame.pack(side=tkinter.BOTTOM)

tkinter.Label(entry_frame, text="Enter date:").grid(column = 0, row= 0)
date_entry = tkinter.Entry(entry_frame, width=22)
date_entry.grid(column = 1, row= 0, sticky='w')

tkinter.Label(entry_frame, text="Enter task:").grid(column = 0, row= 1)
task_entry = tkinter.Entry(entry_frame, width=22)
task_entry.grid(column = 1, row= 1)

btn = tkinter.Button(entry_frame, text = 'Add task', command=parsetask)
btn.grid(column = 0, row= 2)

#Launch the GUI
app.mainloop()

#After GUI closes write the tasks back to file (overwriting it)
#Probably a bit less resource intensive than writing to file every time a change happens
#Also enables deletion
with open('tasks.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    for date, tasks in tasks.items():
        for task in tasks:
            writer.writerow([date, task])

import datetime #datetime lib
import calendar
from tkinter.constants import BOTTOM, LEFT, TOP #calendar object for easier printing so we don't have to just reinvent it with datetime arrays
from colorama import Style, Fore, init #For coloured output in bash
init(convert=True) #Coloured text doesn't work with git bash out the box so added this to help
import tkinter
from tkcalendar import *
import csv

#helper function to add to our task array for both reading DB and parsing a new task
def addtask(date, task):
    if date not in tasks.keys(): #If the date is not yet in the dict add it
        tasks[date] = [task]
    else:
        tasks[date].append(task)

#Load tasks from file into a dict on initial load
tasks = {}
with open('tasks.csv', newline='') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        date = datetime.datetime.fromisoformat(row[0])
        addtask(date, row[1])

#Parse new task on button press and add it to the dict if it was valid
def parsetask():
    date = date_entry.get()
    task = task_entry.get()
    try:
        date = datetime.datetime.strptime(date, "%d.%m.%Y")
        addtask(date, task)
    except ValueError:
        pass
    print(tasks)

app = tkinter.Tk()
app.title('Calendar')
app.geometry('450x300')

tkcalendar = TkCalendar(list(tasks.keys()))

tkinter.Label(app, text='{0:%B} {0:%Y}'.format(datetime.date.today())).pack()

frame = tkcalendar.formatmonth(app, 2021, 12)
frame.pack()

entry_frame = tkinter.Frame(app)
entry_frame.pack()

tkinter.Label(entry_frame, text="Enter date:").grid(column = 0, row= 0)
date_entry = tkinter.Entry(entry_frame, width=20)
date_entry.grid(column = 1, row= 0, sticky='w')

tkinter.Label(entry_frame, text="Enter task:").grid(column = 0, row= 1)
task_entry = tkinter.Entry(entry_frame, width=40)
task_entry.grid(column = 1, row= 1)

btn = tkinter.Button(entry_frame, text = 'Add task', command=parsetask)
btn.grid(column = 0, row= 2)

#Launch the GUI
app.mainloop()

#After GUI closes write the tasks back to file (overwriting it)
#Figure this is better practice than opening the file whenever we want to write something into it
with open('tasks.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    for date, tasks in tasks.items():
        for task in tasks:
            writer.writerow([date, task])

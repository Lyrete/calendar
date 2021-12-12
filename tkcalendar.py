import calendar #calendar object for easy datetime arrays and printing
import datetime #datetime lib
import tkinter

class TkCalendar(calendar.Calendar):
    def __init__(self, busy_dates) -> None:
        super().__init__(0)
        self.busy_dates = busy_dates
        print(busy_dates)
        

    def formatmonth(self, master, year, month):
        dates = self.monthdatescalendar(year, month)

        frame = tkinter.Frame(master)

        self.labels = []

        for row, week in enumerate(dates):
            label_row = []
            for column, date in enumerate(week):
                label = tkinter.Label(frame, text=date.day, font='Roboto 10')
                label.grid(row = row, column = column)

                label['bd'] = 4
                if date.day == datetime.date.today().day:
                    label['fg'] = 'red'
                
                
                if datetime.datetime.fromisoformat(str(date)) in self.busy_dates:
                    label['font'] = 'Roboto 10 bold'
                
                #Hide dates that don't actually belong to the running month
                if(date.month != month):
                    label['text'] = ''

                label_row.append(label)
            self.labels.append(label_row)
        
        return frame
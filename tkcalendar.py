import calendar #calendar object for easy datetime arrays and printing
import datetime #datetime lib
import tkinter

class TkCalendar(calendar.Calendar):
    def formatmonth(self, master, year, month):
        dates = self.monthdatescalendar(year, month)

        frame = tkinter.Frame(master)

        self.labels = []

        for row, week in enumerate(dates):
            label_row = []
            for column, date in enumerate(week):
                label = tkinter.Label(frame, text=date.day)
                label.grid(row = row, column = column)

                if(date.day == datetime.date.today().day):
                    label['fg'] = 'red'
                
                #Hide dates that don't actually belong to the running month
                if(date.month != month):
                    label['text'] = ''

                label_row.append(label)
            self.labels.append(label_row)
        
        return frame
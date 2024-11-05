from tkinter import *
from tkinter import ttk

import dbconnect

# creating the window
root = Tk()
root.title("Reminder App")
wdt = 720
hgt = 540
scw = root.winfo_screenwidth()
sch = root.winfo_screenheight()
x = (scw/2) - (wdt/2)
y = (sch/2) - (hgt/2)
root.geometry('%dx%d+%d+%d' % (wdt, hgt, x, y))

# creating tabs
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Reminder')
tabControl.add(tab2, text='Edit Reminders')
tabControl.pack(expand=1, fill="both")


class AtStart():
    def __init__(self):
        dbconnect.date_remind.delete_auto()
        txt = dbconnect.date_remind
        self.main_lbl = Label(tab1, text=txt, font=("Corbel", 25), bg='red', fg='white')
        self.main_lbl.place(relx=0.5, rely=0.5, anchor=CENTER)

    def lbl_clear(self):
        self.main_lbl.destroy()


class MainPage(AtStart):
    def __init__(self):
        super().__init__()

        self.frame1 = Frame(tab2, bg='cyan')
        self.frame1.pack(side=TOP, fill=X)
        self.set_frame = Frame(self.frame1, bg="grey")
        self.set_frame.grid(column=1, row=2, sticky=E, padx=5, pady=5)
        self.del_frame = Frame(self.frame1, bg="grey")
        self.del_frame.grid(column=1, row=3, sticky=E, padx=5, pady=5)
        self.frame = Frame(tab2)
        self.frame.pack(side=LEFT, fill=Y)

        btn = Button(self.frame1, text="See Reminders", fg="red", command=self.see_reminders, width=20, borderwidth=1)
        btn.grid(column=0, row=1, sticky=W, padx=55, pady=15)
        btn1 = Button(self.frame1, text="Set Reminder", fg="red", command=self.set_reminder, width=20, borderwidth=1)
        btn1.grid(column=0, row=2, sticky=W, padx=55, pady=15)
        btn2 = Button(self.frame1, text="Remove a reminder", fg="red", command=self.delete_reminder, width=20, borderwidth=1)
        btn2.grid(column=0, row=3, sticky=W, padx=55, pady=15)
        refresh = Button(self.frame1, text="Refresh", fg="red", command=self.refresh, width=20, borderwidth=1)
        refresh.grid(column=0, row=4, sticky=W, padx=55, pady=15)

    def frame_clear(self):
        self.frame1.destroy()
        self.frame.destroy()
        self.set_frame.destroy()
        self.del_frame.destroy()

    def refresh(self):
        self.frame_clear()
        self.lbl_clear()
        self.__init__()

    def clear_only_see_lbl(self):
        for lbl in self.frame.winfo_children():
            lbl.destroy()

    def on_edit(self):
        self.clear_only_see_lbl()
        self.see_reminders()
        self.lbl_clear()
        super().__init__()

    def see_reminders(self):
        show = dbconnect.date_remind.show_all()
        count = 0
        if show == "No Reminders!":
            see_lbl = Label(self.frame, text="No Reminders!")
            see_lbl.grid(column=0, row=0)
        else:
            for i in show:
                see_lbl = Label(self.frame, text=i[0] + "-" + i[1] + ":  " + "'{}'".format(i[2]), bg='skyblue', font=("Corbel", 12))
                count += 1
                see_lbl.grid(column=0, row=0 + count, sticky=W, padx=5, pady=5)

    def set_reminder(self):
        self.date_format()
        lbl = Label(self.set_frame, text="Date:")
        lbl.grid(column=1, row=0)
        day = Entry(self.set_frame, width=4)
        day.grid(column=2, row=0)
        month = Entry(self.set_frame, width=4)
        month.grid(column=3, row=0)
        year = Entry(self.set_frame, width=6)
        year.grid(column=4, row=0)
        lbl = Label(self.set_frame, text="Note:")
        lbl.grid(column=5, row=0)
        task = Entry(self.set_frame, width=12)
        task.grid(column=6, row=0)

        def callback():
            try:
                yy = int(year.get())
                mm = int(month.get())
                dd = int(day.get())
                note = str(task.get())
                year.delete(0, END)
                month.delete(0, END)
                day.delete(0, END)
                task.delete(0, END)
                dbconnect.date_remind.set_reminder(yy, mm, dd, note)
                self.on_edit()

            except ValueError:
                self.is_empty()

        clear = Button(self.set_frame, text="Save", fg="red", command=callback)
        clear.grid(column=7, row=0)

    def delete_reminder(self):
        self.date_format()
        lbl = Label(self.del_frame, text="Date:")
        lbl.grid(column=1, row=0)
        day = Entry(self.del_frame, width=4)
        day.grid(column=2, row=0)
        month = Entry(self.del_frame, width=4)
        month.grid(column=3, row=0)
        year = Entry(self.del_frame, width=7)
        year.grid(column=4, row=0)

        def callback():
            try:
                yy = int(year.get())
                mm = int(month.get())
                dd = int(day.get())
                year.delete(0, END)
                month.delete(0, END)
                day.delete(0, END)
                dbconnect.date_remind.remove_reminder(yy, mm, dd)
                self.on_edit()

            except ValueError:
                self.is_empty()

        clear = Button(self.del_frame, text="Delete", fg="red", command=callback)
        clear.grid(column=5, row=0)

    def date_format(self):
        format_lbl = Label(self.frame1, text="Format: DD/MM/YYYY")
        format_lbl.grid(column=1, row=1, sticky=E)

    def is_empty(self):
        not_empty = Label(self.frame1, text="Field cannot be empty!")
        not_empty.grid(column=1, row=4, sticky=E)


start = MainPage()

root.mainloop()


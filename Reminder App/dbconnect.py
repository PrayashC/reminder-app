import mysql.connector
import datetime


class DbConnection:
    def __init__(self):
        # connecting to sql server
        self.db = mysql.connector.connect(host="", user="", password="", database="py_data")
        self.my_cursor = self.db.cursor()
        # my_cursor.execute("create database py_data")
        # my_cursor.execute("create table new_table(days VARCHAR(10), date DATE)")
        # my_cursor.execute("drop table new_table")


class Reminder(DbConnection):
    # get current date and closest remainder
    def __init__(self):
        super().__init__()
        self.current_date = datetime.datetime.now().date()
        self.my_cursor.execute("select date from new_table order by date asc limit 1")
        self.next_date = self.my_cursor.fetchone()  # to get the most recent task
        self.my_cursor.execute("select taskEvent from new_table order by date asc limit 1")
        self.task_event = self.my_cursor.fetchone()
        self.__str__()

    # convert msg into string
    def __str__(self):
        return self.days_remaining()

    # will show if today is any event or task to be carried out
    # or the days left for upcoming reminder
    def days_remaining(self):
        try:
            days_rem = self.next_date[0] - self.current_date
            if days_rem.days == 0:
                msg = str("Today's Reminder: {}".format(self.task_event[0]))
                return msg
            else:
                msg = str("No task/event today\n Next reminder in: {} day(s) on {}\n Note: '{}'".format(days_rem.days, self.next_date[0].strftime('%d/%m/%Y'), self.task_event[0]))
                return msg
        except:
            return self.msg_no_rem()

    def msg_no_rem(self):
        return str("No Reminders!")

    # for setting the reminder
    def set_reminder(self, year, month, day, task_event):
        remind = datetime.datetime(year, month, day)
        day = remind.strftime('%A')
        date = remind.strftime('%Y-%m-%d')
        self.my_cursor.execute("insert into new_table(days, date, taskEvent) values(%s, %s, %s)", (day, date, task_event))
        self.db.commit()  # directly inserts the input into sql table
        self.__init__()  # to update the recent date after new reminder

    # to remove reminder
    def remove_reminder(self, year, month, day):
        remove = datetime.datetime(year, month, day)
        date_to_remove = remove.strftime('%Y-%m-%d')
        self.my_cursor.execute("delete from new_table where date = '{}' limit 1".format(date_to_remove))
        self.db.commit()
        self.__init__()

    # shows all reminders
    def show_all(self):
        self.my_cursor.execute("select count(*) from new_table")
        check_null = self.my_cursor.fetchone()
        if check_null[0] == 0:
            return self.msg_no_rem()
        else:
            remind_list = []
            self.my_cursor.execute("select days, date, taskEvent from new_table order by date")
            all_dates = self.my_cursor.fetchall()
            for date in all_dates:
                remind_list.append([date[0], date[1].strftime('%d/%m/%Y'), date[2]])
            return remind_list  # this list returns all the entries from sql in order of date

    # delete all
    def delete_all(self):
        self.my_cursor.execute("delete from new_table")
        self.db.commit()
        self.__init__()

    # we need to make sure older reminders are automatically deleted
    def delete_auto(self):
        try:
            days_rem = self.next_date[0] - self.current_date
            del_next = self.next_date[0].strftime('%Y-%m-%d')
            if days_rem.days < 0:
                self.my_cursor.execute("delete from new_table where date = '{}'".format(del_next))
                self.db.commit()
        except:
            return None


date_remind = Reminder()
# # Testing # #
# date_remind.set_reminder(2024, 11, 3, 'Remind me to take garbage out')
# date_remind.days_remaining()
# date_remind.remove_reminder(2024, 11, 1)
# date_remind.show_all()
# date_remind.delete_all()
# date_remind.delete_auto()


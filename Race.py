try:
# for Python2
    from Tkinter import *
    from tkMessageBox import *
    from tkSimpleDialog import *## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *
    from tkinter.messagebox import *
    from tkinter.simpledialog import *
    from tkinter import ttk
    
    ## notice lowercase 't' in tkinter here
    
import requests
import logging
from datetime import *
import serial
import threading
import sqlite3
from messages import *
import os
import Settings
from ClassRace import *
from ClassReport import Report
from ClassRacer import *
from ClassApi import *
from ClassDB import *


def main():

    logging.basicConfig(filename="sample.log", level=logging.INFO)
    global ZELBIKE_ACCESS_KEY
    try:
        ZELBIKE_ACCESS_KEY = os.environ['ZELBIKE_ACCESS_KEY'] 
    except:
        ZELBIKE_ACCESS_KEY = input(MESSAGE_ENTER_ZELBIKE_ACCESS_KEY)
    conn = sqlite3.connect(Settings.DBName) 
    cursor = conn.cursor()
    try:
        cursor.execute("""CREATE TABLE Races
                      (id text, name text, start text)
                   """)
    except:
        pass

    try:
        cursor.execute("""CREATE TABLE Points
            (num text, race_id text, dt datetime)
            """)
    except:
        pass

    try:
        cursor.execute("""CREATE TABLE Participants
            (athlete_id text, race_id text, num text)
            """)
    except:
        pass

    try:
        cursor.execute("""CREATE TABLE Racers
            (id text, name text, num text, category text, birthday text)
            """)
    except:
        pass

    ChoiceWindow(cursor)



def ChoiceWindow(cursor):
    def refereeing_window():
        global races
        global api
        # if choice_race_combobox.current() == -1:
        #     showerror('', MESSAGE_NO_RACE_SELECTED)
        # else:
        api = apies[1]
        race=races[choice_race_combobox.current()]
        # if (datetime.now()-race.get_start_dt()) > timedelta(0, 0 , 2, 0, 0, 0, 0):
        #     showerror('', MESSAGE_RACE_FINISHED)
        # elif (race.get_start_dt()-datetime.now()) > timedelta(0, 0 , 2, 0, 0, 0, 0):
        #     showerror('', MESSAGE_RACE_NOT_START)
        # else:
        #     race.add_racers(api.get_racers(race))
        root.destroy()
        MainWindow(api, race, cursor)
        # pass

    def set_number_window():
        global races
        global api
        # if choice_race_combobox.current() == -1:
        #     showerror('', MESSAGE_NO_RACE_SELECTED)
        # else:
        api = apies[1]
        race=races[choice_race_combobox.current()]
        race.add_racers(api.get_racers(race))
        root.destroy()
        SetNumbersWindow(api, race, cursor)

    def get_races_func():
        # if choice_api_combobox.current() == -1:
        #     showerror('', MESSAGE_NO_API_SELECTED)
        # else:
        global api
        # api = apies[choice_api_combobox.current()]
        api = apies[1]
        global races
        races = api.get_races()
        db.insert_races(races)
        choice_race_combobox['values'] = races
        choice_race_combobox.update()

    root = Tk()
    apies = [Api('Vahat', 'http://127.0.0.1:8000/api/'),\
        Api('Zelbike', 'http://api.chrono.zelbike.ru/v1/RaceStages/')]
    db = Database()
    global races
    races = db.get_races()

    apies[1].key = ZELBIKE_ACCESS_KEY
    choice_api_combobox = ttk.Combobox(root, values=[str(x) for x in apies])
    choice_race_combobox = ttk.Combobox(root, values=races)

    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    root.geometry("480x340")
    
    load_races_button = Button(root, text = LABEL_GET_RACES_BUTTON, command = get_races_func)
    # Label(text = LABEL_CHOICE_API).pack()
    # choice_api_combobox.pack(padx = 10, pady = 10)
    load_races_button.pack(padx = 10, pady = 10)

    refereeing_button = Button(root, text="Судейство", command = refereeing_window)
    set_number_button = Button(root, text=LABEL_SET_NUMBERS_BUTTON, \
        command = set_number_window)
    Label(text = LABEL_CHOICE_RACE).pack()
    choice_race_combobox.pack(fill = BOTH, padx = 20, pady = 20)
    refereeing_button.pack(pady = 10)
    set_number_button.pack(pady = 10)
    
    # race=races[cb.current()]
    # db = Database()
    # Button(text = "Получить гонщиков", command = lambda \
    #     r=race, a=api: db.incert_racers(a, r)).pack()

    root.mainloop()

def MainWindow(api, race, cursor):

    # def cat():
    #     db = Database()
    #     start_time = db.get_start_point(race)
    #     grouped_racers = db.get_grouped_racers(race)
    #     # grouped_result = []
    #     # for group in grouped_racers:
    #     #     wer = []
    #     #     for racer in group:
    #     #         a={}
    #     #         points = db.get_points(race, racer.get_number())
    #     #         try:
    #     #             a["laps"] = [point.get_datetime_dt() for point in points]
    #     #         except:
    #     #             continue
    #     #         a["racer"] = racer
    #     #         a["result"] = a["laps"][0] - start_time.get_datetime_dt()
    #     #         a["nlaps"] = len(a["laps"])
    #     #         # print(a)
    #     #         wer.append(a)
    #     #         for item in wer:
    #     #             print(item["racer"])
    #     #             print()
                
    #     #     wer = sorted(wer, key=lambda x: (-x["nlaps"], x["result"]))
    #     #     grouped_result.append(wer)






    # def results():
    #     i = 0
    #     numbers = db.get_numbers(race)
    #     while True:
    #         for number in numbers:
    #             for point in db.get_points(race, number):
    #                 print(point.get_number(), " " , point.get_str_dt())
    #                 i += 1
    #         break
    #     print(i)

    def instance_add_point():
        number = str(askinteger("", LABEL_ENTER_NUMBER))
        db.insert_point(conn, race, number, datetime.now())

    def StartRace(api, race, log_frame, conn):
        # status = api.start_race(race)
        # log_frame.write(status)
        start_time = db.insert_start(conn, race, datetime.now())
        status = str(start_time) + ' ' + MESSAGE_RACE_START
        log_frame.write(status)
        db.get_numbers(race)
        t = threading.Thread(target=ReadTag)
        t.daemon = True
        t.start()

    def AddPoint():
        def callback():
            try:
                number = int(entry_number.get())
            except:
                showerror('', MESSAGE_INVALID_NUMBER, parent=root)
                entry_number.delete(0, END)
                return
            dt = str(datetime.today())[:10]
            dt = dt + ' ' + entry_datetime.get()
            try:
                dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
            except:
                showerror('', MESSAGE_INVALID_TIME, parent=root)
                entry_datetime.delete(0, END)
                return
            db.insert_point(conn, race, number, dt)
            showinfo('', MESSAGE_POINT_ADD, parent=root)
            entry_number.delete(0, END)
            entry_datetime.delete(0, END)
            root.destroy()

        root = Tk()
        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        root.wm_geometry("+%d+%d" % (x, y))
        Label(root, text=LABEL_ENTER_NUMBER).pack(padx=10, pady=10)
        entry_number = Entry(root)
        entry_number.pack(padx=10, pady=10)
        Label(root, text=LABEL_ENTER_TIME).pack(padx=10, pady=10)
        entry_datetime = Entry(root)
        entry_datetime.pack(padx=10, pady=10)
        Button(root, text=LABEL_ADD, command=callback).pack(padx=10, pady=10)

        root.mainloop()

    def DeletePoints():
        def table_of_points():
            def delete_point(dt_label, point):
                if askyesno('', MESSAGE_ASK_DELETE, parent=root):
                    dt_label.config(text='Удалено')
                    db.delete_point(point)

            try:
                fr.destroy()
            except:
                pass
            root.update()
            fr = Frame(root)
            for point in points:
                frame = Frame(fr)
                Label(frame, text = str(point.get_number())).pack(\
                    side = 'left', expand=YES, padx=10)
                dt_label = Label(frame, text=str(point.get_datetime_dt()))
                dt_label.pack(side = 'left', padx = 10)
                Button(frame, text=LABEL_DELETE,\
                    command=lambda t=dt_label, p=point: delete_point(\
                    t, p)).pack(side = 'right', padx = 10)
                frame.pack(fill = BOTH, pady = 5)
            fr.pack()

        number = askinteger('', LABEL_ENTER_NUMBER)
        if number > 0:
            number = str(number)
        else:
            showerror('', MESSAGE_INVALID_NUMBER)
            return
        root = Tk()
        x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
        root.wm_geometry("+%d+%d" % (x, y))
        points = db.get_points(race, number)
        table_of_points()
        
        root.mainloop()
  
    def ReadTag():
        conn = sqlite3.connect(Settings.DBName)
        cursor = conn.cursor()
        while(ser.is_open == True):
            rfidtag = ''
            incomingByte = ser.read(3)
            for i in incomingByte:
                rfidtag = rfidtag + str(i)

            try:
                number = str(race.tags[rfidtag])
            except:
                continue
            dt = datetime.now()

            points = db.get_points(race, number)
            if points == -1:
                start = db.get_start_point(conn, race)
                if start == -1:
                    pass
                else:
                    d = start.get_datetime_dt()
                    if (dt-d) > timedelta(0, 0 , 0, 0, 5, 0, 0):
                        db.insert_point(conn, race, number, dt)
                        # api.set_point(race, number, dt, db, conn)
                        log_frame.write('{0} {1}'.format(str(dt)[:19], number))
            else:
                d = points[0].get_datetime_dt()
                if (dt-d) > timedelta(0, 0 , 0, 0, 5, 0, 0):
                    db.insert_point(conn, race, number, dt)
                    # api.set_point(race, number, dt, db, conn)
                    log_frame.write('{0} {1}'.format(str(dt)[:19], number))

                # cursor.execute("""INSERT INTO Points values (
                #         :num, :race_id, :dt)""", {"num": number,
                #         "race_id": race.get_id(), "dt": dt})
                # conn.commit()
                # api.set_point(race, number, dt)
                    # print(str(race.tags[rfidtag]))
            log_frame.update()

    root = Tk()
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    log_frame = Report(root)

    db = Database()
    try:
        ser = serial.Serial(Settings.COMPortName, Settings.COMBaudRate)
    except:
        pass
    conn = sqlite3.connect(Settings.DBName)    
    
    Button(root, text = LABEL_START_RACE_BUTTON, command = lambda r = race, a = api,\
        l = log_frame, c = conn: StartRace(a, r, l, c)).pack(
        padx=10, pady=10)
    
    log_frame.pack()
    Button(root, text=LABEL_UPLOAD_POINTS_FOR_ALL, command=lambda r=race, d=db:\
        api.upload_points(r, d)).pack(padx=10, pady=10, side='left')
    Button(root, text=LABEL_INSTANCE_POINT_ADD, command=instance_add_point).\
    pack(padx=10, pady=10, side='left')
    Button(root, text=LABEL_CHANGE_POINTS, command=DeletePoints).pack(\
        padx=10, pady=10, side='right')
    Button(root, text=LABEL_ADD_POINT, command=AddPoint).pack(padx=10, pady=10, side='right')
    root.title(str(race) + ' ' + race.get_id())
    root.mainloop()
    

def SetNumbersWindow(api, race, cursor):
    root = Tk()
    #Примерная центровка окна
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    #Далее идет код для возможности прокрутки
    canvas = Canvas(root)
    fr = Frame(canvas)
    myscrollbar = Scrollbar(root, orient = 'vertical', command = canvas.yview)
    canvas.configure(yscrollcommand = myscrollbar.set)
    myscrollbar.pack(side = 'right', fill = Y)
    canvas.pack(side = 'left', fill=BOTH)
    canvas.create_window((0, 0), window = fr, anchor = 'nw')
    def conf(event):
        canvas.configure(scrollregion = canvas.bbox('all'))
    fr.bind('<Configure>', conf)
    #Конец вставки

    def set_number(race, racer, number, number_label):
        #Обертка для апи, чтобы была возможность изенять номера на экране
        if api.set_number(race, racer, number):
            showerror(title=TITLE_ERROR_WINDOW, message=MESSAGE_NUMBER_DIDNT_SET, \
                parent=root)
        else:
            number_label.config(text = str(number))

    def sort_racers(racer):
        #Возможность сортировки класса Racer по имени
        return str(racer)

    racers = race.get_racers()
    racers.sort(key = sort_racers)

    #Отрисовка таблицы на экран
    for racer in racers:
        frame = Frame(fr)
        Label(frame, text=str(racer.get_category())).pack(side = 'left', padx = 10)
        Label(frame, text=str(racer.get_age())[:4]).pack(side = 'left', padx = 10)
        Label(frame, text = str(racer)).pack(side = 'left', expand = YES, padx = 10)
        number_label = Label(frame, text = racer.get_number())
        Button(frame, text = LABEL_CHANGE_NUMBER_BUTTON, \
            command = lambda r = race, x = racer,\
             nl = number_label: set_number(
            r, x, askinteger(TITLE_CHANGE_NUMBER_WINDOW, ''), nl)).pack(side='right')
        number_label.pack(side = 'left', padx = 10)
        frame.pack(fill = BOTH, pady = 5)

    root.title(str(race) + ' ' + race.get_id())
    root.mainloop()

if __name__ == '__main__':
    main()
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
from datetime import *
import serial
import threading
import sqlite3
from messages import *
import os

class Report(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)

        scrollbar = Scrollbar(self)
        scrollbar.pack(side='right', fill='y')
        self._text = Text(self, state=DISABLED, *args, **kwargs)
        self._text.pack(side='left', fill='both', expand=1)

        scrollbar['command'] = self._text.yview
        self._text['yscrollcommand'] = scrollbar.set

    def write(self, text):
        self._text.configure(state=NORMAL)
        self._text.insert(END, text+'\n')
        self._text.configure(state=DISABLED)
        self._text.yview_moveto('1.0')  # Прокрутка до конца вниз после вывода

    def clear(self):
        self._text.configure(state=NORMAL)
        self._text.delete(0.0, END)
        self._text.configure(state=DISABLED)

    def flush(self):
        # Метод нужен для полного видимого соответствия классу StringIO в части вывода
        pass

class Racer:
    def __init__(self, racer_id, name, number, category):
        self.id = racer_id
        self.name = name
        self.number = number
        self.category = category

    def __str__(self):
        return str(self.name)

    def get_id(self):
        return str(self.id)

    def get_number(self):
        return str(self.number)

class Race:

    tags = {"96182208": 1, "96182240": 2, "9618336": 3, "9618324": 4, \
    "9618332": 5, "96182172": 6, "96182212": 7, "96182220": 8, "96182168": 9}

    def __init__(self, name, race_id):
        self.name = name
        self.id = race_id
        self.racers = list()
        
    def __str__(self):
        return self.name

    def add_racer(self, racer):
        self.racers.append(racer)

    def add_racers(self, racers):
        for racer in racers:
            self.add_racer(racer)

    def get_racers(self):
        return self.racers

    def get_id(self):
        return str(self.id)

class Api:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.key = ''

    def __str__(self):
        return self.name

    def get_races(self):
        if self.name == 'Vahat':
            data = requests.get(self.url + 'get_races').json()
            result = []
            for item in data['res']:
                race = Race(item['name'], item['id'])
                result.append(race)
            return result
        elif self.name == 'Zelbike':
            url = self.url + 'List?accessKey={0}'.format(self.key)
            result = []
            data = requests.get(url).json()["data"]
            for item in data:
                first_name = str(item["race"]["displayNamePrimary"]) #Cup Name
                if item["displayNamePrimary"]:
                    second_name = '\t' + str(item["displayNamePrimary"]) #Stage Name
                race_name = first_name + second_name
                race = Race(race_name, item["guid"])
                result.append(race)
            return result


    def get_racers(self, race):
        if self.name == 'Vahat':
            data = requests.get(
                '{0}get_participants?race_id={1}'.format(self.url, race.get_id())).json()
            result = []
            for item in data['res']:
                result.append(Racer(item['athlete_id'],
                    item['athlete__last_name'] + ' ' + item['athlete__first_name'],
                    item['number'], item['category__name']))
            return result
        elif self.name == 'Zelbike':
            url = self.url + 'Details?accessKey={0}&raceStageGuid={1}'.format(\
                self.key, race.get_id())
            data = requests.get(url).json()
            result = []
            for item in data['data']['raceStageRegistrations']:
                racer = Racer(item['guid'], item['account']['lastName'] + ' ' + \
                    item['account']['firstName'], item['registrationNumber'],\
                     item['raceGroupCategories'][0])
                result.append(racer)
            return result

    def set_number(self, race, racer, number):
        if self.name == 'Vahat':
            url = self.url + 'set_number?race_id={0}&athlete_id={1}&number={2}'.format(
                    race.get_id(), racer.get_id(), str(number))
            data = requests.get(url).json()
            try:
                if data['status'] == 'Ok':
                    return 0
            except:
                return 1
        elif self.name == 'Zelbike':
            url = self.url + 'SetRegistrationNumber?accessKey={0}&raceStageGuid={1}\
            &raceStageRegistrationGuid={2}&registrationNumber={3}'.format(\
                self.key, race.get_id(), racer.get_id(), str(number))
            data = requests.get(url).json()
            try: 
                if data['isSuccess']:
                    return 0
                else:
                    return 1
            except:
                pass

    def start_race(self, race):
        url = self.url + 'start_race?race_id={0}&dtime={1}'.format(
            race.get_id(), str(datetime.now())[:19])
        data = requests.get(url).json()
        try:
            if data['res'] == 'ok':
                return '{0} {1}'.format(MESSAGE_RACE_BEGAN, \
                    str(datetime.now())[:19])
        except:
            pass
        try:
            if data['error'] == 'Already running':
                return MESSAGE_RACE_ALREADY_RUNNING
        except:
            pass

    def set_point(self, race, number, dt):
        url = self.url + 'set_point?race_id={0}&num={1}&dtime={2}'.format(\
            race.get_id(), number, str(dt)[:19])
        data = requests.get(url).json()

class Database:

    database = "vahat.db"

    def incert_racers(self, api, race):
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()
        racers = api.get_racers(race)
        print(racers)




def main():
    
    global ZELBIKE_ACCESS_KEY
    try:
        ZELBIKE_ACCESS_KEY = os.environ['ZELBIKE_ACCESS_KEY'] 
    except:
        ZELBIKE_ACCESS_KEY = input(MESSAGE_ENTER_ZELBIKE_ACCESS_KEY)
    conn = sqlite3.connect("vahat.db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    # Создание таблицы
    try:
        cursor.execute("""CREATE TABLE Races
                      (id text, name text)
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
    ChoiceWindow(cursor)



def ChoiceWindow(cursor):
    def refereeing_window():
        global races
        global api
        if choice_race_combobox.current() == -1:
            showerror('', MESSAGE_NO_RACE_SELECTED)
        else:
            race=races[choice_race_combobox.current()]
            race.add_racers(api.get_racers(race))
            root.destroy()
            MainWindow(api, race, cursor)

    def set_number_window():
        global races
        global api
        if choice_race_combobox.current() == -1:
            showerror('', MESSAGE_NO_RACE_SELECTED)
        else:
            race=races[choice_race_combobox.current()]
            race.add_racers(api.get_racers(race))
            root.destroy()
            SetNumbersWindow(api, race, cursor)

    def get_races_func():
        if choice_api_combobox.current() == -1:
            showerror('', MESSAGE_NO_API_SELECTED)
        else:
            global api
            api = apies[choice_api_combobox.current()]
            global races
            races = api.get_races()
            choice_race_combobox['values'] = races
            choice_race_combobox.update()

    root = Tk()
    apies = [Api('Vahat', 'http://127.0.0.1:8000/api/'),\
        Api('Zelbike', 'http://api.chrono.zelbike.ru/v1/RaceStages/')]

    apies[1].key = ZELBIKE_ACCESS_KEY

    races = []
    choice_api_combobox = ttk.Combobox(root, values=[str(x) for x in apies])
    choice_race_combobox = ttk.Combobox(root, values=races)

    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    root.geometry("480x340")
    
    load_races_button = Button(root, text = LABEL_GET_RACES_BUTTON, command = get_races_func)
    Label(text = LABEL_CHOICE_API).pack()
    choice_api_combobox.pack(padx = 10, pady = 10)
    load_races_button.pack(padx = 10, pady = 10)

    # refereeing_button = Button(root, text="Судейство", command = refereeing_window)
    set_number_button = Button(root, text=LABEL_SET_NUMBERS_BUTTON, \
        command = set_number_window)
    Label(text = LABEL_CHOICE_RACE).pack()
    choice_race_combobox.pack(fill = BOTH, padx = 20, pady = 20)
    # refereeing_button.pack(pady = 10)
    set_number_button.pack(pady = 10)
    
    # race=races[cb.current()]
    # db = Database()
    # Button(text = "Получить гонщиков", command = lambda \
    #     r=race, a=api: db.incert_racers(a, r)).pack()
    
    

    root.mainloop()

def MainWindow(api, race, cursor):

    def StartRace(api, race, log_frame):
        status = api.start_race(race)
        log_frame.write(status)
        t = threading.Thread(target=ReadTag)
        t.daemon = True
        t.start()
  

    ser = serial.Serial('COM6', 9600)
    def ReadTag():
        conn = sqlite3.connect("vahat.db") # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()
        while(ser.is_open == True):
            rfidtag = ''
            incomingByte = ser.read(3)
            for i in incomingByte:
                rfidtag = rfidtag + str(i)

            number = str(race.tags[rfidtag])
            dt = datetime.now()

            log_frame.write('{0} {1}'.format(str(dt)[:19], \
                number))
            cursor.execute("""SELECT num, race_id, dt FROM Points 
                where (num = :num and race_id = :race_id)
                ORDER BY dt desc
                """, {"num": number, "race_id": race.get_id()})
            res = cursor.fetchall()
            try:
                d = datetime.strptime(res[0][2][:19], '%Y-%m-%d %H:%M:%S')
                if (dt-d) > timedelta(0, 0 , 0, 0, 1, 0, 0):
                    cursor.execute("""INSERT INTO Points values (
                        :num, :race_id, :dt)""", {"num": number,
                        "race_id": race.get_id(), "dt": dt})
                    conn.commit()
                    api.set_point(race, number, dt)

            except:
                cursor.execute("""INSERT INTO Points values (
                        :num, :race_id, :dt)""", {"num": number,
                        "race_id": race.get_id(), "dt": dt})
                conn.commit()
                api.set_point(race, number, dt)
                    # print(str(race.tags[rfidtag]))
            log_frame.update()

    root = Tk()
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    log_frame = Report(root)
    

    #Далее идет код для возможности прокрутки
    # canvas = Canvas(root)
    # fr = Frame(canvas)
    # myscrollbar = Scrollbar(root, orient = 'vertical', command = canvas.yview)
    # canvas.configure(yscrollcommand = myscrollbar.set)
    # myscrollbar.pack(side = 'right', fill = Y)
    # canvas.pack(side = 'left', fill=BOTH)
    # canvas.create_window((0, 0), window = fr, anchor = 'nw')
    # def conf(event):
    #     canvas.configure(scrollregion = canvas.bbox('all'))
    # fr.bind('<Configure>', conf)
    #Конец вставки
    
    Button(root, text = LABEL_START_RACE_BUTTON, command = lambda r = race, a = api,\
        l = log_frame: StartRace(a, r, l)).pack(
        padx  = 10, pady = 10)
    

    log_frame.pack()
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
            showerror(title = TITLE_ERROR_WINDOW, message = MESSAGE_NUMBER_DIDNT_SET)
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
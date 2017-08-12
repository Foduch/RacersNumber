try:
    # for Python2
    from Tkinter import *
    from tkMessageBox import *
    from tkSimpleDialog import *## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *
    from tkinter.messagebox import *
    from tkinter.simpledialog import *## notice lowercase 't' in tkinter here
    
import requests
from datetime import datetime
import sys


apiSiteName = 'http://api.chrono.zelbike.ru/v1/'
accessKey='qFfiYkJIolAtj6dSLVuVrYjITV8v9axRfzU6mc4Bd4'
#raceStageGuid = '461d1fa4-e720-48fd-a280-e545edea051d'
raceStageGuid = '04e29e6a-b68b-4e0e-9a5c-787f3fcf2e92'

'''def getRequestUrl(apiFunc, accessKey):
    apiFuncs = dict()
    apiFuncs.update({'RaceStages':'RaceStages/List'})
    url = '{0}{1}?accessKey={2}'.format(apiSiteName, apiFuncs[apiFunc], accessKey)
    return url'''
def ErrorInternetConnection():
    showerror(title = 'Ошибка', message = 'Не возможно выполнить запрос. Проверьте интернет соединение')

def getRaces():
    '''Получает список всех гонок по ключу доступа организатора
       Формирует словарь в виде guid:Название'''
    url = 'http://api.chrono.zelbike.ru/v1/RaceStages/List?accessKey=qFfiYkJIolAtj6dSLVuVrYjITV8v9axRfzU6mc4Bd4'
    try:
        data = requests.get(url).json()["data"]
        dRaces = dict()
        for item in data:
            firstName = str(item["race"]["displayNamePrimary"]) #Cup Name
            if item["displayNamePrimary"]:
                secondName = '\t' + str(item["displayNamePrimary"]) #Stage Name
            raceName = firstName + secondName
            dRaces.update({item["guid"]:raceName}) #Adding race in dictionary
        return dRaces
    except:
        ErrorInternetConnection()
        sys.exit()

def getRacers(raceStageGuid):
    '''Получение списка зарегестрированных участников на конкретную гонку
       Словарь вида  guid: { имя, фамилия, номер}'''
    url = 'http://api.chrono.zelbike.ru/v1/RaceStages/Details?accessKey=qFfiYkJIolAtj6dSLVuVrYjITV8v9axRfzU6mc4Bd4'
    url = url + '&raceStageGuid=' + raceStageGuid
    try:
        data = requests.get(url).json()
        racers = dict()
        for item in data['data']['raceStageRegistrations']:
            racer = dict()
            birth = datetime.strptime(item['account']["birthday"], "%Y-%m-%dT%H:%M:%S")
            racer.update({'age': str(datetime.now().year - birth.year)})
            racer.update({'firstName': item['account']['firstName']})
            racer.update({'lastName': item['account']['lastName']})
            racer.update({'number': item['registrationNumber']})
            racers.update({item['guid']: racer})
        return racers
    except:
        ErrorInternetConnection()
        sys.exit()

'''def selectRace(dRaces):
    def f(key):
        global raceGuid
        raceGuid = key
        fr.pack_forget()
        
    fr = Frame(root)
    for key in dRaces:
        Button(fr, text = dRaces[key], command = lambda : f(key)).pack() 
    fr.pack()
'''

def setNum(guid, num, LNum):
    if num == None:
        return
    url = 'http://api.chrono.zelbike.ru/v1/RaceStages/SetRegistrationNumber?accessKey=qFfiYkJIolAtj6dSLVuVrYjITV8v9axRfzU6mc4Bd4'
    url += '&raceStageGuid='
    global raceStageGuid
    url += raceStageGuid
    url += '&raceStageRegistrationGuid='
    url += guid
    url += '&registrationNumber=' + str(num)
    try:
        inf = requests.get(url).json()
        if inf['isSuccess']:
            LNum.config(text=str(num))
        else:
            showerror(title='Error', message=inf['message'])
    except:
        ErrorInternetConnection()

def table(racers):
    temp = list()
    for key in racers.keys():
        temp.append([racers[key]['lastName'], key])
    temp.sort() #Сортировка через жопу
    for item in temp:
        key = item[1]
        frame = Frame(fr) #Изменил привязку root на fr
        racerInfo = str(racers[key]['lastName'] + ' ' + racers[key]['firstName'] + ' (' + racers[key]['age'] + ')')
        Label(frame, text = racerInfo).pack(side = 'left', expand = YES)
        LNum = Label(frame, text = str(racers[key]['number']))

        butDel = Button(frame, text = 'Удалить')
        butDel.config(command = lambda g = key, x = LNum, r = racerInfo:( setNum(g, '', x) if askyesno(
            title = 'Удалить', message = ('Удалить номер для '+r+'?')) else None))
        butDel.pack(side='right')
        Button(frame, text = 'Изменить', command = lambda g = key, x = LNum, r = racerInfo: setNum(g, askinteger(
            'Изменение номера', ('Введите номер для '+r)), x)).pack(side='right')

        LNum.pack(side = 'left')
        frame.pack(fill = BOTH)
        
root = Tk()

#Далее идет новый код для возможности прокрутки
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

#dRaces = getRaces()
racers = getRacers(raceStageGuid)
table(racers)

root.mainloop()



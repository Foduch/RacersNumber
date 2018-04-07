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

def getRaces():
    '''Получает список всех гонок по ключу доступа организатора
       Формирует словарь в виде guid:Название'''
    url = 'http://api.chrono.zelbike.ru/v1/RaceStages/List?accessKey=qFfiYkJIolAtj6dSLVuVrYjITV8v9axRfzU6mc4Bd4'
    data = requests.get(url).json()["data"]
    dRaces = dict()
    for item in data:
        firstName = str(item["race"]["displayNamePrimary"]) #Cup Name
        if item["displayNamePrimary"]:
            secondName = '\t' + str(item["displayNamePrimary"]) #Stage Name
        raceName = firstName + secondName
        dRaces.update({item["guid"]:raceName}) #Adding race in dictionary
    return dRaces

def getRacers(raceStageGuid):
    '''Получение списка зарегестрированных участников на конкретную гонку
       Словарь вида  guid: { имя, фамилия, номер}'''
    url = 'http://api.chrono.zelbike.ru/v1/RaceStages/Details?accessKey=qFfiYkJIolAtj6dSLVuVrYjITV8v9axRfzU6mc4Bd4'
    url = url + '&raceStageGuid=' + raceStageGuid
    data = requests.get(url).json()
    racers = dict()
    for item in data['data']['raceStageRegistrations']:
        racer = dict()
        racer.update({'firstName': item['account']['firstName']})
        racer.update({'lastName': item['account']['lastName']})
        racer.update({'number': item['registrationNumber']})
        racers.update({item['guid']: racer})
    return racers

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
    inf = requests.get(url).json()
    if inf['isSuccess']:
        LNum.config(text = str(num))
    else:
        showerror(title = 'Error', message = inf['message'])
   
    

def table(racers):
    frame = Frame(fr)
    lbf = Label(frame, text = str(data['data'][n]['race']['displayNamePrimary']) + ' ' + 
        str(data['data'][n]['displayNamePrimary']))
    lbf.pack(side = 'left')
    frame.pack(side = 'top', fill = BOTH)
    temp = list()
    for key in racers.keys():
        temp.append([racers[key]['lastName'], key])
    temp.sort() #Сортировка через жопу
    for item in temp:
        key = item[1]
        frame = Frame(fr) #Изменил привязку root на fr
        
        Label(frame, text = str(racers[key]['lastName'] + ' ' + racers[key]['firstName'])).pack(side = 'left', expand = YES)
        LNum = Label(frame, text = str(racers[key]['number']))
        Button(frame, text = 'Удалить', command = lambda g = key, x = LNum: setNum(g, '', x)).pack(side='right')
        Button(frame, text = 'Изменить', command = lambda g = key, x = LNum: setNum(g, askinteger('', ''), x)).pack(side='right')       
        LNum.pack(side = 'left')
        frame.pack(fill = BOTH)
        


#raceStageGuid = '461d1fa4-e720-48fd-a280-e545edea051d'


#raceStageGuid = '884ae33c-298a-4e68-8c58-7a652fdb11d9'

main_api = 'http://api.chrono.zelbike.ru/v1/RaceStages/'

adress = 'List?accessKey=qFfiYkJIolAtj6dSLVuVrYjITV8v9axRfzU6mc4Bd4'
url = main_api + adress

data = requests.get(url).json()
#print(data)

#print()
#print(data['data'])
for i in range(len(data['data'])):
    print(str(i) + ' ' + data['data'][i]['race']['displayNamePrimary'] + ' ' + str(data['data'][i]['displayNamePrimary']) + ' '
     + data['data'][i]['guid'])

n = int(input())
raceStageGuid = data['data'][n]['guid']
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


dRaces = getRaces()
racers = getRacers(raceStageGuid)
table(racers)

root.mainloop()



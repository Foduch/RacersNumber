from tkinter import *
from datetime import datetime
#import urllib.parse
import requests


def getRacers(raceStageGuid):
    url = 'http://api.chrono.zelbike.ru/v1/RaceStages/Details?accessKey=qFfiYkJIolAtj6dSLVuVrYjITV8v9axRfzU6mc4Bd4'
    url = url + '&raceStageGuid=' + raceStageGuid
    data = requests.get(url).json()
    racers = dict()
    for item in data['data']['raceStageRegistrations']:
        racer = dict()
        racer.update({'firstName': item['account']['firstName']})
        racer.update({'lastName': item['account']['lastName']})     
        racers.update({item['registrationNumber']: racer})
    return racers

def f(registrationNumber, frame, butt):
    d = '["' + datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + '"]'
    l = Label(frame, text = d[2:-2])
    butt.config(state = 'disabled')
    requests.get(url1 + str(registrationNumber) + '&customStartDateTime=' + d).json()
    l.pack(side = 'left')

def f1(registrationNumber, frame, butt):
    d = '["' + datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S") + '"]'
    l = Label(frame, text = d[2:-2])
    butt.config(state = 'disabled')
    requests.get(url1 + str(registrationNumber) + '&lapsDateTimeJson=' + d).json()
    l.pack(side = 'left')  

def table(racers):
    frame = Frame(fr)
    lbf = Label(frame, text = str(data['data'][n]['race']['displayNamePrimary']) + ' ' + 
    	str(data['data'][n]['displayNamePrimary']))
    lbf.pack(side = 'left')
    frame.pack(side = 'top', fill = BOTH)


    frame = Frame(fr)
    lbf = Label(frame, text = 'Номер')
    lbf.pack(side = 'left')
    lbf2 = Label(frame, text = 'ФИО')
    lbf2.pack(side = 'left')
    lbf3 = Label(frame, text = 'Старт')
    lbf3.pack(side = 'right')
    frame.pack(side = 'top', fill = BOTH)


    for k in racers.keys():
        frame = Frame(fr)
        
        Label(frame, text = str(k)).pack(side = 'left')
        Label(frame, text = str(racers[k]['lastName'] + ' ' + racers[k]['firstName'])).pack(side = 'left')
        fin = Button(frame, text = 'Финиш')
        fin.config( command = lambda x = k, y = frame, z = fin:f1(x, y, z))
        fin.pack(side = 'right')

        st = Button(frame, text = 'Старт')
        st.config( command = lambda x = k, y = frame, z = st:f(x, y, z))
        st.pack(side = 'right')
        frame.pack(side = 'top', fill = BOTH)


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

#raceStageGuid = 'be80a44f-eb55-4842-bafb-059e94c1b66a'
#raceStageGuid = '884ae33c-298a-4e68-8c58-7a652fdb11d9'

url1='http://api.chrono.zelbike.ru/v1/RaceStages/UpdateLaps?accessKey=qFfiYkJIolAtj6dSLVuVrYjITV8v9axRfzU6mc4Bd4'
url1 += '&raceStageGuid='
url1 += raceStageGuid
url1 += '&registrationNumber='

racers = getRacers(raceStageGuid)

table(racers)

root.mainloop()

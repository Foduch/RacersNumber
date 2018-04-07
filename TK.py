from tkinter import *
from datetime import datetime
#import urllib.parse
import requests
import time
import logging

class StopWatch(Frame):  
    """ Implements a stop watch frame widget. """                                                                
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()               
        self.makeWidgets()      

    def makeWidgets(self):                         
        """ Make the time label. """
        l = Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        l.pack(fill=X, expand=NO, pady=2, padx=2)                      
    
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))
        
    def Start(self):                                                     
        """ Start the stopwatch, ignore if running. """
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1        
    
    def Stop(self):                                    
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
    
    def Reset(self):                                  
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)


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

def f(registrationNumber, frame, butt, sw):
    sw.Start()
    d = '["' + datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + '"]'
    #l = Label(frame, text = d[2:-2])
    butt.config(state = 'disabled')
    resp = requests.get(url1 + str(registrationNumber) + '&customStartDateTime=' + d).json()
    #l.pack(side = 'left')
    logging.info(str(registrationNumber) + ' start ' + d[2:-2])
    if resp['isSuccess']:
        logging.info('status OK')
    else:
        logging.info('status ERROR')

def f1(registrationNumber, frame, butt, sw):
    sw.Stop()
    d = '["' + datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S") + '"]'
    #l = Label(frame, text = d[2:-2])
    butt.config(state = 'disabled')
    resp = requests.get(url1 + str(registrationNumber) + '&lapsDateTimeJson=' + d).json()
    #l.pack(side = 'left')
    logging.info(str(registrationNumber) + ' finish ' + d[2:-2])
    if resp['isSuccess']:
        logging.info('status OK')
    else:
        logging.info('status ERROR')
        
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
        sw = StopWatch(frame)
        sw.pack(side='right')
        fin = Button(frame, text = 'Финиш')
        fin.config( command = lambda x = k, y = frame,
                    z = fin, s = sw:f1(x, y, z, s))
        fin.pack(side = 'right')
        
        st = Button(frame, text = 'Старт')
        st.config( command = lambda x = k, y = frame,
                   z = st, s = sw:f(x, y, z, s))
        st.pack(side = 'right')
        frame.pack(side = 'top', fill = BOTH)

logging.basicConfig(filename="TK.log", level=logging.INFO)
logging.info('run programm '+datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"))

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

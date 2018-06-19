from messages import *
import requests
from datetime import *
from ClassRacer import *
from ClassDB import *
import sqlite3

class Api:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.key = ''

    def __str__(self):
        return self.name

    def get_races(self):
        '''Получает данные о гонках с сервера.
        Возвращает список объектов класса Race.
        При отсутсвии подключение к Интернет выдается ошибка в консоль'''
        if self.name == 'Vahat':
            data = requests.get(self.url + 'get_races').json()
            result = []
            for item in data['res']:
                race = Race(item['name'], item['id'], datetime.now())
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
                start_datetime = datetime.strptime(item['startDateTime'],\
                 '%Y-%m-%dT%H:%M:%S')
                race = Race(race_name, item["guid"], start_datetime)
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
                     item['raceGroupCategories'][0], item['account']['birthday'])
                result.append(racer)
            # for racer in result:
                # print(racer.get_id(), str(racer), racer.get_number(), racer.get_category(), \
                #     racer.get_age(), sep=' ')

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
        if self.name == 'Vahat':
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
        elif self.name == 'Zelbike':
            return '{0} {1}'.format(MESSAGE_RACE_BEGAN, \
                        str(datetime.now())[:19])

    def set_point(self, race, number, dt, db, conn):
        if self.name == 'Vahat':
            url = self.url + 'set_point?race_id={0}&num={1}&dtime={2}'.format(\
                race.get_id(), number, str(dt)[:19])
            data = requests.get(url).json()
        elif self.name == 'Zelbike':
            points = db.get_points(race, number)
            if points == -1:
                pass
            else:
                urlsuffix = '['

                for i in range(1, len(points)+1):
                    tmp = '"{0}T{1}", '.format(points[-i].get_str_dt()[:10], \
                        points[-i].get_str_dt()[11:19])
                    urlsuffix += tmp
                urlsuffix = urlsuffix[:len(urlsuffix)-2] + ']'
                url = self.url + 'UpdateLaps?accessKey={0}&raceStageGuid={1}\
                &registrationNumber={2}&lapsDateTimeJson={3}'.format(
                    self.key, race.get_id(), number, urlsuffix)
                data = requests.get(url).json()

    def upload_points(self, race, db):
        if self.name == 'Zelbike':
            numbers = db.get_numbers(race)
            for number in numbers:
                points = db.get_points(race, number)
                urlsuffix = '['

                for i in range(1, len(points)+1):
                    tmp = '"{0}T{1}", '.format(points[-i].get_str_dt()[:10], \
                        points[-i].get_str_dt()[11:19])
                    urlsuffix += tmp
                urlsuffix = urlsuffix[:len(urlsuffix)-2] + ']'
                url = self.url + 'UpdateLaps?accessKey={0}&raceStageGuid={1}\
                &registrationNumber={2}&lapsDateTimeJson={3}'.format(
                    self.key, race.get_id(), number, urlsuffix)
                data = requests.get(url).json()

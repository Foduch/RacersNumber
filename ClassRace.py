import Settings
from datetime import *

class Race:

    tags = Settings.TagsIntoNumbers

    def __init__(self, name, race_id, start_datetime):
        self.name = name
        self.id = race_id
        self.start_datetime = start_datetime
        self.racers = list()
        
    def __str__(self):
        return self.name

    def add_racer(self, racer):
        self.racers.append(racer)

    def add_racers(self, racers):
        for racer in racers:
            self.add_racer(racer)

    def get_racers(self):
        return list(self.racers)

    def get_id(self):
        return str(self.id)

    def get_start(self):
        return str(self.start_datetime)

    def get_start_dt(self):
        return self.start_datetime

class Point:
    def __init__(self, race, number, dt):
        self.race = race
        self.number = number
        self.dt = dt

    def get_str_dt(self):
        return self.dt[:19]

    def get_datetime_dt(self):
        return datetime.strptime(self.dt[:19], '%Y-%m-%d %H:%M:%S')

    def get_number(self):
        return self.number

    def get_race(self):
        return self.race
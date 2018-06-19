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
class Database:

    DBName = Settings.DBName

    def insert_racers(self, race, racers):
        conn = sqlite3.connect(self.DBName)
        cursor = conn.cursor()
        for racer in racers: 
            cursor.execute("""SELECT id from Racers
                where (id = :id""", {"id":race.get_id()})   
            if len(cursor.fetchall())==0:    
                cursor.execute("""INSERT INTO Racers VALUES
                    (:id , :name, :num, :category, :birthday)""",
                    {"id":racer.get_id(), "name":str(racer), "num":racer.get_number(),\
                     "category":racer.get_category(),\
                    "birthday":str(racer.get_birthday())})

    def get_categories(self, race):
        conn = sqlite3.connect(self.DBName)
        cursor = conn.cursor()
        category = set()
        cursor.execute("""SELECT distinct category from Racers""")
        for item in cursor.fetchall():
            category.add(item[0])
        return category


    # Почему-то выбирает всех и даже по два раза, не смотря на условие WHERE

    # def get_grouped_racers(self, race):
    #     conn = sqlite3.connect(self.DBName)
    #     cursor = conn.cursor()
    #     categories = self.get_categories(race)
    #     res = []
    #     categories = list(categories)
    #     for i in range(len(categories)):

    #     # for cat in categories:
    #         cursor.execute("""SELECT distinct id, name, num, category, birthday FROM Racers
    #             WHERE (category = :cat)""", {"cat":categories[0]})
    #         r = []
    #         for racer in cursor.fetchall():
    #             r.append(Racer(racer[0], racer[1], racer[2], racer[3], racer[4]))
    #         for item in r:
    #             print(str(item))

    #     #     res.append(r)
    #     # for item in res:
    #     #     for i in item:
        #         print(str(i))
        # return res


    def insert_races(self, races):
        conn = sqlite3.connect(self.DBName)
        cursor = conn.cursor()
        for race in races:
            cursor.execute("""SELECT id from Races
            where (id = :race_id)
            """, {"race_id": race.get_id()})
            if len(cursor.fetchall()) == 0:
                cursor.execute("""INSERT INTO Races values
                    (:race_id, :name, :start)
                    """, {"race_id": race.get_id(), "name": str(race),
                    "start": race.get_start()})
                conn.commit()

    def get_races(self):
        conn = sqlite3.connect(self.DBName)
        cursor = conn.cursor()
        cursor.execute("""SELECT id, name, start from Races
            """)
        races = []
        for item in cursor.fetchall():
            start_datetime = datetime.strptime(item[2], '%Y-%m-%d %H:%M:%S')
            race = Race(item[1], item[0], start_datetime)
            races.append(race)
        return races

    def get_points(self, race, number):
        conn = sqlite3.connect(self.DBName)
        cursor = conn.cursor()
        cursor.execute("""SELECT dt FROM Points 
                where (num = :num and race_id = :race_id)
                ORDER BY dt desc
                """, {"num": number, "race_id": race.get_id()})
        points = []
        for item in cursor.fetchall():
            points.append(Point(race, number, item[0]))
        if len(points) == 0:
            return -1
        else:
            return points

    def get_numbers(self, race):
        conn = sqlite3.connect(self.DBName)
        cursor = conn.cursor()
        cursor.execute("""SELECT num FROM Points
            WHERE (race_id = :race_id)""",
            {"race_id": race.get_id()})
        numbers = set()
        tmp = cursor.fetchall()
        if len(tmp) == 0:
            return numbers
        for item in tmp:
            for number in item:
                if number != '-1':
                    numbers.add(number)
        return numbers

    def insert_start(self, conn, race, dt):
        cursor = conn.cursor()
        cursor.execute("""SELECT dt FROM Points
            WHERE (num = -1 and race_id == :race_id)""",
            {"race_id": race.get_id()})
        tmp = cursor.fetchall()
        if len(tmp) == 0:
            cursor.execute("""INSERT INTO Points values (
                            :num, :race_id, :dt)""", {"num": '-1',
                            "race_id": race.get_id(), "dt": dt})
            conn.commit()
            return dt
        elif len(tmp) == 1:
            return datetime.strptime(tmp[0][0][:19], '%Y-%m-%d %H:%M:%S')

    def get_start_point(self, race):
        conn = sqlite3.connect(self.DBName)
        cursor = conn.cursor()
        cursor.execute("""SELECT dt FROM Points 
                where (num = :num and race_id = :race_id)
                """, {"num": '-1', "race_id": race.get_id()})
        try:
            start = Point(race, '-1', cursor.fetchall()[0][0])
            return start
        except:
            return -1

    def insert_point(self, conn, race, number, dt):
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO Points values (
                        :num, :race_id, :dt)""", {"num": number,
                        "race_id": race.get_id(), "dt": dt})
        conn.commit()
        logging.info(MESSAGE_POINT_ADDED+' {0} {1} {2}'.format(\
            number, dt, race.get_id()))

    def delete_point(self, point):
        conn = sqlite3.connect(self.DBName)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM Points
            WHERE (num = :num and race_id = :race_id and dt = :dt)""",
            {"num": point.get_number(), "race_id": point.get_race().get_id(),
            "dt": point.get_datetime_dt()})
        conn.commit()
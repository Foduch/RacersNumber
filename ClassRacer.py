from datetime import *
class Racer:
    def __init__(self, racer_id, name, number, category, birthday):
        self.id = racer_id
        self.name = name
        self.number = number
        self.category = category
        self.birthday = birthday

    def __str__(self):
        return str(self.name)

    def get_id(self):
        return str(self.id)

    def get_number(self):
        return str(self.number)

    def get_category(self):
        return self.category[:5]

    def get_age(self):
        return str(int(str(datetime.today())[:4])-int(self.birthday[:4]))

    def get_birthday(self):
    	return self.birthday
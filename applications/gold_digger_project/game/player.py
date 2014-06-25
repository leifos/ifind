
class Player (object):

    def __init__(self, username, equipment, vehicle, gold):

        self.username = username
        self.equipment = equipment
        self.vehicle = vehicle
        self.gold = gold

    def __str__(self):
        return 'Username: {user}, Equipment: {equip}, Vehicle: {vehicle}, Gold: {gold}'.format\
            (user=self.username, equip=self.equipment, vehicle=self.vehicle, gold=self.gold)
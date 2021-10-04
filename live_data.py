import json
class live_data:
    def __init__(self, id, name, available_bikes, available_places):
        self.recordid = id
        self.name = name
        self.available_bikes = available_bikes
        self.available_places = available_places
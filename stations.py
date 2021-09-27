import json
class station:
    def __init__(self, latitude = None, longitude = None, size = 0, name = None, tpe = False, available = 0):
        self.pos = [latitude, longitude]
        self.size = size
        self.name = name
        self.tpe = tpe
        self.available = available


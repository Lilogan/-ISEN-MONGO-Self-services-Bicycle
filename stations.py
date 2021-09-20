class station:
    def __init__(self, latitude, longitude, size, name, tpe, available):
        self.pos = [latitude, longitude]
        self.size = size
        self.name = name
        self.tpe = tpe
        self.available = available
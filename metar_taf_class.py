class Metar:
    def __init__(self, data):
        self.data = data

    def terrain_id(self):
        print(self.data[0])

    def wind(self):
        print(self.data[1])

    def visibility(self):
        print(self.data[2])

    def temperatures(self):
        print(self.data[3])

    def pressure(self):
        print(self.data[4])

    def trend(self):
        print(self.data[5])


class Taf:
    def __init__(self, data) -> None:
        self.data = data

import re

class Metar:
    def __init__(self, data):
        self.data = data

    def terrain_id(self):
        pass

    def wind(self):
        wind_info = ""
        wind_variable = ""
        gust = False
        variable = False

        # retrieving wind direction and velocity information
        for elmt in self.data:
            if "KT" in elmt:
                wind_info = elmt
            if re.match("[0-9][0-9][0-9]V[0-9][0-9][0-9]", elmt):
                variable = True
                wind_info += elmt

        # testing presence of gust
        for item in wind_info:
            if "G" in item:
                gust = True
        
        # decoding wind
        if not gust:
            if not variable:
                print(f"Wind: {wind_info[:3]}°, {wind_info[3:5]} knots")
            else:
                print(f"Wind: {wind_info[:3]}°, {wind_info[3:5]} knots, variable between {wind_info[7:10]}° and {wind_info[11:]}°")
        else:
            if not variable:
                print(f"Wind: {wind_info[:3]}°, {wind_info[3:5]} knots, gusting to {wind_info[6:8]} knots")
            else:
                print(f"Wind: {wind_info[:3]}°, {wind_info[3:5]} knots, gusting to {wind_info[6:8]} knots, \
variable between {wind_info[10:13]}° and {wind_info[14:]}°")


    def visibility(self):
        pass

    def temperatures(self):
        pass

    def pressure(self):
        pass

    def trend(self):
        pass


class Taf(Metar):
    def __init__(self, data):
        self.data = data

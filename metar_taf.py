import re

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

weather_code = input("Entrez le message à décoder : ")

weather_code_list = weather_code.split(" ")

# Indicators to determine if TAF, else is METAR
taf_indicator_1 = weather_code_list[0]
taf_indicator_2 = len(re.sub("[^0-9]", "", weather_code_list[2]))

# First occurence of time FROM-TO contains 8 digits
if taf_indicator_1 == "TAF" or taf_indicator_2 == 8:
    print("C'est un TAF")
    weather_decode = Taf(weather_code_list)
    print(weather_decode.data)

else:
    print("C'est un METAR")
    weather_decode = Metar(weather_code_list)
    print(weather_decode.data)
    weather_decode.terrain_id()
    weather_decode.wind()
    weather_decode.visibility()
    weather_decode.temperatures()
    weather_decode.pressure()
    weather_decode.trend()

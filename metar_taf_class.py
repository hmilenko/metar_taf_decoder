import re

class Metar:
    def __init__(self, data):
        self.data = data
        print(self.data)

    def terrain_id(self):
        pass

    def wind(self):
        wind_info = ""
        wind_variable = ""
        gust = False
        variable = False

        # retrieving wind direction and velocity information
        for item in self.data:
            if "KT" in item:
                wind_info = item
            if re.match("[0-9][0-9][0-9]V[0-9][0-9][0-9]", item):
                variable = True
                wind_info += item

        # testing presence of gust
        for item in wind_info:
            if "G" in item:
                gust = True
        
        # decoding wind
        if not gust:
            if not variable:
                print(f"WIND: {wind_info[:3]}°, {wind_info[3:5]} knots")
            else:
                print(f"WIND: {wind_info[:3]}°, {wind_info[3:5]} knots, variable between {wind_info[7:10]}° and {wind_info[11:]}°")
        else:
            if not variable:
                print(f"WIND: {wind_info[:3]}°, {wind_info[3:5]} knots, gusting to {wind_info[6:8]} knots")
            else:
                print(f"WIND: {wind_info[:3]}°, {wind_info[3:5]} knots, gusting to {wind_info[6:8]} knots, \
variable between {wind_info[10:13]}° and {wind_info[14:]}°")

    def visibility(self):
        # testing the presence of CAVOK
        for item in self.data:
            if re.search("CAVOK", item):
                print("VISIBILITY: Ceiling and Visibility OK")
                return

    def clouds(self):
        cloud_info = []
        cloud_type = {"FEW": "Few", "SCT": "Scattered", "BKN": "Broken", "OVC": "Overcast"}

        # Testing the presence of "CAVOK"
        for item in self.data:
            if re.search("CAVOK", item):
                return
        # Adding items to clound_info for decode
        for item in self.data:
            if re.search("FEW", item):
                cloud_info.append(item)
            elif re.search("SCT", item):
                cloud_info.append(item)
            elif re.search("BKN", item):
                cloud_info.append(item)
            elif re.search("OVC", item):
                cloud_info.append(item)
        

        # Decoding clound type and altitude
        print("CLOUDS:", end=" ")

        for item in cloud_info:
            for n, c in cloud_type.items():
                if item[:3] == n:
                    if item[3] != 0:
                        print(f"{c} {int(item[3:6] ) * 100} feet", end=" ")
                    else:
                        print(f"{c} {int(item[4:6] ) * 100} feet", end=" ")
        
        print("")

    def temperatures(self):
        pass

    def pressure(self):
        pass

    def trend(self):
        pass


class Taf(Metar):
    def __init__(self, data):
        self.data = data

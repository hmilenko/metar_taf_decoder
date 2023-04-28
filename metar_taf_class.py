import re

from metar_taf_decode import*
from metar_taf_globals import*

class Metar:
    def __init__(self, data):
        self.data = data
        
    def __str__(self):
        return self.data
        
    def decode(self):
        global WEATHER_CODE_DECODE
        
        data = self.data.split(" ")
        
        for item in data:
            if re.match("SPECI", item):
                WEATHER_CODE_DECODE.append("Special message from")
            else:
                WEATHER_CODE_DECODE.append("Observation message from")
                break
        
        identification(data)
        
        # Correcting capital letter if option added (only applicable to Metar)
        if WEATHER_CODE_DECODE[0] == "Automated" or "Corrected":
            if WEATHER_CODE_DECODE[1] == "Observation message from":
                WEATHER_CODE_DECODE[1] = "observation message from"
            elif WEATHER_CODE_DECODE[1] == "Special message from":
                WEATHER_CODE_DECODE[1] = "special message from"
                
        wind(data)
        visibility(data)
        rvr(data)
        WEATHER_CODE_DECODE.append("Present weather")
        present_weather(data)
        clouds(data)
        temperatures(data)
        pressure(data)
        additional(data)
        trend(data)
        
    
    def display(self):
        global WEATHER_CODE_DECODE
        
        for item in WEATHER_CODE_DECODE:
            print(item, end=" ")
        
class Taf:
    def __init__(self, data):
        self.data = data
        
    def __str__(self):
        return self.data

    def decode(self):
        global WEATHER_CODE_DECODE, TAF
        
        data = self.data.split(" ")
        
        data_copy = data
        
        WEATHER_CODE_DECODE.append("Weather forcast from")
        
        identification(data_copy)
        
        for item in data_copy:
            if re.match("[0-9]{4}/[0-9]{4}", item):
                break
            else:
                data_copy = data_copy[1:]
        
        while data_copy != []:
            for item in data_copy:
                if re.match("[0-9]{4}/[0-9]{4}", item):
                    WEATHER_CODE_DECODE.append(f"From the {item[:2]} of current month at {item[2:4]} UTC to the {item[5:7]} of current month at {item[7:]} UTC.")
                    data_copy = data_copy[1:]
                else:
                    wind([item])
                    visibility([item])
                    rvr([item])
                    present_weather([item])
                    clouds([item])
                    temperatures([item])
                    pressure([item])
                    
                    data_copy = data_copy[1:]
    
    def display(self):
        global WEATHER_CODE_DECODE
        
        for item in WEATHER_CODE_DECODE:
            print(item, end=" ")
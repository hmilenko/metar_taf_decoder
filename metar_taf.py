import re

from metar_taf_decode import*
from metar_taf_class import*

def main():
    weather_code = input("Input the METAR or TAF : ")
    weather_type = message_test(weather_code)
    weather_decode = decode(weather_code)
    print(weather_decode)


def message_test(weather_code):
    weather_code_list = weather_code.split(" ")

    # Indicators to determine if TAF, else is METAR
    taf_indicator_1 = weather_code_list[0]
    taf_indicator_2 = len(re.sub("[^0-9]", "", weather_code_list[2]))

    # First occurence of time FROM-TO contains 8 digits
    if taf_indicator_1 == "TAF" or taf_indicator_2 == 8:
        return "TAF"
    else:
        weather_decode = Metar(weather_code_list) # Assigning the code to METAR class
        return "METAR"
    
def decode(weather_code):
    arpt_id = weather_code_arpt_id(weather_code)
    message_time = weather_code_message_time(weather_code)
    wind = weather_code_wind(weather_code)
    visibility = weather_code_visibility(weather_code)
    clouds = weather_code_clouds(weather_code)
    temperatures = weather_code_temperatures(weather_code)
    pressure = weather_code_pressure(weather_code)
    trend = weather_code_trend(weather_code)

    return arpt_id, message_time, wind, visibility, clouds, temperatures, pressure, trend

def assign_class():
    pass

def display():
    pass

main()
import re

from metar_taf_decode import*
from metar_taf_class import*

def main():
    weather_code = input("Input the METAR or TAF : ")
    weather_type = message_test(weather_code)
    weather_decode = decode(weather_code, weather_type)
    print(weather_decode)


def message_test(weather_code):
    weather_code_list = weather_code.split(" ")
    print(weather_code_list)

    if re.match("TAF", weather_code_list[0]) \
        or re.match("[0-9][0-9][0-9][0-9]\\[0-9][0-9][0-9][0-9]", weather_code_list[3]):
        return "TAF"
    else:
        return "METAR"
    
def decode(weather_code, weather_type):
    identification = weather_code_identification(weather_code, weather_type)
    arpt_id = weather_code_arpt_id(weather_code)
    identification_option = weather_code_identification_option(weather_code)
    message_time = weather_code_message_time(weather_code)
    wind = weather_code_wind(weather_code)
    visibility = weather_code_visibility(weather_code)
    rvr = weather_code_rvr(weather_code)
    present_wx = weather_code_present_wx(weather_code)
    clouds = weather_code_clouds(weather_code)
    temperatures = weather_code_temperatures(weather_code)
    pressure = weather_code_pressure(weather_code)
    trend = weather_code_trend(weather_code)

    return identification, arpt_id, identification_option, message_time, wind, visibility, rvr, present_wx, clouds, temperatures, pressure, trend

def assign_class():
    pass

def display():
    pass

main()
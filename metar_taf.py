import re

from metar_taf_class import*

def main():
    weather_code = input("Entrez le message à décoder : ")
    weather_decode = message_test(weather_code)
    decoding(weather_decode)


def message_test(weather_code):
    weather_code_list = weather_code.split(" ")

    # Indicators to determine if TAF, else is METAR
    taf_indicator_1 = weather_code_list[0]
    taf_indicator_2 = len(re.sub("[^0-9]", "", weather_code_list[2]))

    # First occurence of time FROM-TO contains 8 digits
    if taf_indicator_1 == "TAF" or taf_indicator_2 == 8:
        weather_decode = Taf(weather_code_list) # Assigning the code to TAF class
        return weather_decode
    else:
        weather_decode = Metar(weather_code_list) # Assigning the code to METAR class
        return weather_decode

def decoding(weather_decode):
    # weather_decode.terrain_id()
    weather_decode.wind()
    weather_decode.visibility()
    weather_decode.clouds()
    # weather_decode.temperatures()
    # weather_decode.pressure()
    # weather_decode.trend()

main()
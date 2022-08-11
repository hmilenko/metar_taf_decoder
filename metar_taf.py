import re

from metar_taf_class import*

def main():
    weather_code = input("Entrez le message à décoder : ")
    message_test(weather_code)

def message_test(weather_code):
    print("testing")
    weather_code_list = weather_code.split(" ")

    # Indicators to determine if TAF, else is METAR
    taf_indicator_1 = weather_code_list[0]
    taf_indicator_2 = len(re.sub("[^0-9]", "", weather_code_list[2]))

    # First occurence of time FROM-TO contains 8 digits
    if taf_indicator_1 == "TAF" or taf_indicator_2 == 8:
        weather_decode = Taf(weather_code_list)
    else:
        weather_decode = Metar(weather_code_list)

main()
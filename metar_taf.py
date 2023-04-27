import re

from metar_taf_decode_test import*
from metar_taf_class_test import*
from metar_taf_globals import*

def main():
    global WEATHER_CODE, WEATHER_CODE_DECODE
    
    WEATHER_CODE = input("Input the METAR or TAF : ")
    determine_type()
    WEATHER_CODE.decode()
    WEATHER_CODE.display()

def determine_type():
    global WEATHER_CODE
    
    data = WEATHER_CODE.split(" ")

    if re.match("TAF", data[0]) \
        or re.match("[0-9][0-9][0-9][0-9]/[0-9][0-9][0-9][0-9]", data[2] or data[3] or data[4]):
        WEATHER_CODE = Taf(WEATHER_CODE)
    else:
        WEATHER_CODE = Metar(WEATHER_CODE)
    
main()
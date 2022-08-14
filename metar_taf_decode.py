import re

def weather_code_arpt_id(weather_code):
    data = weather_code.split(" ")
    arpt = ""
    
    # Retrieving airport ID
    for item in data:
        if re.match("^[A-Z][A-Z][A-Z][A-Z]$", item):
            arpt = item
    
    # Will search airport ID in library to display full name
    return arpt

def weather_code_message_time(weather_code):
    data = weather_code.split(" ")
    date = ""
    time = ""
    
    # Retrieving message time
    for item in data:
        if re.match("^[0-9][0-9][0-9][0-9][0-9][0-9]Z$", item):
            date = item[:2]
            time = item[2:6]

    return f"Date {date} of the month ; Time {time[0]}{time[1]}:{time[2]}{time[3]} UTC"

def weather_code_wind(weather_code):
    data = weather_code.split(" ")
    wind_unit = ""
    wind = ""
    gust = False
    variability = False
    
    # Retrieving wind
    for item in data:
        if re.match("[0-9][0-9][0-9][0-9][0-9]KT", item) \
        or re.match("[0-9][0-9][0-9][0-9][0-9]MPS", item) \
        or re.match("[0-9][0-9][0-9][0-9][0-9]G[0-9][0-9]KT", item) \
        or re.match("[0-9][0-9][0-9][0-9][0-9]G[0-9][0-9]MPS", item) \
        or re.match("[0-9][0-9][0-9]V[0-9][0-9][0-9]", item):
            wind += item
    
    # Determine wind unit and if gust and/or variability
    if re.search("KT", wind):
        wind_unit = "knots"
        wind = wind.replace("KT", "") # Removing unit because of display index on RETURN
    else:
        wind_unit = "meters per second"
        wind = wind.replace("MPS", "") # Removing unit because of display index on RETURN
    if re.search("G", wind):
        gust = True
    if re.search("V", wind):
        variability = True

    # Return depending of gust and variability
    if not gust:
        if not variability:
            return f"Wind {wind[:3]}° {wind[3:5]} {wind_unit}"
        else:
            return f"Wind {wind[:3]}° {wind[3:5]} {wind_unit} variable between {wind[5:8]}° and {wind[9:]}°"
    else:
        if not variability:
            return f"Wind {wind[:3]}° {wind[3:5]} {wind_unit} gusting {wind[6:]} {wind_unit}"
        else:
            return f"Wind {wind[:3]}° {wind[3:5]} {wind_unit} gusting {wind[6:8]} {wind_unit} variable between {wind[8:11]}° and {wind[12:]}°"

def weather_code_visibility(weather_code):
    data = weather_code.split(" ")
    visibility = ""
    cavok = False
    
    # Retrieving visibility
    for item in data:
        if re.match("^[0-9][0-9][0-9][0-9]$", item):
            visibility = item
    
    return visibility

def weather_code_clouds(weather_code):
    pass

def weather_code_temperatures(weather_code):
    pass

def weather_code_pressure(weather_code):
    pass

def weather_code_trend(weather_code):
    pass

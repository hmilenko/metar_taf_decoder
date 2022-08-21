import re

def weather_code_identification(weather_code, weather_type):
    if weather_type == "TAF":
        return "Forcast from"
    elif weather_type == "METAR":
        data = weather_code.split(" ")

        for item in data:
            if re.match("METAR", item):
                return "Observation message from"
            if re.match("SPECI", item):
                return "Special message from"

def weather_code_arpt_id(weather_code):
    data = weather_code.split(" ")
    arpt = ""
    
    # Retrieving airport ID
    for item in data:
        if re.match("^[A-Z][A-Z][A-Z][A-Z]$", item):
            arpt = item
    
    # Will search airport ID in library to display full name
    return arpt + " airport"

def weather_code_identification_option(weather_code):
    data = weather_code.split(" ")

    for item in data:
        if re.match("AUTO", item):
            return "Automated message"
        if re.match("COR", item):
            return "Corrected message"

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
    VRB = False
    
    # Retrieving wind
    for item in data:
        if re.match("[0-9][0-9][0-9][0-9][0-9]KT", item) \
        or re.match("[0-9][0-9][0-9][0-9][0-9]MPS", item) \
        or re.match("[0-9][0-9][0-9][0-9][0-9]G[0-9][0-9]KT", item) \
        or re.match("[0-9][0-9][0-9][0-9][0-9]G[0-9][0-9]MPS", item) \
        or re.match("[0-9][0-9][0-9]V[0-9][0-9][0-9]", item) \
        or re.search("VRB", item) \
        or re.match("/////", item):
            wind += item
    
    # Determine VRB, wind unit and if gust and/or variability
    if re.search("VRB", wind):
        VRB = True
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
    if wind[:5] == "00000":
        return "Wind calm"
    if VRB:
        return f"Wind variable {wind[3:5]} {wind_unit}"
    if wind[:5] == "/////":
        return "Wind unavailable"
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
        if re.match("CAVOK", item):
            return "Cieling and Visibility OK"
        elif re.match("^[0-9][0-9][0-9][0-9]$", item) \
        or re.match("////", item) \
        or re.match("^[0-9][0-9][0-9][0-9][NSEW][NSEW]$", item):
            visibility += item
    
    # Returning visibility
    if visibility == "9999":
        return "Visibility 10 kilometers or more"
    elif visibility == "////":
        return "Visibility unavailable"
    elif len(visibility) == 4:
        return f"Visibility {visibility} meters"
    elif len(visibility) == 10:
        return f"Dominante visibility {visibility[:4]} meters ; minimal visibility \
{visibility[4:8] if visibility[4] != '0' else visibility[5:8]} meters {visibility[8:]} sector"

def weather_code_rvr(weather_code):
    data = weather_code.split(" ")
    rvr_list = []
    rvr = ""

    # Retrieving RVR
    for item in data:
        if re.match("R[0-9][0-9]/", item) or re.match("R[0-9][0-9][RCL]/", item):
            rvr_list.append(item)
    
    print(rvr_list) # To delete when not necessary anymore

    for item in rvr_list:
        runway = item[1:3] if item[3] == "/" else item[1:4]
        inf_sup = ""
        runway_visibility = ""
        rvr_trend = ""
        rvr_unavailable = False

        # Testing RVR availability
        if re.search("/////", item):
            rvr_unavailable = True
        
        # Testing RVR above or below
        if item[4] == "M":
            inf_sup = "below"
        elif item[4] == "P":
            inf_sup = "above"

        # Retrieving visibility and rvr trend if exist
        if inf_sup != ("below" or "above"):
            runway_visibility = item[4:8]
            rvr_trend = item[8:]
        elif inf_sup == ("below" or "above"):
            runway_visibility = item[5:9]
            rvr_trend = item[9:]
        
        # Testing rvr trend if exist
        if rvr_trend == "D":
            rvr_trend = "decreasing"
        elif rvr_trend == "U":
            rvr_trend = "increasing"
        elif rvr_trend == "N":
            rvr_trend = "unchange"
        
        # Adding up all information to decode
        if rvr_unavailable:
            rvr += f"RVR runway {runway} unavailable" 
        elif inf_sup != "":
            if rvr_trend != "":
                rvr += f"RVR runway {runway} {inf_sup} {runway_visibility} meters {rvr_trend} ; "
            else:
                rvr += f"RVR runway {runway} {inf_sup} {runway_visibility} meters ; "
        else:
            if rvr_trend != "":
                rvr += f"RVR runway {runway} {runway_visibility} meters {rvr_trend} ; "
            else:
                rvr += f"RVR runway {runway} {runway_visibility} meters ; "
    
    # Deleting the last characters
    rvr = rvr[:-3]

    return rvr

def weather_code_present_wx(weather_code):
    pass

def weather_code_clouds(weather_code):
    data = weather_code.split(" ")
    clouds_list = []
    clouds = ""

    # Retrieving clouds
    for item in data:
        if re.match("FEW", item) or re.match("SCT", item) or re.match("BKN", item) or re.match("OVC", item) \
        or re.match("NSC", item) or re.match("NCD", item) or re.match("VV///", item) or re.match("///CB", item) \
        or re.match("///TCU", item) or re.match("/////", item):
            clouds_list.append(item)
    
    print(clouds_list) # To delete when not necessary anymore

    if clouds_list == []:
        return

    for item in clouds_list:
        # May have to add lines for coverage, ex: for FEW/// ///050 if exists
        if re.match("FEW", item):
            clouds += f"Clouds few at {int(item[3:6]) * 100} feet ; "
        elif re.match("SCT", item):
            clouds += f"Clouds scattered at {int(item[3:6]) * 100} feet ; "
        elif re.match("BKN", item):
            clouds += f"Clouds broken at {int(item[3:6]) * 100} feet ; "
        elif re.match("OVC", item):
            clouds += f"Clouds overcast at {int(item[3:6]) * 100} feet ; "
        elif re.match("NSC", item):
            clouds += "No significant clouds ; "
        elif re.match("NCD", item):
            clouds += "No clouds detected ; "
        elif re.match("VV///", item):
            clouds += "Invisible sky ; "
        elif re.match("///CB", item):
            clouds += "Cumulonimbus detected without coverage and altitude information ; "
        elif re.match("///TCU", item):
            clouds += "Towering cumulus detected without coverage and altitude information ; "
        elif re.match("/////", item): # May cause an issue with wind information if "/////"
            clouds += "Clouds information unavailable ; "

    clouds = clouds[:-3]

    return clouds

def weather_code_temperatures(weather_code):
    data = weather_code.split(" ")
    temperature = ""

    # Retrieving temperature information
    for item in data:
        if re.match("^[0-9][0-9]/[0-9][0-9]$", item) or re.match("^[0-9][0-9]/M[0-9][0-9]$", item) \
        or re.match("^M[0-9][0-9]/M[0-9][0-9]$", item) or re.match("/////", item): # To be mistaken with wind or clouds "/////"
            temperature = item

    # Displaying decoded temperature information
    if re.match("^[0-9][0-9]/[0-9][0-9]$", temperature):
        return f"Temperature {temperature[:2]}°C, dewpoint {temperature[2:]}°C"
    elif re.match("^[0-9][0-9]/M[0-9][0-9]$", temperature):
        return f"Temperature {temperature[:2]}°C, dewpoint -{temperature[4:]}°C"
    elif re.match("^M[0-9][0-9]/M[0-9][0-9]$", temperature):
        return f"Temperature -{temperature[1:3]}°C, dewpoint -{temperature[5:]}°C"
    elif re.match("/////", temperature):
        return "Temperature information unavailable"

def weather_code_pressure(weather_code):
    data = weather_code.split(" ")
    pressure = ""

    # Retrieving QNH information
    for item in data:
        if re.match("Q[0-9]", item) or re.match("Q////", item):
            pressure = item
    
    # Displaying decoded QNH
    if re.match("Q[0-9]", pressure):
        return f"QNH {pressure[1:]}"
    elif re.match("Q////", pressure):
        return "QNH information unavailable"

def weather_code_trend(weather_code):
    pass

import re

from metar_taf_globals import*

def identification(data):
    global WEATHER_CODE_DECODE
    
    # Retrieving airport ID
    for item in data:
        if re.match("^(?!AUTO)[A-Z]{4}$", item):
            airport = item
            WEATHER_CODE_DECODE.append(airport + " airport")
    
    # Retrieving message time
    for item in data:
        if re.match("^[0-9]{6}Z$", item):
            date = item[:2]
            time = item[2:6]
            WEATHER_CODE_DECODE.append(f"issued on the {date}th of the current month at {time} UTC.")
    
    # Retrieving identification option if exist      
    for item in data:
        if re.match("AUTO", item):
            WEATHER_CODE_DECODE.insert(0, "Automated")
        if re.match("COR", item):
            WEATHER_CODE_DECODE.insert(0, "Corrected")

def wind(data):
    global WEATHER_CODE_DECODE
    
    wind_unit = ""
    wind = ""
    gust = False
    variability = False
    VRB = False
    
    # Retrieving wind
    for item in data:
        if re.match("[0-9]{5}KT", item) \
        or re.match("[0-9]{5}MPS", item) \
        or re.match("[0-9]{5}G[0-9]{2}KT", item) \
        or re.match("[0-9]{5}G[0-9]{5}MPS", item) \
        or re.match("[0-9]{3}V[0-9]{3}", item) \
        or re.search("VRB", item) \
        or re.match("/////", item):
            wind += item
            break # inserted in case "/////" for temperatures as wind info comes before
    
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

    if wind != "":
        # Return depending of gust and variability
        if wind[:5] == "00000":
            WEATHER_CODE_DECODE.append("Wind calm.")
        elif VRB:
            WEATHER_CODE_DECODE.append("Wind variable {wind[3:5]} {wind_unit}.")
        elif wind[:5] == "/////":
            WEATHER_CODE_DECODE.append("Wind unavailable.")
        elif not gust:
            if not variability:
                WEATHER_CODE_DECODE.append(f"Wind {wind[:3]}° {wind[3:5]} {wind_unit}.")
            else:
                WEATHER_CODE_DECODE.append(f"Wind {wind[:3]}° {wind[3:5]} {wind_unit} variable between {wind[5:8]}° and {wind[9:]}°.")
        else:
            if not variability:
                WEATHER_CODE_DECODE.append(f"Wind {wind[:3]}° {wind[3:5]} {wind_unit} gusting {wind[6:]} {wind_unit}.")
            else:
                WEATHER_CODE_DECODE.append(f"Wind {wind[:3]}° {wind[3:5]} {wind_unit} gusting {wind[6:8]} {wind_unit} variable between {wind[8:11]}° and {wind[12:]}°.")

def visibility(data):
    global WEATHER_CODE_DECODE
    
    visibility = ""
    visibility_unit = ""
    sector = ""
    cavok = False
    
    # Retrieving visibility
    for item in data:
        if re.match("CAVOK", item):
            WEATHER_CODE_DECODE.append("Cieling and Visibility OK.")
        elif re.match("^[0-9]{4}$", item) \
        or re.match("////", item) \
        or re.match("^[0-9]{4}[NSEW]$", item) \
        or re.match("^[0-9]{4}[NSEW]{2}$", item):
            visibility += item
    if re.search("SM", visibility):
        visibility_unit = "statute miles"
    else:
        visibility_unit = "meters"
    
    # Determining minimal visibility sector
    if len(visibility) > 8:      
        if re.match("^N$", visibility[8:]):
            sector = "north"
        elif re.match("^NE$", visibility[8:]):
            sector = "north east"
        elif re.match("^E$", visibility[8:]):
            sector = "east"
        elif re.match("^SE$", visibility[8:]):
            sector = "south east"
        elif re.match("^S$", visibility[8:]):
            sector = "south"
        elif re.match("^SW$", visibility[8:]):
            sector = "south west"
        elif re.match("^W$", visibility[8:]):
            sector = "west"
        elif re.match("^NW$", visibility[8:]):
            sector = "north west"
        else:
            pass
    
    # Returning visibility
    if visibility == "9999":
        WEATHER_CODE_DECODE.append("Visibility 10 kilometers or more.")
    elif visibility == "////":
        WEATHER_CODE_DECODE.append("Visibility unavailable.")
    elif len(visibility) == 4:
        WEATHER_CODE_DECODE.append(f"Visibility {visibility} {visibility_unit}.")
    elif len(visibility) == 10:
        WEATHER_CODE_DECODE.append(f"Dominante visibility {visibility[:4]} {visibility_unit} ; minimal visibility \
{visibility[4:8] if visibility[4] != '0' else visibility[5:8]} {visibility_unit} {sector} sector.")

def rvr(data):
    global WEATHER_CODE_DECODE
    
    rvr_list = []
    rvr = ""

    # Retrieving RVR
    for item in data:
        if re.match("^R[0-9]{2}/[0-9]{4}$", item) \
        or re.match("^R[0-9]{2}[RCL]/[0-9]{4}$", item) \
        or re.match("^R[0-9]{2}/[0-9]{4}[DUN]$", item) \
        or re.match("^R[0-9]{2}[RCL]/[0-9]{4}[DUN]$", item) \
        or re.match("^R[0-9]{2}/[MP][0-9]{4}$", item) \
        or re.match("^R[0-9]{2}[RCL]/[MP][0-9]{4}$", item) \
        or re.match("^R[0-9]{2}/[MP][0-9]{4}[DUN]$", item) \
        or re.match("^R[0-9]{2}[RCL]/[MP][0-9]{4}[DUN]$", item) \
        or re.match("^R[0-9]{2}/////$", item) \
        or re.match("^R[0-9]{2}[RCL]/////$", item):
            rvr_list.append(item)

    for item in rvr_list:
        runway = item[1:3] if item[3] == "/" else item[1:4]
        inf_sup = ""
        runway_visibility = ""
        rvr_trend = ""
        rvr_unavailable = False

        # Testing RVR availability
        if re.match("^R[0-9]{2}/////$", item) \
        or re.match("^R[0-9]{2}[RCL]/////$", item):
            rvr_unavailable = True
        
        # Retrieving RVR above or below if exist
        if re.match("^R[0-9]{2}/[MP][0-9]{4}$", item) \
        or re.match("^R[0-9]{2}/[MP][0-9]{4}[DUN]$", item):
            if item[4] == "M":
                inf_sup = "below"
            elif item[4] == "P":
                inf_sup = "above"
        elif re.match("^R[0-9]{2}[RCL]/[MP][0-9]{4}$", item) \
        or re.match("^R[0-9]{2}[RCL]/[MP][0-9]{4}[DUN]$", item):
            if item[5] == "M":
                inf_sup = "below"
            elif item[5] == "P":
                inf_sup = "above"

        # Retrieving visibility
        if re.match("^R[0-9]{2}/[0-9]{4}$", item):
            runway_visibility = item[4:]
        elif re.match("^R[0-9]{2}[RCL]/[0-9]{4}$", item) \
        or re.match("^R[0-9]{2}/[MP][0-9]{4}$", item):
            runway_visibility = item[5:]
        elif re.match("^R[0-9]{2}/[0-9]{4}[DUN]$", item) \
        or re.match("^R[0-9]{2}[RCL]/[0-9]{4}[DUN]$", item) \
        or re.match("^R[0-9]{2}/[MP][0-9]{4}[DUN]$", item):
            runway_visibility = item[5:-1]
        elif re.match("^R[0-9]{2}[RCL]/[MP][0-9]{4}$", item):
            runway_visibility = item[6:]
        elif re.match("^R[0-9]{2}[RCL]/[MP][0-9]{4}[DUN]$", item):
            runway_visibility = item[6:-1]

        
        # Retrieving rvr trend if exist
        if re.match("^R[0-9]{2}/[0-9]{4}[DUN]$", item) \
        or re.match("^R[0-9]{2}[RCL]/[0-9]{4}[DUN]$", item) \
        or re.match("^R[0-9]{2}/[MP][0-9]{4}[DUN]$", item) \
        or re.match("^R[0-9]{2}[RCL]/[MP][0-9]{4}[DUN]$", item):
            if item[-1] == "D":
                rvr_trend = "decreasing"
            elif item[-1] == "U":
                rvr_trend = "increasing"
            elif item[-1] == "N":
                rvr_trend = "unchanged"
        
        
        # Adding up all information to decode
        if rvr_unavailable:
            rvr += f"RVR runway {runway} unavailable" 
        elif inf_sup != "" and rvr_trend != "":
            rvr += f"RVR runway {runway} {inf_sup} {runway_visibility} meters {rvr_trend} ; "
        elif inf_sup != "" and rvr_trend == "":
            rvr += f"RVR runway {runway} {inf_sup} {runway_visibility} meters ; "
        elif inf_sup == "" and rvr_trend != "":
            rvr += f"RVR runway {runway} {runway_visibility} meters {rvr_trend} ; "
        else:
            rvr += f"RVR runway {runway} {runway_visibility} meters ; "
    
    # Deleting the last characters
    rvr = rvr[:-3]

    if rvr != "":
        WEATHER_CODE_DECODE.append(f"{rvr}.")

def present_weather(data):
    global WEATHER_CODE_DECODE, TREND, INTENSITY_PROXIMITY, DESCRIPTION, PRECIPITATION, DARKENING, OTHER_PHENOMENA

    present_weather_list = []
    present_weather = ""
    
    for item in data:
        if re.match("TEMPO", item) \
        or re.match("BECMG", item) \
        or re.match("FM", item) \
        or re.match("AT", item) \
        or re.match("TL", item) \
        or re.match("RE", item) \
        and TREND == False: # To separate current and trend weather
            break
        for key in INTENSITY_PROXIMITY.keys():
            if re.search(key, item):
                present_weather_list.append(INTENSITY_PROXIMITY[key])
                break
    
    for item in data:
        if re.match("TEMPO", item) \
        or re.match("BECMG", item) \
        or re.match("FM", item) \
        or re.match("AT", item) \
        or re.match("TL", item) \
        or re.match("RE", item) \
        and TREND == False: # To separate current and trend weather
            break
        for key in DESCRIPTION.keys():
            if re.search(key, item):
                present_weather_list.append(DESCRIPTION[key])
                break
    
    for item in data:
        if re.match("TEMPO", item) \
        or re.match("BECMG", item) \
        or re.match("FM", item) \
        or re.match("AT", item) \
        or re.match("TL", item) \
        or re.match("RE", item) \
        and TREND == False: # To separate current and trend weather
            break
        for key in PRECIPITATION.keys():
            if re.search(key, item):
                present_weather_list.append(PRECIPITATION[key])
                break
    
    for item in data:
        if re.match("TEMPO", item) \
        or re.match("BECMG", item) \
        or re.match("FM", item) \
        or re.match("AT", item) \
        or re.match("TL", item) \
        or re.match("RE", item) \
        and TREND == False: # To separate current and trend weather
            break
        for key in DARKENING.keys():
            if re.search(key, item):
                present_weather_list.append(DARKENING[key])
                break
    
    for item in data:
        if re.match("TEMPO", item) \
        or re.match("BECMG", item) \
        or re.match("FM", item) \
        or re.match("AT", item) \
        or re.match("TL", item) \
        or re.match("RE", item) \
        and TREND == False: # To separate current and trend weather
            break
        for key in OTHER_PHENOMENA.keys():
            if re.search(key, item):
                present_weather_list.append(OTHER_PHENOMENA[key])
                break
    
    for item in data:
        if re.match("TEMPO", item) \
        or re.match("BECMG", item) \
        or re.match("FM", item) \
        or re.match("AT", item) \
        or re.match("TL", item) \
        or re.match("RE", item) \
        and TREND == False: # To separate current and trend weather
            break
        if re.match("VC", item):
            present_weather_list.append("in the vicinity")
            
        if re.match(("NSW"), item):
            present_weather_list.append("No significant weather")
    
    for item in present_weather_list:
        present_weather += f"{item}"
    
    if present_weather != "":
            WEATHER_CODE_DECODE.append(f"{present_weather}.")

def clouds(data):
    global WEATHER_CODE_DECODE
    
    clouds_list = []
    clouds = ""

    # Retrieving clouds
    for item in data:
        if re.match("FEW", item) or re.match("SCT", item) or re.match("BKN", item) or re.match("OVC", item) \
        or re.match("NSC", item) or re.match("NCD", item) or re.match("VV///", item) or re.match("///CB", item) \
        or re.match("///TCU", item) or re.match("//////", item): 
            clouds_list.append(item) # No issues with wind as it will take last info if "/////"

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

    if clouds != "":
        WEATHER_CODE_DECODE.append(f"{clouds}.")

def temperatures(data):
    global WEATHER_CODE_DECODE
    
    temperature = ""

    # Retrieving temperature information
    for item in data:
        if re.match("^[0-9]{2}/[0-9]{2}$", item) \
        or re.match("^[0-9]{2}/M[0-9]{2}$", item) \
        or re.match("^M[0-9]{2}/M[0-9]{2}$", item) \
        or re.match("/////", item): 
        # No risk to be mistaken with wind "/////" as item will go through all data
            temperature = item

    # Displaying decoded temperature information
    if re.match("^[0-9]{2}/[0-9]{2}$", temperature):
        WEATHER_CODE_DECODE.append(f"Temperature {temperature[:2]}°C, dewpoint {temperature[3:]}°C.")
    elif re.match("^[0-9]{2}/M[0-9]{2}$", temperature):
        WEATHER_CODE_DECODE.append(f"Temperature {temperature[:2]}°C, dewpoint -{temperature[4:]}°C.")
    elif re.match("^M[0-9]{2}/M[0-9]{2}$", temperature):
        WEATHER_CODE_DECODE.append(f"Temperature -{temperature[1:3]}°C, dewpoint -{temperature[5:]}°C.")
    elif re.match("/////", temperature):
        WEATHER_CODE_DECODE.append("Temperature information unavailable.")

def pressure(data):
    global WEATHER_CODE_DECODE
    
    for item in data:
        if re.match("^Q[0-9]{4}$", item):
            WEATHER_CODE_DECODE.append(f"QNH {item[1:]}.")
        elif re.match("^Q[0-9]{4}=$", item):
            WEATHER_CODE_DECODE.append(f"QNH {item[1:-1]}.")
        elif re.match("^Q////$", item):
            WEATHER_CODE_DECODE.append("QNH information unavailable.")
            
def additional(data):
    global WEATHER_CODE_DECODE, INTENSITY_PROXIMITY, DESCRIPTION, PRECIPITATION, DARKENING, OTHER_PHENOMENA
    
    additional = ""
    
    for item in data:
        if re.match("RE", item[:2]):
            additional += "Recent"
            for key in INTENSITY_PROXIMITY.keys():
                if re.search(key, item):
                    additional += f" {INTENSITY_PROXIMITY[key]}"
            for key in DESCRIPTION.keys():
                if re.search(key, item):
                    additional += f" {DESCRIPTION[key]}"
            for key in PRECIPITATION.keys():
                if re.search(key, item):
                    additional += f" {PRECIPITATION[key]}"
            for key in DARKENING.keys():
                if re.search(key, item):
                    additional += f" {DARKENING[key]}"
            for key in OTHER_PHENOMENA.keys():
                if re.search(key, item):
                    additional += f" {OTHER_PHENOMENA[key]}"
        elif re.match("WS R", item):
            additional += "Windshear detected"
                
    if additional != "":
        WEATHER_CODE_DECODE.append(f"{additional}.")

def trend(data):
    global WEATHER_CODE_DECODE, TREND
    
    trend_list = []
    
    for item in data:
        if re.match("TEMPO", item) \
        or re.match("BECMG", item) \
        or re.match("NOSIG", item) \
        or re.match("^FM[0-9]{4}", item) \
        or re.match("^AT[0-9]{4}", item) \
        or re.match("^TL[0-9]{4}", item):
            trend_list.append(item)
            TREND = True
            continue # Prevent adding 2 times
        if TREND == True:
            trend_list.append(item)
            
    if trend_list == []:
        return
    
    for item in trend_list:
        if re.match("^FM[0-9]{4}", item):
            WEATHER_CODE_DECODE.append(f"from {item[2:]}.")
            continue
        elif re.match("^AT[0-9]{4}", item):
            WEATHER_CODE_DECODE.append(f"at {item[2:]}.")
            continue
        elif re.match("^TL[0-9]{4}", item):
            WEATHER_CODE_DECODE.append(f"until {item[2:]}.")
            continue
        elif item == "TEMPO":
            WEATHER_CODE_DECODE.append("Temporarily:")
            continue
        elif item == "BECMG":
            WEATHER_CODE_DECODE.append("Becoming:")
            continue
        elif item == "NOSIG":
            WEATHER_CODE_DECODE("No significant change in the next 2 hours.")
            return
        
        wind([item])
        visibility([item])
        rvr([item])
        present_weather([item])
        clouds([item])
        temperatures([item])
        pressure([item])
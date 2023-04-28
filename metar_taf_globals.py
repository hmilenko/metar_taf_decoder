global WEATHER_CODE
global WEATHER_CODE_DECODE
global TREND

WEATHER_CODE_DECODE = []
TREND = False

INTENSITY_PROXIMITY = {"-": "low/moderate", "\+": "strong/well formed"}
DESCRIPTION = {"MI": "shallow", "BC": "patches of", "PR": "partial", "DR": "low drifting below eye level", "BL": "blowing at or above eye level", "SH": "showers of", "TS": "thunderstorms", "FZ": "freezing"}
PRECIPITATION ={"DZ": "drizzle", "RA": "rain", "SN": "snow", "SG": "snow grains", "PL": "ice pellets", "GR": "hail", "GS": "graupel (snow pellets and/or small hail)", "UP": "unknown precipitation"}
DARKENING = {"BR": "mist", "FG": "fog", "FU": "smoke", "VA": "volcanic ash", "DU": "widespread dust", "SA": "sand", "HZ": "haze"}
OTHER_PHENOMENA = {"PO": "dust", "SQ": "squall", "FC": "funnel cloud", "SS": "sandstorm", "DS": "duststorm"}
# METAR / TAF DECODER PROJECT


## AIM : Convert METAR / TAF messages into user readable and computer intelligible formats. Implementation should be flexible to allow easy further integration

### Data format specification :

Inputs : string or list of string [Optional argument : aerodrome minima data package ( format to be defined ) ]

        If one single METAR or TAF message : string (e.g. "METAR LBBG 041600Z 12012MPS 090V150 1400 R04/P1500N R22/P1500U +SN BKN022 OVC050 M04/M07 Q1020 NOSIG 8849//91=")
        If several METAR / TAF messages : list of strings (e.g. ["METAR X string","METAR Y string","TAF X string",...] )

Output : List ["Decoded user readable information", "Computer intelligibile format"]
        or List of list ( if several messages to be decoded )
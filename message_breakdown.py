################# COMPILE METAR / TAF into intelligible format ##########################


# Input : message to be decoded as single string, space separated vales (e.g. "METAR XXXX XXX...")

# Test strings = "METAR LBBG 041600Z 12012MPS 090V150 1400 R04/P1500N R22/P1500U +SN BKN022 OVC050 M04/M07 Q1020 NOSIG 8849//91="
        #        "METAR EGGW 090450Z AUTO 04003KT 9999 NCD 13/11 Q1029"


message = input("Please enter METAR/TAF string to be decoded \n")
print("\nInitial message :\n" , message, "\n")

message_split = message.split()
print("Space split message :\n", message_split, "\n")


# Initiate categories for inforamtion classification
categories = ["message_type","airport_ICAO_code","date_time","wind","visibility","rvr","wx_phenoma","clouds","temperature","baro","trend"]

# Initiate dictionary to store decoded data
decoded = {}

### Initate all dictionary keys with an empty list
for item in categories:
    decoded[item] = []




### Message breakfdown ##############################################################


# Message type
if message_split[0] == "METAR" or message_split == "TAF":
    decoded['message_type'] = message_split[0]
    message_split.pop(0)
else:
        decoded['message_type'] = "Unknown"



# ICAO code
if message_split[0].isalpha() and len(message_split[0]) == 4:
    decoded['airport_ICAO_code'] = message_split[0]
    message_split.pop(0)
else:
        decoded['airport_ICAO_code'] = "Unknown"
        raise Exception("Airport ICAO code must be provided")


# Wind info collector
for item in message_split:

    # Stanadard wind #### To be adjusted to accept gust values as well
    if len(item) == 5 and item.isdigit():
        decoded['wind'].append(item)

    # Detect MPS or MPH wind values    
    elif ( "MPS" in item or "MPH" in item ) and len(item)== 8 :
        decoded['wind'].append(item)

    # Detect KT wind values    
    elif "KT" in item and len(item)== 7 :
        decoded['wind'].append(item)

    # Detect variable wind info    
    elif "V" in item :
        if item.split("V")[0].isdigit() and item.split("V")[1].isdigit():
            decoded['wind'].append(item)
    



# Visibility info collector
for item in message_split:
    if item.isdigit() and ( len(item) == 3 or len(item) == 4 ) :
            decoded['visibility'].append(item)



# RVR info collector
for item in message_split:
    if item[0] == "R" and item[1].isdigit() and item[2].isdigit() :
            decoded['rvr'].append(item)



# Cloud info collector
cloud_attributes = ["FEW","SCT","BKN","OVC"]

for item in message_split:
    for cloud_item in cloud_attributes:
        if cloud_item in item:
            #print("yes")
            decoded['clouds'].append(item)


# Temp info collector
for item in message_split:
    if "/" in item:
        if item.split("/")[0].isdigit() and item.split("/")[1].isdigit():
            decoded['temperature'].append(item)


# Baro info collector
for item in message_split:
    if item[0] == "Q" and ( len(item) == 4 or len(item) == 5 ) :
            decoded['baro'].append(item)


print(decoded)










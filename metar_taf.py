weather_code = input("Entrez le message à décoder : ")

weather_code_list = weather_code.split(" ")

print(weather_code_list)

# Si le premier item de la liste == "TAF" ou le 3e item est sous le format "xxxx/xxxx" alors le code est de class TAF
# Sinon le code est de class METAR